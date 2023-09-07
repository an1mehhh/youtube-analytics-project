import os
from googleapiclient.discovery import build


class Video:
    API_KEY = os.getenv("API_KEY")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id):
        self.__video_id = video_id

        if item := self._err(self.__video_id):
            self.title = item['snippet']['title']
            self.view_count = int(item['statistics']['viewCount'])
            self.like_count = int(item['statistics']['likeCount'])
            self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
        else:
            self.title = self.view_count = self.like_count = self.url = None

    def __str__(self):
        return f"{self.title}"

    @property
    def video_id(self):
        return self.__video_id

    def _err(self, video_id):
        try:
            return self.youtube.videos().list(id=video_id, part="snippet,statistics").execute()["items"][0]
        except (IndexError, ValueError):
            print('Please check your video ID')


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
