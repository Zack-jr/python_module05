from abc import ABC, abstractmethod
from typing import Protocol, Any, Dict, Union, List


class NexusManager():

    def __init__(self):
        self.pipelines = []

    def add_pipeline(self, pipeline : List):
        self.pipelines.append(pipeline)

    def process_data(data : Any) -> Any:
        pass


# STAGES --------------------------------

class ProcessingStage(Protocol):
    def process(data: Any) -> Union[str, Any]:
        pass


class InputStage():

    def process(self, data: Any) -> Dict:
        """takes the input"""

        # if it's a dict
        if isinstance(data, dict):
            return data

        # if it's a string
        if isinstance(data, str):
            tokens = data.split(",")
            res = {i: key for i, key in enumerate(tokens)}
            return res
    
        # if it's a list
        if isinstance(data, list):
            return {"count": len(data), "readings": data}
        
        # if it's a number
        if isinstance(data, (int, float)):
            return {"sensor_value": data}

        return {"raw": data}


    


class TransformStage():

    def process(self, data: Any) -> Dict:
        """transforms the input"""

        # json
        if "sensor" in data and "value" in data:
            value = data["value"]
            if value < 0:
                status = "low"
            elif value > 30:
                status = "high"
            else:
                status = "normal"
            data["status"] = status
            return data

        # csv
        if 0 in data:
            actions = len(data)
            return {"type": "user_activity", "actions": actions}

        # sensor readings
        if "readings" in data:
            readings = data["readings"]
            avg = sum(readings) / len(readings)
            data["avg"] = round(avg, 1)
            return data
    
    

class OutputStage():

    def process(self, data: Any) -> str:
        """prepares the output"""

        # JSON sensor output
        if "sensor" in data and "value" in data:
            return f"Processed temperature reading: {data['value']}°C ({data['status']})"

        # CSV output
        if "type" in data:
            return f"User activity logged: {data['actions']} actions processed"

        # Stream output
        if "avg" in data:
            return f"Stream summary: {data['count']} readings, avg: {data['avg']}°C"

        return "Output: Unknown data format"

# ADAPTERS -----------------------------------

class ProcessingPipeline(ABC):

    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)
    
    @abstractmethod
    def process(self, data : Any) -> Any:
        pass


class JSONAdapter(ProcessingPipeline):

    def __init__(self, pipeline_id):
        super().__init__()
        self.pipeline_id = pipeline_id


    def process(self, data: Any) -> Any:
        result = data
        for stage in self.stages:
            result = stage.process(result)
        print(f"Input: {data}")
        print("Transform: Enriched with metadata and validation")

        return result


class CSVAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id):
        super().__init__()
        self.pipeline_id = pipeline_id

    def process(self, data: Any) -> Any:
        result = data
        for stage in self.stages:
            result = stage.process(result)
        return result

class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id):
        super().__init__()
        self.pipeline_id = pipeline_id

    def process(self, data: Any) -> Any:
        result = data
        for stage in self.stages:
            result = stage.process(result)

        return result
#    ---------------------------------------

def main():
    print("=== CODE NEXUS -ENTERPRISE PIPELINE SYSTEM ===\n")

    print("Initializing NexusManager")
    NM = NexusManager()
    print("Pipeline capacity: 1000 streams/second\n")

    print("Creating Data Processing Pipeline...")
    pipeline1 = JSONAdapter("001")

    pipeline1.add_stage(InputStage())
    print("Stage 1: Input validation and parsing")

    pipeline1.add_stage(TransformStage())
    print("Stage 2: Data transformation and enrichment")

    pipeline1.add_stage(OutputStage())
    print("Stage 3: Output formatting and delivery\n")


    print("=== Multi-Format Data Processing ===\n")

    print("Processing JSON data through pipeline...")
    dict_input = {"sensor": "temp", "value": 23.5, "unit": "C"}
    pipeline1.process(dict_input)


    print("\n=== Pipeline Chaining Demo")


    print("\n=== Error Recovery Test ===")
    
if __name__ == '__main__':
    main()


# duck typing = a way to do polymorphism without inheritance (ex sharing same method names)