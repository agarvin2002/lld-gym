# Exercise: Media Player Interfaces

## What You'll Build

A media player system with properly segregated interfaces — each player type only implements what it actually does.

## Interfaces to Define

### `VideoPlayable` (ABC)
- `play_video(source: str) -> None`
- `pause_video() -> None`
- `stop_video() -> None`

### `AudioPlayable` (ABC)
- `play_audio(source: str) -> None`
- `pause_audio() -> None`
- `stop_audio() -> None`

### `SpeedControllable` (ABC)
- `set_speed(speed: float) -> None` — e.g., 0.5x, 1.0x, 2.0x

### `Downloadable` (ABC)
- `download(url: str, destination: str) -> bool`

## Player Classes

| Player | Implements |
|--------|-----------|
| `BasicVideoPlayer` | `VideoPlayable` only |
| `PodcastPlayer` | `AudioPlayable` + `SpeedControllable` |
| `StreamingPlayer` | `VideoPlayable` + `AudioPlayable` |
| `MediaDownloader` | `Downloadable` only |

## Constraints
- `BasicVideoPlayer` must NOT have audio methods
- `PodcastPlayer` must NOT have video methods
- All interfaces must be ABCs

## Hints
1. Multiple inheritance: `class PodcastPlayer(AudioPlayable, SpeedControllable)`
2. Test using `isinstance()` checks to verify correct interface membership

## What You'll Practice
- Small, focused interfaces (ISP)
- Multiple interface inheritance
- Type checking via `isinstance()`
