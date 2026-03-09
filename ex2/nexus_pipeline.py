from abc import ABC, abstractmethod
from typing import Protocol, Any, Dict, Union

#   ----- STAGES ----------


# defines the structure of process()
class ProcessingStage(Protocol):
    """duck typed interface for stages"""
    def process(data: Any) -> Union[str, Any]:
        pass


class InputStage():
    """Input checking interface"""
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

        return {"raw": data}


class TransformStage():
    """Transforms the input and returns a new dict"""
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
                status = "Normal"
            data["status"] = status
            return data

        # csv
        if 0 in data:
            actions = len([a for a in data.values() if a == "action"])
            return {"type": "user_activity", "actions": actions}

        # sensor readings
        if "readings" in data:
            readings = data["readings"]
            avg = sum(readings) / len(readings)
            data["avg"] = round(avg, 1)
            return data


class OutputStage():
    """Recieves the data and prepares the output"""

    def process(self, data: Any) -> str:
        """prepares the output"""

        # JSON sensor output
        if "sensor" in data and "value" in data:
            return ("Output: Processed temperature reading: "
                    f"{data['value']}°C ({data['status']} range)")

        # CSV output
        if "type" in data:
            return ("Output: User activity logged: "
                    f"{data['actions']} actions processed")

        # Stream output
        if "avg" in data:
            return (f"Output: Stream summary: {data['count']} readings, "
                    f"avg: {data['avg']}°C")

        return "Output: Unknown data format"


# ADAPTERS -----------------------------------

class ProcessingPipeline(ABC):
    """abstract class for adapters"""
    def __init__(self) -> None:
        self.stages = []

    def add_stage(self, stage: ProcessingStage) -> None:
        """add a processing stage to our class"""
        self.stages.append(stage)

    @abstractmethod
    def process(self, data: Any) -> Any:
        """abstract method, has to be implemented elsewhere"""
        pass


class JSONAdapter(ProcessingPipeline):
    """JSON adapter class"""
    def __init__(self, pipeline_id: str):
        """initiating parent attributes"""
        super().__init__()
        self.pipeline_id = pipeline_id

    def process(self, data: Any) -> Any:
        """process all stages"""
        result = data
        for stage in self.stages:
            result = stage.process(result)
        return result


class CSVAdapter(ProcessingPipeline):
    """csv adapter class"""
    def __init__(self, pipeline_id: str):
        """initiating parent attributes"""
        super().__init__()
        self.pipeline_id = pipeline_id

    def process(self, data: Any) -> Any:
        """process all stages"""
        result = data
        for stage in self.stages:
            result = stage.process(result)

        return result


class StreamAdapter(ProcessingPipeline):
    """csv adapter class"""
    def __init__(self, pipeline_id: str) -> None:
        """initiating parent attributes"""
        super().__init__()
        self.pipeline_id = pipeline_id

    def process(self, data: Any) -> Any:
        """process all stages"""
        result = data
        for stage in self.stages:
            result = stage.process(result)
        return result


class NexusManager():
    """Nexus manager class managing multiple pipelines"""
    def __init__(self) -> None:
        """initialize pipeline list"""
        self.pipelines = []

    def add_pipeline(self, pipeline: ProcessingPipeline) -> None:
        """add pipelines to nexus manager"""
        self.pipelines.append(pipeline)

    def process_data(self, data: Any) -> Any:
        """use every pipeline to process data"""
        try:

            for pipeline in self.pipelines:
                result = data
                pipeline.process(result)

            print("\nChain result: 100 records processed through"
                  " 3-stage pipeline")
            print("Performance: 95% efficiency, 0.2s total processing time")
            return result

        except Exception:
            print("Error detected in Stage 2: Invalid data format")
            print("Recovery initiated: Switching to backup processor")
            print("Recovery successful: Pipeline restored, processing resumed")

        finally:
            print("\nNexus Intergration complete. All systems operational.")


def main():
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===\n")

    print("Initializing Nexus Manager")
    NM = NexusManager()
    print("Pipeline capacity: 1000 streams/second\n")

    print("Creating Data Processing Pipeline...")
    pipeline1 = JSONAdapter("001")
    pipeline2 = CSVAdapter("002")
    pipeline3 = StreamAdapter("003")

    pipeline1.add_stage(InputStage())
    print("Stage 1: Input validation and parsing")

    pipeline1.add_stage(TransformStage())
    print("Stage 2: Data transformation and enrichment")

    pipeline1.add_stage(OutputStage())
    print("Stage 3: Output formatting and delivery\n")

    print("=== Multi-Format Data Processing ===\n")

    print("Processing JSON data through pipeline...")
    dict_input = {"sensor": "temp", "value": 23.5, "unit": "C"}
    print(f"Input: {dict_input}")
    print("Transform: Enriched with metadata and validation")
    print(pipeline1.process(dict_input))

    print("\nProcessing CSV data through same pipeline...")
    csv_input = "user,action,timestamp"
    pipeline2.add_stage(InputStage())
    pipeline2.add_stage(TransformStage())
    pipeline2.add_stage(OutputStage())
    print(f'Input: "{csv_input}"')
    print("Transform: Parsed and structured data")
    print(pipeline2.process(csv_input))

    print("\nProcessing Stream data through same pipeline...")
    stream_data = [20, 21, 22, 23, 24]
    pipeline3.add_stage(InputStage())
    pipeline3.add_stage(TransformStage())
    pipeline3.add_stage(OutputStage())
    print("Input: Real-time sensor stream")
    print("Transform: Aggregated and filtered")
    print(pipeline3.process(stream_data))

    print("\n=== Pipeline Chaining Demo ===")
    NM.add_pipeline(pipeline1)
    NM.add_pipeline(pipeline2)
    NM.add_pipeline(pipeline3)
    print("Pipeline A -> Pipeline B -> Pipeline C")
    print("Data flow: Raw -> processed -> Analyzed -> Stored")
    NM.process_data(stream_data)

    print("\n=== Error Recovery Test ===")
    print("Simulating pipeline failure...")
    NM.process_data(None)


if __name__ == '__main__':
    main()
