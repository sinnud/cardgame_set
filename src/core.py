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
        rule_details = {}
        is_valid = True
        
        for prop in properties:
            values = [card1[prop], card2[prop], card3[prop]]
            unique_count = len(set(values))
            
            if unique_count == 1:
                rule_details[prop] = {'status': 'satisfied', 'type': 'all_same', 'values': values}
            elif unique_count == 3:
                rule_details[prop] = {'status': 'satisfied', 'type': 'all_different', 'values': values}
            else:
                rule_details[prop] = {'status': 'violated', 'type': 'mixed', 'values': values}
                is_valid = False
        
        return is_valid, rule_details
    
    def process_selection(self, selected_cards):
        if len(selected_cards) != 3:
            return False, "Must select exactly 3 cards"
        
        is_set, rule_details = self.is_valid_set(selected_cards[0], selected_cards[1], selected_cards[2])
        
        if is_set:
            self.score += 1
            result_msg = f"You Win! 🎉\nScore: {self.score}\n\n"
            result_msg += self._format_rule_explanation(rule_details, True)
        else:
            self.score -= 1
            result_msg = f"You Lose! ❌\nScore: {self.score}\n\n"
            result_msg += self._format_rule_explanation(rule_details, False)
        
        return is_set, result_msg
    
    def _format_rule_explanation(self, rule_details, is_win):
        explanation = "Rule Analysis:\n"
        
        property_names = {
            'shape': 'Shape',
            'color': 'Color', 
            'number': 'Number',
            'shading': 'Shading'
        }
        
        for prop, details in rule_details.items():
            prop_name = property_names[prop]
            status = details['status']
            rule_type = details['type']
            values = details['values']
            
            if status == 'satisfied':
                if rule_type == 'all_same':
                    explanation += f"✓ {prop_name}: All same ({values[0]})\n"
                else:  # all_different
                    explanation += f"✓ {prop_name}: All different ({', '.join(map(str, values))})\n"
            else:  # violated
                explanation += f"✗ {prop_name}: Mixed - not all same or all different ({', '.join(map(str, values))})\n"
        
        if is_win:
            explanation += "\nAll 4 rules satisfied - Valid SET!"
        else:
            satisfied_count = sum(1 for details in rule_details.values() if details['status'] == 'satisfied')
            explanation += f"\nOnly {satisfied_count}/4 rules satisfied - Invalid SET"
        
        return explanation
    
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