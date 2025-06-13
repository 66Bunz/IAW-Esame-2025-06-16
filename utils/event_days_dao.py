import sqlite3
from typing import Any, Dict, List, Optional, Union

from utils.logger import get_logger
from utils.vars import DB_PATH, ROOT_PATH

logger = get_logger()


def get_all_days() -> List[Dict[str, Any]]:
    """
    Restituisce tutti i giorni del festival

    Returns:
        list: Lista di dizionari contenenti i dettagli dei giorni del festival
    """

    query = "SELECT * FROM event_days"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    days = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": day[0],
            "name": day[1],
            "date": day[2],
            "current_attendees": day[3],
            "max_attendees": day[4],
            "start_time": day[5],
            "end_time": day[6],
        }
        for day in days
    ]


def get_day_by_id(day_id: int) -> Optional[Dict[str, Any]]:
    """
    Restituisce un giorno dato il suo ID

    Parameters:
        day_id (int): ID del giorno

    Returns:
        dict: Dizionario contenente i dettagli del giorno, o None se non trovato
    """

    query = "SELECT * FROM event_days WHERE id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (day_id,))
    day = cursor.fetchone()
    cursor.close()
    conn.close()

    if day:
        return {
            "id": day[0],
            "name": day[1],
            "date": day[2],
            "current_attendees": day[3],
            "max_attendees": day[4],
            "start_time": day[5],
            "end_time": day[6],
        }

    return None


def update_day_attendees(day_id: int, increment: int) -> None:
    """
    Aggiorna il contatore di partecipanti per un giorno

    Parameters:
        day_id (int): ID del giorno (1=venerdì, 2=sabato, 3=domenica)
        increment (int): Valore da aggiungere al contatore (può essere negativo)
    """

    query = (
        "UPDATE event_days SET current_attendees = current_attendees + ? WHERE id = ?"
    )

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (increment, day_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_days_attendees(
    day_id: Optional[int] = None,
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Restituisce il numero di partecipanti per ciascun giorno del festival

    Parameters:
        day_id (int, optional): ID del giorno. Se non specificato, restituisce i dati per tutti i giorni.

    Returns:
        dict: Dizionario con i dati di partecipazione
    """

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    if day_id is None:
        query = "SELECT id, name, current_attendees, max_attendees FROM event_days"
        cursor.execute(query)
        days = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            {"name": day[1], "current_attendees": day[2], "max_attendees": day[3]}
            for day in days
        ]

    else:
        query = (
            "SELECT name, current_attendees, max_attendees FROM event_days WHERE id = ?"
        )
        cursor.execute(query, (day_id,))
        day = cursor.fetchone()
        cursor.close()
        conn.close()

        if day:
            return {
                "name": day[0],
                "current_attendees": day[1],
                "max_attendees": day[2],
            }

        return {}
