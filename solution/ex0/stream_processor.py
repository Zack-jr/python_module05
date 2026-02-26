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
        count = len(data)
        numbers = (float(n) for n in data)
        total_sum = sum(numbers)
        avg = total_sum / count
        return f"Processed {count} numeric values, sum={total_sum}, avg={avg}"
    
    def validate(self, data : Any):
        if isinstance(data, List):
            for n in data:
                if isinstance(n, (float, int)) == False:
                    return False
            print("Validation: Numeric data verified")
            return True
        else:
            return False

    def format_output(self, result : str) -> str:
        return f"Output: {result}"

                
class TextProcessor(DataProcessor):
   
    def process(self, data) -> str:
        try:
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
        prefix_suffix = []
        prefix_suffix = data.split(":", 1)
        if prefix_suffix[0] == "ERROR":
            return f"[ALERT] ERROR level detected: {prefix_suffix[1]}"
        if prefix_suffix[0] == "INFO":
            return f"[INFO] INFO level detected: {prefix_suffix[1]}"
    
    def validate(self, data: Any) -> bool:
        logs = ["ERROR", "INFO"]
        for log in logs:
            if log in data:
                return True
        return False

    def format_output(self, result: str) -> str:
        return f"Output: {result}"
    

def test():
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    numbers = [1, 2, 3, 4, 5]

    print("Initializing Numeric Processor...")
    data = NumericProcessor(numbers)
    print(f'Processing data: "{numbers}"')
    result = data.process(numbers)
    data.validate(numbers)
    print(data.format_output(result))

    print("\nInitializing Text Processor...")
    text = "This subject is not so good"
    data = TextProcessor(text)
    print(f'Processing data: "{text}"')
    result = data.process(text)
    data.validate(text)
    print(data.format_output(result))

    print("\nInitializing Log Processor...")
    error = "ERROR: Connection timeout"
    data = LogProcessor(error)
    print(f'Processing data: "{error}"')
    result = data.process(error)
    data.validate(error)
    print(data.format_output(result))

    print("\n=== Polymorphic Processing demo ===")
    num = [1, 2, 3]
    data = NumericProcessor(num)
    print(f"Result 1: {data.process(num)}")

    str = "hello world!"
    data = TextProcessor(str)
    print(f"Result 2: {data.process(str)}")

    error = "INFO: System ready"
    data = LogProcessor(error)
    print(f"Result 3: {data.process(error)}")

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == '__main__':
    test()



    

    





# you cannot create objects directly from an abstract class

# the abstract method decorator means:
# - method has no code here
# - all sub classes will need to write the method