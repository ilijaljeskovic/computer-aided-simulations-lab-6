class Car:
    def __init__(self, car_id, num_passengers, arrival, passengers):
        self.car_id=car_id
        self.num_passengers = num_passengers
        self.arrival=arrival
        self.passengers=[]

class Visitor:
    def __init__(self, id, car_id):
        self.id=id
        self.car_id=car_id
        self.ready_to_leave=False
        self.current_location="parking" #can be parking, concourse, food court
        self.eating_time=None
