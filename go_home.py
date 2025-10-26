import pgzero
import math

WIDTH = 1200
HEIGHT = 600

velocity_y = 0
velocity_x = 5
gravity = 1
terminal_velocity=20

game_state = 'Main_Menu'
game_mute = False

player_state = 'idle'
player_on_ground=False

player_move_right_animation = ['alien_pink_walk1','alien_pink_walk2']
player_move_left_animation = ['alien_pink_walk_left1','alien_pink_walk_left2']
player_idle_animation = ['alien_pink_stand','alien_pink_front']


enemy_move_animation = ['fly','fly_move']
#enemy_idle_animation = ['enemy_idle_0','enemy_idle_1','enemy_idle_2']
animator_list=[]

player = Actor('alien_pink_stand')
starting_position=[100,500]
player.topright = starting_position[0],starting_position[1]

ufo=Actor('ufo')
ufo.topright = 90,100

ground_list=[]
enemies_list=[]

start = Rect((20, 20), (250, 30))
mute = Rect((20, 50), (250, 30))
quit_game = Rect((20, 80), (250, 30))





def draw():
    screen.clear()
    #print(game_state)
    if game_state == 'Main_Menu':
        draw_menu()

    elif game_state == 'Game':
        draw_game()

    else:
        draw_win()


def draw_menu():


    screen.draw.filled_rect(start, (255, 0, 0))
    screen.draw.filled_rect(mute, (0, 255, 0))
    screen.draw.filled_rect(quit_game, (0, 0, 255))

    screen.draw.text('Start Game',(25,25), color=(255, 255, 255), fontname='publicpixel', fontsize=20)
    if game_mute:
        screen.draw.text('Unmute',(25,55), color=(255, 255, 255), fontname='publicpixel', fontsize=20)
    else:
        screen.draw.text('Mute',(25,55), color=(255, 255, 255), fontname='publicpixel', fontsize=20)
    screen.draw.text('Exit',(25,85), color=(255, 255, 255), fontname='publicpixel', fontsize=20)


    screen.draw.text('Instrucoes',(25,180), color=(255, 255, 255), fontname='publicpixel', fontsize=30)
    screen.draw.text('Utilise as setas para mover o alien',(25,230), color=(255, 255, 255), fontname='publicpixel', fontsize=20)
    screen.draw.text('Evite as moscas',(25,260), color=(255, 255, 255), fontname='publicpixel', fontsize=20)
    screen.draw.text('Chegue em seu veiculo',(25,290), color=(255, 255, 255), fontname='publicpixel', fontsize=20)
    screen.draw.text('Retorne ao seu lar',(25,320), color=(255, 255, 255), fontname='publicpixel', fontsize=20)


def draw_game():
    player.draw()
    ufo.draw()
    for ground in ground_list:
        screen.draw.filled_rect(ground.ground, ground.color)
        screen.draw.filled_rect(ground.roof, ground.color)
        screen.draw.filled_rect(ground.plataform, ground.color)

    for enemylis in enemies_list:
        enemylis.act.draw()

def draw_win():

    win = Rect((300, 250), (600, 50))
    screen.draw.filled_rect(win, (255, 0, 0))
    screen.draw.text('VOLTOU AO LAR',(400,260), color=(255, 255, 255), fontname='publicpixel', fontsize=30)
    act =Actor('alien_pink_front')
    act.x=600
    act.y=200
    act.draw()


def update():
    global game_state
    if game_state == 'Game':
        movement_manager()
        animation_manager()
        for enemylis in enemies_list:
            enemylis.enemy_update()
        if player.colliderect(ufo):
            #print('win')
            game_state='win_screen'

def movement_manager():
    player_movement_manager()

def animation_manager():
    player_animator()

def player_animator():
    #print('animating',player_state)
    if player_state=='idle':
        animator_player_idle.animator_update()
    elif player_state=='jump':
        player.image=('aliem_pink_jump')
    elif player_state=='run_right':
        animator_player_run_right.animator_update()
    else :
        animator_player_run_left.animator_update()


def player_movement_manager():
    global velocity_y
    global player_state
    global player_on_ground

    player_on_ground=False
    player_jumping=False

    player_movement=0

    collision_ground=False
    collision_plat=False
    collision_roof=False

    player_state='idle'

    if keyboard.left and player.x > 80:
        player_movement=-velocity_x
        player_state='run_left'
    if keyboard.right and player.x < WIDTH - 80:
        player_movement=velocity_x
        player_state='run_right'

    player_move_x(player_movement)
    player_move_y(velocity_y)

    for plat in ground_list:
        if player.colliderect(plat.ground):
            player_on_ground=True

    if keyboard.up and player_on_ground:
        velocity_y = -15
        player.y+= -10
        player_state='jump'
        if not game_mute:
            sounds.jump.play()
        #print('jump')

    if not(collision_plat and (collision_ground or collision_roof)):
        pass



    if not player_on_ground and velocity_y<terminal_velocity:
        player_state='jump'
        velocity_y += gravity


def player_move_x(dist):
    is_positive=True
    collided=False
    if dist<0:
        is_positive=False
        dist=dist*-1
    i=0
    old_x=player.x
    collision_ground_manager(old_x,player.y)
    while i<dist:
        i+=1
        old_x=player.x
        if is_positive:
            player.x+=1
        else:
            player.x-=1

        if collision_ground_manager(old_x,player.y)==0:
            pass


def player_move_y(dist):
    is_positive=True
    collided=False
    if dist<0:
        is_positive=False
        dist=dist*-1
    i=0
    old_y=player.y

    collision_ground_manager(player.x,old_y)
    while i<dist:
        i+=1
        old_y=player.y
        if is_positive:
            player.y+=1
        else:
            player.y-=1

        if collision_ground_manager(player.x,old_y)==0:
            pass

def collision_ground_manager(old_x,old_y):

    collision_ground=False
    collision_plat=False
    collision_roof=False
    global player_on_ground
    player_on_ground=False
    global velocity_y
    for plat in ground_list:

        if player.colliderect(plat.ground):

            #print("CHAO")
            player.y=old_y
            player_on_ground=True
            return 0

        if player.colliderect(plat.plataform):
            #print ("SOLIDO")
            player.x=old_x
            return 1
        if player.colliderect(plat.roof):
            #print("TETO")
            player.y=old_y
            velocity_y=0+gravity
            return 2
    return -1



def on_mouse_down(pos):
    global game_state
    global game_mute
    #print("Mouse clicked", pos)
    #debug
    #if game_state=='Game':
    #    player.x=pos[0]
    #    player.y=pos[1]
    if game_state=='Main_Menu':
        if (pos[0]>20 and pos[0]<270) and (pos[1]>25 and pos[1]<50):
            #print("Start")
            game_start()
            game_state='Game'

        if (pos[0]>20 and pos[0]<270) and (pos[1]>55 and pos[1]<80):

            if game_mute:
                game_mute=False
                #print('unmuted')
            else:
                game_mute=True
                #print('muted')

        if (pos[0]>20 and pos[0]<270) and (pos[1]>80 and pos[1]<110):
            #print("Quit")
            quit()

def game_start():
    #print("Starting game")

    if not game_mute:
        music.play('706366__ztidlen__instrumentaliasound-instrumentalgenre-4')
        music.set_volume(0.4)

    ground_list.append(class_plataform((0, 580), (WIDTH, 40), 102, 255, 102))

    ground_list.append(class_plataform((400, 470), (200, 20), 200, 150, 50))
    ground_list.append(class_plataform((700, 370), (150, 20), 150, 100, 255))

    ground_list.append(class_plataform((950, 320), (180, 20), 200, 150, 50))
    ground_list.append(class_plataform((1050, 220), (50, 20), 200, 150, 50))

    ground_list.append(class_plataform((640, 170), (280, 20), 100, 150, 50))

    ground_list.append(class_plataform((50, 250), (500, 20), 100, 150, 50))
    ground_list.append(class_plataform((50, 140), (50, 20), 100, 250, 150))



    enemies_list.append(class_enemy((620,280),120,0,2,enemy_move_animation))
    enemies_list.append(class_enemy((60,200),150,3,0,enemy_move_animation))


    global animator_player_run_left
    animator_player_run_left = animator(player_move_left_animation,player,7)
    global animator_player_idle
    animator_player_idle = animator(player_idle_animation,player,15)
    global animator_player_run_right
    animator_player_run_right = animator(player_move_right_animation,player,15)


def player_hit_manager():
    #print('bzz')
    if not game_mute:
        sounds.eep.play()
    player.topright = starting_position[0],starting_position[1]


class class_enemy:
    def __init__(self, coord, time, speed_x, speed_y, enemy_animator_list):
        self.coord = coord
        self.time = time
        self.speed_x = speed_x
        self.speed_y = speed_y
        #print(enemy_animator_list)
        self.act = Actor(enemy_animator_list[0])
        self.animator = animator(enemy_animator_list, self.act, 10)
        self.act.topleft = coord
        self.timer = 0

    def enemy_update(self):
        self.animator.animator_update()
        self.move()
        if player.colliderect(self.act):
            player_hit_manager()


    def move(self):
        self.timer += 1
        if self.timer >= self.time:
            self.timer = 0
            self.speed_x *= -1
            self.speed_y *= -1

        self.act.x += self.speed_x
        self.act.y += self.speed_y




class class_plataform:
    def __init__(self,coord, size, red,green,blue):
        self.coord=coord
        self.size = size
        self.color=(red,green,blue)
        self.plataform = Rect(coord, size)
        self.ground = Rect ((coord[0]+1,coord[1]-1),(size[0]-2,5))
        self.roof=Rect ((coord[0]+1,coord[1]+(size[1]-4)),(size[0]-2,5))




class animator:
    def __init__(self,img_list, act,frames):
        self.img_list = img_list
        self.act = act
        self.frames=frames
        self.index = 0
        self.timer = 0

    def animator_update(self):
        self.timer += 1
        if self.timer %  10 == 0:
            self.index = (self.index + 1) % len(self.img_list)
            self.act.image = self.img_list[self.index]


















