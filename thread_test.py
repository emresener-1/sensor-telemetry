import time
import threading


stop = threading.Event()


def sensor_loop(name, hz):
    while not stop.is_set():
        print(name, time.strftime("%H:%M:%S"))
        time.sleep(1 / hz)
    print(f"{name} durdu")

power_thread = threading.Thread(target=sensor_loop, args=("güç", 10))
hr_thread = threading.Thread(target=sensor_loop, args=("nabız", 1))

power_thread.start()
hr_thread.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop.set()
    power_thread.join()
    hr_thread.join()
    print("Program temiz kapandı")
