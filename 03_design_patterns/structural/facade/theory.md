# Facade Pattern

## What is it?
A Facade is a single class that gives you a simple entry point into a set of complex
subsystems. Instead of calling five different services in the right order yourself,
you call one method on the Facade and it handles the coordination. The subsystems still
exist and do all the real work — the Facade just ties them together.

## Analogy
Booking a movie on BookMyShow: you tap "Pay Now" and behind the scenes it checks seat
availability, charges your Paytm wallet, emails a confirmation, and updates the theater's
inventory. You never call those systems individually — the app's checkout Facade does it.

## Minimal code
```python
class Lights:
    def dim(self): print("Lights dimmed")

class Projector:
    def on(self): print("Projector on")

class Sound:
    def set_volume(self, v): print(f"Volume {v}")

class HomeTheater:          # <-- the Facade
    def __init__(self, lights, projector, sound):
        self._lights, self._projector, self._sound = lights, projector, sound

    def watch_movie(self):
        self._lights.dim()
        self._projector.on()
        self._sound.set_volume(30)

theater = HomeTheater(Lights(), Projector(), Sound())
theater.watch_movie()       # one call, three subsystems coordinated
```

## Real-world uses
- Zomato's "Place Order" button coordinates inventory, payment, delivery assignment,
  and push notifications through a single backend Facade.
- A bank's mobile app exposes `transfer_funds()` which internally calls fraud detection,
  ledger debit/credit, and SMS notification services.
- AWS SDK methods like `s3.upload_file()` hide multi-part upload, retry logic, and
  checksum verification behind one call.

## One mistake
Putting business logic inside the Facade. The Facade should only delegate — every
`if/else` or calculation you write inside it belongs in one of the subsystems instead.
A Facade that grows its own logic becomes a hard-to-test God Object.

## What to do next
- See `examples/example1_home_theater.py` for a full six-subsystem demonstration.
- See `examples/example2_order_processing.py` for an e-commerce order Facade.
- Try `exercises/starter.py` — build a SmartHome Facade over four subsystems.
