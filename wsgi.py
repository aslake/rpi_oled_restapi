"""
WSGI entrypoint for Gunicorn server.
"""

from server import app


if __name__ == "__main__":
    app.run()
