import heapq
import random
from collections import defaultdict

#How the plane is set up (all constant)
ROWS = 4
SEATS_PER_ROW = 6
SEAT_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'] #Seats designated for each row
PRIORITY_SEATS = {(0, 'A'), (0, 'F'), (1, 'C'), (1, 'D')} #Priority passenger seats

#Creates the layout of the plane
def generate_seat_map(rows, seats_per_row):
    return {(r, l): None for r in range(rows) for l in SEAT_LETTERS[:seats_per_row]}

#Passengers
class Passenger:
    def __init__(self, name, paid_priority):
        self.name = name
        self.last_name = name.split()[-1] #Looks for the last name
        self.paid_priority = paid_priority #Check if they paid for priority

    def __repr__(self):
        return f"{self.name} ({'Priority' if self.paid_priority else 'Standard'})"

#Class for the way the passegers will be seated
class AirlineSeating:
    def __init__(self, passengers):
        self.passengers = passengers
        self.seat_map = generate_seat_map(ROWS, SEATS_PER_ROW) #Creates the layout of the plane
        self.assigned_seats = {} #Assigns seats
        self.name_groups = defaultdict(list) #Checks the passengers for last name and groups them together
        for p in passengers:
            self.name_groups[p.last_name].append(p) #Makes the passengers group by last name

    def is_valid_seat(self, seat):
        return self.seat_map[seat] is None #Looks for empty seats

    def get_horizontal_block(self, size):
        for row in range(ROWS):
            for start in range(SEATS_PER_ROW - size + 1): #Check for spots to group people together
                block = [(row, SEAT_LETTERS[start + i]) for i in range(size)]
                if all(self.is_valid_seat(seat) for seat in block): #Check if those seats are empty
                    return block 
        return [] #Empty block if not empty

    def assign_group_horizontal(self, group):
        block = self.get_horizontal_block(len(group)) #Find row of seats for one family
        for passenger, seat in zip(group, block):
            self.seat_map[seat] = passenger #Assigns the passenger to that seat
            self.assigned_seats[passenger.name] = seat

    def assign_seats(self):
        priority_passengers = [(0, idx, p) for idx, p in enumerate(self.passengers) if p.paid_priority] #Priority queue for priority passengers
        heapq.heapify(priority_passengers)
        for seat in PRIORITY_SEATS:
            if not priority_passengers:
                break
            if self.seat_map[seat] is None:
                _, _, passenger = heapq.heappop(priority_passengers)
                self.seat_map[seat] = passenger #Assign priority passengers to their seat
                self.assigned_seats[passenger.name] = seat

        for group in self.name_groups.values():
            group = [p for p in group if p.name not in self.assigned_seats]
            if not group:
                continue
            self.assign_group_horizontal(group) #Put families together

        unassigned = [p for p in self.passengers if p.name not in self.assigned_seats] #Look for the unassigned seats
        available_seats = [s for s, v in self.seat_map.items() if v is None]
        random.shuffle(available_seats) #Random result for seats during every run
        for passenger, seat in zip(unassigned, available_seats):
            self.seat_map[seat] = passenger #Assign the left over passengers
            self.assigned_seats[passenger.name] = seat

    def print_seating_chart(self):
        print("\nSeating Chart:\n")
        for r in range(ROWS):
            row = [] #Store the seating information
            for l in SEAT_LETTERS[:SEATS_PER_ROW]:
                seat = (r, l)
                p = self.seat_map[seat] #Give the passenger their seat information
                tag = p.last_name[:3].upper() if p else "___" #Shows the name of the passenger (First 3 letters of last name only)
                row.append(f"{l}:{tag}")
            print(f"Row {r+1:2} | {'  '.join(row)}") #Prints the row

    def print_assignments_in_order(self):
        print("\nPassenger Assignments (In Order of Appearance):\n")
        for passenger in self.passengers:
            seat = self.assigned_seats[passenger.name] #Gets each passengers seat
            print(f"{passenger.name:25} -> Row {seat[0] + 1}{seat[1]}") #Prints the passengers assigned seat

#Sample 24 passengers for 4x6 layout (True = Priority Passenger)
sample_passengers = [
    Passenger("Alice Bryant", True),
    Passenger("Bob Smith", False),
    Passenger("Carol Smith", False),
    Passenger("Daniel Johnson", False),
    Passenger("Eli Johnson", False),
    Passenger("Faye Johnson", False),
    Passenger("Gina Lee", True),
    Passenger("Harry Forge", False),
    Passenger("Isla Kim", False),
    Passenger("Jack Kim", False),
    Passenger("Kara Kim", False),
    Passenger("Liam Brown", False),
    Passenger("Mia Brown", False),
    Passenger("Noah White", False),
    Passenger("Olivia White", False),
    Passenger("Peter Black", False),
    Passenger("Quinn Black", False),
    Passenger("Riley Green", False),
    Passenger("Sophie Green", False),
    Passenger("Tom Blue", True),
    Passenger("Uma Red", False),
    Passenger("Vera Red", False),
    Passenger("Will Gray", False),
    Passenger("Zoe Hughs", True),
]

#Run
airline = AirlineSeating(sample_passengers)
airline.assign_seats()
airline.print_seating_chart()
airline.print_assignments_in_order()
