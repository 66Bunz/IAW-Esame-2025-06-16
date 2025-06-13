import os
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image

from utils import (
    event_days_dao,
    performances_dao, 
    stages_dao, 
    ticket_types_dao, 
    tickets_dao, 
    users_dao
)
from utils.vars import ROOT_PATH
from utils.logger import get_logger

logger = get_logger()
from blueprints.profile import profile_bp


@profile_bp.route("/")
@login_required
def index():
    if not current_user:
        flash("Utente non trovato", "danger")
        return redirect(url_for("main.home"))

    template_data = {
        "username": current_user.username,
        "name": current_user.name,
        "surname": current_user.surname,
        "email": current_user.email,
        "pfp": current_user.pfp,
    }

    if current_user.role == 0:
        ticket = tickets_dao.get_ticket_by_user_id(current_user.id)
        if ticket:
            ticket_type = ticket_types_dao.get_ticket_type_by_id(
                ticket["ticket_type_id"]
            )
            ticket["ticket_type_name"] = (
                ticket_type["name"] if ticket_type else "Biglietto"
            )
            template_data["tickets"] = [ticket]
        else:
            template_data["tickets"] = []

    elif current_user.role == 1:
        performances = performances_dao.get_performances_by_organizer(
            current_user.id, include_unpublished=True
        )

        for p in performances:
            stage = stages_dao.get_stage_by_id(p["stage_id"])
            p["stage_name"] = stage["name"] if stage else "Sconosciuto"

        template_data["performances"] = performances

        event_days = event_days_dao.get_all_days()
        template_data["event_days"] = event_days

    return render_template("profile.html", **template_data)


@profile_bp.route("/update", methods=["POST"])
@login_required
def update():
    current_password = request.form.get("current_password")
    if not current_password:
        flash("La password attuale è obbligatoria", "danger")
        return redirect(url_for("profile.index"))

    if not check_password_hash(current_user.password, current_password):
        flash("Password attuale non corretta", "danger")
        return redirect(url_for("profile.index"))

    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if email and email != current_user.email:
        existing_user = users_dao.user_from_email(email)
        if existing_user and existing_user["id"] != current_user.id:
            flash("Email già in uso da un altro utente", "danger")
            return redirect(url_for("profile.index"))

    if new_password:
        if new_password != confirm_password:
            flash("Le password non corrispondono", "danger")
            return redirect(url_for("profile.index"))
        password_hash = generate_password_hash(new_password, method="scrypt")
    else:
        password_hash = current_user.password

    users_dao.update_user(
        current_user.id, name=name, surname=surname, email=email, password=password_hash
    )

    current_user.name = name
    current_user.surname = surname
    current_user.email = email
    current_user.password = password_hash

    flash("Profilo aggiornato con successo", "success")
    return redirect(url_for("profile.index"))


@profile_bp.route("/update_picture", methods=["POST"])
@login_required
def update_picture():
    pfp = request.files["profile_picture"]

    if pfp and pfp.filename:
        os.makedirs(f"{ROOT_PATH}static/images/pfp", exist_ok=True)
        img = Image.open(pfp.stream)
        max_size = (500, 500)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        if img.mode in ("RGBA", "LA"):
            if "A" in img.mode:
                img = img.convert("RGBA")
            else:
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img)
                img = background
        elif img.mode != "RGB" and img.mode != "RGBA":
            img = img.convert("RGB")

        file_ext = "webp"
        pfp_path = f"images/pfp/{current_user.id}.{file_ext}"
        img_path = f"{ROOT_PATH}static/" + pfp_path
        img.save(img_path, "WEBP", quality=85, method=6)
        users_dao.update_user_pfp(current_user.id, pfp_path)

        current_user.pfp = pfp_path

        flash("Immagine profilo aggiornata con successo", "success")
    else:
        flash("Nessuna immagine selezionata", "danger")

    return redirect(url_for("profile.index"))
