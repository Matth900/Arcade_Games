# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards_hand = [] ## cards_hand is a list of cards
        self.hand_value = 0
     
        
    def __str__(self):
        message= "Hand contains "
        for each_card in self.cards_hand:
            message += str(each_card) + " "
        return message

    def add_card(self, card):
        self.cards_hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.hand_value = 0
        aces = 0
        for each_card in self.cards_hand:
            self.hand_value += VALUES[each_card.rank]
            if each_card.rank == "A" and (self.hand_value+10) <= 21:
                self.hand_value += 10
                aces += 1
            if aces>0 and len(self.cards_hand)>2:
                self.hand_value -=10
                aces =0
        return self.hand_value
   
    def draw(self, canvas,pos):
        # Drawing all cards for player or dealer hands
        n = 0
        for each_card in self.cards_hand:
            n+=1
            each_card.draw(canvas,[pos[0]*n,pos[1]])
            
                                                          
 
  # Define deck class
class Deck:
    def __init__(self):
        
        # Creating the deck through a list comprehension using the CARD CLASS to create CARDS
        self.deck = [Card(s,r) for s in SUITS for r in RANKS]
       
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        message_deck= "Deck contains "
        for each_card in self.deck:
            message_deck += str(each_card) + " "
        return message_deck



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand
    deck = Deck()
    deck.shuffle() 
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    outcome ="Hit or Stand?" 
    
    in_play=True
    #print "Player Hand : ", player_hand
    #print "Dealer Hand : ",dealer_hand
    

def hit():
    global player_hand,deck,in_play,outcome,score
    
    # if the hand is in play, hit the player
    if in_play== True:
        if player_hand.get_value() < 21:
            player_hand.add_card(deck.deal_card())
            if player_hand.get_value() > 21:
                outcome = "You have busted! Deal?"
                score -= 1
                in_play = False
        elif player_hand.get_value() == 21:
            stand()
    
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global player_hand,dealer_hand,deck, in_play,outcome,score
    
    
    if in_play == True:
        if player_hand.get_value()> 21:
            outcome = "You have busted! Deal?"
        else:
            if dealer_hand.get_value()>=17:
                if dealer_hand.get_value() == player_hand.get_value() or dealer_hand.get_value() > player_hand.get_value():
                    outcome= "The dealer has won! Deal?"
                    score -=1
                else:
                    outcome= "You Won"
                    score +=1
            else:
                while dealer_hand.get_value() <17:
                    dealer_hand.add_card(deck.deal_card())
                    if dealer_hand.get_value() > 21:
                        outcome= "The dealer has busted! Deal?" 
                        score +=1
                    elif dealer_hand.get_value() == player_hand.get_value() or dealer_hand.get_value() > player_hand.get_value():
                        outcome= "The dealer has won! Deal?"
                        score -=1
                    else:
                        outcome= "You Won! Deal?"
                        score +=1
   
    in_play = False
   
def reset():
    global score
    
    #Reset score to 0 for new game
    score = 0
    
    
def draw(canvas):
    global player_hand, dealer_hand
    
    #Draw Game Title
    canvas.draw_text("BLACKJACK - WEEK 6", (50,100),50,"Yellow")
    
    #Draw player and dealer labels and outcome
    canvas.draw_text("Player  ",(75,150),30,"Black")
    canvas.draw_text("Dealer  ",(75,350),30,"Black")
    canvas.draw_text(outcome,(180,150),30,"Yellow")
    
    #Draw Score
    canvas.draw_text("Score : " + str(score),(450,40),30,"Yellow")
                     
    player_hand.draw(canvas,[75,200])
    dealer_hand.draw(canvas,[75,400])
    
    if in_play == True:
        canvas.draw_image(card_back, (CARD_BACK_CENTER[0],CARD_BACK_CENTER[1]), CARD_BACK_SIZE, [75+CARD_BACK_SIZE[0]/2,400+CARD_BACK_SIZE[1]/2],CARD_SIZE)
  
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset Score",reset,200)
frame.set_draw_handler(draw)


# get things rolling
deck = Deck() # Initialize the Deck and store it as a global vaiable
player_hand = Hand() 
dealer_hand = Hand()

frame.start()
in_play=True
deal()
