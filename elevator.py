import random as r

class Skyscraper:
    def __init__(self, num_floors, num_elevators,Elv,firstfloorp=0.5,toofirstfloorp=0.5):
        self.top = num_floors
        self.elevators = [Elv(5) for i in range(num_elevators)]
        #Antar att floorstates är en lista av tasks som väntar där
        self.floor_state = [[] for i in range(num_floors)]  

        #hur många tidsteg det tar att släppa på/av
        self.wait_cost = 4 

        #andelen tasks som genereras på första våningen
        self.ffg = firstfloorp

        #andelen tasks som vill till första våningen
        self.tff = toofirstfloorp

    def generate_task(self):

        if r.random() < self.ffg:
            start = 0
            dest = r.randint(1,self.top-1)
        else:
            start = r.randint(1, self.top-1)
            if r.random() < self.tff:
                dest = 0
            else:
                dest = r.choice([i for i in range(1,self.top-1) if not i==start])
        self.floor_state[start].append(Task(start, dest))

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
                elv.distance += 1
                elv.current_floor += 1
            elif choice == 1:
                elv.distance += 1
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
        self.sqrttot = 0
        self.distance = 0

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
                self.totaltime += self.tasks[i].time
                self.sqrttot += self.tasks[i].time**2
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
                    waited_longest = task
        for task in self.tasks:
            if waited_longest == None:
                waited_longest = task
                onElevator = True
            elif waited_longest.time < task.time:
                onElevator = True
                waited_longest = task

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

class UpAndDown(Elevator):
    def __init__(self, max_load):
        super().__init__(max_load)
        self.going_up = True

    def make_choice(self, information:list):
        arrivals = bool([task for task in self.tasks if task.dest == self.current_floor])
        departurs = bool(information[self.current_floor])

        if arrivals or departurs:
            return 2
        elif self.going_up:
            elev = bool([task for task in self.tasks if task.dest > self.current_floor]) 
            house = bool([task for floor in information for task in floor if task.floor > self.current_floor])
            if not any([elev, house]):
                self.going_up = False
                return 1
            return 0
        else:
            elev = bool([task for task in self.tasks if task.dest < self.current_floor]) 
            house = bool([task for floor in information for task in floor if task.floor < self.current_floor])
            if not any([elev, house]):
                self.going_up = True
                return 0
            return 1

#för debugging/få fram resultat
if __name__ == "__main__":
    skyscrape = Skyscraper(5,1,UpAndDown,firstfloorp=0.5,toofirstfloorp=0.8)
    skyscrape.elevators[0].maxload = 7
    n = 0
    for i in range(50000):
        if r.randint(1,100) < 40:
            n += 1
            skyscrape.generate_task()
        skyscrape.time_step()
        if i % 1000==0:
            print(i)

    for t in skyscrape.elevators[0].tasks:
        skyscrape.elevators[0].totaltime += t.time
        skyscrape.elevators[0].sqrttot += t.time **2
    for f in skyscrape.floor_state:
        for t in f:
            skyscrape.elevators[0].totaltime += t.time
            skyscrape.elevators[0].sqrttot += t.time **2           
    print(f"snitt tid:{skyscrape.elevators[0].totaltime/n}")
    print(f"kvadratisk tid:{skyscrape.elevators[0].sqrttot/n}")
    print(f"Antal passagerare:{n}")
    print(f"Stäck färdad:{skyscrape.elevators[0].distance}")



    
        