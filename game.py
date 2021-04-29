from collections import Counter
import operator
import random

class Game(object):

    def __init__(self, players):
        self.suits = ['♦', '♠', '♥', '♣']
        self.numbers = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.deck = [number + suit for number in self.numbers for suit in self.suits]
        self.players = players
        self.round_value = 1
        self.score = [0, 0]

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

    def display_cards(self, player, hide=False, turned_down=False):
            player_deck = self.players_decks[player]
            print(f'\nCarta para cima: {self.turned_card}')
            print(f'Jogador {player + 1}: Escolha uma carta{"para esconder" if turned_down else ""}:')
            for card in player_deck:
                if hide:
                    print(f'\t[{player_deck.index(card)}] - XXX')
                else:
                    print(f'\t[{player_deck.index(card)}] - {card}')
            if self.round_value == 1:
                print('\t[T] - Truco')
            elif self.round_value == 3:
                print('\t[6] - Seis')
            elif self.round_value == 6:
                print('\t[9] - Nove')
            elif self.round_value == 9:
                print('\t[12] - Doze')

    def select_cards(self, hide=False):
        self.round_cards = []
        for player in range(self.players):
            self.display_cards(player=player, hide=hide)
            self.get_choice()

    def get_choice(self):
        while True:
            try:
                # choice = input('Insira a opção: ').upper()
                choice = 'T'
                if choice == 'T':
                    print('TRUCO!')
                    answer = self.accept(value=choice)
                    if answer == 'correu':
                        print('correu')
                    elif answer == 'aceitou':
                        print('aceitou')
                    else:
                        print('SEIS!')
                elif choice == '6':
                    answer = self.accept(value=choice)
                    if answer == 'correu':
                        print('correu')
                    elif answer == 'aceitou':
                        print('aceitou')
                    else:
                        print('NOVE!')
                elif choice == '9':
                    self.round_value = 9
                    print('NOVE!')
                elif choice == '12':
                    self.round_value = 12
                    print('DOZE!')
                else:
                    choice = int(choice)
                player_deck = self.players_decks[player]
                self.round_cards.append(player_deck[choice])
                del self.players_decks[player][choice]
                break
            except:
                print('Insira uma opção válida!')
                continue

    def battle(self):
        round_cards = self.round_cards[:]
        print(round_cards)
        self.cards_order = self.numbers[:]
        self.cards_order.remove(self.manille)
        self.cards_order.append(self.manille)
        card_values = [(self.cards_order.index(card[0])+1) for card in round_cards]
        max_value = max(card_values)
        values_dict = dict(Counter(card_values))
        if values_dict[max_value] != 1 and max_value != 10:
            print('Empate!')
            return None
        elif values_dict[max_value] != 1 and max_value == 10:
            suits_values = [(self.suits[:].index(card[1])+1) for card in round_cards]
            winner = suits_values.index(max(suits_values))
            print(f'Jogador {winner+1} venceu!')
            return winner
        else:
            winner = card_values.index(max(card_values))
            print(f'Jogador {winner + 1} venceu!')
            return winner

    def turn(self, hide=False):
        round_score = [0, 0]
        first_round_winner = None
        while (max(round_score) < 2 or (min(round_score) == 2 and max(round_score) != 3)) or round_score == [2, 2]:
            try:
                self.select_cards(hide=hide)
                winner = self.battle()
                if winner is not None:
                    if max(round_score) == 0:
                        first_round_winner = winner
                    round_score[winner] += 1
                else:
                    round_score = list(map(operator.add, round_score, [1, 1]))
                print(round_score)
            except:
                print(f'Jogador {first_round_winner + 1} venceu!')
                break
        if round_score == [3, 3]:
            round_winner = None
            print('\nA rodada empatou!')
        else:
            round_winner = round_score.index(max(round_score))
            print(f'Jogador {round_winner + 1} venceu a rodada!')
        return round_winner

    def round(self, hide=False):
        round_winner = self.turn(hide=hide)
        if round_winner is not None:
            self.score[round_winner] += self.round_value
        print(f'\nPlacar: {self.score[0]} x {self.score[1]}')

    def accept(self, value):
        print('value', value)
        values_dict = {'T': 'Truco', '6': 'Seis', '9': 'Nove', '12': 'Doze'}
        print(f'O oponente pediu {values_dict[value]}. O que deseja fazer?')
        print('[C] - Correr')
        print('[A] - Aceitar')
        next_truco_int = list(values_dict.keys())[(list(values_dict.keys()).index(value))+1]
        next_truco_str = values_dict[list(values_dict.keys())[list(values_dict.keys()).index(value) + 1]].capitalize()
        print(f'[{next_truco_int}] - Pedir {next_truco_str}')
        option = input('Insira a opção: ').upper()
        # option = 'P'
        if option == 'C':
            print('Correu!')
            return 'correu'
        if option == 'A':
            print('Aceitou!')
            self.round_value = 3
            return values_dict[value]
        if option == next_truco_int:
            print(f'Pediu {next_truco_str}')
            return next_truco_str

    def play(self):
        while max(self.score) < 12:
            self.deal()
            if self.score != [11, 11]:
                self.round()
            else:
                self.round(hide=True)
        winner = self.score.index(max(self.score))
        print(f'Jogador {winner+1} venceu o jogo por {self.score[0]} x {self.score[1]}!')
        self.score = [0, 0]

