import time
import redis
import socket
import requests
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis.internal-bookingapp.com', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            print("Exception occured while connecting redis")
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/home')
def hit():
    count = get_hit_count()
    response = requests.get("http://movie.internal-bookingapp.com:5000/movie")
    return "<html>Welcome to BookingApp - Home Page - on node %s.<br \>Hit count = %i.<br \>Response from movie.internal-bookingapp.com service: %s" % ( socket.gethostname(), int(count), response.content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
