import numpy as np
import random
import math

def generate_cooking_and_eating_time(mu_cook, sigma_cook, mu_eat, sigma_eat):
    u1=random.random()
    u2=random.random()

    z1=math.sqrt(-2 * math.log(u1))*math.cos(2*math.pi*u2)
    z2=math.sqrt(-2 * math.log(u1))*math.sin(2*math.pi*u2)
    x1=math.exp(mu_cook +sigma_cook*z1)
    x2=math.exp(mu_eat+sigma_eat*z2)
    
    return x1,x2

def generate_interarrival_time(mu):
    return random.expovariate(1/mu)
