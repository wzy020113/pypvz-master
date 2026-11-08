#!/usr/bin/env python
# pygbag 浏览器入口：仅用于网页版打包；桌面版仍然运行 pypvz.py
import asyncio
import sys

if sys.platform == "emscripten":  # 浏览器环境无法写日志文件
    import logging
    logging.basicConfig(level=logging.INFO)

import os
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
import pygame as pg
# 由于在后续本地模块中存在对pygame的调用，在此处必须完成pygame的初始化
pg.init()

from source import tool
from source import constants as c
from source.state import mainmenu, screen, level


async def main():
    # 控制状态机运行
    game = tool.Control()
    state_dict = {
        c.MAIN_MENU:    mainmenu.Menu(),
        c.GAME_VICTORY: screen.GameVictoryScreen(),
        c.GAME_LOSE:    screen.GameLoseScreen(),
        c.LEVEL:        level.Level(),
        c.AWARD_SCREEN: screen.AwardScreen(),
        c.HELP_SCREEN:  screen.HelpScreen(),
    }
    game.setup_states(state_dict, c.MAIN_MENU)
    await game.run_web()


asyncio.run(main())
