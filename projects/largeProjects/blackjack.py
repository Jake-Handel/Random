from random import shuffle
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum, auto

class GameAction(Enum):
    HIT = auto()
    STAND = auto()
    DOUBLE = auto()
    SPLIT = auto()
    SURRENDER = auto()

@dataclass
class Card:
    rank: str
    value: int
    suit: str = ''
    
    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

class Hand:
    def __init__(self):
        self.cards: List[Card] = []
        self.is_soft: bool = False
        self.is_blackjack: bool = False
        self.is_busted: bool = False
    
    def add_card(self, card: Card) -> None:
        """Add a card to the hand and update the score."""
        self.cards.append(card)
        self._update_score()
    
    def _update_score(self) -> None:
        """Calculate the current score of the hand."""
        score = 0
        aces = 0
        
        for card in self.cards:
            score += card.value
            if card.rank == 'A':
                aces += 1
        
        # Handle aces as 11 or 1
        self.is_soft = aces > 0 and score <= 11
        if self.is_soft:
            score += 10  # Count one ace as 11
        
        self.score = score
        self.is_busted = score > 21
        self.is_blackjack = len(self.cards) == 2 and score == 21
    
    def clear(self) -> None:
        """Clear the hand for a new round."""
        self.cards = []
        self.is_soft = False
        self.is_blackjack = False
        self.is_busted = False
        self.score = 0

class Player:
    def __init__(self, name: str, initial_funds: float = 1000.0):
        """Initialize a player with a name and starting funds.
        
        Args:
            name: The player's name
            initial_funds: Starting bankroll (default: 1000.0)
        """
        self.name = name
        self.funds: float = float(initial_funds)
        self.hand = Hand()
        self.current_bet: float = 0.0
        self.insurance_bet: float = 0.0
        self.has_doubled: bool = False
        self.has_split: bool = False
        self.is_standing: bool = False
    
    def place_bet(self, amount: float) -> bool:
        """Place a bet from the player's funds.
        
        Args:
            amount: The amount to bet
            
        Returns:
            bool: True if bet was placed successfully, False otherwise
        """
        if amount <= 0:
            raise ValueError("Bet amount must be positive")
            
        if amount > self.funds:
            return False
            
        self.funds -= amount
        self.current_bet += amount
        return True
    
    def can_double(self) -> bool:
        """Check if the player can double down."""
        return len(self.hand.cards) == 2 and not self.has_doubled and self.funds >= self.current_bet
    
    def can_split(self) -> bool:
        """Check if the player can split their hand."""
        return (len(self.hand.cards) == 2 and 
                self.hand.cards[0].rank == self.hand.cards[1].rank and
                not self.has_split and
                self.funds >= self.current_bet)
    
    def double_down(self) -> None:
        """Double the current bet and receive exactly one more card."""
        if not self.can_double():
            raise ValueError("Cannot double down in current state")
            
        self.funds -= self.current_bet
        self.current_bet *= 2
        self.has_doubled = True
    
    def split_hand(self) -> 'Player':
        """Split the current hand into two separate hands.
        
        Returns:
            Player: A new Player instance with the second hand
        """
        if not self.can_split():
            raise ValueError("Cannot split hand in current state")
            
        # Create a new hand for the split
        new_player = Player(f"{self.name}'s Split")
        new_player.funds = 0
        new_player.current_bet = self.current_bet
        new_player.has_split = True
        
        # Move the second card to the new hand
        new_player.hand.add_card(self.hand.cards.pop())
        self.has_split = True
        
        # Both hands must have the same bet
        self.place_bet(self.current_bet)
        
        return new_player
    
    def payout(self, blackjack: bool = False) -> float:
        """Calculate and process winnings for the current hand.
        
        Args:
            blackjack: Whether the hand is a blackjack (pays 3:2)
            
        Returns:
            float: The amount won
        """
        if blackjack:
            winnings = self.current_bet * 2.5  # 3:2 payout for blackjack
        else:
            winnings = self.current_bet * 2    # 1:1 payout for normal win
            
        self.funds += winnings + self.current_bet
        self.current_bet = 0
        return winnings
    
    def surrender(self) -> float:
        """Surrender the current hand and receive half the bet back.
        
        Returns:
            float: The amount returned to the player (half the bet)
        """
        refund = self.current_bet / 2
        self.funds += refund
        self.current_bet = 0
        return refund
    
    def hit_or_stick(self) -> bool:
        """Prompt the player to hit or stand.
        
        Returns:
            bool: True if player chooses to hit, False to stand
        """
        while True:
            print("\nOptions:")
            print("1. Hit (take another card)")
            print("2. Stand (keep current hand)")
            
            if self.can_double():
                print("3. Double Down (double bet, take one more card)")
            if self.can_split():
                print("4. Split (split into two hands)")
                
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice in ['1', 'hit']:
                return True
            elif choice in ['2', 'stand', 's']:
                self.is_standing = True
                return False
            elif (choice in ['3', 'double', 'd']) and self.can_double():
                self.double_down()
                return True  # Player gets exactly one more card
            elif (choice in ['4', 'split', 'p']) and self.can_split():
                return self.split_hand()
            else:
                print("Invalid choice. Please try again.")

class Dealer(Player):
    def __init__(self):
        """Initialize the dealer with a name and no initial funds."""
        super().__init__("Dealer", 0)
    
    def should_hit(self) -> bool:
        """Determine if the dealer should hit based on standard casino rules."""
        return self.hand.score < 17 or (self.hand.score == 17 and self.hand.is_soft)
    
    def show_hand(self, hide_first_card: bool = False) -> str:
        """Return a string representation of the dealer's hand.
        
        Args:
            hide_first_card: Whether to hide the first card (for initial deal)
            
        Returns:
            str: Formatted string of the dealer's hand
        """
        if hide_first_card and len(self.hand.cards) > 0:
            return f"[HIDDEN] {', '.join(str(card) for card in self.hand.cards[1:])}"
        return ', '.join(str(card) for card in self.hand.cards)

class Table(object):

    def __init__(self, player: Player, funds: float = 100.0):

        self.dealer = Dealer()
        self.player = player
        self.deck = Deck()

        self.table_setup()

    def table_setup(self):

        self.deck.shuffle()

        self.player.place_bet(10)

        self.deal_card(self.player)
        self.deal_card(self.dealer)
        self.deal_card(self.player)
        self.calculate_score(self.player) 
        self.calculate_score(self.dealer)

        self.main()

    def main(self):

        while True:
            print()
            print(self)
            player_move = self.player.hit_or_stick()
            if player_move is True:
                self.deal_card(self.player)
                self.calculate_score(self.player)
            elif player_move is False:
                self.dealer_hit()

    def dealer_hit(self):

        score = self.dealer.hand.score
        while True:
            if score < 17:
                self.deal_card(self.dealer)
                self.calculate_score(self.dealer)
                print(self)
            elif score >= 17:
                self.check_final_score()

    def __str__(self):

        dealer_hand = [card for card in self.dealer.hand.cards]
        player_hand = [card for card in self.player.hand.cards]

        print("Dealer hand : {}".format(dealer_hand))
        print("Dealer score : {}".format(self.dealer.hand.score))
        print()
        print("{}'s hand : {}".format(self.player.name, player_hand))
        print("{}'s score : {}".format(self.player.name, self.player.hand.score))
        print()
        print(("{}'s current bet: {}.".format(self.player.name, self.player.current_bet)))
        print("{}'s current bank: {}.".format(self.player.name, self.player.funds))
        print("-" * 40)
        return ''

    def deal_card(self, player: Player):

        card = self.deck.stack.pop()
        player.hand.add_card(card)

    def calculate_score(self, player: Player):

        if player.hand.is_busted:
            print()
            print(self)
            print("{} busts".format(player.name))
            print()
            self.end_game()
        elif player.hand.is_blackjack:
            print(self)
            print("{} blackjack!".format(player.name))
            try:  
                player.payout(True)
            except:
                pass
            self.end_game()
        else:
            return

    def check_final_score(self):

        dealer_score = self.dealer.hand.score
        player_score = self.player.hand.score

        if dealer_score > player_score:
            print("Dealer wins!")
            self.end_game()
        else:
            print("{} wins!".format(self.player.name))
            self.player.payout()
            self.end_game()

    def end_game(self):

        bank = self.player.funds
        if bank >=10:
            again = input("Do you want to play again (Y/N)? ")
            if again.lower().startswith('y'):
                self.__init__(self.player, funds=self.player.funds)
            elif again.lower().startswith('n'):
                exit(1) 
        elif bank < 10:
            print("You're all out of money!  Come back with some more dough, good luck next time!")
            exit(2)


class Deck(object):

    def __init__(self):

        self.stack = [Card('A', 1), Card('2', 2), Card('3', 3), Card('4', 4), Card('5', 5),
                      Card('6', 6), Card('7', 7), Card('8', 8), Card('9', 9), Card('10', 10),
                      Card('J', 10), Card('Q', 10), Card('K', 10)] * 4
        self.shuffle()

    def shuffle(self):

        shuffle(self.stack)

    def deal_card(self):

        card = self.stack.pop()
        return card


def main():

    player_name = input("Welcome to the casino!  What's your name? ")
    player = Player(player_name)
    Table(player)


if __name__ == '__main__':

    main()