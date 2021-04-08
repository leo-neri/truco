import random

class Game(object):

    def __init__(self, players):
        self.suits = ['♦', '♠', '♥', '♣']
        self.numbers = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.deck = [number + suit for number in self.numbers for suit in self.suits]
        self.players = players

    def deal(self):
        round_deck = self.deck[:]
        self.players_decks = []
        for player in range(self.players):
            player_deck = []
            for i in range(3):
                card = round_deck[random.randint(0, len(round_deck)-1)]
                round_deck.remove(card)
                player_deck.append(card)
            self.players_decks.append(player_deck)
        self.turned_card = round_deck[random.randint(0, len(round_deck) - 1)]
        try:
            self.manille = self.numbers[self.numbers.index(self.turned_card[0])+1]
        except:
            self.manille = '4'

    def select_cards(self):
        self.round_cards = []
        for player in range(self.players):
            player_deck = self.players_decks[player]
            print(f'\nCarta para cima: {self.turned_card}')
            # print(f'Jogador {player+1}: Escolha uma carta:')
            # for card in player_deck:
            #     print(f'\t[{player_deck.index(card)}] - {card}')
            # choice = int(input('Insira o dígito: '))
            choice = 0
            # print(f'Insira o dígito: {choice}')
            # print(f'Carta escolhida: {player_deck[choice]}')
            self.round_cards.append(player_deck[choice])

    def round(self):
        round_cards = self.round_cards[:]
        self.card_order = self.numbers[:]
        self.card_order.remove(self.manille)
        self.card_order.append(self.manille)



