import sqlite3
from typing import Dict, List, Optional, Union

from utils.logger import get_logger
from utils.vars import DB_PATH, ROOT_PATH

logger = get_logger()


def get_all_stages() -> List[Dict[str, Union[int, str]]]:
    """
    Restituisce tutti i palchi

    Returns:
        List[Dict[str, Union[int, str]]]: Lista di dizionari contenenti i dettagli dei palchi
    """

    query = "SELECT * FROM stages"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    stages = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {"id": stage[0], "name": stage[1], "description": stage[2], "image": stage[3]}
        for stage in stages
    ]


def get_stage_by_id(stage_id: int) -> Optional[Dict[str, Union[int, str]]]:
    """
    Restituisce un palco dato il suo ID

    Parameters:
        stage_id (int): L'ID del palco

    Returns:
        Optional[Dict[str, Union[int, str]]]: Dizionario contenente i dettagli del palco o None se non trovato
    """

    query = "SELECT * FROM stages WHERE id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (stage_id,))
    stage = cursor.fetchone()
    cursor.close()
    conn.close()

    if stage:
        return {
            "id": stage[0],
            "name": stage[1],
            "description": stage[2],
            "image": stage[3],
        }

    return None
