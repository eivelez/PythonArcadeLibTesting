import arcade
import os
import random
import pandas as pd
initialposx=7
initialposy=12
mapHeight=25
mapWidth=25
tilesSize=100
scalesize=1
SCREEN_WIDTH=900
SCREEN_HEIGHT=700
SCREEN_TITLE="Game"
map = pd.read_excel('map.xlsx', sheet_name='map')
monsters = pd.read_excel('map.xlsx', sheet_name='monsters')
walkableList=[1]

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        for i  in range(4):
            for j in range(4):
                string="folder/"+str(i)+str(j)+".png"
                texture=arcade.load_texture(string,scale=1)
                self.textures.append(texture)
        self.set_texture(1)
        self.look=2
    def update(self):
        if self.look==0:
            self.set_texture(13)
        if self.look==1:
            self.set_texture(5)
        if self.look==2:
            self.set_texture(1)
        if self.look==3:
            self.set_texture(9)
class Monster(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.waiter=500
    def update(self):
        self.waiter+=-1
        if self.waiter<=0:
            aux=random.randint(0,3)
            if aux==0:
                self.posx+=1
            if aux==1:
                self.posx+=-1
            if aux==2:
                self.posy+=1
            if aux==3:
                self.posy+=-1
            self.waiter=500
class MapObject(arcade.Sprite):
    def __init__(self):
        super().__init__()
        #texture = arcade.load_texture("orc.png", scale=0.4)
        #self.textures.append(texture)
        #self.set_texture(0)
        self.block=False
        self.counter=0
        self.walkable=0
    #def setup(self):


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.all_sprites_list = None
        self.all_map=None
        self.all_monsters=None
        self.all_visible_monsters=None
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.playerxpos=initialposx
        self.playerypos=initialposy
        self.all_sprites_list = arcade.SpriteList()
        self.all_map=arcade.SpriteList()
        self.all_visible_monsters=arcade.SpriteList()
        self.all_monsters=arcade.SpriteList()
        self.player=Player()
        self.player.center_x=SCREEN_WIDTH/2
        self.player.center_y=SCREEN_HEIGHT/2
        self.all_sprites_list.append(self.player)
        self.block=0
        self.ctrlLock=0
        for i in range(mapWidth):
            for j in range(mapHeight):
                aux=monsters.iloc[j,i]
                if aux>0:
                    self.new_monster=Monster()
                    string="Monsters/"+str(aux)+".png"
                    self.new_monster.texture=arcade.load_texture(string)
                    self.new_monster.posx=j
                    self.new_monster.posy=i
                    self.all_monsters.append(self.new_monster)
                    self.all_sprites_list.insert(0,self.new_monster)
        for i in range(5):
            for j in range(3):
                self.new_map_sprite=MapObject()
                aux=map.iloc[self.playerypos+j-1,self.playerxpos+i-2]
                string="MapSprites/"+str(aux)+".png"
                if aux in walkableList:
                    self.new_map_sprite.walkable=1
                self.new_map_sprite.texture=arcade.load_texture(string)
                self.new_map_sprite.center_x=SCREEN_WIDTH/2+(i-2)*tilesSize
                self.new_map_sprite.center_y=SCREEN_HEIGHT/2-(j-1)*tilesSize
                self.all_map.append(self.new_map_sprite)
                self.all_sprites_list.insert(0,self.new_map_sprite)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites_list.draw()
    def on_update(self, delta_time):
        self.all_sprites_list.update()
        for i in self.all_visible_monsters:
            self.all_sprites_list.remove(i)
        self.all_visible_monsters=arcade.SpriteList()
        for i in self.all_monsters:
            if abs(i.posx-self.playerxpos)<6 and abs(i.posy-self.playerypos)<6:
                i.center_x=SCREEN_WIDTH/2-(self.playerxpos-i.posx)*tilesSize
                i.center_y=SCREEN_HEIGHT/2+(self.playerypos-i.posy)*tilesSize
                self.all_visible_monsters.append(i)
                self.all_sprites_list.append(i)


    def on_key_press(self, key, modifiers):
        if key==arcade.key.LCTRL:
            self.ctrlLock=1
        if self.block==0:
            if key==arcade.key.UP:
                if self.ctrlLock==0:
                    if self.all_map[6].walkable==1:
                        self.playerypos+=-1
                self.player.look=0
                self.block=1
            elif key==arcade.key.DOWN:
                if self.ctrlLock==0:
                    if self.all_map[8].walkable==1:
                        self.playerypos+=1
                self.player.look=2
                self.block=1
            elif key==arcade.key.RIGHT:
                if self.ctrlLock==0:
                    if self.all_map[10].walkable==1:
                        self.playerxpos+=1
                self.player.look=1
                self.block=1
            elif key==arcade.key.LEFT:
                if self.ctrlLock==0:
                    if self.all_map[4].walkable==1:
                        self.playerxpos+=-1
                self.player.look=3
                self.block=1
        for i in self.all_map:
            self.all_sprites_list.remove(i)
        self.all_map=arcade.SpriteList()
        for i in range(5):
            for j in range(3):
                self.new_map_sprite=MapObject()
                aux=map.iloc[self.playerypos+j-1,self.playerxpos+i-2]
                string="MapSprites/"+str(aux)+".png"
                if aux in walkableList:
                    self.new_map_sprite.walkable=1
                self.new_map_sprite.texture=arcade.load_texture(string)
                self.new_map_sprite.center_x=SCREEN_WIDTH/2+(i-2)*tilesSize
                self.new_map_sprite.center_y=SCREEN_HEIGHT/2-(j-1)*tilesSize
                self.all_map.append(self.new_map_sprite)
                self.all_sprites_list.insert(0,self.new_map_sprite)
        self.all_sprites_list.update()
    def on_key_release(self, key, modifiers):
        if key==arcade.key.LCTRL:
            self.ctrlLock=0
        self.block=0



def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
