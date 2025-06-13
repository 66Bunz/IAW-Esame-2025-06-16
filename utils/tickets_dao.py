import sqlite3
from typing import Any, Dict, List, Optional, Tuple

from utils.event_days_dao import get_days_attendees, update_day_attendees
from utils.logger import get_logger
from utils.vars import DB_PATH, ROOT_PATH

logger = get_logger()


def get_ticket_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Restituisce il biglietto di un utente se esiste

    Parameters:
        user_id (int): L'ID dell'utente

    Returns:
        dict: Dizionario contenente i dettagli del biglietto, o None se non trovato
    """
    query = "SELECT * FROM tickets WHERE user_id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    ticket = cursor.fetchone()
    cursor.close()
    conn.close()

    if ticket:
        return {
            "id": ticket[0],
            "user_id": ticket[1],
            "ticket_type_id": ticket[2],
            "purchase_date": ticket[3],
            "is_valid": ticket[4],
            "friday": ticket[5],
            "saturday": ticket[6],
            "sunday": ticket[7],
        }

    return None


def create_ticket(
    user_id: int, ticket_type_id: int, days: List[int]
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Crea un nuovo biglietto per l'utente

    Parameters:
        user_id (int): ID dell'utente
        ticket_type_id (int): ID del tipo di biglietto
        days (list): Lista dei giorni per cui è valido il biglietto [1=venerdì, 2=sabato, 3=domenica]

    Returns:
        bool: True se la creazione è andata a buon fine, False altrimenti
        dict (optional): Dettagli del biglietto creato
    """

    existing_ticket = get_ticket_by_user_id(user_id)
    if existing_ticket:
        logger.error("L'utente ha già un biglietto.")
        return False, existing_ticket

    friday = 1 if 1 in days else 0
    saturday = 1 if 2 in days else 0
    sunday = 1 if 3 in days else 0

    for day_id in days:
        day_availability = get_days_attendees(day_id)
        if day_availability["current_attendees"] >= day_availability["max_attendees"]:  # type: ignore
            logger.error(f"Posti esauriti per il giorno {day_id}.")
            return False, None

    query = """
    INSERT INTO tickets (user_id, ticket_type_id, friday, saturday, sunday) 
    VALUES (?, ?, ?, ?, ?)
    """

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (user_id, ticket_type_id, friday, saturday, sunday))
        conn.commit()

        for day_id in days:
            update_day_attendees(day_id, 1)

        logger.info("Biglietto creato con successo.")
        return True, get_ticket_by_user_id(user_id)

    except Exception as e:
        conn.rollback()
        logger.error(f"Errore durante la creazione del biglietto: {e}")
        return False, None

    finally:
        cursor.close()
        conn.close()
