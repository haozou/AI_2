'''
Created on 2013-2-11

This file includes the Agent class, which is the 

computer that will find the best way to get the 

gold and then return to the start position.

@author: Hao Zou
'''
import Queue

class Agent:

    GOFORWARD = 1
    GRAB = 2
    SHOOT = 3
    END = 4 
    
    ISGOLD = 1
    ISSAFE = 2
    
    def __init__(self,wumpus_world,kb):
        self.kb = kb
        self.wumpus_world = wumpus_world
        # the mark that the agent has got
        self.mark = 1000
        # the gold that the agent has got
        self.gold = 0
        self.gold_count = wumpus_world.gold_count
        # the position that the agent in now
        self.pos = wumpus_world.start
        # the exit position
        self.exit = wumpus_world.end
        # the position that the agent will go
        self.next_pos = wumpus_world.start
        # the number of arrow
        self.arrow = 1
        # used to save the positions that have been visited
        self.steps = [self.pos]
        # used to save the position whose state has been deduced
        self.deduced_pos = [self.pos]
        # the position of wumpus has deduced
        self.wumpus_pos = {}
        # the position of gold has deduced
        self.gold_pos = {}
        # the possible position that has wumpus and pit
        self.possible_wp = []
        # every position has several possible next position which is store in this dictionary
        # the position is the key, and the value is a queue that store the several possible 
        # next positions
        self.situation = {}
        # initial the knowledge base tell it the neighbor of each position 
        self.initial_kb()
    # initial the knowledge base, tell the knowledge base the size of the world
    # help the KB decide which two positions are counted as neighbor
    def initial_kb(self):
        sentence = ""
        row = self.wumpus_world.row
        # the close for row
        sentence += "all X (closex(1,X) <-> X=2).\n"
        for i in range(2,row):
            sentence += "all X (closex(%d,X) <-> X=%d | X=%d).\n" % (i,i-1,i+1)
        sentence += "all X (closex(%d,X) <-> X=%d).\n" % (row,row-1)
        # the close for column
        sentence += "all Y (closey(1,Y) <-> Y=2).\n"
        column = self.wumpus_world.column
        for i in range(2,column):
            sentence += "all Y (closey(%d,Y) <-> Y=%d | Y=%d).\n" % (i,i-1,i+1)
        sentence += "all Y (closey(%d,Y) <-> Y=%d).\n" % (column,column-1)
                    
#        sentence += "all X all Y (X=0 | Y=0 | X=%d | Y=%d <-> boundary(X,Y)).\n" \
#        % (self.wumpus_world.row+1,self.wumpus_world.column+1)
        
        
        self.kb.tell(sentence)
    # go to next position based on the decision    
    def next_step (self):
        tmp = self.pos
        self.pos = self.next_pos
        self.mark -= 1
        # change the world and the board of the wumpus_world
        if self.wumpus_world.world.has_key(self.pos):
                self.wumpus_world.change_board(tmp,self.pos,self.wumpus_world.world[self.pos]+'A')
        else:
                self.wumpus_world.change_board(tmp,self.pos,'A')
    # after shoot the wumpus, we need to modify the world. All the neighbors should no longer 
    # have stench if there are no other wumpus near the position. And also, we need to tell
    # the KB which position no longer has stench now  
    def shoot(self):
        self.arrow = 0
        self.mark -= 100
        str = self.wumpus_world.world[self.next_pos]
        self.wumpus_world.world[self.next_pos] = str.replace('W', '')
        self.wumpus_world.change_board(None,self.next_pos,self.wumpus_world.world[self.next_pos])
        tmp1 = []
        tmp1.append((self.next_pos[0]+1,self.next_pos[1]))
        tmp1.append((self.next_pos[0]-1,self.next_pos[1]))
        tmp1.append((self.next_pos[0],self.next_pos[1]+1))
        tmp1.append((self.next_pos[0],self.next_pos[1]-1))
        for pos in tmp1:
            if self.wumpus_world.world.has_key(pos):
                tmp2 = []
                tmp2.append((pos[0]+1,pos[1]))
                tmp2.append((pos[0]-1,pos[1]))
                tmp2.append((pos[0],pos[1]+1))
                tmp2.append((pos[0],pos[1]-1))
                for p in tmp2:
                    if self.wumpus_world.world.has_key(p) and self.wumpus_world.world[p].find('W') < 0:
                        str = self.wumpus_world.world[pos]
                        self.wumpus_world.world[pos] = str.replace('S', '')
                        if self.steps.count(pos) > 0:
                            self.wumpus_world.change_board(None,pos,self.wumpus_world.world[pos])
                        self.kb.change(pos)
        self.wumpus_pos[self.next_pos] = 0
    # grab the gold and then change the real world and also the board shown to people
    def grab(self):
        self.gold += 1
        self.mark += 1000
        str = self.wumpus_world.world[self.pos]
        self.wumpus_world.world[self.pos] = str.replace('G', '')
        self.wumpus_world.change_board(None,self.pos,self.wumpus_world.world[self.pos]+'A')

    # reset the game
    def reset(self,wumpus_world,kb):
        self.__init__(wumpus_world,kb)
        
    # tell the KB some knowledge bases.
    def tell(self):
        sentence = ''
            
        # if the position has Stench, it means the neighbor of this position probably has Wumpus 
        if self.wumpus_world.world.has_key(self.pos) and self.wumpus_world.world[self.pos].find('S') >= 0 :
            print "found stench"
            sentence += "%s(%d,%d).\n" % ('stench',self.pos[0],self.pos[1])
#            sentence += "stench(%d,%d) -> wumpus(%d,%d) | wumpus(%d,%d) | wumpus(%d,%d) | wumpus(%d,%d).\n" \
#                 % (self.pos[0],self.pos[1],self.pos[0]+1,self.pos[1],self.pos[0],self.pos[1]+1,\
#                    self.pos[0]-1,self.pos[1],self.pos[0],self.pos[1]-1)
            
        # if the position has no Stenches, it means the neighbor of this position has no Wumpus
        if ((not self.wumpus_world.world.has_key(self.pos)) or self.wumpus_world.world[self.pos].find('S') < 0):
            
            sentence += "%s(%d,%d).\n" % ('-stench',self.pos[0],self.pos[1])

        # if the position has Breeze, it means the neighbor of this position probably has Pits    
        if self.wumpus_world.world.has_key(self.pos) and self.wumpus_world.world[self.pos].find('B') >= 0 :
            print "found breeze"
            sentence += "%s(%d,%d).\n" % ('breeze',self.pos[0],self.pos[1])
#            sentence += "breeze(%d,%d) -> pit(%d,%d) | pit(%d,%d) | pit(%d,%d) | pit(%d,%d).\n" \
#                 % (self.pos[0],self.pos[1],self.pos[0]+1,self.pos[1],self.pos[0],self.pos[1]+1,\
#                    self.pos[0]-1,self.pos[1],self.pos[0],self.pos[1]-1)
        # if the position has no Breeze, it means the neighbor of this position has Pits
        if (not self.wumpus_world.world.has_key(self.pos)) or self.wumpus_world.world[self.pos].find('B') < 0 :
            sentence += "%s(%d,%d).\n" % ('-breeze',self.pos[0],self.pos[1])

        # if the position has Gold, it means this position has gold
        if self.wumpus_world.world.has_key(self.pos) and self.wumpus_world.world[self.pos].find('G') >= 0:
            print "found gold"
            self.gold_pos[self.pos] = 1
            sentence += "%s(%d,%d).\n" % ('glitter',self.pos[0],self.pos[1])

        # tell the knowledge base that the agent has known so far
        self.kb.tell(sentence)
    # ask the KB whether the given position is safe now
    def ask(self,pos,flag):
        # 1 means the agent want to deduced the position
        if flag == 1:
            if self.kb.ask("%s(%d,%d).\n" % ('wumpus',pos[0],pos[1])) == True:
                self.wumpus_pos[pos] = 1
                self.deduced_pos.append(pos)
                print "deduced wumpus at",pos
            if self.kb.ask("%s(%d,%d).\n" % ('pit',pos[0],pos[1])) == True:
                self.deduced_pos.append(pos)
                print "deduced pit at",pos
        # 2 means the agent want to know whether the position has gold
        elif flag == 2:
            # if the position has gold, just return it has gold
            if self.kb.ask("%s(%d,%d).\n" % ('gold',pos[0],pos[1])) == True:
                self.deduced_pos.append(pos)
                return self.ISGOLD
        # otherwise the agent want to know whether the next step is safe
        else:
            # if the position doesn't have Wumpus and Pits, it is safe, return safe
            if self.kb.ask("%s(%d,%d).\n" % ('-wumpus',pos[0],pos[1])) == True and self.kb.ask("%s(%d,%d).\n" % ('-pit',pos[0],pos[1])) == True:
                self.deduced_pos.append(pos)
                return self.ISSAFE
            # otherwise, it is not safe at this situation
            else:
                return 0
    def get_next_pos(self):
        next = []
        # the position right to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos 
        self.next_pos = (self.pos[0]+1,self.pos[1])
        if self.next_pos[0] <= self.wumpus_world.row and self.steps[len(self.steps)-2] != self.next_pos:
            next.append(self.next_pos)  
            if self.possible_wp.count(self.next_pos) < 1:
                self.possible_wp.append(self.next_pos)
        # the position up to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos 
        self.next_pos = (self.pos[0],self.pos[1]+1)
        if self.next_pos[1] <= self.wumpus_world.column and self.steps[len(self.steps)-2] != self.next_pos:
            next.append(self.next_pos)
            if self.possible_wp.count(self.next_pos) < 1:
                self.possible_wp.append(self.next_pos)
        # the position left to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos  
        self.next_pos = (self.pos[0]-1,self.pos[1])
        if self.next_pos[0] > 0 and self.steps[len(self.steps)-2] != self.next_pos:
            next.append(self.next_pos)
            if self.possible_wp.count(self.next_pos) < 1:
                self.possible_wp.append(self.next_pos)
        # the position down to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos 
        self.next_pos = (self.pos[0],self.pos[1]-1)
        if self.next_pos[1] > 0 and self.steps[len(self.steps)-2] != self.next_pos:
            next.append(self.next_pos)
            if self.possible_wp.count(self.next_pos) < 1:
                self.possible_wp.append(self.next_pos)
    
        # if all the above action is not qualified, then the agent should go back to the previous position 
        if len(self.steps) > 1:
            self.next_pos = self.steps[len(self.steps)-2]
            next.append(self.next_pos)
        return next
    # when the agent has got all the gold, it will go to the goal, this 
    # function is used to compute the best step to the goal
    def get_best_back_pos(self,nexts):
        min = 1000
        best_pos2 = (min,min)
        for pos in nexts:
            tmp = abs(pos[0] - self.exit[0])
            if tmp < min and (self.steps.count(pos) > 0 or self.ask(pos, 3) == self.ISSAFE):
                min = tmp
                best_pos1 = pos
            elif tmp == 0:
                best_pos2 = pos
                
        if abs(best_pos1[1] - self.exit[1]) > abs(best_pos2[1] - self.exit[1]):
            return best_pos2
        else:
            return best_pos1
                
    # the most important function to decide the next movement of the agent
    def make_decision(self):

# 1st step--------------------------------------------------------------------------
        # get all the possible next positions
        nexts = self.get_next_pos()
# 2nd step--------------------------------------------------------------------------                 
        # if the position has been told to the KB, we don't need to tell again
        # otherwise, we should tell the situation in the position to the KB
        if self.steps.count(self.pos) < 2:
            self.tell()
            # deduce the wumpus and pits
            for pos in self.possible_wp:    
                if self.deduced_pos.count(pos) < 1:
                    self.ask(pos, 1)
                
        # if the agent has got the gold, it should choose the go to the goal
        if self.gold == self.gold_count:
            if self.pos != self.exit:
                self.next_pos = self.get_best_back_pos(nexts)
                return self.GOFORWARD
            else:
                return self.END
           
# 3rd step--------------------------------------------------------------------------
        # if the agent see the gold, it should grab it.
        # otherwise, it should ask the next movement
        if self.gold_pos.has_key(self.pos) and self.gold_pos[self.pos] == 1:
            self.gold_pos[self.pos] = 0
            return self.GRAB
# 4th step--------------------------------------------------------------------------       
        # if the agent has deduced the 60% of the world, then the agent will choose the position
        # that it has never deduced and safe to go, or shoot the wumpus if it is around it
        if float(len(set(self.deduced_pos))) \
            /float(self.wumpus_world.row * self.wumpus_world.column) > 0.6\
                and self.gold < self.gold_count:
            for pos in nexts:
                if self.deduced_pos.count(pos) < 1 and self.ask(pos, 3) == self.ISSAFE:
                    self.next_pos = pos
                    return self.GOFORWARD
            for pos in nexts:
                if self.arrow > 0 and self.wumpus_pos.has_key(pos) and self.wumpus_pos[pos] == 1:
                    self.next_pos = pos
                    return self.SHOOT
# 5th step----------------------------------------------------------------------------
        # add the possible next pos into the queue        
        for pos in nexts:
            if self.situation.has_key(self.pos):
                self.situation[self.pos].put(pos)
            else:
                self.situation[self.pos] = Queue.Queue(0)
                self.situation[self.pos].put(pos)
        for pos in nexts:
            if self.deduced_pos.count(pos) < 1 and self.ask(pos, 3) == self.ISSAFE:
                self.next_pos = pos
                return self.GOFORWARD        
        # while the next pos queue is not empty
        while not self.situation[self.pos].empty():
            self.next_pos = self.situation[self.pos].get()
#            print self.next_pos
            if self.steps.count(self.next_pos) > 0 \
            or self.ask(self.next_pos,3) == self.ISSAFE:
                return self.GOFORWARD
                
    # depend on the decision, choose the next action
    def action_process(self):
        
        # the next action based on the decision
        action = self.make_decision()
               
        if action == self.GRAB:
            print "grab the gold"
            self.grab()
        elif action == self.SHOOT:
            print "shoot the wumpus at ",self.next_pos
            self.shoot()
            print "move",self.next_pos
            self.next_step()
            self.steps.append(self.pos)
            #print self.back_path
        elif action == self.GOFORWARD:
            print "move",self.next_pos
            self.next_step()
            self.steps.append(self.pos)
        elif action == self.END:
            print "arrive the exit"
            return self.done()
        
    # when the agent get out, the game is successful over
    def done(self):
        print "You Win"
        return 1
        
if __name__ == '__main__':
    #test use

    pass