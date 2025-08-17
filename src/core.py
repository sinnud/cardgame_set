import random

class SetGame:
    def __init__(self):
        self.score = 0
        self.deck = self.generate_full_deck()
        self.game_running = True
        self.deck_exhausted = False
        
    def generate_full_deck(self):
        shapes = ['○', '△', '□']
        colors = ['red', 'green', 'blue']
        numbers = [1, 2, 3]
        shadings = ['outline', 'striped', 'filled']
        
        deck = []
        for shape in shapes:
            for color in colors:
                for number in numbers:
                    for shading in shadings:
                        card = {'shape': shape, 'color': color, 'number': number, 'shading': shading}
                        deck.append(card)
        
        random.shuffle(deck)
        return deck
    
    def deal_initial_cards(self):
        initial_cards = self.deck[:12]
        self.deck = self.deck[12:]
        return initial_cards
    
    def is_valid_set(self, card1, card2, card3):
        properties = ['shape', 'color', 'number', 'shading']
        
        for prop in properties:
            values = [card1[prop], card2[prop], card3[prop]]
            if not (len(set(values)) == 1 or len(set(values)) == 3):
                return False
        return True
    
    def process_selection(self, selected_cards):
        if len(selected_cards) != 3:
            return False, "Must select exactly 3 cards"
        
        is_set = self.is_valid_set(selected_cards[0], selected_cards[1], selected_cards[2])
        
        if is_set:
            self.score += 1
            result_msg = f"You Win! 🎉\nScore: {self.score}"
        else:
            self.score -= 1
            result_msg = f"You Lose! ❌\nScore: {self.score}"
        
        return is_set, result_msg
    
    def get_replacement_cards(self, num_cards):
        if len(self.deck) == 0:
            self.deck_exhausted = True
            return []
        
        available_cards = min(num_cards, len(self.deck))
        replacement = self.deck[:available_cards]
        self.deck = self.deck[available_cards:]
        
        if len(self.deck) == 0:
            self.deck_exhausted = True
            
        return replacement
    
    def is_deck_exhausted(self):
        return self.deck_exhausted
    
    def cards_remaining_in_deck(self):
        return len(self.deck)
    
    def reset_game(self):
        self.score = 0
        self.deck = self.generate_full_deck()
        self.game_running = True
        self.deck_exhausted = False
        return self.deal_initial_cards()
    
    def end_game(self):
        self.game_running = False