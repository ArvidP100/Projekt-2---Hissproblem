import random as r
#test test test
class Skyscraper:
    def __init__(self, num_floors, num_elevators):
        self.top = num_floors
        self.elevators = [Elevator(5) for i in range(num_elevators)]
        self.floor_state = [None for i in range(num_floors)]    

    def generate_task(self):
        start = r.randint(0, self.top)
        dest = r.choice([i for i in range(0,self.top) if not i==start])
        new_task = Task(start, dest)


class Elevator:
    def __init__(self, max_load):
        self.current_floor = 0
        self.max_load = max_load
        self.dest = 0 
        self.tasks = []
    
    def finish_task 


class Task:
    def __init__(self, start, dest):
        self.floor = start
        self.dest = dest 
        self.time = 0 
    


    
        