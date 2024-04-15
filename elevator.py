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
    
    #bestämmer om hissen ska gå upp(return 0), ner(return 1) eller släppa av/på passagerare(return 2)
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

#för debugging
if __name__ == "__main__":
    skyscrape = Skyscraper(4,1)
    skyscrape.floor_state[0].append(Task(0,2))
    print(skyscrape.floor_state,skyscrape.elevators[0].tasks)
    skyscrape.time_step()
    print(skyscrape.floor_state,skyscrape.elevators[0].tasks)
    skyscrape.elevators[0].current_floor = 2
    skyscrape.elevators[0].waiting_on_floor = 0
    skyscrape.time_step()
    print(skyscrape.floor_state,skyscrape.elevators[0].tasks)



    
        