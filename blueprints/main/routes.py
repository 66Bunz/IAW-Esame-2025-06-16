from flask import render_template

from utils import event_days_dao, performances_dao, stages_dao, genres_dao
from utils.logger import get_logger

logger = get_logger()
from blueprints.main import main_bp


@main_bp.route("/")
def home():
    featured_performances = performances_dao.get_featured_performances()
    return render_template("index.html", featured_performances=featured_performances)


@main_bp.route("/info")
def info():
    event_days = event_days_dao.get_all_days()
    stages = stages_dao.get_all_stages()
    return render_template("info.html", event_days=event_days, stages=stages)


@main_bp.route("/lineup")
def lineup():
    performances = performances_dao.get_all_performances(include_unpublished=False)
    event_days = event_days_dao.get_all_days()
    stages = stages_dao.get_all_stages()
    genres = genres_dao.get_all_genres()

    return render_template(
        "lineup.html",
        performances=performances,
        event_days=event_days,
        stages=stages,
        genres=genres,
    )
