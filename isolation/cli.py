"""
Module cli provides entry points to launch Isolation
"""

import argparse

from . import game
from . import ai
from . import gui_runner
from . import player
from .ui import TUI


def main():
    difficulty = {
        "hard": ai.Difficulty.hard,
        "normal": ai.Difficulty.normal,
        "easy": ai.Difficulty.easy,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--console", default=False, action="store_true")
    parser.add_argument(
        "--console-difficulty",
        default="normal",
        choices=list(difficulty),
    )

    args = parser.parse_args()
    if not args.console:
        gui_runner.main()
    else:
        ui = TUI()
        player_a = player.UserControlledPlayer(ui, ui.ANN_ICON)
        player_b = player.RobotControlledPlayer(
            ui,
            difficulty[args.console_difficulty],
        )
        game.run_game(ui, player_a, player_b)


if __name__ == "__main__":
    main()
