import arcade
import os
import random
#from PIL import Image
#im = Image.open("test2.png")
#for i in range(4):
#    for j in range(4):
#        imc=im.crop((47*i, 61.25*j, 47*(i+1), 61.25*(j+1)))
#        string="folder/"+str(j)+str(i)+".png"
#        imc.save(string)
SPRITE_SCALING = 1
UPDATES_PER_FRAME = 12
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Juego Bacan"
MOVEMENT_SPEED = 1


class Orcs(arcade.Sprite):
    def __init__(self):
        super().__init__()
        texture = arcade.load_texture("orc.png", scale=0.4)
        self.textures.append(texture)
        self.set_texture(0)

        self.block=False
        self.counter=0
        self.ymov=0
        self.xmov=0

    def update(self):
        if self.block==False:
            if self.change_x<0:
                self.xmov=-1
                self.counter=64
                self.block=True
            elif self.change_x>0:
                self.xmov=1
                self.counter=64
                self.block=True
            elif self.change_y>0:
                self.ymov=1
                self.counter=64
                self.block=True
            elif self.change_y<0:
                self.ymov=-1
                self.counter=64
                self.block=True

        elif self.block==True:
            self.center_x += self.xmov
            self.center_y += self.ymov
            self.counter+=-1
            if self.counter==0:
                self.block=False
                self.xmov=0
                self.ymov=0
class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()
        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        for i in range(4):
            for j in range(4):
                string="folder/"+str(i)+str(j)+".png"
                texture = arcade.load_texture(string, scale=SPRITE_SCALING)
                self.textures.append(texture)

        # By default, face right.
        self.set_texture(0)
        self.a=0
        self.b=0
        self.block=False
        self.counter=0
        self.spell=0

    def update(self):
        if self.block==False:
            if self.change_x<0:
                self.a=8
                self.counter=64
                self.block=True
            elif self.change_x>0:
                self.a=4
                self.counter=64
                self.block=True
            elif self.change_y>0:
                self.a=12
                self.counter=64
                self.block=True
            elif self.change_y<0:
                self.a=0
                self.counter=64
                self.block=True

        elif self.block==True:
            self.counter+=-1
            self.set_texture(self.a+(64-self.counter)//16)
            if self.counter==1:
                self.block=False

class MapThings(arcade.Sprite):

    def __init__(self):
        super().__init__()
        texture = arcade.load_texture("6.gif", scale=2)
        self.textures.append(texture)
        self.set_texture(0)
        self.block=False
        self.counter=0
        self.ymov=0
        self.xmov=0

    def update(self):
        if self.block==False:
            if self.change_x<0:
                self.xmov=-1
                self.counter=64
                self.block=True
            elif self.change_x>0:
                self.xmov=1
                self.counter=64
                self.block=True
            elif self.change_y>0:
                self.ymov=1
                self.counter=64
                self.block=True
            elif self.change_y<0:
                self.ymov=-1
                self.counter=64
                self.block=True

        elif self.block==True:
            self.center_x += self.xmov
            self.center_y += self.ymov
            self.counter+=-1
            if self.counter==0:
                self.block=False
                self.xmov=0
                self.ymov=0

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.all_sprites_list = None
        self.all_map=None

        # Set up the player info
        self.player_sprite = None
        self.things_sprites = None
        self.spell_sprites=None
        self.orcs_sprite=None
        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.all_map =arcade.SpriteList()
        self.spell_sprites=arcade.SpriteList()
        self.orcs_sprites_List=arcade.SpriteList()
        # Set up the player
        x=0
        y=0
        for i in range(10):
            for j in range(15):
                self.things_sprites = MapThings()
                self.things_sprites.center_x = x+SCREEN_WIDTH / 2
                self.things_sprites.center_y = y+SCREEN_HEIGHT / 2
                self.all_sprites_list.append(self.things_sprites)
                self.all_map.append(self.things_sprites)
                y+=64
            y=0
            x+=64
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.all_sprites_list.append(self.player_sprite)
        self.orcs_sprite = Orcs()
        self.orcs_sprite.center_x = SCREEN_WIDTH / 2+128
        self.orcs_sprite.center_y = SCREEN_HEIGHT / 2+128
        self.all_sprites_list.append(self.orcs_sprite)
        self.orcs_sprites_List.append(self.orcs_sprite)
        self.all_map.append(self.orcs_sprite)
        self.spellActive=0
        self.spellCD=40

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.all_sprites_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.all_sprites_list.update()
        if self.spellActive==1:
            self.spellCD+=-1
            if self.spellCD<=0:
                removetwice=[]
                for i in self.spell_sprites:
                    removetwice.append(i)
                    self.all_sprites_list.remove(i)
                    self.spellCD=40
                    self.spellActive=0
                for i in removetwice:
                    self.spell_sprites.remove(i)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.player_sprite.block==False and self.spellActive==0:
            listaX=[-1,0,1,-1,1,-1,0,1]
            listaY=[1,1,1,0,0,-1,-1,-1]
            for i in range(8):
                self.spellActive=1
                self.things_sprites = MapThings()
                self.things_sprites.center_x = (SCREEN_WIDTH/2)+listaX[i]*64
                self.things_sprites.center_y = (SCREEN_HEIGHT/2)+listaY[i]*64
                self.things_sprites.texture=arcade.load_texture("hitmark.png", scale=0.1)
                self.all_sprites_list.insert(len(self.all_sprites_list)-1,self.things_sprites)
                self.all_map.append(self.things_sprites)
                self.spell_sprites.append(self.things_sprites)
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
            for spr in self.all_map:
                spr.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            for spr in self.all_map:
                spr.change_y = MOVEMENT_SPEED
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            for spr in self.all_map:
                spr.change_x = MOVEMENT_SPEED
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            for spr in self.all_map:
                spr.change_x = -MOVEMENT_SPEED
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.RIGHT or key==arcade.key.LEFT:
            for spr in self.all_map:
                spr.change_x = 0
            self.player_sprite.change_x = 0
        if key == arcade.key.UP or key==arcade.key.DOWN:
            for spr in self.all_map:
                spr.change_y = 0
            self.player_sprite.change_y = 0

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
