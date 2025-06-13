import os
import qrcode
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from qrcode.constants import ERROR_CORRECT_L

from utils import event_days_dao, ticket_types_dao, tickets_dao
from utils.vars import ROOT_PATH
from utils.logger import get_logger

logger = get_logger()
from blueprints.tickets import tickets_bp

@tickets_bp.route("/")
@login_required
def index():
    ticket = None
    if current_user.is_authenticated and current_user.role == 0:
        ticket = tickets_dao.get_ticket_by_user_id(current_user.id)

    ticket_types = ticket_types_dao.get_all_ticket_types()
    event_days = event_days_dao.get_all_days()

    return render_template(
        "tickets.html", ticket=ticket, ticket_types=ticket_types, event_days=event_days
    )


@tickets_bp.route("/buy", methods=["POST"])
@login_required
def buy():
    if current_user.role != 0:
        flash("Solo i partecipanti possono acquistare biglietti", "danger")
        return redirect(url_for("tickets.index"))

    existing_ticket = tickets_dao.get_ticket_by_user_id(current_user.id)
    if existing_ticket:
        flash("Hai già acquistato un biglietto per questa edizione", "warning")
        return redirect(url_for("profile.index"))

    ticket_type_id = request.form.get("ticket_type_id")
    days = request.form.getlist("days")

    if not ticket_type_id or not days:
        flash("Seleziona un tipo di biglietto e i giorni", "danger")
        return redirect(url_for("tickets.index"))

    ticket_type_id = int(ticket_type_id)
    days = [int(day) for day in days]

    ticket_type = ticket_types_dao.get_ticket_type_by_id(ticket_type_id)
    if not ticket_type:
        flash("Tipo di biglietto non valido", "danger")
        return redirect(url_for("tickets.index"))

    if len(days) != ticket_type["days_count"]:
        flash(
            "Numero di giorni non valido per il tipo di biglietto selezionato", "danger"
        )
        return redirect(url_for("tickets.index"))

    success, ticket = tickets_dao.create_ticket(current_user.id, ticket_type_id, days)

    if success and ticket:
        flash(f"Biglietto {ticket_type['name']} acquistato con successo!", "success")

        qr = qrcode.QRCode(
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(ticket))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        os.makedirs(f"{ROOT_PATH}static/images/tickets", exist_ok=True)

        pil_img = img.get_image()
        if pil_img.mode != "RGBA":
            pil_img = pil_img.convert("RGBA")

        img_path = f"{ROOT_PATH}static/images/tickets/{ticket['id']}.webp"
        pil_img.save(img_path, "WEBP", quality=90, method=6)

        return redirect(url_for("profile.index"))

    else:
        flash(
            "Si è verificato un errore durante l'acquisto del biglietto. Alcuni giorni potrebbero essere esauriti.",
            "danger",
        )
        return redirect(url_for("tickets.index"))
