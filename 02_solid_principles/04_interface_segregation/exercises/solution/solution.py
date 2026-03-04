"""Solution: Media Player Interfaces (ISP)"""
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
    def play_video(self, source: str) -> None:
        print(f"Playing video: {source}")

    def pause_video(self) -> None:
        print("Video paused")

    def stop_video(self) -> None:
        print("Video stopped")


class PodcastPlayer(AudioPlayable, SpeedControllable):
    def __init__(self) -> None:
        self.current_speed: float = 1.0

    def play_audio(self, source: str) -> None:
        print(f"Playing podcast at {self.current_speed}x: {source}")

    def pause_audio(self) -> None:
        print("Podcast paused")

    def stop_audio(self) -> None:
        print("Podcast stopped")

    def set_speed(self, speed: float) -> None:
        self.current_speed = speed
        print(f"Speed set to {speed}x")


class StreamingPlayer(VideoPlayable, AudioPlayable):
    def play_video(self, source: str) -> None:
        print(f"Streaming video: {source}")

    def pause_video(self) -> None:
        print("Stream paused")

    def stop_video(self) -> None:
        print("Stream stopped")

    def play_audio(self, source: str) -> None:
        print(f"Streaming audio: {source}")

    def pause_audio(self) -> None:
        print("Audio stream paused")

    def stop_audio(self) -> None:
        print("Audio stream stopped")


class MediaDownloader(Downloadable):
    def download(self, url: str, destination: str) -> bool:
        print(f"Downloading {url} to {destination}")
        return True
