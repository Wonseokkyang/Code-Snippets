"""
#####################################################
##                  RL Maze Agent                  ##
#####################################################
#   
#   Name: Won Seok Yang
#   
##PRE:  'maze.txt' is a valid maze- 
#           every row has an equal number of elements
#           the maze has one or more solution
#
#   Agent will start the maze on (0,0)top left and try to reach
#   target at (numberOfRows-1, numberOfCols-1)bottom right
#
#   Green rectangle:    walls [reward = ?]
#   Yellow rectangle:    open space [reward = ?]
#   Blue  oval:          agent/explorer
#   Purple rectangle:    target/exit
#
#
#####################################################
##                  Resources                      ##
#####################################################
# Random mazes generated from:      https://www.dcode.fr/maze-generator
# Graphics method reference sheet:  https://mcsp.wartburg.edu/zelle/python/graphics/graphics.pdf
#                                   http://anh.cs.luc.edu/150s07/notes/graphics/graphics_py.htm
# Pandas documentation:             https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
######################################################
"""
from graphics import *
import pandas as pd
import numpy as np

#for demo only, continues from saved csv file
DEMO = True
CYCLE_FILE_NUM = 100
CSV_NAME = 'brain_saves/'+FILENAME+'_'+str(CYCLE_FILE_NUM)+'.csv'

SPEED = 0.2             #the speed at which the screen renders (refreshrate) in seconds
CYCLES = 101            #the number of times the agent will travel through the maze till completion

ALPHA = 0.5             #how heavily the learning algorithm gets changed toward a positive reward (learning rate)
GAMMA = 0.9             #the discount factor of future rewards (0 nearsighted vs 1 farsighted)
EPSILON = 0.9           #the weight of the algo's 'greediness', less greedy = explore, more greedy = exploit

#Reward values:
OUT_OF_FRAME = -100.0   #out of bounds penalty
WALL = -50.0            #hitting a wall penalty
MOVE = -0.5             #moving into a square penalty
TARGET = 100.0          #finding the end of the maze reward

FILENAME = 'maze5x5_1'
UNIT =  30  #unit size of squares in the graphical representation
class Maze:
    #Populate self with maze from FILENAME
    def __init__(self, mazeTextFile):
        self.mazeList=[]
        mazeText=open('maze/original/'+mazeTextFile+'.txt')
        for line in mazeText:
            rowList=[]
            for ch in line[:-1]:    #[:-1] all but the last char- new line 
                rowList.append(ch)
            self.mazeList.append(rowList)
        mazeText.close()

        #Cardinal directions:
        # 0 = UP,   1 = DOWN,   2 = LEFT,   3 = RIGHT
        self.actions = [0, 1, 2, 3] 
        self.numberOfCols = len(self.mazeList[0])
        self.numberOfRows = len(self.mazeList)
        print("Number of rows: %d \tNumber of cols: %d" % 
                    (self.numberOfRows, self.numberOfCols))

        #Graphics window init
        self.win = GraphWin("Maze Visual "+FILENAME, 
            width=UNIT*self.numberOfCols, 
            height=UNIT*self.numberOfRows)    #setup display window according to maze size

        #Agent oval objct init, starting position
        self.pos = (0, 0)   #always start at 0,0
        xpos, ypos = self.pos
        self.agent = Oval( Point(xpos*UNIT, ypos*UNIT), Point(xpos*UNIT+UNIT, ypos*UNIT+UNIT))
        self.agent.setFill("blue")

        #Maze target position
        self.tpos = (self.numberOfRows-1, self.numberOfCols-1)  #target pos always in the opposite corner
        print("Starting pos: %s \tTarget pos: %s\n" % (self.pos, self.tpos))
      
    """
    #FOR TESTING#
    #Print a text version of the maze- prints all elements in the array in maze format as well as the maze in the 2d array 
    def printText(self, arrayToPrint):
        s = [[str(e) for e in row] for row in arrayToPrint]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ''.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print('=========================')
        for row in arrayToPrint:
            print(row)
        print('=========================')
    """

    def resetAgent(self):  #resets agent to last known/valid x y position
        #Agent starting pos represented by pink circle- starts top left of graphical screen
        xpos, ypos = self.pos
        self.agent.undraw()
        self.agent = Oval( Point(xpos*UNIT, ypos*UNIT), Point(xpos*UNIT+UNIT, ypos*UNIT+UNIT))
        self.agent.setFill("blue")
        self.agent.draw(self.win)
        time.sleep(SPEED)
    
    #restarts the maze like it was initialized (resetting agent's tracked xpos, ypos)
    def restart(self):
        self.pos = (0,0)
        self.resetAgent()

    #Takes care of pixel positioning in function
    #returns: next state, reward for next state, done flag
    def moveAgent(self, direction_num):
        if direction_num == 0: dy, dx = 1, 0        #UP
        elif direction_num == 1: dy, dx = -1, 0     #DOWN
        elif direction_num == 2: dy, dx = 0, -1     #LEFT
        elif direction_num == 3: dy, dx = 0, 1      #RIGHT
        
        x,y = self.pos
        tx, ty = self.tpos
        # print("\nMoving agent at (%s,%s)" % self.pos)  #just to see
        # print("Moving agent to (%s,%s)" % (x+dx, y+dy))  #just to see

        #if the agent attempts to move off screen, remove agent from window before resetting
        #agent is out of bounds so give penalty
        if ((x+dx < 0) or (x+dx > self.numberOfRows-1)) or ((y+dy < 0) or (y+dy > self.numberOfRows-1)):
            print('Agent went out of bounds')
            self.agent.undraw()
            time.sleep(SPEED)
            self.resetAgent()
            reward = OUT_OF_FRAME
            done = False
        #agent hit a wall, blink agent on wall before resetting
        #wall hit so give penalty
        elif self.mazeList[x+dx][y+dy] == '#':
            print('Agent hit a wall')
            self.agent.move(dx*UNIT,dy*UNIT)
            time.sleep(SPEED)
            for i in range(2):  #blinking animation
                self.agent.undraw()
                time.sleep(SPEED/4)
                self.agent.draw(self.win)
                time.sleep(SPEED/4)
            self.resetAgent()
            reward = WALL
            done = False
        #agent found the target so reward and trigger done flag
        elif x+dx == tx and y+dy == ty:
            print('Agent found the target!')
            self.agent.move(dx*UNIT,dy*UNIT)
            self.pos = (x+dx, y+dy)
            time.sleep(SPEED)
            reward = TARGET
            done = True
        #agent landed on regular tile
        else:
            print('Agent moved')
            self.agent.move(dx*UNIT,dy*UNIT)
            self.pos = (x+dx, y+dy)
            time.sleep(SPEED)
            reward = MOVE
            done = False
        return self.pos, reward, done

    #Graphic visualization of maze
    def drawMaze(self):
        for x in range(self.numberOfRows):      #populating maze squares
            for y in range(self.numberOfCols):
                dSquare = Rectangle(Point(x*UNIT,y*UNIT), Point(x*UNIT+UNIT,y*UNIT+UNIT))
                if self.mazeList[x][y] =='#':   #walls
                    dSquare.setFill("green")
                    dSquare.draw(self.win)
                else:                           #empty squares
                    dSquare.setFill("yellow")
                    dSquare.draw(self.win)

        #Target square to reach represented by a green square- finishes bottom right of screen
        exitSquare = Rectangle(Point((self.numberOfRows-1)*UNIT, (self.numberOfCols-1)*UNIT), 
                        Point((self.numberOfRows-1)*UNIT+UNIT, (self.numberOfCols-1)*UNIT+UNIT))
        exitSquare.setFill("purple")
        exitSquare.draw(self.win)

        time.sleep(SPEED)
        self.resetAgent()

    #during this step the maze redraws the agent's location returns it's pos as a tuple of xpos, ypos
    def reset(self):
        self.agent.undraw()
        self.resetAgent()
        return self.pos


class Brain:
    #list of actions provided during first func call
    def __init__(self, actions, ALPHA, GAMMA, EPSILON):
        self.actions = actions
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    #given state, choose an action according to EPSILON/greediness
    #return: a number 0 to 3, a cardinal direction
    def choose_action(self, state):
        self.state_exist_check(state)   #append to q_table if it doesnt
        if np.random.uniform() < self.epsilon:  #greediness 'roll'- if less, then be greedy
            #choose greedy
            action_choices = self.q_table.loc[str(state), :]     #a list of directional values from 'state' ex: [0, 0, 0.5, 0]   left has highest value
            #from chooseable actions, pick out of the largest/max
            action = np.random.choice(action_choices[action_choices == np.max(action_choices)].index)
        else:   #otherwise, choose random
            action = np.random.choice(self.actions)
        return str(action)
    
    #updating q_table values
    def calculate(self, state, action, reward, new_state, target):
        # print('\n=$$ Inside calculate $$=')
        self.state_exist_check(new_state)   #append the new_state to q_table to add/manip calculations
        # print('q_table:')
        # print(self.q_table)

        q = self.q_table.loc[str(state), action]   #Q value

        # print('q = self.q_table.loc[str(state), action] = %s' % str(q))
        # time.sleep(1)
        # #I dont have to know if it's an exit because the maze function returns the flag to indicate an exit.
        # #I just have to update the q_table with every move because any move will give a new q_value unless the reward values are changed
        # print('Print the q_table row\'s action value I need')
        # print('action = %s' % action)
        # print('action value = %s' % self.q_table.loc[(str(state), action)])
        
        # #figure out what Q' is
        # print('Q\' is discount_factor * the max possible outcome of the future state, s\'')
        # print('reward = %s \t gamma or discount = %s \tmax of new_state = %s' % (str(reward), str(self.gamma), str(self.q_table.loc[str(new_state),:].max())))
        # q_ = reward+self.gamma*self.q_table.loc[str(new_state),:].max()

        # print('\nNow run the calculation of q_')
        # print(reward + self.gamma * self.q_table.loc[str(new_state),:].max())

        # print('Find self.alpha*(q_ - q) and update the right entry')
        # time.sleep(2)
        # exit()

        if new_state != target:   #agent didnt find exit
            q_ = reward + self.gamma * self.q_table.loc[str(new_state),:].max()    #max possible Q of new state
        else:   # agent found exit so there is no future state, just give reward
            q_ = reward
        self.q_table.loc[str(state),action] += self.alpha*(q_ - q) #update q_table with difference between estimate and actual * learning rate

    #check if state exists in q_table, if not append it
    def state_exist_check(self, state):
        if str(state) not in self.q_table.index:
            self.q_table = self.q_table.append(     #required to assign a copy of the append q_table to original to keep values for some reason
                pd.Series(      #make an entrie to the q_table according to this format for easy manipulation later
                    [0] * len(self.actions),
                    index = self.q_table.columns,   #columns of series entry according to dataframe(q_table) columns
                    name = str(state),   #the name(left most column for indexing)
                )
            )
            # print('%s WAS APPENDED' % str(state))   #for testing
       
#################
#   TESTING     #
#################
def testing():
    myMaze = Maze(FILENAME)
    myMaze.drawMaze()
    # myMaze.printText(myMaze.mazeList)  #print text version of maze
    # myMaze.printText(myMaze.valueTable)
    # print('\nnow to test moving agent off screen')

    print('testing maze.reset()')
    print(myMaze.reset())

    myMaze.moveAgent(5,5)
    print(myMaze.reset())
    myMaze.moveAgent(1,1)

    mLearning = Brain(list(range(4)), ALPHA, GAMMA, EPSILON)
    mLearning.test()


# maze_sol = [0,3,3,3,3,3,0,0,0,0,0,0,3,3,0,0,3,3,3,0] #testing for maze5x5_1.txt
#################
#   PROGRAM     #
#################
def RL_program():
    myMaze = Maze(FILENAME)     #init maze
    myMaze.drawMaze()
    myAgent = Brain(list(range(len(myMaze.actions))), ALPHA, GAMMA, EPSILON)    #init agent brain

    if DEMO == True:    #download the brain to myAgent
        myAgent.q_table = pd.read_csv(CSV_NAME, index_col=0)    #this required changing the return types of some of my function to get working

    cycle_numbers = []
    cycle_count = 0
    for iterations in range(CYCLES):
        steps_to_exit, reward_sum = 0
        myMaze.restart()    #reset the maze to starting values, but leaves myAgent's q_table for next cycle
        while True: #this loops until the maze sends the 'done' flag
            steps_to_exit += 1
            #to process, the agent needs it's relation in the maze, s = current agent state
            state = myMaze.pos

            #choose an action given agents current state
            action = myAgent.choose_action(state) 

            # #action is an int. need to pass that int to moveAgent to get s', reward and done flag
            new_state, reward, done = myMaze.moveAgent(int(action))
            reward_sum += reward
            #   IMPLEMENTING FORMULA    #
            #   Q[s, a] = Q[s, a] + lr * (reward + gamma * np.max(Q[s', :]) — Q[s, a])
            #       need: s = curr_state,   a = chosen action,  lr = ALPHA, gamma = discount factor,    s' = future state
            #function where the learning takes place- population of q_table
            myAgent.calculate(state, action, reward, new_state, myMaze.tpos)
                        
            if done == True:    #triggered by maze.moveAgent function
                if (DEMO == False and cycle_count % 10 == 0):   #if you're not running a demo, gather and save q_values for evaluation
                    csv_name = 'brain_saves/'+FILENAME+'_'+str(cycle_count)+'.csv'
                    myAgent.q_table.to_csv(csv_name, index=True, header=True)
                print('Cycle number: %s \tSteps taken: %s \tTotal reward: %s' % (cycle_count, steps_to_exit, reward_sum))
                cycle_count += 1
                cycle_numbers.append(steps_to_exit)
                break;      #break nesting while True loop
    return cycle_numbers
        
# print(RL_program())
RL_program()



