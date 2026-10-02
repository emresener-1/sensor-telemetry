import numpy as np


RESTING_HR = 60
HR_PER_WATT = 0.37
HR_RESPONSE = 0.03
BASE_CADENCE = 65
CADENCE_PER_WATT = 0.1
AIR_DENSITY = 1.2
CDA = 0.3

class BikeSimulator:
    def __init__(self):
        self.power = 250.0
        self.hr = 120.0
        self.lat = 45.04
        self.lon = 7.40
        self.speed = 0.0
    
    def read_power(self):
        self.power += np.random.normal(0,5)
        self.power = min(max(self.power, 150), 350)
        return self.power + np.random.normal(0,10)
    
    def read_hr(self):
        target_heart_rate = RESTING_HR + HR_PER_WATT * self.power
        self.hr += (target_heart_rate - self.hr) * HR_RESPONSE
        return self.hr + np.random.normal(0,1)
    
    def read_cadence(self):
        cadence = BASE_CADENCE + CADENCE_PER_WATT * self.power
        return cadence + np.random.normal(0,2)
    
    def read_speed(self):
        speed_ms = (2 * self.power / (AIR_DENSITY * CDA)) ** (1/3)
        self.speed = speed_ms * 3.6
        return self.speed + np.random.normal(0, 0.5)


    
if __name__ == "__main__":
    bike = BikeSimulator()
    for _ in range(100):
        print(round(bike.read_power(), 2), round(bike.read_hr(), 2), round(bike.read_cadence(), 2), round(bike.read_speed(), 2))
    
