'''
Created on 2013-2-10

the program is based on python 2.6

it is to simulate the wumpus world game.

The world will be composed of squares 

with pits, gold, and a Wumpus. The

environment will be static. the agent is 

the computer which will find the best way

to get the gold and then return to the start

position.

@author: Hao Zou
'''
import sys
from world.wumpus_world import Wumpus_World
from KB.knowledge_base import KB
from agent.agent import Agent


   

# the run function, it is the main logic of this game,
# the agent is playing the game based on the action decision
def run():  
    if len(sys.argv) < 3:
        print "usage: %s <prover9 location> <the world filename> ...\n" % (sys.argv[0])
        quit()
    else:
        prover9_dir = sys.argv[1]
        world_filename =sys.argv[2]
    # the world
    wumpus_world = Wumpus_World(world_filename) 
    # the knowledge base
    kb = KB(prover9_dir)
    # the agent
    agent = Agent(wumpus_world,kb)
    
    # before the game we should reset the agent,kb and the wumpus world
    wumpus_world.reset()
    kb.reset(prover9_dir)
    agent.reset(wumpus_world,kb)
    
    # the agent won't stop until it finds the gold and return to the start position
    while 1:
        # show the current position of the agent 
        print "***********************************************************************"
        print "current position:", agent.pos
        print "arrow:",agent.arrow,"gold:", agent.gold,"mark:",agent.mark
        wumpus_world.draw_board()
        # if it returns 1, it means the agent has finished the task and we 
        # should exit the game successfully
        if agent.action_process() == 1:
            break
    print "all the steps are:", agent.steps

if __name__ == '__main__':
    run()