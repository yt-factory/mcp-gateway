import os
import time
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from ..schemas.youtube import PublishVideoInput, PublishVideoOutput
from ..services.auth_manager import PreemptiveAuthManager
from ..services.rate_limiter import RateLimiter
from ..utils.logger import logger

SHORTS_REQUIREMENTS = {
    "max_duration_seconds": 60,
    "aspect_ratio": "9:16",
    "min_resolution": (1080, 1920),
    "required_hashtag": "#Shorts",
    "hashtag_position": "description_first_line",
}


class YouTubePublisher:
    """YouTube video publishing service with resumable upload and Shorts support."""

    def __init__(self, auth_manager: PreemptiveAuthManager, rate_limiter: RateLimiter):
        self.auth = auth_manager
        self.rate_limiter = rate_limiter

    def _get_youtube_service(self, channel_id: Optional[str] = None):
        creds = self.auth._load_credentials("youtube", channel_id)
        return build("youtube", "v3", credentials=creds)

    async def publish_video(self, input_data: PublishVideoInput) -> PublishVideoOutput:
        start_time = time.time()
        file_size = os.path.getsize(input_data.video_path)

        await self.rate_limiter.acquire("youtube_upload")

        youtube = self._get_youtube_service(input_data.channel_id)

        try:
            description = self._prepare_description(input_data)

            body: dict = {
                "snippet": {
                    "title": input_data.title,
                    "description": description,
                    "tags": input_data.tags,
                    "categoryId": input_data.category_id,
                },
                "status": {
                    "privacyStatus": input_data.privacy.value,
                    "selfDeclaredMadeForKids": False,
                },
            }

            if input_data.scheduled_publish_time:
                body["status"]["publishAt"] = input_data.scheduled_publish_time.isoformat()
                body["status"]["privacyStatus"] = "private"

            if input_data.localized_metadata:
                body["localizations"] = {}
                for lang, meta in input_data.localized_metadata.items():
                    body["localizations"][lang] = {
                        "title": meta.get("title", input_data.title),
                        "description": meta.get("description", description),
                    }

            media = MediaFileUpload(
                input_data.video_path,
                mimetype="video/*",
                resumable=True,
                chunksize=1024 * 1024 * 10,
            )

            request = youtube.videos().insert(
                part="snippet,status,localizations",
                body=body,
                media_body=media,
            )

            video_id = await self._resumable_upload(request)

            if not video_id:
                return PublishVideoOutput(
                    success=False,
                    error="Upload failed after retries",
                    upload_duration_seconds=time.time() - start_time,
                    file_size_bytes=file_size,
                )

            thumbnail_set = False
            if input_data.thumbnail_path:
                thumbnail_set = await self._set_thumbnail(youtube, video_id, input_data.thumbnail_path)

            comment_posted = False
            comment_id = None
            if input_data.auto_comment:
                comment_id = await self._post_pinned_comment(youtube, video_id, input_data.auto_comment)
                comment_posted = comment_id is not None

            video_url = f"https://www.youtube.com/watch?v={video_id}"
            shorts_url = None
            if input_data.shorts_config and input_data.shorts_config.is_short:
                shorts_url = f"https://www.youtube.com/shorts/{video_id}"

            logger.info("Video published", video_id=video_id, is_short=bool(shorts_url))

            return PublishVideoOutput(
                success=True,
                video_id=video_id,
                video_url=video_url,
                shorts_url=shorts_url,
                thumbnail_set=thumbnail_set,
                comment_posted=comment_posted,
                comment_id=comment_id,
                upload_duration_seconds=time.time() - start_time,
                file_size_bytes=file_size,
            )

        except HttpError as e:
            logger.error("YouTube API error", error=str(e))
            return PublishVideoOutput(
                success=False,
                error=str(e),
                upload_duration_seconds=time.time() - start_time,
                file_size_bytes=file_size,
            )

    def _prepare_description(self, input_data: PublishVideoInput) -> str:
        parts = []
        if input_data.shorts_config and input_data.shorts_config.is_short:
            parts.append("#Shorts")
            parts.append("")

        parts.append(input_data.description)

        if input_data.chapters and not (input_data.shorts_config and input_data.shorts_config.is_short):
            parts.append("")
            parts.append("Chapters:")
            parts.append(input_data.chapters)

        if input_data.tags:
            parts.append("")
            hashtags = " ".join(f"#{tag.replace(' ', '')}" for tag in input_data.tags[:5])
            parts.append(hashtags)

        return "\n".join(parts)

    async def _resumable_upload(self, request) -> Optional[str]:
        response = None
        retry = 0
        max_retries = 10

        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    logger.debug("Upload progress", progress=f"{int(status.progress() * 100)}%")
                if response:
                    return response.get("id")
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    if retry < max_retries:
                        sleep_seconds = 2**retry
                        logger.warning("Upload error, retrying", retry=retry, sleep=sleep_seconds)
                        time.sleep(sleep_seconds)
                        retry += 1
                    else:
                        raise
                else:
                    raise
            except Exception:
                if retry < max_retries:
                    sleep_seconds = 2**retry
                    logger.warning("Network error, retrying", retry=retry, sleep=sleep_seconds)
                    time.sleep(sleep_seconds)
                    retry += 1
                else:
                    raise
        return None

    async def _set_thumbnail(self, youtube, video_id: str, thumbnail_path: str) -> bool:
        try:
            youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path)).execute()
            return True
        except HttpError as e:
            logger.error("Thumbnail set error", error=str(e))
            return False

    async def _post_pinned_comment(self, youtube, video_id: str, comment_text: str) -> Optional[str]:
        try:
            comment_response = (
                youtube.commentThreads()
                .insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "videoId": video_id,
                            "topLevelComment": {"snippet": {"textOriginal": comment_text}},
                        }
                    },
                )
                .execute()
            )
            comment_id = comment_response["id"]
            logger.info("Comment posted", comment_id=comment_id)
            return comment_id
        except HttpError as e:
            logger.error("Comment post error", error=str(e))
            return None
