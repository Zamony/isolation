import isolation

if __name__ == "__main__":
    player_a = isolation.UserControlledPlayer(isolation.TUI.ANN_ICON)
    player_b = isolation.RobotControlledPlayer()
    ui = isolation.TUI()
    isolation.run_game(ui, player_a, player_b)