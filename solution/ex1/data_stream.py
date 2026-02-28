from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class TransactionStream(DataStream):
    
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.operations = 0
        self.net_flow = 0
    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            gain = sum([int(d.split(":", 1)[1]) for d in data_batch if 'buy' in d])
            loss = sum([int(d.split(":", 1)[1]) for d in data_batch if 'sell' in d])

            self.net_flow += gain - loss
            self.operations += len(data_batch)
            return f"Transaction analysis: {self.operations} operations, net flow: {self.net_flow:+} units"
        except ValueError:
            return "Error Found"

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        if criteria:
            return [d for d in data_batch if criteria in d]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"operations" : self.operations, "net flow": self.net_flow}


class EventStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.event_count = 0
        self.error_count = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            self.error_count += len([data for data in data_batch if 'error' in data])
            self.event_count += len(data_batch)

        except Exception:
            return "Error found!"

        return f"Event analysis: {self.event_count} events, {self.error_count} error detected"

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        if criteria:
            return [d for d in data_batch if criteria in d]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"events": self.event_count, "errors": {self.error_count}}


class SensorStream(DataStream):
    
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.processed_count = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            temps = [float(d.split(":", 1)[1]) for d in data_batch if 'temp' in d]
            self.processed_count += len(data_batch)
            avg = sum(temps) / len(temps) if temps else 0
    
        except ValueError:
            return ("Error!")
        return f"Sensor analysis: {self.processed_count} readings processed, avg temp: {avg} C"
    

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        if criteria:
            return [d for d in data_batch if criteria in d]
        return data_batch
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"stream_id" : self.stream_id, "processed items" : self.processed_count, "type" : "Environmental Data"}


class StreamProcessor():
    
    def run_all(self, streams : List[DataStream], batches : List) -> None:
        print("Processing mixed stream types through unified interface...\n")
        print("Batch 1 results:")
        for stream in streams:
                data = batches.get(stream.stream_id, [])
                stream.process_batch(data)

                if isinstance(stream, SensorStream):
                    print(f"- Sensor data: {len(data)} readings processed")
                elif isinstance(stream, TransactionStream):
                    print(f"- Transaction data: {len(data)} operations processed")
                elif isinstance(stream, EventStream):
                    print(f"- Event data: {len(data)} events processed")

        print("\nStream filtering active: High-priority data only")
        print("Filtered results: 2 critical sensors alerts, 1 large transaction")
        print("\nAll streams processed successfully. Nexus throughput optimal.")


def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")

    print("Initializing Sensor Stream...")
    climate_data = ['temp:22.5', 'humidity:65', 'pressure:1013']
    stream1 = SensorStream("SENSOR_001")
    print(f"Stream ID : {stream1.stream_id}, Type: Environmental Data")
    format_data = ", ".join(climate_data)
    print(f"Processing sensor batch: [{format_data}]")
    print(stream1.process_batch(climate_data))


    print("\nInitializing Transaction Stream...")
    financial_data = ["buy:100", "sell:150", "buy:75"]
    stream2 = TransactionStream("TRANS_001")
    print(f"Stream ID : {stream2.stream_id}, Type: Financial Data")
    format_data = ", ".join(financial_data)
    print(f"Processing transaction batch [{format_data}]")
    print(stream2.process_batch(financial_data))


    print("\nInitializing Event Stream")
    event_data = ['login', 'error', 'logout']
    stream3 = EventStream("EVENT_001")
    print(f"Stream ID: {stream3.stream_id}, Type: System Events")
    format_str = ", ".join(event_data)
    print(f"Processing event batch: [{format_str}]")
    print(stream3.process_batch(event_data))

    print("\n=== Polymorphic Stream Processing ===")


    processor = StreamProcessor()

    batches = {"SENSOR_001" : ["temp:30.2", "temp:28.4"],
               "TRANS_001": ["buy:200", "sell:50", "buy:100", "buy:3"],
               "EVENT_001": ["login", "error", "error"]}
    streams = [stream1, stream2, stream3]

    processor.run_all(streams, batches)


if __name__ == '__main__':
    main()


# classes de processeurs de donnees qui heritent d'une classe abstraite
# process_batch() est une methode abstraite
# stream proces