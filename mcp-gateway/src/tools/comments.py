from enum import Enum
from typing import List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel

from ..services.auth_manager import PreemptiveAuthManager
from ..utils.logger import logger


class CommentAction(str, Enum):
    POST = "post"
    PIN = "pin"
    REPLY = "reply"
    DELETE = "delete"
    HIDE = "hide"


class ManageCommentsInput(BaseModel):
    action: CommentAction
    video_id: str
    comment_text: Optional[str] = None
    reply_to_comment_id: Optional[str] = None
    comment_id: Optional[str] = None
    auto_reply_enabled: bool = False
    reply_templates: Optional[List[str]] = None


class CommentsService:
    """YouTube comment management service."""

    def __init__(self, auth_manager: PreemptiveAuthManager):
        self.auth = auth_manager

    def _get_youtube_service(self, channel_id: Optional[str] = None):
        creds = self.auth._load_credentials("youtube", channel_id)
        return build("youtube", "v3", credentials=creds)

    async def manage_comments(self, input_data: ManageCommentsInput) -> dict:
        youtube = self._get_youtube_service()
        try:
            if input_data.action == CommentAction.POST:
                return await self._post_comment(youtube, input_data.video_id, input_data.comment_text or "")
            elif input_data.action == CommentAction.REPLY:
                return await self._reply_to_comment(
                    youtube, input_data.reply_to_comment_id or "", input_data.comment_text or ""
                )
            elif input_data.action == CommentAction.DELETE:
                return await self._delete_comment(youtube, input_data.comment_id or "")
            elif input_data.action == CommentAction.HIDE:
                return await self._hide_comment(youtube, input_data.comment_id or "")
            else:
                return {"success": False, "error": "Unknown action"}
        except HttpError as e:
            logger.error("Comments API error", error=str(e))
            return {"success": False, "error": str(e)}

    async def _post_comment(self, youtube, video_id: str, text: str) -> dict:
        response = (
            youtube.commentThreads()
            .insert(
                part="snippet",
                body={"snippet": {"videoId": video_id, "topLevelComment": {"snippet": {"textOriginal": text}}}},
            )
            .execute()
        )
        return {"success": True, "comment_id": response["id"], "action": "posted"}

    async def _reply_to_comment(self, youtube, parent_id: str, text: str) -> dict:
        response = (
            youtube.comments()
            .insert(part="snippet", body={"snippet": {"parentId": parent_id, "textOriginal": text}})
            .execute()
        )
        return {"success": True, "comment_id": response["id"], "action": "replied"}

    async def _delete_comment(self, youtube, comment_id: str) -> dict:
        youtube.comments().delete(id=comment_id).execute()
        return {"success": True, "comment_id": comment_id, "action": "deleted"}

    async def _hide_comment(self, youtube, comment_id: str) -> dict:
        youtube.comments().setModerationStatus(id=comment_id, moderationStatus="heldForReview").execute()
        return {"success": True, "comment_id": comment_id, "action": "hidden"}
