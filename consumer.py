import pika
import json
from services.preprocessing import Preprocessing
from services.lda import Lda
from services.llm import Llm
from models.tweet import Tweet
from models.topics import Topics

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
        num_topics = lda_model.num_topics
        topics = lda_model.show_topics(log=False, formatted=False)
        documents_prob = lda.document(dataTweet, data, lda_model, num_topics)

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

        Topics.createTopic(topic_res)
        Topics.createDocument(documents_prob)

        topicModellingProduce = {
            "projectId": projectId,
            "tweetId": tweetId,
        }
        publish_message(topicModellingProduce)
    except Exception as e:
        print(f"Error processing topic modeling: {e}")

def consumer():
    connection = pika.BlockingConnection(
        pika.URLParameters("amqps://socialabs:Code@labs011013@b-c64d820c-55be-4d28-a9ca-e3a45d7a1873.mq.ap-southeast-1.amazonaws.com:5671")
    )
    channel = connection.channel()

    channel.queue_declare(queue="dataGatheringQueue", durable=True)

    def callback(ch, method, properties, body):
        try:
            tweet = json.loads(body.decode('utf-8'))
            topicModelling(tweet)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error consuming message: {e}")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="dataGatheringQueue",
        on_message_callback=callback,
        auto_ack=False,
    )

    print("Waiting for messages. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer interrupted. Closing connection.")
    finally:
        connection.close()

def publish_message(tweet):
    connection = pika.BlockingConnection(
        pika.URLParameters("amqps://socialabs:Code@labs011013@b-c64d820c-55be-4d28-a9ca-e3a45d7a1873.mq.ap-southeast-1.amazonaws.com:5671")
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

def start_consumer():
    consumer()
