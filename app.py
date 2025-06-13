import os
from datetime import datetime, timedelta

from flask import Flask
from flask_login import LoginManager

from utils import users_dao
from utils.logger import get_logger, setup_logger
from utils.models import User

setup_logger()
logger = get_logger()

from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.performances import performances_bp
from blueprints.profile import profile_bp
from blueprints.tickets import tickets_bp

logger.info("Avvio dell'applicazione Sonosphere")

app = Flask(__name__)
app.config["SECRET_KEY"] = "O*nY)jDH92t1g2K"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=30)
app.config["REMEMBER_COOKIE_SECURE"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(performances_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(tickets_bp)

login_manager = LoginManager()
login_manager.init_app(app)


# Funzione da usare in Jinja per formattare in un modo specifico le date
@app.template_filter("strfdate")
def _filter_date(date, fmt=None):
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime(fmt or "%d %B %Y")


# Funzione da usare in Jinja per formattare in un modo specifico la data e ora
@app.template_filter("strfdatetime")
def _filter_datetime(dt, fmt=None):
    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return dt.strftime(fmt or "%d %B %Y %H:%M")


@login_manager.user_loader
def load_user(user_id):
    db_user = users_dao.get_user_by_id(user_id)

    if not db_user:
        return None

    user = User(
        id=db_user["id"],
        username=db_user["username"],
        password=db_user["password"],
        name=db_user["name"],
        surname=db_user["surname"],
        email=db_user["email"],
        pfp=db_user["pfp"],
        role=db_user["role"],
    )
    return user


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
