"""Tests for ISP Media Player exercise."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import (
    BasicVideoPlayer, PodcastPlayer, StreamingPlayer, MediaDownloader,
    VideoPlayable, AudioPlayable, SpeedControllable, Downloadable
)


class TestBasicVideoPlayer:
    def test_is_video_playable(self):
        assert isinstance(BasicVideoPlayer(), VideoPlayable)

    def test_is_not_audio_playable(self):
        assert not isinstance(BasicVideoPlayer(), AudioPlayable)

    def test_play_video_runs(self):
        BasicVideoPlayer().play_video("movie.mp4")

    def test_pause_video_runs(self):
        BasicVideoPlayer().pause_video()

    def test_stop_video_runs(self):
        BasicVideoPlayer().stop_video()


class TestPodcastPlayer:
    def test_is_audio_playable(self):
        assert isinstance(PodcastPlayer(), AudioPlayable)

    def test_is_speed_controllable(self):
        assert isinstance(PodcastPlayer(), SpeedControllable)

    def test_is_not_video_playable(self):
        assert not isinstance(PodcastPlayer(), VideoPlayable)

    def test_play_audio_runs(self):
        PodcastPlayer().play_audio("episode.mp3")

    def test_set_speed_updates_speed(self):
        p = PodcastPlayer()
        p.set_speed(1.5)
        assert p.current_speed == 1.5


class TestStreamingPlayer:
    def test_is_video_playable(self):
        assert isinstance(StreamingPlayer(), VideoPlayable)

    def test_is_audio_playable(self):
        assert isinstance(StreamingPlayer(), AudioPlayable)

    def test_is_not_downloadable(self):
        assert not isinstance(StreamingPlayer(), Downloadable)


class TestMediaDownloader:
    def test_is_downloadable(self):
        assert isinstance(MediaDownloader(), Downloadable)

    def test_is_not_playable(self):
        assert not isinstance(MediaDownloader(), VideoPlayable)
        assert not isinstance(MediaDownloader(), AudioPlayable)

    def test_download_returns_true(self):
        result = MediaDownloader().download("http://example.com/video.mp4", "/tmp/video.mp4")
        assert result is True
