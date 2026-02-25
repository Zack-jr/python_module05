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

    def process(self, data : Any)-> str:
        print(f"Processing data: {data}")
        count = len(data)
        numbers = (float(n) for n in data)
        total_sum = sum(numbers)
        avg = total_sum / count
        return f"Processed {count} numeric values, sum={total_sum}, avg={avg}"
    
    def validate(self, data : Any):
        if isinstance(data, List):
            count = 0
            total_sum = 0
            try:
                for e in data:
                    total_sum += int(e)
                    count += 1
                print("Validation: Numeric data verified")
                return True
            except Exception:
                return False
        else:
            return False

    def format_output(self, result : str) -> str:
        return f"Output: {result}"

                
class TextProcessor(DataProcessor):
   
    def process(self, data) -> str:
        try:
            print(f'Processing data: "{data}"')
            length = len(data)
            word_count = len(data.split(" "))
            return f"Processed text: {length} characters, {word_count} words"
        except Exception:
            return f"An error has been found."

    def validate(self, data : Any) -> bool:
        if isinstance(data, str):
            print("Validation: Text data verified")
            return True
        else:
            return False
    def format_output(self, result : str) -> str:
        return f"Output: {result}"

class   LogProcessor(DataProcessor):

    def process(self, data) -> str:
        print(f"processing data: {data}")

    def validate(self, data: Any) -> bool:
        return True
    def format_output(self, result: str) -> str:
        return f"Output: {result}"
    

def test():
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    numbers = ["1", "2", "3", "4", "5"]

    print("Initializing Numeric Processor...")
    data = NumericProcessor(numbers)
    result = data.process(numbers)
    data.validate(numbers)
    print(data.format_output(result))


    print("\nInitializing Text Processor...")
    text = "This subject is not so good"
    data2 = TextProcessor(text)
    result2 = data2.process(text)
    data2.validate(text)
    print(data2.format_output(result2))


    print("\nInitializing Log Processor...")
    data3 = LogProcessor()
    result3 = data3.process(error)
    data3.validate(error)
    print(data3.format_output(result3))


if __name__ == '__main__':
    test()



    

    





# you cannot create objects directly from an abstract class

# the abstract method decorator means:
# - method has no code here
# - all sub classes will need to write the method