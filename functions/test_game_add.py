import unittest
from game_library import GameLibrary


class TestGameLibrary(unittest.TestCase):
    "Test for the GameLibrary class"

    def setUp(self) -> None:
        self.new_game = GameLibrary()

    def test_add_single_game(self):
        "Test that a single game is stored correctly"
        self.new_game.add_game("zelda: windwaker", 25)  # Hard coding here is faster
        self.assertIn(
            "zelda: windwaker", self.new_game.game_library, "zelda: windwaker not found"
        )

    def test_add_three_games(self):
        "Test that three individual games are stored correctly"
        games = {
            "zelda: windwaker": {"progress": 15},
            "rampage": {"progress": 50},
            "the secret of mana": {"progress": 65},
        }
        # Loop through nested dict to add games
        for i in games:
            for j in games[i].values():
                self.new_game.add_game(i, j)

        # Loop through nested dict to run test
        for i in games:
            for j in games[i].values():
                self.assertIn(i, self.new_game.game_library, f'Missing "{i}"')

    def test_exception_handling_for_string(self):
        "Test that an exception is thrown when a string is passed as the second argument"
        value = "sdf8"
        self.assertRaises(
            TypeError,
            self.new_game.add_game,
            "Stardew Valley",
            value,  # This should fail
        )

    def test_exception_handling_for_disallowed_number_above_100(self):
        "Test that an exception is thrown when a number that is not 0-100 is passed as the second argument"
        value = "150"
        self.assertFalse(
            self.new_game.add_game("Stardew Valley", value), f"{value} is disallowed."
        )

    def test_exception_handling_for_disallowed_number_below_0(self):
        "Test that an exception is thrown when a number that is not 0-100 is passed as the second argument"
        value = "-10"
        self.assertFalse(
            self.new_game.add_game("Stardew Valley", value), f"{value} is disallowed."
        )


if __name__ == "__main__":
    unittest.main()
