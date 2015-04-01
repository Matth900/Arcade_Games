# implementation of card game - Memory

import simplegui
import random

canvas_WIDTH = 800
canvas_HEIGHT = 100
exposed = []
deck = []

# helper function to initialize globals
def new_game():
    global deck,exposed,turn,state
    deck=range(0,8)
    deck += deck
    random.shuffle(deck)
    exposed = [False for ncards in range(16)]
    turn = 0
    state = 0
    
     
# define event handlers
def mouseclick(pos):
    global exposed,state,card_t0,card_t1,turn
    # add game state logic here
    clicked_card = pos[0]//50 # Each card takes 50 pixels in width
    print clicked_card
    # Control logic of the game according to which state the game is on
    if state == 0:
        exposed[clicked_card] = True  
        card_t0 = clicked_card
        state = 1
    elif state == 1:
        if exposed[clicked_card] == False:
            exposed[clicked_card] = True  
            card_t1 = clicked_card
            state = 2    
    elif state == 2:
        
        if deck[card_t0] == deck[card_t1]:
            exposed[card_t0] = True
            exposed[card_t1] = True
        else:
            exposed[card_t0] = False
            exposed[card_t1] = False
        
        turn +=1
        if exposed[clicked_card] == False:
            exposed[clicked_card] = True  
            card_t0 = clicked_card
            state = 1    

            
             
# cards are logically 50x100 pixels in size    
def draw(canvas):
    # Drawing Cards in the deck
    drawn = 0
    for card in deck:
        if exposed[drawn] == True:
            canvas.draw_text(str(card),(12+50*drawn,60),50,"White")
            #canvas.draw_line((50*drawn,0),(50*drawn,100),5,"White")
        else:
            canvas.draw_polygon([(50*drawn,0),(50*(drawn+1),0),(50*(drawn+1),100),(50*drawn,100)],5,"Black","Green")
        drawn +=1
        
        label.set_text("Turns = " + str(turn))
       

    # create frame and add a button and labels
frame = simplegui.create_frame("Memory", canvas_WIDTH, canvas_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
