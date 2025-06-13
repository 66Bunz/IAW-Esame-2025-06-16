import os
from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from PIL import Image

from utils import event_days_dao, genres_dao, performances_dao, stages_dao, users_dao
from utils.vars import ROOT_PATH
from utils.logger import get_logger

logger = get_logger()
from blueprints.performances import performances_bp


@performances_bp.route("/<int:id>")
def detail(id: int):
    source = request.args.get("from", "main.lineup")
    source_name = request.args.get("source_name", "Lineup")

    performance = performances_dao.get_performance_by_id(id)

    if not performance:
        flash("Performance non trovata.", "danger")
        return redirect(url_for("main.lineup"))

    if performance["is_published"] == 0:
        if (
            not current_user.is_authenticated
            or current_user.role != 1
            or performance["organizer_id"] != current_user.id
        ):
            flash("Questa performance non esiste", "danger")
            return redirect(url_for("main.lineup"))

    stage = stages_dao.get_stage_by_id(performance["stage_id"])
    performance["stage_name"] = stage["name"] if stage else "Sconosciuto"

    day = event_days_dao.get_day_by_id(performance["day_id"])
    performance["day_name"] = day["name"] if day else "Sconosciuto"
    performance["day_date"] = day["date"] if day else None

    genre = genres_dao.get_genre_by_id(performance["genre_id"])
    performance["genre_name"] = genre["name"] if genre else "Sconosciuto"

    organizer = users_dao.get_user_by_id(performance["organizer_id"])
    performance["organizer_name"] = (
        organizer["username"] if organizer else "Sconosciuto"
    )

    return render_template(
        "performance-detail.html",
        performance=performance,
        source=source,
        source_name=source_name,
    )


@performances_bp.route("/management")
@login_required
def management():
    if current_user.role != 1:
        flash("Non hai i permessi per accedere a questa pagina.", "danger")
        return redirect(url_for("main.home"))

    performances = performances_dao.get_all_performances(include_unpublished=True)

    for performance in performances:
        stage = stages_dao.get_stage_by_id(performance["stage_id"])
        performance["stage_name"] = stage["name"] if stage else "Sconosciuto"

        genre = genres_dao.get_genre_by_id(performance["genre_id"])
        performance["genre_name"] = genre["name"] if genre else "Sconosciuto"

        day = event_days_dao.get_day_by_id(performance["day_id"])
        performance["day_name"] = day["name"] if day else "Sconosciuto"

        organizer = users_dao.get_user_by_id(performance["organizer_id"])
        performance["organizer_name"] = (
            organizer["name"] + " " + organizer["surname"]
            if organizer
            else "Sconosciuto"
        )

    return render_template("performance-management.html", performances=performances)


@performances_bp.route("/management/<action>", methods=["GET", "POST"])
@performances_bp.route("/management/<action>/<int:id>", methods=["GET", "POST"])
@login_required
def editor(action, id=None):
    source = request.args.get("from", "main.lineup")
    source_name = request.args.get("source_name", "Lineup")

    if current_user.role != 1:
        flash("Non hai i permessi per accedere a questa pagina.", "danger")
        return redirect(url_for("main.home"))

    stages = stages_dao.get_all_stages()
    days = event_days_dao.get_all_days()
    genres = genres_dao.get_all_genres()

    if action == "edit" and id:
        performance = performances_dao.get_performance_by_id(id)

        if not performance:
            flash("Performance non trovata.", "danger")
            return redirect(url_for("performances.management"))

        if performance["organizer_id"] != current_user.id:
            flash("Non hai i permessi per modificare questa performance.", "danger")
            return redirect(url_for("performances.management"))

        if performance["is_published"] == 1:
            flash(
                "Non è possibile modificare una performance già pubblicata.", "warning"
            )
            return redirect(url_for("performances.management"))

        # Se la richiesta è POST, significa che l'utente sta cercando di modificare la performance
        if request.method == "POST":
            artist_name = request.form.get("artist_name")
            day_id = int(request.form.get("day_id", 0))
            stage_id = int(request.form.get("stage_id", 0))
            start_time = request.form.get("start_time")
            duration = int(request.form.get("duration", 0))
            description = request.form.get("description")
            genre_id = int(request.form.get("genre_id", 0))

            if (
                not artist_name
                or not day_id
                or not stage_id
                or not start_time
                or not duration
                or not description
                or not genre_id
            ):
                flash("Tutti i campi sono obbligatori.", "danger")
                return redirect(url_for("performances.management"))

            image_path = performance["image_path"]
            artist_image = request.files.get("artist_image")

            if artist_image and artist_image.filename:
                os.makedirs(f"{ROOT_PATH}static/images/artists", exist_ok=True)
                img = Image.open(artist_image.stream)
                max_size = (800, 800)
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

                filename = f"artist_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.webp"
                image_path = f"images/artists/{filename}"
                img_path = f"{ROOT_PATH}static/{image_path}"
                img.save(img_path, "WEBP", quality=85, method=6)

            success, message = performances_dao.update_performance(
                performance_id=id,
                artist_name=artist_name,
                start_time=start_time,
                duration=duration,
                description=description,
                image_path=image_path,
                day_id=day_id,
                stage_id=stage_id,
                genre_id=genre_id,
            )

            if success:
                flash("Performance aggiornata con successo!", "success")
                return redirect(url_for("performances.management"))
            else:
                flash(f"Errore durante l'aggiornamento: {message}", "danger")

        # Se la richiesta è GET, significa che l'utente vuole visualizzare la pagina di modifica
        else:
            return render_template(
                "performance-editor.html",
                action="edit",
                performance=performance,
                stages=stages,
                days=days,
                genres=genres,
                source=source,
                source_name=source_name,
            )

    elif action == "add":
        default_day_id = request.args.get("day_id", "")
        default_stage_id = request.args.get("stage_id", "")

        # Se la richiesta è POST, significa che l'utente vuole aggiungere una nuova performance
        if request.method == "POST":
            artist_name = request.form.get("artist_name")
            day_id = int(request.form.get("day_id", 0))
            stage_id = int(request.form.get("stage_id", 0))
            start_time = request.form.get("start_time")
            duration = int(request.form.get("duration", 0))
            description = request.form.get("description")
            genre_id = int(request.form.get("genre_id", 0))

            if (
                not artist_name
                or not day_id
                or not stage_id
                or not start_time
                or not duration
                or not description
                or not genre_id
            ):
                flash("Tutti i campi sono obbligatori.", "danger")
                return redirect(url_for("performances.management"))

            temp_image_path = ""
            artist_image = request.files.get("artist_image")

            if artist_image and artist_image.filename:
                os.makedirs(f"{ROOT_PATH}static/images/uploads", exist_ok=True)
                os.makedirs(f"{ROOT_PATH}static/images/performances", exist_ok=True)
                img = Image.open(artist_image.stream)
                max_size = (800, 800)
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

                temp_filename = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}.webp"
                temp_image_path = f"images/uploads/{temp_filename}"
                img.save(
                    f"{ROOT_PATH}static/{temp_image_path}", "WEBP", quality=85, method=6
                )

            performance_id, message = performances_dao.add_performance(
                artist_name=artist_name,
                start_time=start_time,
                duration=duration,
                description=description,
                image_path=temp_image_path,
                day_id=day_id,
                stage_id=stage_id,
                genre_id=genre_id,
                organizer_id=current_user.id,
            )

            if performance_id > 0 and temp_image_path:
                final_filename = f"performance_{performance_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.webp"
                final_image_path = f"images/performances/{final_filename}"
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

                success, update_message = performances_dao.update_performance(
                    performance_id=performance_id,
                    artist_name=artist_name,
                    start_time=start_time,
                    duration=duration,
                    description=description,
                    image_path=final_image_path,
                    day_id=day_id,
                    stage_id=stage_id,
                    genre_id=genre_id,
                    is_published=0,
                    is_featured=0,
                )

                if not success:
                    flash(
                        f"Performance creata ma si è verificato un errore nell'associazione dell'immagine: {update_message}",
                        "warning",
                    )

            if performance_id > 0:
                flash("Performance creata con successo!", "success")
                return redirect(url_for("performances.management"))
            else:
                flash(f"Errore durante la creazione: {message}", "danger")

        # Se la richiesta è GET, significa che l'utente vuole visualizzare la pagina per aggiungere una nuova performance
        else:
            return render_template(
                "performance-editor.html",
                action="add",
                performance=None,
                stages=stages,
                days=days,
                genres=genres,
                default_day_id=default_day_id,
                default_stage_id=default_stage_id,
                source=source,
                source_name=source_name,
            )

    return redirect(url_for("performances.management"))


@performances_bp.route("/publish", methods=["POST"])
@login_required
def publish():
    if current_user.role != 1:
        flash("Non hai i permessi per pubblicare performance.", "danger")
        return redirect(url_for("main.home"))

    performance_id = int(request.form.get("performance_id", 0))
    is_featured = request.form.get("is_featured", "0") == "1"

    if not performance_id:
        flash("ID performance non valido.", "danger")
        return redirect(url_for("performances.management"))

    performance = performances_dao.get_performance_by_id(performance_id)

    if not performance:
        flash("Performance non trovata.", "danger")
        return redirect(url_for("performances.management"))

    if performance["organizer_id"] != current_user.id:
        flash("Non hai i permessi per pubblicare questa performance.", "danger")
        return redirect(url_for("performances.management"))

    if performance["is_published"] == 1:
        flash("Questa performance è già pubblicata.", "warning")
        return redirect(url_for("performances.management"))

    is_available, error_message = performances_dao.check_time_slot_available(
        performance["day_id"],
        performance["stage_id"],
        performance["start_time"],
        performance["duration"],
        performance["id"],
    )

    if not is_available:
        flash(error_message, "danger")
        return redirect(url_for("performances.management"))

    success, message = performances_dao.update_performance(
        performance_id=performance_id,
        artist_name=performance["artist_name"],
        start_time=performance["start_time"],
        duration=performance["duration"],
        description=performance["description"],
        image_path=performance["image_path"],
        day_id=performance["day_id"],
        stage_id=performance["stage_id"],
        genre_id=performance["genre_id"],
        is_published=1,
        is_featured=1 if is_featured else 0,
    )

    if success:
        flash("Performance pubblicata con successo!", "success")
    else:
        flash(f"Errore durante la pubblicazione: {message}", "danger")

    return redirect(url_for("performances.management"))


@performances_bp.route("/delete", methods=["POST"])
@login_required
def delete():
    if current_user.role != 1:
        flash("Non hai i permessi per eliminare performance.", "danger")
        return redirect(url_for("main.home"))

    performance_id = int(request.form.get("performance_id", 0))

    if not performance_id:
        flash("ID performance non valido.", "danger")
        return redirect(url_for("performances.management"))

    performance = performances_dao.get_performance_by_id(performance_id)

    if not performance:
        flash("Performance non trovata.", "danger")
        return redirect(url_for("performances.management"))

    if performance["organizer_id"] != current_user.id:
        flash("Non hai i permessi per eliminare questa performance.", "danger")
        return redirect(url_for("performances.management"))

    if performance["is_published"] == 1:
        flash("Non è possibile eliminare una performance già pubblicata.", "warning")
        return redirect(url_for("performances.management"))

    success, message = performances_dao.delete_performance(performance_id)

    if success:
        flash("Performance eliminata con successo!", "success")
    else:
        flash(f"Errore durante l'eliminazione: {message}", "danger")

    return redirect(url_for("performances.management"))
