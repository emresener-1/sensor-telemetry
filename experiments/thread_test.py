import time
import threading
import queue


stop = threading.Event()
data_q = queue.Queue()


def sensor_loop(name, hz):
    while not stop.is_set():
        data_q.put({"sensor": name, "t": time.time(), "value": 0})
        stop.wait(1 / hz)
    print(f"{name} durdu")


def printer_loop():
    while not stop.is_set():
        try:
            msg = data_q.get(timeout=1)
        except queue.Empty:
            continue
        print(msg)
    print("yazıcı durdu")


power_thread = threading.Thread(target=sensor_loop, args=("güç", 10))
hr_thread = threading.Thread(target=sensor_loop, args=("nabız", 1))
printer_thread = threading.Thread(target=printer_loop)

power_thread.start()
hr_thread.start()
printer_thread.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop.set()
    power_thread.join()
    hr_thread.join()
    printer_thread.join()
    print("Program temiz kapandı")
