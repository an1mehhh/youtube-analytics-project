import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    API_KEY = os.getenv("API_KEY")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # id канала
        self.__channel_id = channel_id
        # название канала
        self.title = \
            self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()["items"][0][
                "snippet"]["title"]
        # описание канала
        self.channel_description = \
            self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()["items"][0][
                "snippet"][
                "description"]
        # ссылка на канал
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        # количество подписчиков
        self.subscriber_count = \
            self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()["items"][0][
                "statistics"][
                "subscriberCount"]
        # количество видео
        self.video_count = \
            self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()["items"][0][
                "statistics"][
                "videoCount"]
        # количество просмотров
        self.view_count = \
            self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()["items"][0][
                "statistics"][
                "viewCount"]


    @property
    def channel_id(self):
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        data = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "channel_description": self.channel_description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(filename, "w") as f:
            f.write(json.dumps(data))
