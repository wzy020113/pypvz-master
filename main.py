#!/usr/bin/env python
# pygbag 浏览器入口：仅用于网页版打包；桌面版仍然运行 pypvz.py
import asyncio
import sys

if sys.platform == "emscripten":  # 浏览器环境无法写日志文件
    import logging
    logging.basicConfig(level=logging.INFO)

import os
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
print("[pypvz] 正在初始化 pygame ...", flush=True)
import pygame as pg
# 由于在后续本地模块中存在对pygame的调用，在此处必须完成pygame的初始化
pg.init()
print("[pypvz] pygame 初始化完成", flush=True)

from source import tool
print("[pypvz] 正在加载图片素材（浏览器中较慢，请耐心等待）...", flush=True)
from source import constants as c
from source.state import mainmenu, screen, level
print("[pypvz] 素材加载完成", flush=True)


async def main():
    # 控制状态机运行
    try:
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
    except Exception:
        # 浏览器中看不到控制台，把启动错误直接画在画布上
        import traceback
        import pygame.font as pgfont
        surface = pg.display.get_surface()
        surface.fill((0, 0, 0))
        font = pgfont.Font(None, 22)
        lines = traceback.format_exc().splitlines()
        for i, line in enumerate(lines[-28:]):
            surface.blit(font.render(line, True, (255, 100, 100)), (20, 25 * i))
        pg.display.update()
        print(traceback.format_exc(), flush=True)
        while True:  # 保持页面存活以便查看错误
            await asyncio.sleep(1)
    print("[pypvz] 游戏启动", flush=True)
    await game.run_web()


asyncio.run(main())
