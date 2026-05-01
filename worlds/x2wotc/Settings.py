from settings import Group, UserFolderPath


class X2WOTCSettings(Group):
    class GamePath(UserFolderPath):
        """Path to your installation of XCOM 2, most likely ending in `/XCOM 2`."""

        description = "XCOM 2 installation folder"

    class WorkshopPath(UserFolderPath):
        """Path to your Steam workshop folder, most likely ending in `/steamapps/workshop`.
        This is only required if the mod is installed in a different Steam archive to the game (e.g. on another drive)."""

        description = "Steam workshop folder"

    game_path: GamePath = GamePath("C:/Program Files (x86)/Steam/steamapps/common/XCOM 2")
    workshop_path: WorkshopPath = WorkshopPath("C:/Program Files (x86)/Steam/steamapps/workshop")
