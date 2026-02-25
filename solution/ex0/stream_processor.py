from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self, data):
        self.data = data
    
    @abstractmethod
    def process(self, data: Any) -> str:
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result : str) -> str:
        """has a default behavior, needs to be overridden"""
        return f"Processed: {result}"

class NumericProcessor(DataProcessor):

    def process(self, data : Any):
        return f"Processing data: {data}"
    
    def validate(self, data : Any):
        if isinstance(data, list):
            count = 0
            total_sum = 0
            try:
                for e in data:
                    total_sum += int(e)
                    count += 1
                return True
            except Exception:
                return False
        else:
            return False
    def format_output(self, result : str) -> str:
        return f"output {result}"

                
class LogProcessor(DataProcessor):
   pass


def test():
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    numbers = ["1", "2", "3", "4", "5"]

    print("Initializing numeric processor...")
    data = NumericProcessor(numbers)
    data.process(numbers)
    res = data.validate(numbers)
    if res == True:
        print("Validation: Numeric data verified")
    print(data.format_output())



if __name__ == '__main__':
    test()



    

    





# you cannot create objects directly from an abstract class

# the abstract method decorator means:
# - method has no code here
# - all sub classes will need to write the method