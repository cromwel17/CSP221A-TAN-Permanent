from abc import ABC, abstractmethod
from functools import wraps
import logging

class InsufficientBatteryError(Exception):
    def __init__(self, name, required, available):
        self.name = name
        self.required = required
        self.available = available
        super().__init__(
            f"{name} needs {required}% battery for this task "
            f"but only has {available}%."
        )

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Starting: {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished: {func.__name__}")
        return result

    return wrapper

class Robot(ABC):
    manufacturer = "RoboTik nyort"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))

    def __str__(self):
        return f"{self.name} (Battery: {self.battery}%)"

    def __repr__(self):
        return f"{type(self).__name__}(name='{self.name}', battery={self.battery})"

    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(
                self.name, amount, self.battery
            )
        self.battery -= amount

    @classmethod
    def from_config(cls, config):
        return cls(config["name"], config.get("battery", 100))
        
    @abstractmethod
    def perform_task(self):
        pass

def fleet_report(robots):
    for robot in robots:
        print(str(robot))

def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as error:
        logging.error(error)
    else:
        print(result)
    finally:
        print(f"{robot.name} battery: {robot.battery}%")

class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=100):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    @log_action
    def perform_task(self):
        self.use_battery(20)
        return f"{self.name} is flying at an altitude of {self.max_altitude}m."

class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=10):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    @log_action
    def perform_task(self):
        self.use_battery(10)
        return f"{self.name} is cleaning with {self.dust_capacity} dust capacity."
    
print("=== Fleet Report ===")

drone = DroneRobot("Aqua-Drone", 50, 200)
cleaner = CleaningRobot("Roomba", 50, 10)

fleet_report([drone, cleaner])

print("\n=== Drone Task ===")
run_task_safely(drone)

print("\n=== Cleaning Task ===")
run_task_safely(cleaner)

print("\n=== Insufficient Battery ===")

low_drone = DroneRobot("Low-Drone", 5, 100)
run_task_safely(low_drone)

print("\n=== From Config ===")

config = {
    "name": "Config-Drone",
    "battery": 15
}

config_drone = DroneRobot.from_config(config)
print(config_drone)

print("\n=== Repr ===")
print(repr(config_drone))

print("\n=== Decorator Test ===")
print(DroneRobot.perform_task.__name__)

print("\n=== Population ===")
print(Robot.population)

"""class Bug:
items = []
tyek = Bug()
ekis = Bug()

tyek.items.append("T")

print("Bug:")
print(ekis.items)
print(tyek.items)

class Fix:
    def __init__(self):
        self.items = []

tyek = Fix()
ekis = Fix()

tyek.items.append("T")

print("Fix:")
print(ekis.items)
print(tyek.items)"""