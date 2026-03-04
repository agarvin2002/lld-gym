# Explanation: ISP Media Player

## The Split
Each capability is its own ABC. Classes combine only what they need:
```
BasicVideoPlayer(VideoPlayable)
PodcastPlayer(AudioPlayable, SpeedControllable)
StreamingPlayer(VideoPlayable, AudioPlayable)
MediaDownloader(Downloadable)
```

No class implements methods it doesn't actually support.

## Why This Matters
Code that needs a video player:
```python
def render_video(player: VideoPlayable, source: str):
    player.play_video(source)
```
This works with `BasicVideoPlayer` AND `StreamingPlayer` — two very different classes that share only `VideoPlayable`. Neither knows about the other.

## Python's Protocol Alternative
With `typing.Protocol`, you don't even need explicit inheritance:
```python
from typing import Protocol

class VideoPlayable(Protocol):
    def play_video(self, source: str) -> None: ...
```
Any class with a `play_video` method satisfies `VideoPlayable` automatically (structural subtyping).
