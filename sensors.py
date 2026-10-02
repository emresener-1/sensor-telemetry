import numpy as np


RESTING_HR = 60
HR_PER_WATT = 0.37
HR_RESPONSE = 0.03


class BikeSimulator:
    def __init__(self):
        self.power = 250.0
        self.hr = 120.0
        self.lat = 45.04
        self.lon = 7.40
    
    def read_power(self):
        self.power += np.random.normal(0,5)
        self.power = min(max(self.power, 150), 350)
        return self.power + np.random.normal(0,10)
    
    def read_hr(self):
        target_heart_rate = RESTING_HR + HR_PER_WATT * self.power
        self.hr += (target_heart_rate - self.hr) * HR_RESPONSE
        return self.hr + np.random.normal(0,1)

    
if __name__ == "__main__":
    bike = BikeSimulator()
    for _ in range(100):
        print(round(bike.read_power(), 2), round(bike.read_hr(), 2))
    
