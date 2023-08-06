import click
import builtins
from io import StringIO
from contextlib import redirect_stdout


class PrintControl:
    """Take control over the print."""

    template = None
    bg_color = None
    fg_color = None
    print_enabled = True
    print_function = print

    @staticmethod
    def reset() -> None:
        """Resets static data.
        :return: None
        """

        PrintControl.template = None
        PrintControl.bg_color = None
        PrintControl.fg_color = None
        PrintControl.print_enabled = True
        PrintControl.print_function = print

    @staticmethod
    def enable() -> None:
        """Enables printing.
        :return: None
        """

        PrintControl.print_enabled = True

    @staticmethod
    def disable() -> None:
        """Disables printing.
        :return: None
        """

        PrintControl.print_enabled = False


def print_extended(*args, **kwargs) -> None:
    """Main method for extending the functionalists of
    Python's built-in print() method.
    :return: None
    """

    if __debug__ and PrintControl.print_enabled:
        printed = StringIO()

        with redirect_stdout(printed):
            PrintControl.print_function(*args, **kwargs)

        # the last character is new line (\n)
        # so it has been removed
        printed = printed.getvalue()[:-1]

        if PrintControl.template:
            printed = PrintControl.template.format(print=printed)

        printed = click.style(printed,
                              fg=PrintControl.fg_color,
                              bg=PrintControl.bg_color)

        click.echo(printed)


# Monkey patch built-in print method
builtins.print = print_extended
