import time
import redis
import socket
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis.bookingapp.local.com', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/home')
def hit():
    count = get_hit_count()
    return "Welcome to BookingApp - Home Page - on node %s. This page has been hit %i times since deployment" % ( socket.gethostname(), int(count))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
