import sqlite3
from typing import Any, Dict, List, Optional

from utils.logger import get_logger
from utils.vars import DB_PATH, ROOT_PATH

logger = get_logger()


def get_all_ticket_types() -> List[Dict[str, Any]]:
    """
    Restituisce tutti i tipi di biglietto

    Returns:
        list: Lista di dizionari contenenti i dettagli dei tipi di biglietto
    """

    query = "SELECT * FROM ticket_types"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    ticket_types = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": ticket_type[0],
            "name": ticket_type[1],
            "description": ticket_type[2],
            "price": ticket_type[3],
            "days_count": ticket_type[4],
        }
        for ticket_type in ticket_types
    ]


def get_ticket_type_by_id(ticket_type_id: int) -> Optional[Dict[str, Any]]:
    """
    Restituisce un tipo di biglietto dato il suo ID

    Parameters:
        ticket_type_id (int): ID del tipo di biglietto

    Returns:
        dict: Dizionario contenente i dettagli del tipo di biglietto, o None se non trovato
    """
    query = "SELECT * FROM ticket_types WHERE id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (ticket_type_id,))
    ticket_type = cursor.fetchone()
    cursor.close()
    conn.close()

    if ticket_type:
        return {
            "id": ticket_type[0],
            "name": ticket_type[1],
            "description": ticket_type[2],
            "price": ticket_type[3],
            "days_count": ticket_type[4],
        }

    return None
