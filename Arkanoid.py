# FIXING...Not working

import simplegui
import random

# initialize globals - pos and vel encode vertical info fohr paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 15
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
brick = list(range(50)) # We're assuming the grid of bricks has 50 elements by default

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    ball_vel= [0,0]
    
    # Select random velocity for vertical and horizontal movements
    vel_hor = random.randrange(120,240)
    vel_vert = random.randrange(60,180)
    
    if direction == "RIGHT":
        ball_vel = [vel_hor//60,-vel_vert//60]
    elif direction == "LEFT":
        ball_vel = [-vel_hor//60,-vel_vert//60]

# define event handlers
def new_game():
    global paddle1_pos, paddle1_vel,brick  # these are number
    global score1, score2  # these are ints
    spawn_ball("LEFT")
    paddle1_pos = WIDTH/2
    paddle1_vel = 0
    score1 = 0
    score2 = 0
    #Initialize grid of bars - Default GRID of BRICKS = 5 * 10 MATRIX - Later on: Regulate with user inputs
    for i in range(50):
        brick[i] = 1
        
def restart():
    new_game()
    
def draw(canvas):
    global score1, score2, paddle1_pos,  ball_pos, ball_vel,brick
    
    # draw scores
    canvas.draw_text(str(score1), ((WIDTH/3), 40), 40, 'White')
    canvas.draw_text(str(score2), (2*WIDTH/3, 40), 40, 'White')
    
    # draw bottom gutter
    canvas.draw_line([0, HEIGHT-PAD_WIDTH],[WIDTH, HEIGHT-PAD_WIDTH], 1, "White")
    
    # draw GRID OF BRICKS
    for i in range(50):
        if  brick[i] == 1 and i <10:
            l = 0
            canvas.draw_polygon([(i*WIDTH/10,l),(WIDTH*(i+1)/10,l),(WIDTH*(i+1)/10,(l+1)*HEIGHT/20),(i*WIDTH/10,(l+1)*HEIGHT/20)],2,"Yellow","Blue")
        elif brick[i] == 1 and  i<20:
            l = 1
            canvas.draw_polygon([((i-10)*WIDTH/10,l*HEIGHT/20),((i-10+1)*WIDTH/10,l*HEIGHT/20),((i-10+1)*WIDTH/10,(l+1)*HEIGHT/20),((i-10)*WIDTH/10,(l+1)*HEIGHT/20)],2,"Yellow","Green")
        elif brick[i] == 1 and  i<30:
            l = 2
            canvas.draw_polygon([((i-20)*WIDTH/10,l*HEIGHT/20),((i-20+1)*WIDTH/10,l*HEIGHT/20),((i-20+1)*WIDTH/10,(l+1)*HEIGHT/20),((i-20)*WIDTH/10,(l+1)*HEIGHT/20)],2,"Yellow","Violet")   
        elif brick[i] == 1 and  i<40:
            l = 3
            canvas.draw_polygon([((i-30)*WIDTH/10,l*HEIGHT/20),((i-30+1)*WIDTH/10,l*HEIGHT/20),((i-30+1)*WIDTH/10,(l+1)*HEIGHT/20),((i-30)*WIDTH/10,(l+1)*HEIGHT/20)],2,"Yellow","Red")
        elif brick[i] == 1 and  i<50:
            l = 4
            canvas.draw_polygon([((i-40)*WIDTH/10,l*HEIGHT/20),((i-40+1)*WIDTH/10,l*HEIGHT/20),((i-40+1)*WIDTH/10,(l+1)*HEIGHT/20),((i-40)*WIDTH/10,(l+1)*HEIGHT/20)],2,"Yellow","Brown")
                
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
                    
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,"Yellow","White")
    
    # determine whether ball collide with the paddle or it with the lower gutter
    
    if ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # update paddle's horizontal, keep paddle on the screen
    
    if (paddle1_pos + paddle1_vel) < (HALF_PAD_HEIGHT) or (paddle1_pos + paddle1_vel) > (WIDTH-HALF_PAD_HEIGHT):
        paddle1_pos  = paddle1_pos
    else:
        paddle1_pos += paddle1_vel
       
    # draw paddles
    
    canvas.draw_line([paddle1_pos-HALF_PAD_HEIGHT,HEIGHT], [paddle1_pos+HALF_PAD_HEIGHT,HEIGHT],PAD_WIDTH, "White")
   
    # determine whether ball collide with the Right or Left Wall
    if ball_pos[0] <= (BALL_RADIUS):
            ball_vel[0]= -ball_vel[0]
    
    if ball_pos[0] >= (WIDTH-1-PAD_WIDTH-BALL_RADIUS):
            ball_vel[0]= -ball_vel[0]
            
    
    # determine whether ball collide with some bricks (Vertical Position check)
    # Gotta start from the lowerst bricks layer. In the example positioned at 2*HEIGHT/20
    
    
    if ball_pos[1] <= (HEIGHT/4+BALL_RADIUS):
        position = (ball_pos[0]) //( WIDTH/ 10)
        if brick[position+40] ==  1:
            brick[position+40] = 0
            ball_vel[1] = -ball_vel[1]*1.05
            #print brick[position+40]
        else:
            if ball_pos[1] <= (HEIGHT/5+BALL_RADIUS):
                position = (ball_pos[0]) //( WIDTH/ 10)
                if brick[position+30] ==  1:
                    brick[position+30] = 0
                    ball_vel[1] = -ball_vel[1]*1.05
                    #print brick[position+30]
                else:
                    if ball_pos[1] <= (3*HEIGHT/20+BALL_RADIUS):
                        position = (ball_pos[0]) //( WIDTH/ 10)
                        if brick[position+20] ==  1:
                            brick[position+20] = 0
                            ball_vel[1] = -ball_vel[1]*1.05
                             #print brick[position+20]    
                        else:  	
                            if ball_pos[1] <= (HEIGHT/10+BALL_RADIUS):
                                position = (ball_pos[0]) //( WIDTH/ 10)
                                if brick[position+10] ==  1:
                                    brick[position+10] = 0
                                    ball_vel[1] = -ball_vel[1]*1.05
                                    #print brick[position+10]
                                else:
                                    if ball_pos[1] <= (HEIGHT/20+BALL_RADIUS):
                                        position = (ball_pos[0]) //( WIDTH/ 10)
                                        if brick[position] ==  1:
                                            brick[position] = 0
                                            ball_vel[1] = -ball_vel[1]*1.05
                                            #print brick[position]
                                        else:
                                            if ball_pos[1] <= (BALL_RADIUS):
                                                ball_vel[1] = -ball_vel[1]*1.05
            

        
def keydown(key):
    global paddle1_vel
    
    pixels_step = 4
    
    if  key == simplegui.KEY_MAP["right"]:
        paddle1_vel += pixels_step
    elif  key == simplegui.KEY_MAP["left"]:
        paddle1_vel  -= pixels_step
    
        
def keyup(key):
    global paddle1_vel
    paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",restart,100)


# start frame
new_game()
frame.start()
