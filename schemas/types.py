import strawberry
from typing import List, Optional
from strawberry.scalars import JSON
from dataclasses import dataclass

@strawberry.type
class TopicDocument:
    full_text: str
    topic: str
    tweet_url: str
    username: str

@strawberry.type
@dataclass
class TopicDocResponse:
    data: List[TopicDocument]
    message: str
    status: int


@strawberry.type
class TopicProject:
    context: str
    keyword: str
    projectId: str
    topicId: int
    words: List[str]

@strawberry.type
class TopicResponse:
    data: List[TopicProject]
    message: str
    status: int


