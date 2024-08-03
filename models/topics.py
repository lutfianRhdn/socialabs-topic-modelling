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