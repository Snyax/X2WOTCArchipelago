from Options import Toggle


class ExampleModOption(Toggle):
    """This is an example mod option."""
    display_name = "Example Mod Option"
    default = False


options = [
    ("example_mod_option", ExampleModOption),
]
