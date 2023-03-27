from copy import deepcopy
import time
import heapq
import random

class Board: # define 2d list for board
    def __init__(self, cars=[], xcar=[]):
        self.board = [['.' for x in range(6)] for y in range(6)]
        self.sup_sol = str() 
        self.cars = cars
        self.xcar = xcar
        self.comp_sol = []

    def __eq__(self, other):
        return self.cars == other.cars

    def __str__(self):
        return str(self.__dict__)

    def __hash__(self):
        return hash(self.__repr__())


    def check_sol(self): # Check if the way towards the goal is clear for the red car 
        red_car = [car for car in self.cars if car.name == 'X'][0]
        row, column = red_car.coord[1][0], red_car.coord[1][1]
        lst = [row,column + 1]
        distance = 5 - red_car.coord[1][1] # Subtract the cars position from the size of the board

        for i in range(1,distance + 1):  # Check all positions to the right of the red car to see if they're clear
            lst = [row,column + i]
            if self.check_collision(lst):
                return False
        return True

    def dspy(b, i): # display board to console
        print("Game:", i, "\n")
        print('+'.rjust(5), end = '')
        for k in range (0, 57):
            print('-', end = '')
        print('+')
        for j in range(0,6):
            print("|".rjust(5), end = '')
            for k in range(0,6):
                    print("".ljust(6), end = '')
                    print(b.board[j][k], " ", end = '')
            if j == 2: 
                print("".ljust(2), "==> \n")
            else:
                print("| \n".rjust(6))
        print('+'.rjust(5), end = '')
        for k in range (0, 57):
            print('-', end = '')
        print('+')
    
    @staticmethod
    def check_range(i):
        return i <= 5 and i >= 0

    def check_collision(self,tile): #check if any objects are on the destination to determine if there is a collision moving to destination.
            for car in self.cars:
            
                if(car.length == 2):
                    for i in range(0,2):
                        if(car.coord[i][0] == tile[0] and car.coord[i][1] == tile[1]):
                            return True
                else:
                    for i in range(0,3):
                        if(car.coord[i][0] == tile[0] and car.coord[i][1] == tile[1]):
                             return True
            return False
                

    def calculate_cars(board): # Create car objects within the selected board
        cars = []
        x_car = False
        for i in range(0,6):
            for j in range(0,6):
                if(board.board[i][j].isalpha()): # Check if board position contains a car object
                    check = False
                    for k in cars: # Check if this car object already exists
                        if(k.name == board.board[i][j]): 
                            check = True
                            break
                    if(check == False): # Find car variables and add new car object to car list
                        name = board.board[i][j]
                        coord = []
                        temp = [i,j]
                        coord.append(temp)
                        if(board.board[i][j] <= 'K' or  board.board[i][j] == 'X' ): # Check if car or truck
                            length = 2
                        else:
                            length = 3
                        if not(board.check_range(j + 1)): # Check if horizontal or vertical
                           plane = 'VERTICAL'
                        else:
                            if(board.board[i][j] == board.board[i][j + 1]):
                                plane = 'HORIZONTAL'
                            else:
                                plane = 'VERTICAL'
                        if(plane == 'HORIZONTAL'): # Insert all coordinates for the vehicle object
                            for n in range (1, length):
                                lst = [i,j+n]
                                coord.append(lst)
                        else:
                            for n in range (1, length):
                                lst = [i+n,j]
                                coord.append(lst)
                        car = board.Car(coord,plane,length,name)
                        #board.cars.append(car)
                        cars.append(car)
        return cars

    class Car: # Define car object
        def __init__(self,coord,plane,length,name):
            self.coord = coord
            self.plane = plane
            self.length = length
            self.name = name
            
        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __str__(self):
            return str(self.__dict__)


        def __hash__(self):
             return hash(self.__repr__())

        def __repr__(self):
            if self.length == 3:
                return "{} {} [{},{},{}]".format(self.name, self.plane, self.coord[0], self.coord[1], self.coord[2])
            else:
                return "{} {} [{},{}]".format(self.name, self.plane, self.coord[0], self.coord[1])
    
    def calculate_moves(self): # Explores a given state
        for car in self.cars:
            if car.plane == 'HORIZONTAL': # Check car objects plane of movement
                length = car.length -1
                row, column = car.coord[0][0], car.coord[0][1]
                lst = [row,column - 1]
                # Left
                if(self.check_range(column - 1) and not self.check_collision(lst)): #Check if movement is in range and doesn't collide with other objects
                    new_state = deepcopy(self.cars)
                    new_car = [x for x in new_state if x.name == car.name][0]
                    #new_car.move_left(self)
                    for i in range(0,new_car.length):
                        new_car.coord[i][1] -= 1
                    yield[[[car.name, 'L', 1]], Board(new_state,self.xcar)]
                # Right
                row, column = car.coord[length][0], car.coord[length][1]
                lst = [row,column + 1]
                if(self.check_range(column + 1) and not self.check_collision(lst)):
                    new_state = deepcopy(self.cars)
                    new_car = [x for x in new_state if x.name == car.name][0]
                    for i in range(0,new_car.length):
                        new_car.coord[i][1] += 1
                    #new_car.move_right(self)
                    yield[[[car.name, 'R', 1]], Board(new_state, self.xcar)]
            else:
                # Up
                length = car.length -1
                row, column = car.coord[0][0], car.coord[0][1]
                lst = [row - 1,column]    
                if(self.check_range(row - 1) and not self.check_collision(lst)):
                    new_state = deepcopy(self.cars)
                    new_car = [x for x in new_state if x.name == car.name][0]
                    for i in range(0,new_car.length):
                        new_car.coord[i][0] -= 1
                    #new_car.move_up(self)
                    yield[[[car.name, 'U', 1]], Board(new_state,self.xcar)]
                # Down
                row, column = car.coord[length][0], car.coord[length][1]
                lst = [row + 1,column]    
                if(self.check_range(row + 1) and not self.check_collision(lst)):
                    new_state = deepcopy(self.cars)
                    new_car = [x for x in new_state if x.name == car.name][0]
                    for i in range(0,new_car.length):
                        new_car.coord[i][0] += 1
                    #new_car.move_down(self)
                    yield[[[car.name, 'D', 1]], Board(new_state,self.xcar)]
    


    def format_sol(self): # Format the solution for easy manipulation and readability
        i = 0
        j  = len(self.comp_sol)
        while i < j:
             if(i < len(self.comp_sol)-1):
                if self.comp_sol[i][0] == self.comp_sol[i + 1][0]:
                   self.comp_sol[i][2] += 1
                   self.comp_sol.pop(i + 1)
                   i -= 1
             i += 1
        red_car = [car for car in self.cars if car.name == 'X'][0]
        distance = 6 -  red_car.coord[0][1]
        temp = ['X','R',distance]
        self.comp_sol.append(temp)
        return self.comp_sol

class Adv_Blocking_Heuristic: # Heuristic to determine number of cars blocking x and cars blocking those cars  etc...
     def compute_x(self, board):
        x_car = [car for car in board.cars if car.name == 'X'][0]
        blocking_cars = 0
        row, column = x_car.coord[1][0], x_car.coord[1][1]
        distance = 5 - x_car.coord[1][1] # Subtract the cars position from the size of the board
        car_list = []

        for i in range(1,distance + 1):  # Check all positions to the right of the red car to see if they're clear
            lst = [row,column + i]
            if board.check_collision(lst):
                blocking_car = [car for car in board.cars 
                                if car.coord[0] == lst or car.coord[1] == lst or car.length == 3 and car.coord[2] == lst][0]
                if blocking_car not in car_list:
                    car_list.append(blocking_car)
                    if(blocking_car.plane == 'VERTICAL'):
                        blocking_cars += self.compute_down(board, blocking_car, x_car)
                        blocking_cars += self.compute_up(board, blocking_car, x_car)
                    blocking_cars += 1

        return blocking_cars

     def compute_up(self, board, blocking_car, x_car):
        count = 0
        other_blocking_car = None
        if blocking_car.length  == 3:
            distance = blocking_car.coord[0][0]
            row, column =  blocking_car.coord[0][0],  blocking_car.coord[0][1]
        else:
            distance = blocking_car.coord[0][0]
            row, column =  blocking_car.coord[0][0],  blocking_car.coord[0][1]
        for i in range(1,distance + 1):
            lst = [row - i,column]
            if board.check_collision(lst):
                other_blocking_car = [car for car in board.cars 
                                if car.coord[0] == lst or car.coord[1] == lst or car.length == 3 and car.coord[2] == lst][0]
                count += 1
        return count

     def compute_down(self, board, blocking_car, x_car):
        count = 0
        other_blocking_car = None
        if blocking_car.length  == 3:
            distance = 5 - blocking_car.coord[2][0]
            row, column =  blocking_car.coord[2][0],  blocking_car.coord[2][1]
        else:
            distance = 5 - blocking_car.coord[1][0]
            row, column =  blocking_car.coord[1][0],  blocking_car.coord[1][1]
        for i in range(1,distance + 1):
            lst = [row + i,column]
            if board.check_collision(lst):
                other_blocking_car = [car for car in board.cars 
                                if car.coord[0] == lst or car.coord[1] == lst or car.length == 3 and car.coord[2] == lst][0]
                count += 1
        return count

    # def compute_left(self, board, blocking_cars):

    # def compute_right(self, board, blocking_cars):

def read(list): # read in problems from txt
     with open('rhs.txt', 'r') as f:
         
        index  = 0  
        
        for line in f:
            if 'RH-input' in line: 
                    if 'end RH-input' in line:
                        break
                    for i in range(0,40): 
                        index = 0
                        line =  next(f)
                        for j in range(0, 6):
                            for k in range(0, 6):
                                list[i].board[j][k] = line[index]
                                index = index + 1
        index  = 0  
        for ln in f:
           if 'Sol:'in ln:
               if '.' not in ln:
                   while '.' not in ln:
                       list[index].sup_sol += ln
                       #list[index].sup_sol  = list[index].sup_sol[7:]
                       list[index].sup_sol  = list[index].sup_sol[:-1]
                       check = True
                       ln  = next(f)
               list[index].sup_sol += ln
               list[index].sup_sol  = list[index].sup_sol[7:]
               list[index].sup_sol  = list[index].sup_sol[:-2]  
               list[index].sup_sol =  list[index].sup_sol.split()
               list[index].sup_sol =  ' '.join(list[index].sup_sol)
               index = index + 1

class Solver: # Define solver object
        def __init__(self,supp_moves, supp_sol, average, heu = None):
            self.comp_moves = 0
            self.supp_moves = supp_moves
            self.supp_sol = supp_sol
            self.depth = 0
            self.searched = 0
            self.heu = heu
            self.solved = True
            self.average = average
            self.time = 0
            self.comp_sol = None
                
        def dspy_values(self,board): # Display values from solver object in a readable manner
            if self.solved == False: print('Failed.\n')
            else:
                self.comp_sol = board.format_sol()
                print('Supplied Solution:', self.supp_sol)
                print("Computed Solution: ", end = "")
                for j in  board.comp_sol:
                    self.comp_moves += j[2]
                    for k in j:
                        print(k, end = "")
                    print(" ", end = "")
                self.comp_sol = board.comp_sol
                print("\nDiffernce: ", self.comp_moves - self.supp_moves)
                print("Depth:", self.depth)
                print("Searched:", self.searched)
                print("\n")
        
        def bfs_search(self,board): # Breadth-First-Search
            start = time.time()
            print("BFS:")
            frontier = [[board]]
            children = 0
            seen_states = set()
            seen_states.add(hash(str(board)))
            while frontier:
                current_state = frontier.pop(0) # Pop neighbour before popping child

                if self.average != None:
                    current_time = time.time()
                    elapsed_time = current_time - start
                    if elapsed_time > self.average:
                        self.solved = False
                        self.dspy_values(board)
                        return

                for b, next_state in current_state[-1].calculate_moves():
                    children += 1
                    if hash(str(next_state)) not in seen_states:
                        
                        if current_state[-1].check_sol():
                            end = time.time()
                            self.time = end-start
                            print("CPU Time:", self.time)
                            solution = []
                            check = False
                            for path in current_state:
                                if check == True:
                                    solution += path.comp_sol
                                    self.depth += 1
                                check = True
                            board = current_state[-1]
                            board.comp_sol = solution
                            self.searched = children
                            self.dspy_values(board)
                            return 
                            
                        seen_states.add(hash(str(next_state)))
                        next_state.comp_sol += b
                        frontier.append(current_state + [next_state])
            
            self.solved = False

        def dls(self,max_depth, board, start): # Depth-Limited-Search
            frontier = [[board]]
            cur_depth = 0
            children = 0
            seen_states = {}
            while frontier:
                current_state = frontier.pop() # Pop most recent child or neithbour if at max depth

                if self.average != None:
                    current_time = time.time()
                    elapsed_time = current_time - start
                    if elapsed_time > self.average:
                        self.solved = False
                        self.dspy_values(board)
                        return True

                if current_state[-1].check_sol():
                    end = time.time()
                    self.time = end-start
                    print("CPU Time:", self.time)
                    solution = []
                    check = False
                    for path in current_state:
                        if check == True:
                          solution += path.comp_sol
                          self.depth += 1
                        check = True
                    board = current_state[-1]
                    board.comp_sol = solution
                    self.depth = len(current_state)
                    self.searched = children
                    self.dspy_values(board)
                    return True
                
                cur_depth = len(current_state) - 1
                if(cur_depth < max_depth):
                    for moves, next_state in current_state[-1].calculate_moves():
                            children += 1
                            if hash(str(next_state)) not in seen_states:
                                seen_states[hash(str(next_state))] = cur_depth
                                next_state.comp_sol += moves
                                frontier.append(current_state + [next_state])
                            else:
                                if (seen_states.get(hash(str(next_state))) > cur_depth):  
                                    seen_states.update({hash(str(next_state)): cur_depth})
                                    next_state.comp_sol += moves
                                    frontier.append(current_state + [next_state])
            return False
        
        def ids_search(self,board): #iteritive deepening search
            start = time.time()
            print("IDS:")
            max_depth = 0
            while True:
                if not self.dls(max_depth,board,start):
                    max_depth +=1
                else: return 

        def a_star(self,board): # A*
            start = time.time()
            children = 0
            print("A*:")
            frontier = Priority_Queue()
            seen_states = set()
            frontier.push([[], board], 0)
            cost = {}
            cost[hash(str(board))] = 0
            while not frontier.empty():
                moves, current_state = frontier.pop()

                if self.average != None:
                    current_time = time.time()
                    elapsed_time = current_time - start
                    if elapsed_time > self.average:
                        self.solved = False
                        self.dspy_values(board)
                        return

                if current_state.check_sol():
                            end = time.time()
                            self.time = end-start
                            print("CPU Time:", self.time)
                            solution = []
                            board = current_state
                            board.comp_sol = moves
                            self.searched = children
                            self.depth = len(board.comp_sol)
                            self.dspy_values(board)
                            return 

                for new_moves, next_state in current_state.calculate_moves():
                    children += 1
                    new_cost = len(moves) + 1 # Ensure that neigbours are popped before children to find optimal solution
                    priority = new_cost + self.heu.compute_x(next_state)
                    
                    if hash(str(next_state)) not in seen_states:
                        frontier.push([moves + new_moves, next_state], priority)
                        seen_states.add(hash(str(next_state)))
                    
                    else:
                        if new_cost < cost[hash(str(next_state))]:
                            a = cost[hash(str(next_state))]
                            frontier.push( [moves + new_moves, next_state], priority)
                        else:
                            continue
                    cost[hash(str(next_state))] = new_cost
                    self.searched +=1
           
            self.solved = False
        
        def steep_asc(self, board): # Steepest Ascent Hill Climbing
            start = time.time()
            children = 0
            print("Steepest Ascent:")
            frontier = Priority_Queue()
            seen_states = set()
            frontier.push([[], board], 0)
            cost = {}
            cost[hash(str(board))] = 0

            while not frontier.empty():
                moves, current_state = frontier.pop()

                if self.average != None:
                    current_time = time.time()
                    elapsed_time = current_time - start
                    if elapsed_time > self.average:
                        self.solved = False
                        self.dspy_values(board)
                        return

                if current_state.check_sol():
                            end = time.time()
                            self.time = end-start
                            print("CPU Time:", self.time)
                            solution = []
                            board = current_state
                            board.comp_sol = moves
                            self.depth = len(board.comp_sol)
                            self.searched = children
                            self.dspy_values(board)
                            return 

                for new_moves, next_state in current_state.calculate_moves():
                    priority = self.heu.compute_x(next_state)
                    children += 1
                    
                    if hash(str(next_state)) not in seen_states:
                        frontier.push([moves + new_moves, next_state], priority)
                        seen_states.add(hash(str(next_state)))
                    else:
                        if priority < cost[hash(str(next_state))]:
                            frontier.push( [moves + new_moves, next_state], priority)
                        else:
                            continue
                    cost[hash(str(next_state))] = priority
                    self.searched +=1
           
            self.solved = False
        
        def rand_hill(self, board):# Random-Restart Hill Climbings
            start = time.time()
            children = 0
            print("Random-Restart:")
            frontier = Priority_Queue()
            restart_frontier = [board]
            seen_states = set()

            i = 0
            while len(restart_frontier) < 500: #  Generate 500 board states
                current_state = restart_frontier[i]

                if self.average != None:
                    current_time = time.time()
                    elapsed_time = current_time - start
                    if elapsed_time > self.average:
                        self.solved = False
                        self.dspy_values(board)
                        return

                for new_moves, next_state in current_state.calculate_moves():                  
                    if hash(str(next_state)) not in seen_states:
                        restart_frontier.append(next_state)
                        seen_states.add(hash(str(next_state)))                   
                i += 1
            for i in range(0, 100): # Try 100 of the 500 random board states
                rand = random.randint(0, 499)
                seen_states = set()
                priority = self.heu.compute_x(restart_frontier[rand])
                frontier.push([[], restart_frontier[rand]], priority)

class Priority_Queue: # Basic priority queue structure for use with heuristics

    def __init__(self):
        self.queue = []
        self.index = 0

    def push(self, item, priority):
        heapq.heappush(self.queue, (priority, self.index, item))
        self.index += 1

    def empty(self):
        return len(self.queue) == 0

    def pop(self):
        return heapq.heappop(self.queue)[-1]

        
def count_moves(board): # Count total moves for supplied solution
    moves = 0
    for char in board.sup_sol:
        if char.isdigit():
            no = int(char)
            moves += no
    return moves
 
def append(game, bfs, ids, a_star, greedy, random = None ): # Append solutions to a txt file
    sol_str = ''
    f=open("output.txt", "a+")
    f.write("Game: %d\n" %(game))
    f.write("BFS:\n")
    if(bfs.solved):
        for i in bfs.comp_sol:
            for j in i:
                sol_str += str(j)
            sol_str += ' '
        f.write(sol_str)
    else: f.write("Failed.")
    f.write('\n')

    sol_str = ''
    f.write("IDS:\n")
    if ids.solved:
        for i in ids.comp_sol:
            for j in i:
                sol_str += str(j)
            sol_str += ' '
        f.write(sol_str)
    else: f.write("Failed.")
    f.write('\n')

    sol_str = ''
    f.write("A*:\n")
    if  a_star.solved:
        for i in a_star.comp_sol:
            for j in i:
                sol_str += str(j)
            sol_str += ' '
        f.write(sol_str)
    else: f.write("Failed.")
    f.write('\n')

    sol_str = ''
    f.write("Steepest Ascent:\n")
    if greedy.solved:
        for i in greedy.comp_sol:
            for j in i:
                sol_str += str(j)
            sol_str += ' '
        f.write(sol_str)
    else: f.write("Failed.")
    f.write('\n')
    f.write('\n')

    f.close


def main(): # main function
    list = []
    maximal = 26.5
    f=open("output.txt", "w")
    f.close()

    for i in range(1, 41):
        list.append(Board())
    read(list)
    check = False
    for i in range(0, 40):
        # Generate board data
        list[i].cars =  list[i].calculate_cars()
        list[i].dspy(i + 1)
        print("\n")
        supp_moves = count_moves(list[i])
        
        # BFS
        bfs_solver = Solver(supp_moves, list[i].sup_sol, maximal)
        bfs_solver.bfs_search(list[i])

        # IDS
        ids_solver = Solver(supp_moves, list[i].sup_sol, maximal)
        ids_solver.ids_search(list[i])

        # A*  
        a_solver =  Solver(supp_moves, list[i].sup_sol, maximal, Adv_Blocking_Heuristic())
        a_solver.a_star(list[i])

        # Steepest Ascent
        greedy_solver = Solver(supp_moves, list[i].sup_sol, maximal, Adv_Blocking_Heuristic())
        greedy_solver.steep_asc(list[i])
            
        # Random Restart
        #rand_solver = Solver(supp_moves, list[i].sup_sol, maximal, Adv_Blocking_Heuristic())
        #rand_solver.rand_hill(list[i])
        
        append(i + 1, bfs_solver, ids_solver, a_solver, greedy_solver)

        input("Press enter for next problem...")
    

if __name__ == "__main__":
    main()
