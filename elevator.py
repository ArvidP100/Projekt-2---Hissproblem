import random as r
#test test test
#ingrid är här
class Skyscraper:
    def __init__(self, num_floors, num_elevators):
        self.top = num_floors
        self.elevators = [Elevator(5) for i in range(num_elevators)]
        #Antar att floorstates är en lista av tasks som väntar där
        self.floor_state = [[] for i in range(num_floors)]  

        #hur många tidsteg det tar att släppa på/av
        self.wait_cost = 3 

    def generate_task(self):
        start = r.randint(0, self.top)
        dest = r.choice([i for i in range(0,self.top) if not i==start])
        new_task = Task(start, dest)

    def time_step(self)-> None:
        for elv in self.elevators:

            #sköter logik för elevators val
            choice = elv.make_choice(self.floor_state)
            if elv.waiting_on_floor != 0:
                elv.waiting_on_floor -= 1
            elif choice == 2:
                #släpper av passagerare
                elv.check_for_arraival()

                #passagerare går på
                for task in self.floor_state[elv.current_floor]:
                    if elv.max_load > len(elv.tasks):
                        elv.tasks.append(task)
                        self.floor_state[elv.current_floor].remove(task)

                elv.waiting_on_floor = self.wait_cost
            elif choice == 0:
                elv.current_floor += 1
            elif choice == 1:
                elv.current_floor += -1          
    #får tiden att gå frammåt
            for task in elv.tasks:
                task.time += 1
        for floor in self.floor_state:
            for task in floor:
                task.time += 1


#Förslagvis gör vi varje elevator en child class där vi bara ändrar make choice för varje stratergi
class Elevator:
    def __init__(self, max_load):
        #sparar hut mycket tid passageare väntat
        self.totaltime = 0

        self.current_floor = 0
        self.max_load = max_load
        self.dest = 0 
        self.tasks = []

        #håller koll om hissen väntar på passagerare att gå på/av
        self.waiting_on_floor = 0
    
    #bestämmer om hissen ska gå upp(return 0), ner(return 1) eller släppa av/på passagerare(return 2) (kan skicka -1 om du vill att den inte ska göra ngt)
    def make_choice(self,information:list)->int:
        return 2

    def check_for_arraival(self):
        for task in self.tasks:
            if task.dest == self.current_floor:
                self.totaltime += task.time**2
                self.tasks.remove(task)


 #   def finish_task 

class Task:
    def __init__(self, start, dest):
        self.floor = start
        self.dest = dest 
        self.time = 0 

class WaitLong(Elevator):
    def __init__(self, max_load):
        super().__init__(max_load)
    
    def make_choice(self, information: list) -> int:
        waited_longest = None
        onElevator = False
        for floor in information:
            for task in floor:
                if waited_longest == None:
                    waited_longest = task
                elif waited_longest.time < task.time:
                    waited_longest = task.time
        for task in self.tasks:
            if waited_longest == None:
                waited_longest = task
                onElevator = True
            elif waited_longest.time < task.time:
                onElevator = True
                waited_longest = task.time 

        if waited_longest == None:
            return -1   

        if onElevator:
            if self.current_floor == waited_longest.dest:
                return 2
            elif self.current_floor - waited_longest.dest < 0:
                return 0
            else:
                return 1
        else:
            if self.current_floor == waited_longest.floor:
                return 2
            elif self.current_floor - waited_longest.floor < 0:
                return 0
            else:
                return 1

#för debugging
if __name__ == "__main__":
    skyscrape = Skyscraper(4,1)
    skyscrape.elevators[0] = WaitLong(5)
    skyscrape.floor_state[3].append(Task(3,2))
    for i in range(10):

        skyscrape.time_step()
        print(skyscrape.elevators[0].current_floor)
        print(skyscrape.elevators[0].tasks)


    
        