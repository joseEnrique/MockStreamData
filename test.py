import asyncio
from river import datasets

from MockStreamData.generator import RiverDatasetGenerator
from MockStreamData.operator import KafkaOperator


async def main():
    dataset = datasets.Bikes()  # River dataset

    # Example using KafkaOperator (the operator is optional)
    operator = KafkaOperator(topic='test_topic', kafka_server='localhost:9092')
    generator_with_operator = RiverDatasetGenerator(
        dataset,
        operator=operator,
        stream_period=0,
        item_per_iter=1000
    )

    print("Using operator:")
    async for batch in generator_with_operator:
        print("Processing batch:", batch)

    # Example without any operator (just generating data)
    generator_without_operator = RiverDatasetGenerator(
        dataset,
        operator=None,
        stream_period=0,
        item_per_iter=10
    )

    print("\nWithout operator (just generating):")
    async for batch in generator_without_operator:
        print("Processing batch:", batch)

    print (dataset.n_samples)
if __name__ == '__main__':
    asyncio.run(main())