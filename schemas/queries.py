import strawberry
from schemas.types import TopicByProjectResponse, TopicDocByProjectResponse, TopicProject, TopicDocument
from models.topics import Topics

@strawberry.type
class Query:

    @strawberry.field
    def get_topic_by_project(self, projectId: str) -> TopicByProjectResponse:
        try:
            topics_data = Topics.getTopicByProjectId(projectId)

            topics = [TopicProject(**item) for item in topics_data]
            return TopicByProjectResponse(
                status=200,
                message="Data Topics",
                data=topics
            )
        except Exception as e:
            raise Exception(str(e))

    @strawberry.field
    def get_document_topic_by_project(self, projectId: str, topic: str) -> TopicDocByProjectResponse:
        try:
            document_topic_data = Topics.getDocumentTopicByProjectId(projectId, topic)

            documents = [TopicDocument(**item) for item in document_topic_data]
            return TopicDocByProjectResponse(
                status=200,
                message="Data Documents",
                data=documents
            )
        except Exception as e:
            raise Exception(str(e))


