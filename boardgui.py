import pygame as p
from isolation import Board
from mcts import MCTS

HEIGHT = 512
WIDTH = (516 // 6) * 8
DIMENSION_X = 8
DIMENSION_Y = 6
SQ_SIZE = HEIGHT // DIMENSION_Y
MAX_FPS = 15
IMAGES = {}
colors = []
BOT_TIME = 0.5 #in secs

def load_images():
    IMAGES['bN'] = p.transform.scale(p.image.load('images/bN.png'), (SQ_SIZE, SQ_SIZE)) 
    IMAGES['wN'] = p.transform.scale( p.image.load('images/wN.png'), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    p.mixer.init()
    move_sound = p.mixer.Sound('sounds/move-self.mp3')
    victory_sound = p.mixer.Sound('sounds/won.mp3')
    loss_sound = p.mixer.Sound('sounds/loss.mp3')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = Board("white","black", 8, 6)
    white_player = None
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False
    game_started = False
    sound_flag = True
    while(running):
        if(white_player and gs.active_player == "black" and game_started):
            # bot move
            move = MCTS(gs, BOT_TIME, "black")
            p.mixer.Sound.play(move_sound)
            gs.apply_move(move)
        
        if(not white_player and gs.active_player == "white" and game_started):
            move = MCTS(gs, BOT_TIME, "white")
            p.mixer.Sound.play(move_sound)
            gs.apply_move(move)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if(not game_over and game_started):
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if(len(gs.get_legal_moves()) == 48 or len(gs.get_legal_moves()) == 47):
                        sq_selected = (row, col)
                        if(sq_selected in gs.get_legal_moves()):
                            gs.apply_move(sq_selected)
                        
                        sq_selected = ()
                    
                    if(sq_selected == (row,col)):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    
                    if(len(player_clicks) == 2):
                        current_player_loc = gs.get_player_location("white") if gs.active_player == "white" else gs.get_player_location("black")
                        if(player_clicks[0] == current_player_loc):
                            if(gs.move_is_legal(player_clicks[1])):
                                # the move can be performed
                                animate_move(player_clicks, screen, gs, clock, move_sound)
                                gs.apply_move(player_clicks[1])
                                print(gs.to_string())
                                
                                

                        sq_selected = ()
                        player_clicks = []
            elif e.type == p.KEYDOWN:
                if(e.key == p.K_r):
                    gs = Board("white","black",8,6)
                    sq_selected = ()
                    player_clicks = []
                    game_started = False
                    game_over = False
                    sound_flag = True
                if(e.key == p.K_w and not game_started):
                    white_player = True
                    game_started = True
                if(e.key == p.K_b and not game_started):
                    white_player = False
                    game_started = True
                    


        draw_game_state(screen, gs, sq_selected, game_started)

        if(len(gs.get_legal_moves()) == 0):
            game_over = True
            
            if(gs.is_winner('white')):
                draw_text(screen, "White Wins! (Press R to Reset)")
                if(sound_flag):
                    if(white_player):
                        p.mixer.Sound.play(victory_sound)
                    else:
                        p.mixer.Sound.play(loss_sound)
            else:
                draw_text(screen, "Black Wins!(Press R to Reset)")
                if(sound_flag):
                    if(white_player):
                        p.mixer.Sound.play(loss_sound)
                    else:
                        p.mixer.Sound.play(victory_sound)
            sound_flag = False

        clock.tick(MAX_FPS)
        p.display.flip()

def highlight_square(screen, gs, sq_selected):
    if(sq_selected != ()):
        r,c = sq_selected
        current_player_loc = gs.get_player_location("white") if gs.active_player == "white" else gs.get_player_location("black")
        if sq_selected == current_player_loc:
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('dark blue'))
            screen.blit(s, (c * SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in gs.get_legal_moves():
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))


def draw_board(screen, game_started):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION_Y):
        for c in range(DIMENSION_X):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if(not game_started):
        draw_text(screen, "Press W for White Piece and B for Black")

def draw_pieces(screen, gs):
    p1_loc = gs.get_player_location("white")
    if(p1_loc):
        screen.blit(IMAGES['wN'], p.Rect(p1_loc[1] * SQ_SIZE, p1_loc[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    p2_loc = gs.get_player_location("black")
    if(p2_loc):
        screen.blit(IMAGES['bN'], p.Rect(p2_loc[1] * SQ_SIZE, p2_loc[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    blank_spaces = gs.get_blank_spaces()
    for i in range(DIMENSION_Y):
        for j in range(DIMENSION_X):
            pos = (i,j)
            if pos not in blank_spaces and (pos != p1_loc and pos != p2_loc): 
                p.draw.rect(screen, p.Color('gray12'), p.Rect(pos[1] * SQ_SIZE, pos[0] * SQ_SIZE, SQ_SIZE-2, SQ_SIZE-2))



def draw_game_state(screen, gs, sq_selected, game_started):
    draw_board(screen, game_started)
    highlight_square(screen, gs, sq_selected)
    draw_pieces(screen, gs)


def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True)
    text_object = font.render(text, 0, p.Color('white'))
    text_location = p.Rect(0,0,WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT / 2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text,0, p.Color('black'))
    screen.blit(text_object, text_location.move(2,2))

def animate_move(move, screen, gs, clock, move_sound):
    global colors
    dR = move[1][0] - move[0][0]
    dC = move[1][1] - move[0][1]
    framePerSquare = 10
    frameCount = (abs(dR) - abs(dC)) * framePerSquare
    piece_moved = "wN" if gs.get_player_location("white") == move[0] else "bN"
    for frame in range(frameCount + 1):
        r,c = move[0][0] + dR * frame / frameCount, move[0][1] + dC * frame / frameCount
        draw_board(screen, True)
        draw_pieces(screen, gs)
        color = colors[(move[1][0] + move[1][1]) % 2]
        end_square = p.Rect(move[1][1] * SQ_SIZE, move[1][0] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)

        screen.blit(IMAGES[piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    
    p.mixer.Sound.play(move_sound)

if __name__ == "__main__":
    main()


