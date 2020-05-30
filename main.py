import argparse
import isolation

if __name__ == "__main__":
    difficulty = {
        "hard": isolation.ai.Difficulty.hard,
        "normal": isolation.ai.Difficulty.normal,
        "easy": isolation.ai.Difficulty.easy,
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
        isolation.gui_runner.main()
    else:
        ui = isolation.TUI()
        player_a = isolation.UserControlledPlayer(ui, ui.ANN_ICON)
        player_b = isolation.RobotControlledPlayer(
            ui,
            difficulty[args.console_difficulty],
        )
        isolation.run_game(ui, player_a, player_b)
