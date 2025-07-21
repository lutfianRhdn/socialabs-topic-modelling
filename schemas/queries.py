import strawberry
from typing import Optional
from schemas.types import TopicResponse, TopicDocResponse, TopicProject, TopicDocument
from models.topics import Topics

@strawberry.type
class Query:

    @strawberry.field
    def get_topic_by_project(self, projectId: str) -> TopicResponse:
        try:
            topics_data = Topics.getTopicByProjectId(projectId)

            topics = [TopicProject(**item) for item in topics_data]
            return TopicResponse(
                status=200,
                message="Data Topics",
                data=topics
            )
        except Exception as e:
            raise Exception(str(e))

    @strawberry.field
    def get_document_topic_by_project(self, projectId: str, topic: Optional[str] = None) -> TopicDocResponse:
        try:
            document_topic_data = Topics.getDocumentTopicByProjectId(projectId, topic)

            documents = [TopicDocument(**item) for item in document_topic_data]
            return TopicDocResponse(
                status=200,
                message="Data Documents",
                data=documents
            )
        except Exception as e:
            raise Exception(str(e))


