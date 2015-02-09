'''
Created on 2013-2-11

This file includes the Agent class, which is the 

computer that will find the best way to get the 

gold and then return to the start position.

@author: Hao Zou
'''
from world.wumpus_world import Wumpus_World
import knowledge_base


wumpus_world = Wumpus_World("wumpus_world.txt") 
    
class Agent:

    GOFORWARD = 1
    GRAB = 2
    SHOOT = 3
    RELEASE = 4
    GOBACK = 5
    END = 6 
    
    ISGOLD = 1
    ISSAFE = 2
    
    def __init__(self):
        self.kb = knowledge_base.KB()
        # the mark that the agent has got
        self.mark = 1000
        # the gold that the agent has got
        self.gold = 0
        # the position that the agent in now
        self.pos = wumpus_world.start
        # the position that the agent will go
        self.next_pos = wumpus_world.start
        # the number of arrow
        self.arrow = 1
        # used to save the positions that have been visited
        self.steps = [self.pos]
        # used to save the path the agent should go back to the start point
        self.back_path = []
        # used to save the position whose state has been deduced
        self.deduced_pos = []
    # go to next position based on the decision    
    def next_step (self):
        tmp = self.pos
        self.pos = self.next_pos
        self.mark -= 1
        # change the world and the board of the wumpus_world
        if wumpus_world.world.has_key(self.pos):
                wumpus_world.change_board(tmp,self.pos,wumpus_world.world[self.pos]+'A')
        else:
                wumpus_world.change_board(tmp,self.pos,'A')
        

    def shoot(self):
        self.arrow = 0
        self.mark -= 100
    # grab the gold and then change the real world and also the board shown to people
    def grab(self):
        self.gold += 1
        self.mark += 1000
        str = wumpus_world.world[self.pos]
        wumpus_world.world[self.pos] = str.replace('G', '')
        wumpus_world.change_board(None,self.pos,wumpus_world.world[self.pos]+'A')
    def release(self):
        self.gold -= 1
        self.mark -= 1000
    
    # reset the game
    def reset(self):
        self.__init__()
    
    # tell the KB some knowledge bases.
    def tell(self):
        sentence = ''

        # if the position has Stench, it means the neighbor of this position probably has Wumpus 
        if wumpus_world.world.has_key(self.pos) and wumpus_world.world[self.pos].find('S') >= 0 :
            print "found stench"
            sentence += "%s%d%d.\n" % ('S',self.pos[0],self.pos[1])
            sentence += "%s%d%d -> " % ('S',self.pos[0],self.pos[1])
            if self.pos[1]+1 < wumpus_world.column: 
                sentence += "%s%d%d | " % ('W',self.pos[0],self.pos[1]+1)
            if self.pos[0]+1 < wumpus_world.row:
                sentence += "%s%d%d | " % ('W',self.pos[0]+1,self.pos[1])
            if self.pos[1]-1 > 0:
                sentence += "%s%d%d | " % ('W',self.pos[0],self.pos[1]-1)
            if self.pos[0]-1 > 0:
                sentence += "%s%d%d | " % ('W',self.pos[0]-1,self.pos[1])
            sentence = sentence[0:-3] 
            sentence += ".\n"
        # if the position has no Stenches, it means the neighbor of this position has no Wumpus
        if (not wumpus_world.world.has_key(self.pos)) or wumpus_world.world[self.pos].find('S') < 0 :
            
            sentence += "%s%d%d.\n" % ('-S',self.pos[0],self.pos[1])
            sentence += "%s%d%d -> " % ('-S',self.pos[0],self.pos[1])
            sentence += "%s%d%d & " % ('-W',self.pos[0],self.pos[1])
            if self.pos[1]+1 < wumpus_world.column: 
                sentence += "%s%d%d & " % ('-W',self.pos[0],self.pos[1]+1)
            if self.pos[0]+1 < wumpus_world.row:
                sentence += "%s%d%d & " % ('-W',self.pos[0]+1,self.pos[1])
            if self.pos[1]-1 > 0:
                sentence += "%s%d%d & " % ('-W',self.pos[0],self.pos[1]-1)
            if self.pos[0]-1 > 0:
                sentence += "%s%d%d & " % ('-W',self.pos[0]-1,self.pos[1])
            sentence = sentence[0:-3]
            sentence += ".\n"
        # if the position has Breeze, it means the neighbor of this position probably has Pits    
        if wumpus_world.world.has_key(self.pos) and wumpus_world.world[self.pos].find('B') >= 0 :
            print "found breeze"
            sentence += "%s%d%d.\n" % ('B',self.pos[0],self.pos[1])
            sentence += "%s%d%d -> " % ('B',self.pos[0],self.pos[1])
            if self.pos[1]+1 < wumpus_world.column: 
                sentence += "%s%d%d | " % ('P',self.pos[0],self.pos[1]+1)
            if self.pos[0]+1 < wumpus_world.row:
                sentence += "%s%d%d | " % ('P',self.pos[0]+1,self.pos[1])
            if self.pos[1]-1 > 0:
                sentence += "%s%d%d | " % ('P',self.pos[0],self.pos[1]-1)
            if self.pos[0]-1 > 0:
                sentence += "%s%d%d | " % ('P',self.pos[0]-1,self.pos[1])
            sentence = sentence[0:-3]
            sentence += ".\n"
        # if the position has no Breeze, it means the neighbor of this position has Pits
        if (not wumpus_world.world.has_key(self.pos)) or wumpus_world.world[self.pos].find('B') < 0 :
            sentence += "%s%d%d.\n" % ('-B',self.pos[0],self.pos[1])
            sentence += "%s%d%d -> " % ('-B',self.pos[0],self.pos[1])
            sentence += "%s%d%d & " % ('-P',self.pos[0],self.pos[1])
            if self.pos[1]+1 < wumpus_world.column: 
                sentence += "%s%d%d & " % ('-P',self.pos[0],self.pos[1]+1)
            if self.pos[0]+1 < wumpus_world.row:
                sentence += "%s%d%d & " % ('-P',self.pos[0]+1,self.pos[1])
            if self.pos[1]-1 > 0:
                sentence += "%s%d%d & " % ('-P',self.pos[0],self.pos[1]-1)
            if self.pos[0]-1 > 0:
                sentence += "%s%d%d & " % ('-P',self.pos[0]-1,self.pos[1])
            sentence = sentence[0:-3]
            sentence += ".\n"
        # if the position has Gold, it means this position has gold
        if wumpus_world.world.has_key(self.pos) and wumpus_world.world[self.pos].find('G') >= 0:
            print "found gold"
            sentence += "%s%d%d.\n" % ('G',self.pos[0],self.pos[1])
        # tell the knowledge base that the agent has known so far
        self.kb.tell(sentence)
    # ask the KB whether the given position is safe now
    def ask(self,pos,flag):
        # 1 means the agent want to deduced the position
        if flag == 1:
            if self.kb.ask("%s%d%d.\n" % ('W',pos[0],pos[1])) == True:
                self.deduced_pos.append(pos)
                print "deduced wumpus at",pos
            if self.kb.ask("%s%d%d.\n" % ('P',pos[0],pos[1])) == True:
                self.deduced_pos.append(pos)
                print "deduced pit at",pos
        # 2 means the agent want to know whether the position has gold
        elif flag == 2:
            # if the position has gold, just return it has gold
            if self.kb.ask("%s%d%d.\n" % ('G',pos[0],pos[1])) == True:
                self.deduced_pos.append(pos)
                return self.ISGOLD
        # otherwise the agent want to know whether the next step is safe
        else:
            # if the position doesn't have Wumpus and Pits, it is safe, return safe
            if self.kb.ask("%s%d%d.\n" % ('-W',pos[0],pos[1])) == True and self.kb.ask("%s%d%d.\n" % ('-P',pos[0],pos[1])) == True:
                self.deduced_pos.append(pos)
                return self.ISSAFE
            # otherwise, it is not safe at this situation
            else:
                return 0
    # the most important function to decide the next movement of the agent
    def make_decision(self):

        # if the position has been told to the KB, we don't need to tell again
        # otherwise, we should tell the situation in the position to the KB
        if self.steps.count(self.pos) < 2:
            self.tell()
        
        # deduce the wumpus and pits
        for i in range(1,wumpus_world.row):
            for j in range(1,wumpus_world.column):
                pos = (i,j)
                if self.deduced_pos.count(pos) < 1:
                    self.ask(pos,1)
        # if the agent has got the gold, it should go back to the start point
        if self.gold > 0:
            if len(self.back_path) > 0:
                self.next_pos = self.back_path.pop()
                return self.GOBACK
            else:
                return self.END    
        # if the agent see the gold, it should grab it.
        # otherwise, it should ask the next movement
        if self.ask(self.pos,2) == self.ISGOLD:
            return self.GRAB
        
        # the position right to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos 
        if self.pos[0]+1 < wumpus_world.row: 
            self.next_pos = (self.pos[0]+1,self.pos[1])
            if self.steps[len(self.steps)-2] != self.next_pos and self.ask(self.next_pos,3) == self.ISSAFE:
                return self.GOFORWARD 
        # the position up to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos 
        if self.pos[1]+1 < wumpus_world.column:
            self.next_pos = (self.pos[0],self.pos[1]+1)
            if self.steps[len(self.steps)-2] != self.next_pos and self.ask(self.next_pos,3) == self.ISSAFE:
                return self.GOFORWARD
        # the position left to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos  
        if self.pos[0]-1 > 0: 
            self.next_pos = (self.pos[0]-1,self.pos[1])
            if self.steps[len(self.steps)-2] != self.next_pos and self.ask(self.next_pos,3) == self.ISSAFE:
                return self.GOFORWARD
        # the position down to the agent is not out of boundary and it is not the position it just came
        # from, and the position is safe, then this position should be the next_pos 
        if self.pos[1]-1 > 0:
            self.next_pos = (self.pos[0],self.pos[1]-1)
            if self.steps[len(self.steps)-2] != self.next_pos and self.ask(self.next_pos,3) == self.ISSAFE:
                return self.GOFORWARD
        
        # if all the above action is not qualified, then the agent should go back to the previous position 
        self.next_pos = self.steps[len(self.steps)-2]
        return self.GOBACK    
    # depend on the decision, choose the next action
    def action_process(self):
        
        # the next action based on the decision
        action = self.make_decision()
        
        
        if action == self.GRAB:
            print "grab the gold and go back to the start position"
            self.grab()
            for step in self.steps:
                if self.back_path.count(step) > 0:
                    while self.back_path.pop() == step:
                        pass
                else:
                    self.back_path.append(step)
            self.back_path.pop()
            #print self.back_path
        elif action == self.GOBACK or action == self.GOFORWARD:
            print "move",self.next_pos
            self.next_step()
            self.steps.append(self.pos)
        elif action == self.END:
            return self.done()
        
    # when the agent get out, the game is successful over
    def done(self):
        print "You Win"
        return 1        
        
if __name__ == '__main__':
    #test use
    agent = Agent()   
    agent.reset()
    agent.action_process()
