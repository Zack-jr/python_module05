from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):

    def __init__(self, stream_id: str):
        self.data = None
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        return data_batch

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class TransactionStream(DataStream):
    
    def __init__(self, stream_id: str):
        super().__init__(stream_id)
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class EventStream(DataStream):

    def __init__(self, stream_id: str):
        super().__init__(stream_id)
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    
    def __init__(self, stream_id: str):
        super().__init__(stream_id)
        self.processed_count = 0
        self.total_temp = 0


    def process_batch(self, data_batch: List[Any]) -> str:
        print(f"Stream ID : {self.stream_id}, type: Environmental Data")
        try:
            for data in data_batch:
                prefix, suffix = data.split(":", 1)
                if prefix == "temp":
                    self.total_temp += float(suffix)
                self.processed_count += 1

        except ValueError:
            return ("Error!")
        return f"Processing sensor batch: [{data_batch[0]}, {data_batch[1]}, {data_batch[2]}]"
    

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        print()
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        if self.processed_count > 0:
            average = self.total_temp / self.processed_count
        else:
            average = self.total_temp
        sensor_dict = {"count": self.processed_count, "avg tmp": average}
        return sensor_dict



class StreamProcessor():

    def __init__(self, stream):
        self.stream = stream

    def run(self, stream):
        self.stream.process_batch()
        self.stream.filter_data()
        self.stream.get_stats()



def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    print("Initializing Sensor Stream...")
    batch = ['temp:22.5', 'humidity:65', 'pressure:1013', 'temp:12.2']

    stream1 = SensorStream("SENSOR_001")
    print(stream1.process_batch(batch))
    #stream1.filter_data(batch, "Environmental Data")


    print("Initializing Transaction Stream...")


    print("Initializing Event Stream")

if __name__ == '__main__':
    main()



# stream proces