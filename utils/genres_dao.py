import sqlite3
from typing import Any, Dict, List, Optional

from utils.logger import get_logger
from utils.vars import DB_PATH, ROOT_PATH

logger = get_logger()


def get_all_genres() -> List[Dict[str, Any]]:
    """
    Restituisce tutti i generi musicali

    Returns:
        list: Lista di dizionari contenenti i dettagli dei generi musicali
    """

    query = "SELECT * FROM genres"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    genres = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"id": genre[0], "name": genre[1]} for genre in genres]


def get_genre_by_id(genre_id: int) -> Optional[Dict[str, Any]]:
    """
    Restituisce un genere dato il suo ID

    Parameters:
        genre_id (int): ID del genere

    Returns:
        dict: Dizionario contenente i dettagli del genere, o None se non trovato
    """

    query = "SELECT * FROM genres WHERE id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (genre_id,))
    genre = cursor.fetchone()
    cursor.close()
    conn.close()

    if genre:
        return {"id": genre[0], "name": genre[1]}

    return None
