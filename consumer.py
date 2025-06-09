import pika
import json
import logging
import os
from services.preprocessing import Preprocessing
from services.lda import Lda
from services.llm import Llm
from models.tweet import Tweet
from models.topics import Topics
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=100)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def consumer():
    connection_params = pika.URLParameters(os.getenv("RABBITMQ_URL"))
    
    try:
        with pika.BlockingConnection(connection_params) as connection:
            channel = connection.channel()

            # Ensure the queue exists
            channel.queue_declare(queue="dataGatheringQueue", durable=True)

            def callback(ch, method, properties, body):
                try:
                    tweet = json.loads(body.decode('utf-8'))
                    executor.submit(topicModelling, tweet)

                    # topicModelling(tweet)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decoding error: {e}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                except Exception as e:
                    logging.error(f"Error consuming message: {e}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            channel.basic_qos(prefetch_count=0)
            channel.basic_consume(queue="dataGatheringQueue", on_message_callback=callback, auto_ack=False)

            logging.info("Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()

    except KeyboardInterrupt:
        logging.info("Consumer interrupted. Closing connection.")
    except Exception as e:
        logging.error(f"Error in consumer: {e}")

def topicModelling(dataGatheringQueue):
    try:
        tweetId = dataGatheringQueue['tweetId']
        projectId = dataGatheringQueue['projectId']
        keyword = dataGatheringQueue['keyword']

        tweets_cursor = Tweet.getTweetByIdStr(tweetId)

        dataTweet = []
        dataForLda = []

        for tweet in tweets_cursor:
            tweet_with_project_id = {
                **tweet,
                "projectId": projectId,
            }
            dataTweet.append(tweet_with_project_id)
            dataForLda.append(tweet['full_text'])

        data = Preprocessing(dataForLda).get_data()
        lda = Lda()
        lda_model = lda.generateTopic(data)
        topics = lda_model.show_topics(log=False, formatted=False)
        documents_prob = lda.document(dataTweet, data, lda_model)

        topic_res = []
        for topic_id, topic in topics:
            words = [word for word, _ in topic]
            context = Llm.getContextByTopics(words, keyword)
            topic_dict = {
                "topicId": topic_id,
                "projectId": dataGatheringQueue['projectId'],
                "context": context,
                "words": words
            }
            topic_res.append(topic_dict)


        documents_prob_id = [ doc['id_str'] for doc in documents_prob]
        project_documents = [ {**doc, "projectId": projectId} for doc in documents_prob]

        Topics.createTopic(topic_res)
        Topics.createDocument(project_documents)

        topicModellingProduce = {
            "projectId": projectId,
            "tweetId": documents_prob_id,
        }

        publish_message(topicModellingProduce)
        produceProjectStatusQueue(projectId)
        
    except Exception as e:
        print(f"Error processing topic modeling: {e}")


def publish_message(tweet):
    connection = pika.BlockingConnection(
        pika.URLParameters(os.getenv("RABBITMQ_URL"))
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="topicExchange", exchange_type="fanout", durable=True)

    channel.basic_publish(
        exchange="topicExchange",
        routing_key="",
        body=json.dumps(tweet),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

def produceProjectStatusQueue(projectId):
    connection = pika.BlockingConnection(
            pika.URLParameters(os.getenv("RABBITMQ_URL"))
        )
    channel = connection.channel()

    header = {
        "projectId": projectId,
    }
    
    payload = {
        "topic_modelling": True
    }
    print("Project Status Queue Sent with header: ", header, "\n and payload: ", payload)
    
    channel.queue_declare(queue="projectStatusQueue", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="projectStatusQueue",
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            headers=header,
            delivery_mode=2,
        ),
    )
    print("Project Status Queue Sent to Project ID: ", projectId)
    connection.close()

def start_consumer():
    consumer()