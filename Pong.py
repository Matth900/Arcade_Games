# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info fohr paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    # Select random velocity for vertical and horizontal movements
    vel_hor = random.randrange(120,240)
    vel_vert = random.randrange(60,180)
    
    if direction == "RIGHT":
        ball_vel = [vel_hor/60,-vel_vert/60]
    elif direction == "LEFT":
        ball_vel = [-vel_hor/60,-vel_vert/60]
   
#Code for computer response (update of the other paddle)

def paddle2():
    global paddle2_vel,paddle2_pos
    paddle2_vel = 0
    level = {"Easy" : 2, "Medium" : 3, "Hard" : 4}
    paddle2_vel += (ball_pos[1]-paddle2_pos)*(1/(WIDTH-ball_pos[0]))*level["Easy"]
    
            
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball("LEFT")
     
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw scores
    canvas.draw_text(str(score1), ((WIDTH/3), 40), 40, 'White')
    canvas.draw_text(str(score2), (2*WIDTH/3, 40), 40, 'White')
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
                    
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,"Black","White")
    
    # determine whether ball collide with upper and lower bounds
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # update paddle's vertical position, keep paddle on the screen
      
    if (paddle1_pos + paddle1_vel) < (HALF_PAD_HEIGHT) or (paddle1_pos + paddle1_vel) > (HEIGHT -HALF_PAD_HEIGHT):
        paddle1_pos  = paddle1_pos
    else:
        paddle1_pos += paddle1_vel
    
    paddle2()
    if (paddle2_pos + paddle2_vel) < (HALF_PAD_HEIGHT) or (paddle2_pos + paddle2_vel) > (HEIGHT -HALF_PAD_HEIGHT):
        paddle2_pos  = paddle2_pos
    else:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    
    canvas.draw_polygon([(0,paddle1_pos - HALF_PAD_HEIGHT),(PAD_WIDTH,paddle1_pos - HALF_PAD_HEIGHT),(PAD_WIDTH,paddle1_pos + HALF_PAD_HEIGHT),(0,paddle1_pos + HALF_PAD_HEIGHT)], 10, "White", "White")
    canvas.draw_polygon([(WIDTH-PAD_WIDTH,paddle2_pos - HALF_PAD_HEIGHT),(WIDTH,paddle2_pos - HALF_PAD_HEIGHT),(WIDTH,paddle2_pos + HALF_PAD_HEIGHT),(WIDTH-PAD_WIDTH,paddle2_pos + HALF_PAD_HEIGHT)], 10, "White", "White")
    
    # determine whether ball collide with the gutters and/or the Paddles
    if ball_pos[0] <= (BALL_RADIUS+PAD_WIDTH):
        if (ball_pos[1]+BALL_RADIUS) < (paddle1_pos-HALF_PAD_HEIGHT) or (ball_pos[1]-BALL_RADIUS)>(paddle1_pos+HALF_PAD_HEIGHT):
            spawn_ball("RIGHT")
            score2 +=1
        else:
            ball_vel[0]= -ball_vel[0]*1.1
    
    if ball_pos[0] >= (WIDTH-1-PAD_WIDTH-BALL_RADIUS):
        if (ball_pos[1]+BALL_RADIUS) < (paddle2_pos-HALF_PAD_HEIGHT) or (ball_pos[1]-BALL_RADIUS)>(paddle2_pos+HALF_PAD_HEIGHT):
            spawn_ball("LEFT")
            score1 +=1
        else:
            ball_vel[0]= -ball_vel[0]*1.1
            
            
def keydown(key):
    global paddle1_vel
    
    pixels_step = 4
    
    if  key == simplegui.KEY_MAP["up"]:
        paddle1_vel -= pixels_step
    elif  key == simplegui.KEY_MAP["down"]:
        paddle1_vel  += pixels_step
    

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
