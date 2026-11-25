from queue import PriorityQueue
import random
import numpy as np
import math
import places
import entities
import resources
import distributions

class Event:
    def __init__(self, time, event_type, data=None):
        self.time = time
        self.event_type=event_type
        self.data=data

class Simulation:
    def __init__(self,config):
        self.current_time=0
        self.FES=PriorityQueue()
        self.event_counter=0

        self.visitors={}
        self.cars={}
        self.statistics={}
        
        self.parking_lot=resources.Parking_lot(config.park_capacity)
        self.dining_area=resources.DiningArea(config.dining_capacity)
        self.service_area = resources.ServiceArea(config.service_capacity)
        self.concourse=places.Location()
        self.food_court=places.Location()

        self.simulation_time=config.simulation_time
        self.parking_to_concourse_time=config.parking_to_concourse_time
        self.concourse_to_food_time=config.concourse_to_food_time
        self.mean_cooking_time=config.mean_cooking_time
        self.mean_eat_time=config.mean_eat_time
        self.sigma_cooking_time=config.sigma_cooking_time
        self.sigma_eat_time=config.sigma_eat_time
        self.mean_interarrival=config.mean_interarrival

        self.car_id=0
        self.visitor_id=0

        # Food Court queues and resources

        self.servers = [
    resources.Server(i, self.mean_cooking_time, self.sigma_cooking_time)
    for i in range(config.num_servers)]
        
        self.cooking_queue = []
        self.service_queue = []

        self.occupied_counter = 0

    def schedule_event(self, time, event_type, data=None):
        event=Event(time,event_type,data)

        self.FES.put(time, self.event_counter, event)
        self.event_counter+=1

    #CAR ARRIVALS

    def generate_arrivals(self):
        passengers=[]
        num_passengers=random.randint(1,5)
        for _ in num_passengers:
            visitor = entities.Visitor(self.visitor_id, self.car_id)
            passengers.append(visitor)
            self.visitors[self.visitor_id]=visitor
            self.visitor_id+=1
        car=entities.Car(self.car_id, num_passengers, self.current_time, passengers)
        self.cars[self.car_id]=car

        #generate next arrival
        next_arrival = time+distributions.generate_interarrival_time(self.mean_interarrival_time)
        if next_arrival<=self.simulation_time:
            self.schedule_event(next_arrival, "CAR_ARRIVAL")


        #try parking current car
        if not self.parking_lot.is_full():
            self.parking_lot.park()
            car.parking_time=self.current_time

            self.schedule_event(self.current_time+self.parking_to_concourse_time, "VISITORS_REACH_CONCOURSE", self.car_id)
        
        else:
            self.parking_queue.append(self.car_id)
        
        car_id+=1


    #VISITOR MOVEMENT
    def handle_concourse_arrival(self, car_id):
        car=self.cars[car_id]

        for visitor in car.passengers:
            if random.random()<0.7: #temporary until other places logic written
                self.schedule_event(self.current_time+self.concourse_to_food_time, "FOOD_COURT_ARRIVAL", visitor.visitor_id)
            else:
                visitor.ready_to_leave=True

    #FOOD PREP
    def handle_food_court_arrival(self, visitor_id):
        self.cooking_queue.append(visitor_id)
        self.start_cooking()

    def start_cooking(self):
        for server in self.servers:
            if self.cooking_queue and server.is_available():

                visitor_id = self.cooking_queue.pop(0)
                visitor = self.visitors[visitor_id]

                server.start_cooking(visitor)

                cooking_time, eating_time = distributions.generate_cooking_and_eating_time(self.mean_cooking_time,self.sigma_cooking_time,self.mean_eat_time,self.sigma_eat_time)
                visitor.eating_time=eating_time
                self.schedule_event(
                    self.current_time + cooking_time,
                    "COOKING_COMPLETE",
                    server.server_id
                )

    def handle_cooking_complete(self, server_id):
        server=self.servers[server_id]
        visitor = server.finish_cooking()

        if visitor is None:
            return
        self.service_queue.append(server_id)
        self.move_to_service_area()

    def move_to_service_area(self):

        while self.service_queue and not self.dining_area.is_full():
            server_id = self.service_queue.pop(0)
            server = self.servers[server_id]

            visitor = server.release_visitor()

            self.service_area.occupy_space()

            self.start_eating(visitor)

            #servers can accept another order
            self.start_cooking()


    def start_eating(self, visitor):
        if not self.dining_area.is_full():
            self.service_area.release_space()
            self.dining_area.seat(visitor,self.current_time)
            self.schedule_event(self.current_time+visitor.eating_time, "EATING COMPLETE", visitor.visitor_id)

            #a service area space is now freed up
            self.move_to_service_area()
        else:
            self.table_queue.append(visitor)

    def handle_eating_complete(self, visitor_id):
        visitor=self.visitors[visitor_id]

        self.dining_area.release_space(visitor, self.current_time)
        visitor.ready_to_leave=True
        self.seat_waiting_customer()

    def seat_waiting_customer(self):
        while self.table_queue and not self.dining_area.is_full():

            visitor=self.table_queue.pop(0)
            self.dining_area.seat(visitor,self.current_time)
            eating_time=visitor.eating_time

            self.schedule_event( self.current_time + eating_time,"EATING_COMPLETE",visitor.visitor_id)

        # a server is unblocked because of a freed up service space
        self.move_to_service_area()