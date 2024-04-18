import random as r
#test test test
#ingrid är här
class Skyscraper:
    def __init__(self, num_floors, num_elevators):
        self.top = num_floors
        self.elevators = [MajorityElevator(5) for i in range(num_elevators)]
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
                elv.check_for_arrival()
                #passagerare går på
                m = 0
                for i in range(len(self.floor_state[elv.current_floor])):
                    if elv.max_load > len(elv.tasks):
                        elv.tasks.append(self.floor_state[elv.current_floor][i])
                    else:
                        m= i
                        break
                if m != 0:
                    self.floor_state[elv.current_floor] = self.floor_state[elv.current_floor][m+1:]
                else: self.floor_state[elv.current_floor] = []

                

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

    def check_for_arrival(self):
        l = []
        for i in range(len(self.tasks)):
            if self.tasks[i].dest == self.current_floor:
                self.totaltime += self.tasks[i].time**2
                l.append(i)
        l.reverse()
        for i in l:
            self.tasks.remove(self.tasks[i])


 #   def finish_task 
                
# Hissen som går till den våning där det finns flest människor som vill på/av
class MajorityElevator(Elevator):

    # samma konstruktor, med ett extra attribut
    def __init__(self, max_load):
        super().__init__(max_load)
        self.destination = (False, None) # om den har bestämt sig för en destination, ska den åka dit tills den är klar
        # self.passengers_entering = 0 # håller koll på passagerare som håller på att stiga upp

    def choice_to_return(self, travel_to):
        # 2 stannar den, 1 går den ner, 2 går den upp
            if self.current_floor == travel_to:
                return 2
            elif self.current_floor > travel_to:
                return 1
            elif self.current_floor < travel_to: 
                return 0

    # får in floor_states som information, det är en lista med listor
    def make_choice(self, information: list) -> int:
        
        if self.destination[0]:
            if self.destination[1] == self.current_floor:
                self.destination = (False, None)
                return 2
            else:
                return self.choice_to_return(self.destination[1])

        # om den inte har en destination, beräknar den det ist
        # skapar en lista, med hur många som väntar på varje våning
        floor_list = list() 
        floors = len(information)    
        for i in range(floors):
            floor_list.append(len(information[i]))
        for task in self.tasks:
            floor_list[task.dest] += 1

        # ger den våning dit flest vill
        # har två samma tar den den våningen som är närmast bottenplan
        travel_to = floor_list.index(max(floor_list))
        self.destination = (True, travel_to)
        return self.choice_to_return(travel_to)

        

        #return floor_list

class Task:
    def __init__(self, start, dest):
        self.floor = start
        self.dest = dest 
        self.time = 0 

    # för debugging
    def __repr__(self):
        return f'Task(start: {self.floor}, dest: {self.dest}, time: {self.time})'
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
    
    skyscrape.floor_state[1].append(Task(1,2))
    skyscrape.floor_state[2].append(Task(2,3))
    skyscrape.floor_state[2].append(Task(2,3))

    for _ in range(20):
        skyscrape.time_step()
        print(f'floor states: {skyscrape.floor_state} \n tasks: {skyscrape.elevators[0].tasks} \n floor: {skyscrape.elevators[0].current_floor} \n =====')
        
   

    # skyscrape = Skyscraper(4,1)
    # skyscrape.floor_state[0].append(Task(0,2))
    # print(skyscrape.floor_state,skyscrape.elevators[0].tasks)
    # skyscrape.time_step()
    # print(skyscrape.floor_state,skyscrape.elevators[0].tasks)
    # skyscrape.elevators[0].current_floor = 2
    # skyscrape.elevators[0].waiting_on_floor = 0
    # skyscrape.time_step()
    # print(skyscrape.floor_state,skyscrape.elevators[0].tasks)

        skyscrape.time_step()
        print(skyscrape.elevators[0].current_floor)
        print(skyscrape.elevators[0].tasks)


    
        