'''
Created on 2013-2-11

This module is used to generate the 

wumpus world and show it to the board

@author: Hao Zou
'''
import os 

class Wumpus_World:
    # the array used to show the world.
    board = []
    # the dictionary used to save the content of the world such as W, B, P...
    # the key word is the position.
    world = {}
    # use to reset the world
    reset_world = {}
    # use to reset the board
    reset_board = {}
    # the gold numbers in the world
    gold_count = 1
    def __init__(self,filename):
        w = open(filename)
        # read the world from the file
        
        for line in w:
            line = line.strip()
            if len(line) == 3:
                pos = (int(line[1]),int(line[2]))
                # read the start pos and end pos, and the size of the world
                if line[0] == 'A':
                    self.start = pos
                elif line[0] == 'M':
                    self.row = pos[0]
                    self.column = pos[1]
                    self.board = [([''] * self.row) for i in range(self.column)]
                # read the content of the world 
                elif line[0] == 'B':
                    if self.world.has_key(pos):
                        self.world[pos] = ''.join(self.world[pos]+'B')
                    else:
                        self.world[pos] = 'B'
                        
                elif line[0] == 'P':
                    if self.world.has_key(pos):
                        self.world[pos] = ''.join(self.world[pos]+'P')
                    else:
                        self.world[pos] = 'P'
                        
                elif line[0] == 'S':
                    if self.world.has_key(pos):
                        self.world[pos] = ''.join(self.world[pos]+'S')
                    else:
                        self.world[pos] = 'S'
                        
                elif line[0] == 'W':
                    if self.world.has_key(pos):
                        self.world[pos] = ''.join(self.world[pos]+'W')
                    else:
                        self.world[pos] = 'W'
                        
                elif line[0] == 'G':
                    if self.world.has_key(pos):
                        self.world[pos] = ''.join(self.world[pos]+'G')
                    else:
                        self.world[pos] = 'G'
                else:
                    print "error"
                    quit()
            elif len(line) == 4:
                if line[0:2] == 'GO':
                    pos = (int(line[2]),int(line[3]))
                    self.end = pos
                elif line[0:3] == 'POT':
                    self.gold_count = int(line[3])
            else:
                print "error"
                quit()
           
        
        self.board[self.column-self.start[1]][self.start[0]-1] = 'A'  
        self.reset_world = self.world
        self.reset_board = self.board
        #print self.world
    def reset(self):
        self.world = self.reset_world
        self.board = self.reset_board
    # change the board
    def change_board(self,old, pos,content):
        if old:
            str = self.board[self.column-old[1]][old[0]-1]
            self.board[self.column-old[1]][old[0]-1] = str.replace('A','')
        
        self.board[self.column-pos[1]][pos[0]-1] = content
        
    # draw the world
    def draw_board(self):
        j = 0
        for row in self.board:
            print '-----------------------------------------------------------------------'
            i = 0
            for column in row:
                if i == 0:
                    print '|',
                    i += 1
                print '%s\t' % (column),'|',
             
            print 
            j += 1
            if j == self.column:
                print '-----------------------------------------------------------------------'

          
        
if __name__ == '__main__':
    
    # just for test use
    #world.board[1][1] = world.board[1][1].replace('G','')
    #world.change_board((world.start[0],world.start[1]+1), world.world[(world.start[0],world.start[1]+1)]+'A')
    w = Wumpus_World("wumpus_world2.txt") 
    w.draw_board()
    print w.gold_count