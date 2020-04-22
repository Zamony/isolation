import isolation

if __name__ == "__main__":
    ui = isolation.TUI()
    player_a = isolation.UserControlledPlayer(ui, isolation.TUI.ANN_ICON)
    player_b = isolation.UserControlledPlayer(ui, isolation.TUI.BOB_ICON)
    isolation.run_game(ui, player_a, player_b)
