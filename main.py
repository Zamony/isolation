import isolation

if __name__ == "__main__":
    ui = isolation.GUI()
    player_a = isolation.UserControlledPlayer(ui)
    player_b = isolation.RobotControlledPlayer()
    isolation.run_game(ui, player_a, player_b)