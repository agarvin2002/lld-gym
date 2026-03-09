"""
WHAT YOU'RE BUILDING
====================
A media player system with four separate, focused interfaces.
Each player class implements only the interfaces it actually supports.

  BasicVideoPlayer   → VideoPlayable only (no audio, no download)
  PodcastPlayer      → AudioPlayable + SpeedControllable (no video)
  StreamingPlayer    → VideoPlayable + AudioPlayable (no download)
  MediaDownloader    → Downloadable only (no playback)

The tests check that each class is an instance of the right interfaces
and NOT an instance of the interfaces it doesn't support.

Fill in the TODOs below. Run the tests to verify your work.
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
        # TODO: Print f"Playing video: {source}"
        pass

    def pause_video(self) -> None:
        # TODO: Print "Video paused"
        pass

    def stop_video(self) -> None:
        # TODO: Print "Video stopped"
        pass


class PodcastPlayer(AudioPlayable, SpeedControllable):
    """Plays audio with speed control. No video."""

    def __init__(self) -> None:
        # TODO: Set self.current_speed = 1.0
        # HINT: This is the only class that needs state — the speed value.
        pass

    def play_audio(self, source: str) -> None:
        # TODO: Print f"Playing podcast at {self.current_speed}x: {source}"
        pass

    def pause_audio(self) -> None:
        # TODO: Print "Podcast paused"
        pass

    def stop_audio(self) -> None:
        # TODO: Print "Podcast stopped"
        pass

    def set_speed(self, speed: float) -> None:
        # TODO: Update self.current_speed = speed, then print f"Speed set to {speed}x"
        pass


class StreamingPlayer(VideoPlayable, AudioPlayable):
    """Plays both video and audio. No download, no speed control."""

    def play_video(self, source: str) -> None:
        # TODO: Print f"Streaming video: {source}"
        pass

    def pause_video(self) -> None:
        # TODO: Print "Stream paused"
        pass

    def stop_video(self) -> None:
        # TODO: Print "Stream stopped"
        pass

    def play_audio(self, source: str) -> None:
        # TODO: Print f"Streaming audio: {source}"
        pass

    def pause_audio(self) -> None:
        # TODO: Print "Audio stream paused"
        pass

    def stop_audio(self) -> None:
        # TODO: Print "Audio stream stopped"
        pass


class MediaDownloader(Downloadable):
    """Downloads media. Does not play."""

    def download(self, url: str, destination: str) -> bool:
        # TODO: Print f"Downloading {url} to {destination}" and return True
        pass


# =============================================================================
# HOW TO RUN TESTS
# =============================================================================
# Step 1 — set up the test runner (only needed once):
#   python3 -m venv /tmp/lld_venv && /tmp/lld_venv/bin/pip install pytest -q
#
# Step 2 — run the tests for this exercise:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/04_interface_segregation/exercises/tests.py -v
#
# Run all SOLID exercises at once:
#   /tmp/lld_venv/bin/pytest 02_solid_principles/ -v
# =============================================================================
