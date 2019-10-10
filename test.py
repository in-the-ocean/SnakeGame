from tkinter import * 
import random

MAP_SIZE = 40
SIDE = 15

class Snake:
    def __init__(self):
        self.body = [(5,5)]
        self.direction = (1,0)
    def change_dir(self,event):
        if event.keysym=='i' and self.direction!=(0,1):
            self.direction = (0,-1)
        elif event.keysym=='j' and self.direction!= (1,0):
            self.direction = (-1,0)
        elif event.keysym == 'k' and self.direction!=(0,-1):
            self.direction = (0,1)
        elif event.keysym == 'l' and self.direction!=(-1,0):
            self.direction = (1,0)
    def check_death(self,food):
        #new= (self.body[0]+self.direction[0],self.body[1]+self.direction[1])
        if self.body[0] in self.body[1:]:
            return 1
        elif self.body[0][0] >(MAP_SIZE-1) or self.body[0][0]<0:
            return 1
        elif self.body[0][1]>(MAP_SIZE-1) or self.body[0][1]<0:
            return 1
        else :
            return 0
    def move(self,food):
        new = ((self.body[0][0]+self.direction[0])%MAP_SIZE,
               (self.body[0][1]+self.direction[1])%MAP_SIZE)
        self.body = [new]+self.body
        if new!=food.location:
            self.body.pop()
    def check_eat(self,food):
        if self.body[0]==food.location:
            return True
        else:
            return False



class Display:
    def __init__(self):
        self.game = Game()
        self.root = Tk()
        self.Map = Canvas(self.root,bg = "black",height = MAP_SIZE*SIDE,width = MAP_SIZE*SIDE)
        self.root.bind('<KeyPress>',self.game.snake.change_dir)
        self.Map.after(100,self.next_image)
        self.Map.grid()
        self.root.mainloop()
    def draw_map(self):
        for a in self.game.snake.body:
            self.Map.create_rectangle(a[0]*SIDE,a[1]*SIDE,
                                      (a[0]+1)*SIDE,(a[1]+1)*SIDE,
                                      fill = 'blue violet')
        self.Map.create_rectangle(self.game.food.location[0]*SIDE,
                                  self.game.food.location[1]*SIDE,
                                  (self.game.food.location[0]+1)*SIDE,
                                  (self.game.food.location[1]+1)*SIDE,
                                  fill = 'orange')
    def draw_death(self):
        self.Map.delete("all")
        self.Map.create_text(MAP_SIZE*SIDE/2,MAP_SIZE*SIDE/2,
                             text = "YOU ARE DEAD",
                             font = 15,
                             fill = "DarkRed")
        self.restart = Button(self.root,text = "New Game", command = self.new_game)
        self.restart.configure(width = 20,bg = "black",fg = "DarkRed",relief = RAISED)
        self.Map.create_window(MAP_SIZE*SIDE/2,MAP_SIZE*SIDE*0.75,anchor = NW,window = self.restart)
        self.restart.grid()

    def next_image(self):
        if self.game.state == "continue":
            self.game.Refresh()
            self.Map.delete("all")
            self.draw_map()
            self.Map.after(100,self.next_image)
        else:
            self.draw_death()

    def new_game(self):
        self.restart.destroy()
        self.Map.delete("all")
        self.game = Game()
        self.root.bind('<KeyPress>',self.game.snake.change_dir)
        self.Map.after(100,self.next_image)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake)
        self.state = "continue"
    def Refresh(self):
        self.snake.move(self.food) 
        if self.snake.check_death(self.food) == 1:
            self.state = "dead"
        else:
            self.state = "continue"
        if self.snake.check_eat(self.food):
            self.food.new_food(self.snake)

class Food:
    def __init__(self,snake):
        self.location= (random.randrange(0,MAP_SIZE),random.randrange(0,MAP_SIZE)) 
        while self.location in snake.body:
            self.location= (random.randrange(0,MAP_SIZE),random.randrange(0,MAP_SIZE))
    def new_food(self,snake):
        while self.location in snake.body:
            self.location= (random.randrange(0,MAP_SIZE),random.randrange(0,MAP_SIZE))

