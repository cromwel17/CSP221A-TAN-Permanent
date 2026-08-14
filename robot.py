from abc import ABC, abstractmethod

class InsufficientBatteryError(Exception):
    pass

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
            raise InsufficientBatteryError("way kana battery, charge na dnay!")
        self.battery -= amount
    
    @abstractmethod
    def perform_task(self):
        pass
    
    def run_task_safely(robot, cute):
        try:
            result = robot.perform_task(cute)
        except InsufficientBatteryError as error:
            print(f"Error: {error}")
        else:
            print(result)
        finally:
            print("Task attempt finished.")

class DroneRobot(Robot):
        def __init__(self, name, battery=100, max_altitude=100):
            super().__init__(name, battery)
            self.max_altitude = max_altitude
        
        def perform_task(self):
            self.use_battery(20)
            return f"{self.name} is flying at an altitude of {self.max_altitude}m."
        
class CleaningRobot(Robot):
        def __init__(self, name, battery=100, dust_capacity=10):
            super().__init__(name, battery)
            self.dust_capacity = dust_capacity
        
        def perform_task(self):
            self.use_battery(10)
            return f"{self.name} is cleaning with {self.dust_capacity} dust capacity."

