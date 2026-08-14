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

def log_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Starting: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished: {func.__name__}")
        return result

    return wrapper

class Robot(ABC):
    manufacturer = "RoboTik"
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

    @log_task
    def perform_task(self):
        self.use_battery(20)
        return f"{self.name} is flying at an altitude of {self.max_altitude}m."

class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=10):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    @log_task
    def perform_task(self):
        self.use_battery(10)
        return f"{self.name} is cleaning with {self.dust_capacity} dust capacity."
