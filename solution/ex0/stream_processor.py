from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self, data):
        self.data = data
    
    @abstractmethod
    def process(self, data: Any):
        pass
    
    @abstractmethod
    def validate(self, data: Any):
        pass

    def format_output(self, result : str):
        """has a default behavior, needs to be overridden"""
        print("Processed: example")
        pass
class NumericProcessor(DataProcessor):
    pass

class LogProcessor(DataProcessor):
    pass



    

    





# you cannot create objects directly from an abstract class

# the abstract method decorator means:
# - method has no code here
# - all sub classes will need to write the method