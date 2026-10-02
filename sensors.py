import numpy as np


RESTING_HR = 60
HR_PER_WATT = 0.37
HR_RESPONSE = 0.03
BASE_CADENCE = 65
CADENCE_PER_WATT = 0.1
AIR_DENSITY = 1.2
CDA = 0.3
METERS_PER_DEG_LAT = 111000
GPS_DT = 1.0
FAULT_RATE = 0.01


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
        if np.random.random() < FAULT_RATE:
            return -50
        return self.power + np.random.normal(0,10)
    
    def read_hr(self):
        target_heart_rate = RESTING_HR + HR_PER_WATT * self.power
        self.hr += (target_heart_rate - self.hr) * HR_RESPONSE
        if np.random.random() < FAULT_RATE:
            return 250
        return self.hr + np.random.normal(0,1)
    
    def read_cadence(self):
        cadence = BASE_CADENCE + CADENCE_PER_WATT * self.power
        if np.random.random() < FAULT_RATE:
            return None
        return cadence + np.random.normal(0,2)
    
    def read_speed(self):
        speed_ms = (2 * self.power / (AIR_DENSITY * CDA)) ** (1/3)
        self.speed = speed_ms * 3.6
        if np.random.random() < FAULT_RATE:
            return 0
        return self.speed + np.random.normal(0, 0.5)
    
    def read_gps(self):
        distance = (self.speed / 3.6) * GPS_DT
        self.lat += distance / METERS_PER_DEG_LAT
        noise = np.random.normal(0,3) / METERS_PER_DEG_LAT
        if np.random.random() < FAULT_RATE:
            return self.lat + 0.005, self.lon
        return self.lat + noise, self.lon
    



    
if __name__ == "__main__":
    bike = BikeSimulator()
    for _ in range(100):
        power = bike.read_power()
        hr = bike.read_hr()
        cadence = bike.read_cadence()
        speed = bike.read_speed()
        lat, lon = bike.read_gps()
        if cadence is not None:
            cadence_str = f"{cadence:.2f}"
        else:
            cadence_str = "None"
        print(f"{power:.2f} W - {hr:.2f} bpm - {cadence_str} rpm - {speed:.2f} km/h - {lat:.6f}, {lon:.6f}")

    
