from abc import ABC, abstractmethod

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
        return f"{type(self).__name__}(name='{self.name}', battery={self.battery})"\
    
    @abstractmethod
    def perform_task(self):
        pass
    
class DroneRobot(Robot):
        def __init__(self, name, battery=100, max_altitude=100):
            super().__init__(name, battery)
            self.max_altitude = max_altitude
        
        def perform_task(self):
            return f"{self.name} is flying at an altitude of {self.max_altitude}m."
        