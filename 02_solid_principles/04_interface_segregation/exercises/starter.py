"""
Exercise: Media Player Interfaces (ISP)
Fill in the TODOs. Run: pytest tests.py -v
"""
from abc import ABC, abstractmethod


class VideoPlayable(ABC):
    @abstractmethod
    def play_video(self, source: str) -> None: ...

    @abstractmethod
    def pause_video(self) -> None: ...

    @abstractmethod
    def stop_video(self) -> None: ...


class AudioPlayable(ABC):
    @abstractmethod
    def play_audio(self, source: str) -> None: ...

    @abstractmethod
    def pause_audio(self) -> None: ...

    @abstractmethod
    def stop_audio(self) -> None: ...


class SpeedControllable(ABC):
    @abstractmethod
    def set_speed(self, speed: float) -> None: ...


class Downloadable(ABC):
    @abstractmethod
    def download(self, url: str, destination: str) -> bool: ...


class BasicVideoPlayer(VideoPlayable):
    """Only plays video. No audio, no download."""

    def play_video(self, source: str) -> None:
        # TODO: print f"Playing video: {source}"
        pass

    def pause_video(self) -> None:
        # TODO: print "Video paused"
        pass

    def stop_video(self) -> None:
        # TODO: print "Video stopped"
        pass


class PodcastPlayer(AudioPlayable, SpeedControllable):
    """Plays audio with speed control. No video."""

    def __init__(self) -> None:
        # TODO: store current_speed = 1.0
        pass

    def play_audio(self, source: str) -> None:
        # TODO: print f"Playing podcast at {self.current_speed}x: {source}"
        pass

    def pause_audio(self) -> None:
        # TODO: print "Podcast paused"
        pass

    def stop_audio(self) -> None:
        # TODO: print "Podcast stopped"
        pass

    def set_speed(self, speed: float) -> None:
        # TODO: set current_speed, print f"Speed set to {speed}x"
        pass


class StreamingPlayer(VideoPlayable, AudioPlayable):
    """Plays both video and audio. No download, no speed control."""

    def play_video(self, source: str) -> None:
        # TODO: print f"Streaming video: {source}"
        pass

    def pause_video(self) -> None:
        # TODO: print "Stream paused"
        pass

    def stop_video(self) -> None:
        # TODO: print "Stream stopped"
        pass

    def play_audio(self, source: str) -> None:
        # TODO: print f"Streaming audio: {source}"
        pass

    def pause_audio(self) -> None:
        # TODO: print "Audio stream paused"
        pass

    def stop_audio(self) -> None:
        # TODO: print "Audio stream stopped"
        pass


class MediaDownloader(Downloadable):
    """Downloads media. Does not play."""

    def download(self, url: str, destination: str) -> bool:
        # TODO: print f"Downloading {url} to {destination}", return True
        pass
