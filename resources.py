class Parking_lot:
    def __init__(self,capacity):
        self.capacity=capacity
        self.available_spaces=capacity
        self.occupied_spaces=0
        self.cars_waiting=0

    def park(self, car, time):
        self.available_spaces-=1
        self.occupied_spaces+=1  
        car.parked_time=time

    def release_space(self,car,time):
        self.available_spaces+=1
        self.occupied_spaces-=1  
        car.departure_time=time

    def is_full():
        return self.available_spaces==0



import numpy as np

class Server:
    def __init__(self, server_id, mean_cooking_time):
        self.server_id = server_id
        self.mean_cooking_time = mean_cooking_time
        self.status = "idle"
        self.current_visitor = None

    def start_cooking(self, visitor_id):
        if self.status != "idle":
            return None

        self.status = "busy"
        self.current_visitor = visitor_id

        cooking_time = np.random.exponential(self.mean_cooking_time)

        return cooking_time

    def finish_cooking(self):
        if self.status != "busy":
            return False

        self.status = "idle"
        self.current_visitor = None

        return True

    def is_available(self):
        return self.status == "idle"

    