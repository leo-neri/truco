from game import Game

game = Game(2)
while True:
    game.deal()
    # game.select_cards()
    game.round()