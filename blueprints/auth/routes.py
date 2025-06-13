from datetime import datetime
import os
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image

from utils import users_dao
from utils.models import User
from utils.vars import ROOT_PATH
from utils.logger import get_logger

logger = get_logger()
from blueprints.auth import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Sei già autenticato", "info")
        return redirect(url_for('main.home'))
    
    # Se la richiesta è POST, significa che l'utente sta cercando di effettuare il login
    if request.method == "POST":
        utente_form = request.form.to_dict()

        if not utente_form["usernameoremail"] or not utente_form["password"]:
            flash("Nome utente/email e password sono obbligatori", "danger")
            return redirect(url_for("auth.login"))

        identifier = utente_form["usernameoremail"].strip()
        password = utente_form["password"].strip()
        remember = "remember" in utente_form

        if "@" in identifier:
            utente_db = users_dao.user_from_email(identifier)
        else:
            utente_db = users_dao.user_from_nickname(identifier)

        if not utente_db or not check_password_hash(utente_db["password"], password):
            flash("Credenziali non valide", "danger")
            return redirect(url_for("auth.login"))
        else:
            new_user = User(
                id=utente_db["id"],
                username=utente_db["username"],
                password=utente_db["password"],
                name=utente_db["name"],
                surname=utente_db["surname"],
                email=utente_db["email"],
                pfp=utente_db["pfp"],
                role=utente_db["role"],
            )

            login_user(new_user, remember=remember)
            flash("Accesso efettuato con successo", "success")
            return redirect(url_for("main.home"))

    # Se la richiesta è GET, significa che l'utente sta cercando di visualizzare la pagina di login
    else:
        return render_template("login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        flash("Sei già autenticato. Esci prima di creare un nuovo account", "info")
        return redirect(url_for('main.home'))

    # Se la richiesta è POST, significa che l'utente sta cercando di registrarsi
    if request.method == "POST":
        utente_form = request.form.to_dict()

        if (
            not utente_form["username"]
            or not utente_form["name"]
            or not utente_form["surname"]
            or not utente_form["email"]
            or not utente_form["password"]
        ):
            flash("Tutti i campi sono obbligatori", "danger")
            return redirect(url_for("auth.signup"))
        
        if "@" in utente_form["username"]:
            flash("Il nome utente non può contenere '@'", "danger")
            return redirect(url_for("auth.signup"))

        utente_db_username = users_dao.user_from_nickname(utente_form["username"])
        utente_db_email = users_dao.user_from_email(utente_form["email"])

        if utente_db_username:
            flash("Nome utente già esistente", "danger")
            return redirect(url_for("auth.signup"))
        elif utente_db_email:
            flash("Email già registrata", "danger")
            return redirect(url_for("auth.signup"))
        else:
            username = utente_form["username"]
            name = utente_form["name"]
            surname = utente_form["surname"]
            email = utente_form["email"]
            password = generate_password_hash(utente_form["password"], method="scrypt")
            role = int(utente_form["role"])

            temp_image_path = ""
            immagine = request.files["profile_picture"]

            if immagine and immagine.filename:
                os.makedirs(f"{ROOT_PATH}static/images/uploads", exist_ok=True)
                os.makedirs(f"{ROOT_PATH}static/images/pfp", exist_ok=True)
                img = Image.open(immagine.stream)
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

                temp_filename = f"pfp_{datetime.now().strftime('%Y%m%d%H%M%S')}.webp"
                temp_image_path = f"images/uploads/{temp_filename}"
                img.save(
                    f"{ROOT_PATH}static/{temp_image_path}", "WEBP", quality=85, method=6
                )

            user_id = users_dao.new_user(
                username, name, surname, email, password, temp_image_path, role
            )

            if temp_image_path:
                final_image_path = f"images/pfp/{user_id}.webp"
                img = Image.open(f"{ROOT_PATH}static/{temp_image_path}")
                img.save(
                    f"{ROOT_PATH}static/{final_image_path}",
                    "WEBP",
                    quality=85,
                    method=6,
                )

                try:
                    os.remove(f"{ROOT_PATH}static/{temp_image_path}")
                except:
                    pass

                users_dao.update_user_pfp(user_id, final_image_path)

            flash(
                "Registrazione completata con successo. Ora puoi accedere.", "success"
            )
            return redirect(url_for("auth.login"))

    # Se la richiesta è GET, significa che l'utente sta cercando di visualizzare la pagina di registrazione
    else:
        return render_template("signup.html")


@auth_bp.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logout efettuato con successo", "success")
        return redirect(url_for("main.home"))
    else:
        flash("Non sei autenticato", "warning")
        return redirect(url_for("auth.login"))
