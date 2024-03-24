class GameLibrary:
    """Add and remove games from user library"""

    def __init__(self) -> None:
        self.game_library = {}

    def add_game_prompt(self):
        """Show the prompt"""
        print("Enter game title and progress:")

    def add_game(self, game_title: str, game_progress: int) -> None:
        """Add a game to user library"""
        try:
            game_title = str(game_title)
        except ValueError:
            print("Game title format error. Try adding game again.")

        try:
            game_progress = int(game_progress)
        except ValueError:
            print("Game progress format error. Try adding game again.")

        else:
            self.game_library[game_title] = {
                # Storing only progress for now
                "progress": game_progress
            }
            print(f"{game_title} added to your library.")

    def list_games(self) -> None:
        """Show all games in library"""
        print("Game library:")
        for game, game_stats in self.game_library.items():
            print(f"\n🎮 {game.title()}")

            for key in game_stats:
                print(f"{key.title()} (%): {game_stats[key]}")
