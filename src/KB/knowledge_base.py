'''
Created on 2013-2-12

This file includes the KB class, which is 

contain the knowledge base for the agent to

decide the next action. The knowledge base is

based on the prover9, which the directory is 

'E:/LADR1007B-win/bin/prover9'. If you want 

to use your own prover9, you should change the

directory to your own.

@author: Hao Zou
'''

import subprocess

# The knowledge base class, which uses the prover9 to
# decide whether an assumption is right based on the 
# knowledge that the KB has already known
class KB:
    
    # initialize the prover9 input file
    def __init__(self,process_name):
        # the prover9 process, you need to change the location for your prover9
        self.process_name = process_name
        # the input file for the prover9
        self.file_name = "wumpus_prop.txt"
        # the command line for the prover9
        self.command = self.process_name + ' -f ' + self.file_name
        file = open(self.file_name,'w')
        strs = ['assign(max_seconds, 1).\n',
                'formulas(sos).\n',
                'all X1 all Y1 all X2 all Y2 (neighbor(X1,Y1,X2,Y2)'+
                ' <-> (((X1=X2) & closey(Y1,Y2)) | (closex(X1,X2) & (Y1=Y2)))).\n',
                'all X1 all Y1 all X2 all Y2 '+
                '((-stench(X1,Y1) & neighbor(X1, Y1, X2, Y2))-> -wumpus(X2, Y2)).\n',
                'all X1 all Y1 all X2 all Y2 '+
                '((-breeze(X1,Y1) & neighbor(X1, Y1, X2, Y2))-> -pit(X2, Y2)).\n',
                'all X1 all Y1 (breeze(X1,Y1) -> '+
                '(exists X2 exists Y2 (pit(X2,Y2) & neighbor(X1, Y1, X2, Y2)))).\n',
                'all X1 all Y1 (stench(X1,Y1) -> '+
                '(exists X2 exists Y2 (wumpus(X2,Y2) & neighbor(X1, Y1, X2, Y2)))).\n',
                '%all X all Y (boundary(X,Y)-> -wumpus(X,Y) & -pit(X,Y)).\n',
                '%all X1 all Y1 ((-stench(X1,Y1))-> -wumpus(X1,Y1)).\n',
                '%all X1 all Y1 ((-breeze(X1,Y1))-> -pit(X1,Y1)).\n',
                'all X1 all Y1 ((glitter(X1,Y1))-> gold(X1,Y1)).\n',
                'end_of_list.\n','formulas(goals).\n\n','end_of_list.']
        file.writelines(strs)
        file.close()
    def reset(self,process_name):
        self.__init__(process_name)
    # tell the prover9 the assumption
    def tell(self,sentence):
        file = open(self.file_name,'r+')
        lines = file.readlines()

        lines.insert(len(lines)-4,sentence)
        file.seek(0,0)
        file.writelines(lines)
        file.close()
    # ask the prover9 what's your goal
    def ask(self,sentence):
        file = open(self.file_name,'r')
        lines = file.readlines()
        
        #print lines
        lines[len(lines)-2] = sentence
        lines[len(lines)-1] = "end_of_list."
        #print lines[len(lines)-1]
        file.close()
        file = open(self.file_name,'w')
        file.writelines(lines)
        
        #quit()
        file.close()
        prc = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # if the prover9 return the 'Exiting with 1 proof.' that means the goal has been reached
        if prc.stdout.read().find('THEOREM PROVED') > 0:
            #print "PROVED", sentence,
            return True
        # otherwise, the goal is failed
        else:
            #print "failed", sentence, 
            return False
    def change(self,pos):
        file = open(self.file_name,'r+')
        lines = file.readlines()
        newlines= []
        for line in lines:
            if line == ('stench(%d,%d).\n' % (pos[0],pos[1])):
                line = ('-stench(%d,%d).\n' % (pos[0],pos[1]))
            newlines.append(line)
        file.close()
        file = open(self.file_name,'w')
        file.writelines(newlines)
 
if __name__ == '__main__': 
    # just for the test use  
    kb = KB('E:/LADR1007B-win/bin/prover9')
    #kb.tell("P33.\n")
    kb.ask('-wumpus((2,1)).\n')
    kb.change((3,6))        