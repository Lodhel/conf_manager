import os
import random

import speech_recognition as speech_recog
from speech_recognition import Recognizer as recog

import moviepy.editor as mp


class SoundMixin:
    """
        class for return text from audio file
        example to use:
            result = SoundMixin('/{}.wav'.format(audio)).get_data()
    """

    def __init__(self):
        self.BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def _get_content(audio_file):
        with audio_file as audio_file:
            audio_content = recog().record(audio_file)

        return audio_content

    def get_data(self, audio_file) -> str:
        return recog().recognize_google(self._get_content(audio_file), language='ru-RU')


class VideoConvertor:
    """
        class for converting format from video to audio
        example to use:
            audio = VideoConvertor('test.mp4').to_convert(0, 21)
    """

    def __init__(self, video_file):
        self.BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
        self.video = mp.VideoFileClip(video_file)

    def _take_len(self, start: int):
        return self.video.subclip(start)

    def to_convert(self, start: int) -> str:
        audio = str(random.randint(1, 1000000000))
        self._take_len(start).audio.write_audiofile(
            "{}.wav".format(audio)
        )
        return audio


class MainManager(VideoConvertor, SoundMixin):

    def get_text_from_video(self):
        audio = self.to_convert(0)
        return self.get_data(speech_recog.AudioFile(self.BASE_DIR + '/{}.wav'.format(audio)))
