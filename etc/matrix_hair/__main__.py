#!/usr/bin/python3

import commands

from core import Commandhandler


# registra os comandos com o Commandhandler
Commandhandler.command(alias='I')(commands.create)
Commandhandler.command(alias='C')(commands.clear)
Commandhandler.command(alias='L')(commands.paint_pixel)
Commandhandler.command(alias='V')(commands.draw_vertical_line)
Commandhandler.command(alias='H')(commands.draw_horizontal_line)
Commandhandler.command(alias='K')(commands.draw_rectangle)
Commandhandler.command(alias='F')(commands.fill_region)
Commandhandler.command(alias='S')(commands.save_image)
Commandhandler.command(alias='X')(commands.quit)


if __name__ == '__main__':
    pass
