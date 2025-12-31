class State:
    def __init__(self):
        self._subscribers = set()

    def subscribe(self, subscriber):
        self._subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self._subscribers.discard(subscriber)

    def notify(self):
        for subscriber in list(self._subscribers):
            subscriber.invalidate()
