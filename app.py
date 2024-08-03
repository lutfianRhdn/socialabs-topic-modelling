from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import re
import json
from services.preprocessing import Preprocessing
from services.lda import Lda
from services.llm import Llm
from models.tweet import Tweet
from models.topics import Topics

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/topic")
def result():
    keyword = request.args.get('keyword')
    period = request.args.get('period').split(' - ')
    start_date = datetime.strptime(period[0], "%m/%d/%Y")
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = datetime.strptime(period[1], "%m/%d/%Y")
    end_date = end_date.strftime("%Y-%m-%d")
    num_tweets = int(request.args.get('num_tweets'))
    with_context = bool(request.args.get('with_context'))
    with_document = bool(request.args.get('with_document'))
    tweets = Tweet.getTweetByKeyword(keyword, start_date, end_date, num_tweets)

    dataTweetText = []
    dataTweet = []
    for tweet in tweets:
        del tweet['_id']
        dataTweet.append(tweet)
        dataTweetText.append(tweet['full_text'])

    data = Preprocessing(dataTweetText)
    data = data.get_data()
    lda = Lda()
    lda_model = lda.generateTopic(data)
    num_topics = lda_model.num_topics
    topics = lda_model.show_topics(log=False, formatted=False)

    topic_res = []
    for topic_id, topic in topics:
        topic_res.append([word for word, _ in topic])

    res = { 
        "status" : 200, 
        "message" : "Data Topics",
        "data": {
            "topic": topic_res
        }, 
    } 

    # if with_context:
    context = Llm.getContext(topics, keyword, num_topics, dataTweetText)
    res['data']['context'] = context

    print(num_topics)
    # if with_document:
    documents_prob = lda.document(dataTweet, data, lda_model, num_topics)
    res['data']['documents_topic'] = documents_prob

    # return render_template('result.html', context=context, topic=topic)
    return jsonify(res)

@app.route("/documents")
def documents():
    keyword = request.args.get('keyword')
    num_topics = 5
    num_tweets = 1000
    rgx = re.compile(f'.*{keyword}.*', re.IGNORECASE)
    cursor = Tweet.getTweetByKeyword(keyword=rgx, limit=num_tweets)

    dataForLda = [tweet['full_text'] for tweet in cursor]
    topics = Lda.documents(data=dataForLda, keyword=keyword, num_topics=num_topics)

    data = {
        "status": 200,
        "message": "Data Topics",
        "data": topics
    }

    return jsonify(data)

@app.route("/topic-by-project/<string:projectId>", methods=['GET'])
def get_topic_by_project(projectId):
    topic = Topics.getTopicByProjectId(projectId)
    data = {
        "status": 200,
        "message": "Data Topics",
        "data": topic
    }
    return jsonify(data)

def start_app():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    app_port = int(os.getenv('APP_PORT', 6000))
    app_debug = os.getenv('APP_DEBUG', 'True') == 'True'
    app.run(debug=app_debug, port=app_port, use_reloader=False)