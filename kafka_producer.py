from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9094')

for idx in range(10):
    # transform string message to byte
    msg = f'{idx}. Hello World'.encode()

    # send message
    future = producer.send('test', msg)
    result = future.get(timeout=10)
    print(result)

    time.sleep(5)