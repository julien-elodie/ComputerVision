import sys

from PyQt5.QtWidgets import QApplication

from ComputerVision.UI import Advance
from ComputerVision.UI import CommandLine

import click


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('PyCV 1.0.0')
    ctx.exit()


@click.command()
@click.option(
    '--version',
    help='Show version',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True
)
@click.option(
    '--mode',
    default='command',
    help='Select the mode you want to enter',
    type=click.Choice(['gui', 'command']),
    prompt='Please enter the mode',
    nargs=1
)
def main(mode):
    # GUI
    def Gui():
        app = QApplication(sys.argv)

        advance = Advance()
        advance.show()

        sys.exit(app.exec_())
    # Command

    def Command():
        CommandLine()
    # 选择器
    switcher = {
        'gui': Gui,
        'command': Command,
    }
    core = switcher.get(mode, Command)
    return core()


if __name__ == '__main__':
    main()
