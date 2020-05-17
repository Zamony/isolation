import isolation

if __name__ == "__main__":
    ui = isolation.GUI()
    player_a = isolation.UserControlledPlayer(ui, ui.ANN_ICON)
    player_b = isolation.UserControlledPlayer(ui, ui.BOB_ICON)
    isolation.run_game(ui, player_a, player_b)
