# models/models.py
from pydantic import BaseModel, Field
from typing import Optional
import datetime
from bson import ObjectId # Import ObjectId for json_encoders

def default_utc_timestamp():
    return datetime.datetime.now(datetime.timezone.utc)

class ChatMessage(BaseModel):
    """
    Represents a single chat message in the conversation.
    """
    id: Optional[str] = Field(alias='_id', default=None)
    user_id: str = Field(..., min_length=1, max_length=50)
    message: str = Field(..., min_length=1)
    sender: str = Field(..., pattern="^(user|bot|dialogflow)$")
    timestamp: datetime.datetime = Field(default_factory=default_utc_timestamp) # <<< MODIFIED THIS LINE


    class Config:
        populate_by_name = True
        # CRUCIAL for Pydantic 1.x to handle ObjectId serialization to string
        json_encoders = {
            ObjectId: str
        }
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "message": "Hello, what is FinEasy?",
                "sender": "user"
            }
        }