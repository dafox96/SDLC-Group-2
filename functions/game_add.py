from game_library import GameLibrary

# Add a new game library
new_game = GameLibrary()
progress = None

new_game.add_game_prompt()
print("Enter 'q' at any time to quit.\n")
while True:
    title = input("Game title: ").strip()
    if title == "q":
        break

    while progress is None:
        progress = input("Game progress (%): ")
        if progress == "q":
            break
        if isinstance(progress, int):
            raise TypeError("Only integers are allowed.")

        if progress < 0 or progress > 100:
            progress = None
            raise Exception("Progress must be an integer from 0-100.")

    new_game.add_game(title, progress)

# List games after adding them
# TODO: Make this only execute when asked to
new_game.list_games()
