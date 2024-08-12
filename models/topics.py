from config.db import db1

class Topics:
    def createTopic(data):
        return db1.topics.insert_many(data)
    
    def createDocument(data):
        return db1.documents.insert_many(data)
    
    def createContext(data):
        return db1.context.insert_many(data)
    
    def getTopicByProjectId(projectId):
        topicProject =  db1.topics.find(
            {"projectId": projectId},
            {"_id": 0}
        )
        return list(topicProject)
    
    def getContextTopicByProjectId(projectId):
        contextTopic =  db1.topics.find(
            {"projectId": projectId},
            {"_id": 0, "context": 1, "topicId": 1, "keyword": 1}
        )
        return list(contextTopic)

    def getDocumentTopicByProjectId(projectId, topic=None):
        filter = {"projectId": projectId}
        if topic != None:
            filter["topic"] = topic
        
        documentTopic =  db1.documents.find(
            filter,
            {"_id": 0, "full_text": 1, "username": 1, "tweet_url": 1, "topic": 1}
        )
        return list(documentTopic)