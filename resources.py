import random
import numpy as np
import math

class Parking_lot:
    def __init__(self,capacity):
        self.capacity=capacity
        self.available_spaces=capacity
        self.occupied_spaces=0
        self.cars_waiting=0

    def park(self):
        self.available_spaces-=1
        self.occupied_spaces+=1  
        

    def release_space(self):
        self.available_spaces+=1
        self.occupied_spaces-=1  


    def is_full(self):
        return self.available_spaces==0


class Server:
    def __init__(self, server_id, mean_cooking_time, sigma_cooking_time):
        self.server_id = server_id
        self.mean_cooking_time = mean_cooking_time
        self.sigma_cooking_time=sigma_cooking_time
        self.status = "idle" #can be idle,busy or blocked
        self.current_visitor = None

    def start_cooking(self, visitor):
        if self.status != "idle":
            return False

        self.status = "busy"
        self.current_visitor = visitor
        return True


    def finish_cooking(self):
        if self.status != "busy":
            return None
        self.status = "blocked"
        return self.current_visitor

    def release_visitor(self):
        if self.status!="blocked":
            return None
        visitor=self.current_visitor
        self.current_visitor=None
        self.status="idle"
        return visitor

    def is_available(self):
        return self.status == "idle"

class DiningArea:
    def __init__(self,capacity):
            self.capacity=capacity
            self.available_spaces=capacity
            self.occupied_spaces=0
            
    def seat(self, visitor, time):
        self.available_spaces-=1
        self.occupied_spaces+=1


    def release_space(self,visitor,time):
        self.available_spaces+=1
        self.occupied_spaces-=1  
        

    def is_full(self):
        return self.available_spaces==0

    class ServiceArea:
        def __init__(self,capacity):
            self.capacity=capacity
            self.available_spaces=capacity
            self.occupied_spaces=0
    
        def occupy_space(self):
            self.available_spaces-=1
            self.occupied_spaces+=1  
            
    
        def release_space(self):
            self.available_spaces+=1
            self.occupied_spaces-=1  
    
    
        def is_full(self):
            return self.available_spaces==0
    