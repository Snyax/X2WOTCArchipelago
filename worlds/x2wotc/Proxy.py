from aiohttp import web
import asyncio
from typing import TYPE_CHECKING

from CommonClient import NetworkItem, NetworkSlot, logger
from NetUtils import ClientStatus

if TYPE_CHECKING:
    from .Client import X2WOTCContext
from .Items import item_table, item_id_to_key
from .Locations import location_table, loc_id_to_key

from .mods import mods_data


ctx: "X2WOTCContext"

LocationsInfo = dict[
    str,  # Location name (internal)
    tuple[
        str | None,  # Item name (internal or external)
        NetworkItem | None,
        NetworkSlot | None
    ]
]

ItemsInfo = list[
    tuple[
        str,  # Item name (internal)
        NetworkItem,
        NetworkSlot | None
    ]
]

#======================================================================================================================#
#                                                  HELPER FUNCTIONS                                                    #
#----------------------------------------------------------------------------------------------------------------------#

def get_slot_info(slot: int) -> NetworkSlot | None:
    try:
        return ctx.slot_info[slot]
    except KeyError:
        logger.debug(f"Proxy: No slot {slot}")
        return None

# ----------------------------------------------------- SCOUT -------------------------------------------------------- #

async def scout_loop():
    try:
        while True:
            await ctx.scouted.wait_clear()
            await ctx.connected.wait()

            for loc_id in ctx.server_locations:  # If the server knows the location
                if loc_id in loc_id_to_key.keys():  # If it's ours
                    ctx.locations_scouted.add(loc_id)  # Scout it

            if ctx.locations_scouted:
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": list(ctx.locations_scouted)
                }])

            await ctx.scouted.wait()
            ctx.fill_spoiler([{
                "location": loc_id_to_key[loc_id],
                "item": ctx.item_names.lookup_in_slot(item.item, item.player),
                "player": ctx.slot_info[item.player].name,
                "game": ctx.slot_info[item.player].game,
                "flags": item.flags
            } for loc_id, item in ctx.locations_info.items()])

            logger.debug("Proxy: Locations scouted")

    except asyncio.CancelledError:
        logger.debug("Proxy: Scout loop cancelled")

def get_locations_info(checks: list[str]) -> LocationsInfo:
    locations_info: LocationsInfo = {}
    for loc_name in checks:
        try:
            loc_data = location_table[loc_name]
            loc_id = loc_data.id
        except KeyError:
            logger.warning(f"Proxy: Location {loc_name} not found")
            continue

        if loc_id is None:
            logger.debug(f"Proxy: Location {loc_name} is event, checking for victory")
            if not ctx.finished_game and loc_name == ctx.slot_data["goal_location"]:
                locations_info[loc_name] = ("Victory", None, None)
            continue

        if loc_id in (ctx.checked_locations | ctx.locations_checked):
            logger.debug(f"Proxy: Location {loc_name} already checked")
            continue

        if loc_id not in ctx.locations_scouted:
            logger.debug(f"Proxy: Location {loc_name} not scouted, will be treated as disabled")
            item_name = loc_data.normal_item  # Send internal key for disabled locations
            locations_info[loc_name] = (item_name, None, None)
            continue

        network_item = ctx.locations_info[loc_id]
        slot_info = get_slot_info(network_item.player)

        # Send external name for all locations touched by generation
        # (Receiving is handled by tick calls)
        item_name = ctx.item_names.lookup_in_game(network_item.item, slot_info.game)

        locations_info[loc_name] = (item_name, network_item, slot_info)

    return locations_info

# ----------------------------------------------------- CHECK -------------------------------------------------------- #

async def send_checks(checks: list[str], connected: bool = True):
    for loc_name in checks:

        # Resolve APworld mod location mapping
        for mod_data in reversed(mods_data):
            if mod_data.name in ctx.active_mods and loc_name in mod_data.location_map:
                loc_name = mod_data.location_map[loc_name]
                break

        try:
            loc_id = location_table[loc_name].id
        except KeyError:
            logger.warning(f"Proxy: Location {loc_name} not found")
            continue

        if loc_id is None:
            if not connected:
                logger.debug(f"Proxy: Client not connected, cannot check for victory")
                continue

            logger.debug(f"Proxy: Location {loc_name} is event, checking for victory")
            if not ctx.finished_game and loc_name == ctx.slot_data["goal_location"]:
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
            continue

        ctx.locations_checked.add(loc_id)

    if not connected:
        logger.debug("Proxy: Client not connected, cannot send location checks")
        return

    await ctx.check_locations(ctx.locations_checked)
    logger.debug("Proxy: Location checks sent")

# ---------------------------------------------------- RECEIVE ------------------------------------------------------- #

def get_received_items(layer: str, number_received: int) -> ItemsInfo:
    items_info: ItemsInfo = []
    progressive_index: dict[str, int] = {}
    number = 0  # Number in sequence of received items (from 1)

    for network_item in ctx.items_received:
        item_name = item_id_to_key[network_item.item]
        item_data = item_table[item_name]

        # Track progressive items
        stages = item_data.stages
        if stages is not None:
            progressive_index[item_name] = progressive_index.get(item_name, -1) + 1

        if item_data.layer != layer or item_data.type == "Nothing":
            continue

        number += 1
        if number <= number_received:
            continue

        # Translate progressive items
        if stages is not None:
            index = progressive_index[item_name]
            if index < len(stages):
                stage = stages[index]
                if stage is not None:
                    item_name = stage

        # Resolve APWorld mod item mapping
        for mod_data in reversed(mods_data):
            if mod_data.name in ctx.active_mods and item_name in mod_data.item_map:
                item_name = mod_data.item_map[item_name]
                break

        slot_info = get_slot_info(network_item.player)
        items_info.append((item_name, network_item, slot_info))

    return items_info

#======================================================================================================================#
#                                                  REQUEST HANDLERS                                                    #
#----------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------- CHECK -------------------------------------------------------- #

async def handle_check(request: web.Request):
    checks = [check for check in request.match_info["tail"].split("/") if check != ""]

    if not ctx.connected.is_set():
        await send_checks(checks, connected=False)
        return web.Response(status=503)
    await ctx.scouted.wait()

    response_body = ""
    for loc_name, (item_name, network_item, slot_info) in get_locations_info(checks).items():
        if response_body != "":
            response_body += "\n\n"

        if item_name is None:
            logger.debug(f"Proxy: Location {loc_name} disabled, no regular item")
            response_body += "None\n"
            response_body += "None"

        # Victory
        elif item_name == "Victory":
            logger.debug(f"Proxy: Goal has been reached")
            response_body += "Victory!\n"
            response_body += "Congratulations! You have reached your goal!"

        # For disabled locations, item_name is the internal key
        elif network_item is None:
            logger.debug(f"Proxy: Location {loc_name} disabled, regular item found")
            item_data = item_table[item_name]
            response_body += f"[{item_data.type}]{item_name}\n"
            response_body += f"Regular Item Found\n"
            response_body += f"Found your {item_data.display_name}!"

        elif network_item.player == ctx.slot:
            response_body += "Archipelago Item Sent\n"
            response_body += f"Sent {item_name} to yourself!"
        elif slot_info is not None:
            response_body += "Archipelago Item Sent\n"
            response_body += f"Sent {item_name} to {slot_info.name} ({slot_info.game})!"
        else:
            response_body += "Archipelago Item Sent\n"
            response_body += f"Sent {item_name} to no one..."

    await send_checks(checks)
    return web.Response(text=response_body)

# ----------------------------------------------------- HINT --------------------------------------------------------- #

async def handle_hint(request: web.Request):
    if not ctx.connected.is_set():
        return web.Response(status=503)
    
    hints = [hint for hint in request.match_info["tail"].split("/") if hint != ""]
    await ctx.send_msgs([{
        "cmd": "LocationScouts",
        "locations": [
            location_table[hint].id
            for hint in hints
            if hint in location_table
        ],
        "create_as_hint": 2
    }])

    return web.Response()

# ----------------------------------------------------- TICK --------------------------------------------------------- #

def handle_tick(layer: str, number_received: int) -> str:
    # Send state back for verification
    response_body = f"{number_received}"

    for (item_name, network_item, slot_info) in get_received_items(layer, number_received):
        response_body += "\n\n"

        item_data = item_table[item_name]

        # Info for the game to process
        if item_data.stages is None:
            response_body += f"[{item_data.type}]{item_name}\n"

        if network_item.player == ctx.slot:
            response_body += "Archipelago Item Received\n"
            response_body += f"Received {item_data.display_name} from yourself!"
        elif slot_info is not None:
            response_body += "Archipelago Item Received\n"
            response_body += f"Received {item_data.display_name} from {slot_info.name} ({slot_info.game})!"
        else:
            response_body += "Archipelago Item Received\n"
            response_body += f"Received {item_data.display_name} from the server."

    return response_body

async def handle_tick_strategy(request: web.Request):
    if not ctx.connected.is_set():
        return web.Response(status=503)
    
    number_received = int(request.match_info["tail"])
    response_body = handle_tick("Strategy", number_received)
    return web.Response(text=response_body)

async def handle_tick_tactical(request: web.Request):
    if not ctx.connected.is_set():
        return web.Response(status=503)
    
    number_received = int(request.match_info["tail"])
    response_body = handle_tick("Tactical", number_received)
    return web.Response(text=response_body)

#======================================================================================================================#
#                                                     RUN PROXY                                                        #
#----------------------------------------------------------------------------------------------------------------------#

async def run_proxy(local_ctx: "X2WOTCContext"):
    global ctx
    ctx = local_ctx
    
    app = web.Application()
    app.router.add_get("/Tick/Strategy/{tail:[0-9]+}", handle_tick_strategy)
    app.router.add_get("/Tick/Tactical/{tail:[0-9]+}", handle_tick_tactical)
    app.router.add_get("/Check/{tail:.*}", handle_check)
    app.router.add_get("/Hint/{tail:.*}", handle_hint)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", ctx.proxy_port)
    await site.start()

    ctx.proxy_port = int(site._server.sockets[0].getsockname()[1])
    ctx.print_info(f"Proxy: Server started at localhost:{ctx.proxy_port}")
    ctx.proxy_started.set()

    scout_task = asyncio.create_task(scout_loop(), name="scout_loop")

    try:
        await ctx.exit_event.wait()
    finally:
        await site.stop()
        await runner.cleanup()
        scout_task.cancel()
        await scout_task
        logger.debug("Proxy: Server stopped")
