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

    def __init__(self, is_file):
        self.BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
        self.IS_FILE = speech_recog.AudioFile(self.BASE_DIR + is_file)

    def _get_content(self):
        with self.IS_FILE as audio_file:
            audio_content = recog().record(audio_file)

        return audio_content

    def get_data(self) -> str:
        return recog().recognize_google(self._get_content(), language='ru-RU')


class VideoConvertor:
    """
        class for converting format from video to audio
        example to use:
            audio = VideoConvertor('test.mp4').to_convert(0, 21)
    """

    def __init__(self, video_file):
        self.video = mp.VideoFileClip(video_file)

    def _take_len(self, start: int, end: int):
        return self.video.subclip(start, end)

    def to_convert(self, start: int, end: int) -> str:
        audio = str(random.randint(1, 1000000000))
        self._take_len(start, end).audio.write_audiofile(
            "{}.wav".format(audio)
        )
        return audio
