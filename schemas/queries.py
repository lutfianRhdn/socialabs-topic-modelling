import strawberry
from schemas.types import TopicByProjectResponse, TopicDocByProjectResponse
from models.topics import Topics

@strawberry.type
class Query:

    @strawberry.field
    def get_topic_by_project(self, projectId: str) -> TopicByProjectResponse:
        try:
            topic = Topics.getTopicByProjectId(projectId)
            return TopicByProjectResponse(
                status=200,
                message="Data Topics",
                data=topic
            )
        except Exception as e:
            raise Exception(str(e))

    @strawberry.field
    def get_document_topic_by_project(self, projectId: str, topic: str) -> TopicDocByProjectResponse:
        try:
            document_topic = Topics.getDocumentTopicByProjectId(projectId, topic)
            return TopicDocByProjectResponse(
                status=200,
                message="Data Documents",
                data=document_topic
            )
        except Exception as e:
            raise Exception(str(e))


