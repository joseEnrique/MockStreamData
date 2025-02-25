# MockStreamData
MockStreamData is a Python tool designed to stress-test online machine 
learning models by continuously streaming data. It simulates real-time data flows by 
generating batches from popular datasets (such as any of River's dataset) so you can evaluate your models' 
performance and capacity under load.

## Features

- **Stress Testing for Online Machine Learning Models:** Stream data continuously to challenge and evaluate the capacity of online machine learning models.
- **Batch Data Streaming:** Splits datasets into manageable batches to simulate a high-volume data stream.
- **Optional Data Transmission:** Choose to simply generate the data or send each batch to external systems (like Kafka) for further processing.

## Installation

1. Clone the repository.
2. Set up a virtual environment.
3. Install the required packages via `pip install -r requirements.txt`

## Usage
Below is an example of how to use MockStreamData with River's Phishing dataset:

```python
import asyncio
from river import datasets
from mockstreamdata.generator import RiverDatasetGenerator
from mockstreamdata.operators.kafka_operator import KafkaOperator  # Optional: only if you want to send data to Kafka

async def main():
    # Load a River dataset (e.g., Phishing) for stress testing.
    dataset = datasets.Phishing()

    operator = KafkaOperator(topic='test_topic', kafka_server='localhost:9092')
    generator = RiverDatasetGenerator(dataset, operator=operator, stream_period=1, item_per_iter=10)

    async for batch in generator:
        print("Processing batch:", batch)

if __name__ == '__main__':
    asyncio.run(main())
```

This tool helps you put your online machine learning models under stress by simulating a high-speed data stream. Enjoy testing your models’ capacity!

## License

This project is licensed under the MIT License.