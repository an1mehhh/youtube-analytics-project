import os
from googleapiclient.discovery import build


class Video:
    API_KEY = os.getenv("API_KEY")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id):
        self.__video_id = video_id
        self.name_video = \
            self.youtube.videos().list(part="snippet,statistics", id=self.__video_id).execute()["items"][0]["snippet"][
                "title"]
        self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
        self.view_count = \
            self.youtube.videos().list(part='snippet,statistics', id=self.__video_id, ).execute()["items"][0][
                "statistics"][
                "viewCount"]
        self.like_count = \
            self.youtube.videos().list(part='snippet,statistics', id=self.__video_id, ).execute()["items"][0][
                "statistics"][
                "likeCount"]

    def __str__(self):
        return f"{self.name_video}"


class PLVideo(Video):
    API_KEY = os.getenv("API_KEY")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__video_id = video_id
        self.name_video = self.name_video
        self.url = self.url
        self.view_count = self.view_count
        self.like_count = self.like_count
        self.__playlist_id = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                               part='snippet',
                                                               maxResults=50,
                                                               ).execute()["items"][0]["snippet"]["playlistId"]
