# backend/routers/chat.py

from fastapi import APIRouter, HTTPException, status, Depends
from models.models import ChatMessage
from typing import List
import datetime


from .bot_logic import get_final_response

async def get_db_instance():
    from main import client
    if client is None:
        raise HTTPException(status_code=503, detail="Database client not initialized.")
    return client["chatbotdb"] 

router = APIRouter(
    tags=["Chat"],
    responses={404: {"description": "Not found"}}
)

@router.post("/chat/send", response_model=ChatMessage, status_code=status.HTTP_201_CREATED)
async def send_chat_message(message_payload: ChatMessage, db_instance = Depends(get_db_instance)):
    """
    Receives a user's message, saves it with a corrected server-side UTC timestamp,
    gets a response from bot_logic, saves the bot's response, and returns it.
    """
    try:
        # 1. Prepare user message for DB with a fresh server timestamp.
        # This is the key fix from your code to ensure correct chronological order.
        user_message_data_for_db = {
            "user_id": message_payload.user_id,
            "message": message_payload.message,
            "sender": "user",
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
        }
        await db_instance.messages.insert_one(user_message_data_for_db)

        # 2. Get the response by calling your friend's clean logic function.
        bot_response_text = get_final_response(message_payload.message)
        
        # 3. Save the bot's response.
        bot_message_obj = ChatMessage(
            user_id=message_payload.user_id,
            message=bot_response_text,
            sender="bot",
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        bot_message_dict = bot_message_obj.dict(by_alias=True, exclude_none=True)
        if 'id' in bot_message_dict: del bot_message_dict['id']
        bot_insert_result = await db_instance.messages.insert_one(bot_message_dict)
        
        # 4. Return the response to the frontend.
        final_bot_message_from_db = await db_instance.messages.find_one({"_id": bot_insert_result.inserted_id})
        
        if not final_bot_message_from_db:
             raise HTTPException(status_code=500, detail="Failed to retrieve saved bot message.")
        
        final_bot_message_from_db['_id'] = str(final_bot_message_from_db['_id'])
        return ChatMessage(**final_bot_message_from_db)

    except Exception as e:
        print(f"An unexpected error occurred in send_chat_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{user_id}", response_model=List[ChatMessage])
async def get_chat_history(user_id: str, db_instance=Depends(get_db_instance)):
    """
    Retrieves the chat history for a given user ID, ordered by timestamp.
    """
    try:
        messages_cursor = db_instance.messages.find({"user_id": user_id}).sort("timestamp", 1)
        history = await messages_cursor.to_list(length=1000)
        
        # Convert _id (ObjectId) to str before creating ChatMessage model
        for msg in history:
            if "_id" in msg:
                msg["_id"] = str(msg["_id"])
        
        return [ChatMessage(**msg) for msg in history]
    except Exception as e:
        print(f"Error retrieving chat history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chat history: {str(e)}")

# ADD THIS NEW FUNCTION FROM YOUR CODE
@router.delete("/chat/history/{user_id}", status_code=status.HTTP_200_OK)
async def delete_chat_history(user_id: str, db_instance = Depends(get_db_instance)):
    """
    Deletes all chat messages for a given user ID.
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID cannot be empty.")

        delete_result = await db_instance.messages.delete_many({"user_id": user_id})

        if delete_result.deleted_count > 0:
            return {"message": f"Successfully deleted {delete_result.deleted_count} messages for user '{user_id}'."}
        else:
            return {"message": f"No messages found to delete for user '{user_id}'."}
            
    except Exception as e:
        print(f"Error deleting chat history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete chat history: {str(e)}")

