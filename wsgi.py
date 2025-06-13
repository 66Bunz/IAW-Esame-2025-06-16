import logging
# pip install waitress
from waitress import serve
from app import app
from werkzeug.middleware.proxy_fix import ProxyFix

logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


if __name__ == "__main__":
    logging.info("Server starting up...")

    serve(app, host="0.0.0.0", port=5000, threads=4)
    logging.info("Server shutting down...")
