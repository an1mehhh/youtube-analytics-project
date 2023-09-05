from datetime import timedelta
import isodate
import os
from googleapiclient.discovery import build


class PlayList:
    API_KEY = os.getenv("API_KEY")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id):
        """
        иницилизация переменных
        """
        item = self._get_playlist_item(playlist_id)
        self.title = item['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

        self._video_ids = self._get_playlist_video_ids(playlist_id)
        self._video_items = self.__get_video_items(*self._video_ids)

    def _get_playlist_item(self, playlist_id):
        """получение элементов плейлиста"""
        res = self.youtube.playlists().list(id=playlist_id, part='snippet').execute()
        return res['items'][0]

    @property
    def total_duration(self):
        """
        суммарная длительность плейлиста
        """
        total_duration = timedelta()
        for video in self._video_items:
            duration = self.__get_video_item_duration(video)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """
        самое популярное видео
        """
        best_video_id = None
        max_like_count = 0

        for video in self._video_items:
            like_count = int(video['statistics']['likeCount'])
            if like_count >= max_like_count:
                max_like_count = like_count
                best_video_id = video['id']

        return f'https://youtu.be/{best_video_id}' if best_video_id else None

    def _get_playlist_video_ids(self, playlist_id):
        """
        получение id видео
        """
        res = self.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails').execute()

        return (video['contentDetails']['videoId'] for video in res['items'])

    def __get_video_items(self, *video_ids):
        """
        получение элементов видео
        """
        res = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

        return res['items']

    @staticmethod
    def __get_video_item_duration(video_item):
        """
        длительность видео
        """
        duration = video_item['contentDetails']['duration']
        return isodate.parse_duration(duration)
