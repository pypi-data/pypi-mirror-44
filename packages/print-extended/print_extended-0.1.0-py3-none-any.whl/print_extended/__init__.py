import click
import builtins
from io import StringIO
from contextlib import redirect_stdout


class PrintControl:
    """Take control over the print."""

    template = None
    bg_color = None
    fg_color = None
    print_function = print


def print_extended(*args, **kwargs) -> None:
    """Main method for extending the functionalists of
    Python's built-in print() method.
    :return: None
    """

    if __debug__:
        printed = StringIO()

        with redirect_stdout(printed):
            PrintControl.print_function(*args, **kwargs)

        printed = printed.getvalue().strip()

        if PrintControl.template:
            printed = PrintControl.template.format(print=printed)

        printed = click.style(printed,
                              fg=PrintControl.fg_color,
                              bg=PrintControl.bg_color)

        click.echo(printed)


# Monkey patch built-in print method
builtins.print = print_extended
