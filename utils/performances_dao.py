import sqlite3
from typing import Any, Dict, List, Optional, Tuple

from utils import event_days_dao
from utils.logger import get_logger
from utils.vars import DB_PATH, ROOT_PATH

logger = get_logger()


def get_all_performances(include_unpublished: bool = False) -> List[Dict[str, Any]]:
    """
    Restituisce tutte le performance

    Parameters:
        include_unpublished (bool): Se True, include anche le performance non pubblicate (default: False)

    Returns:
        list: Lista di dizionari contenenti i dettagli delle performance
    """

    if include_unpublished:
        query = "SELECT * FROM performances"
    else:
        query = "SELECT * FROM performances WHERE is_published = 1"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    performances = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": p[0],
            "artist_name": p[1],
            "start_time": p[2],
            "duration": p[3],
            "description": p[4],
            "image_path": p[5],
            "day_id": p[6],
            "stage_id": p[7],
            "genre_id": p[8],
            "organizer_id": p[9],
            "is_published": p[10],
            "created_at": p[11],
            "updated_at": p[12],
            "is_featured": p[13],
        }
        for p in performances
    ]


def get_performance_by_id(performance_id: int) -> Optional[Dict[str, Any]]:
    """
    Restituisce una performance dato il suo ID

    Parameters:
        performance_id (int): ID della performance

    Returns:
        dict: Dizionario contenente i dettagli della performance, o None se non trovato
    """

    query = "SELECT * FROM performances WHERE id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (performance_id,))
    p = cursor.fetchone()
    cursor.close()
    conn.close()

    if p:
        return {
            "id": p[0],
            "artist_name": p[1],
            "start_time": p[2],
            "duration": p[3],
            "description": p[4],
            "image_path": p[5],
            "day_id": p[6],
            "stage_id": p[7],
            "genre_id": p[8],
            "organizer_id": p[9],
            "is_published": p[10],
            "created_at": p[11],
            "updated_at": p[12],
            "is_featured": p[13],
        }

    return None


def get_performances_by_organizer(
    organizer_id: int, include_unpublished: bool = False
) -> List[Dict[str, Any]]:
    """
    Restituisce tutte le performance di un organizzatore specifico

    Parameters:
        organizer_id (int): ID dell'organizzatore
        include_unpublished (bool): Se True, include anche le performance non pubblicate (default: False)

    Returns:
        list: Lista di dizionari contenenti i dettagli delle performance dell'organizzatore specificato
    """

    if include_unpublished:
        query = "SELECT * FROM performances WHERE organizer_id = ? ORDER BY day_id, start_time"
    else:
        query = "SELECT * FROM performances WHERE organizer_id = ? AND is_published = 1 ORDER BY day_id, start_time"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (organizer_id,))
    performances = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": p[0],
            "artist_name": p[1],
            "start_time": p[2],
            "duration": p[3],
            "description": p[4],
            "image_path": p[5],
            "day_id": p[6],
            "stage_id": p[7],
            "genre_id": p[8],
            "organizer_id": p[9],
            "is_published": p[10],
            "created_at": p[11],
            "updated_at": p[12],
            "is_featured": p[13],
        }
        for p in performances
    ]


def get_featured_performances() -> List[Dict[str, Any]]:
    """
    Restituisce tutte le performance in evidenza

    Returns:
        list: Lista di dizionari contenenti i dettagli delle performance in evidenza
    """

    query = "SELECT * FROM performances WHERE is_featured = 1 AND is_published = 1 ORDER BY day_id, start_time"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    performances = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": p[0],
            "artist_name": p[1],
            "start_time": p[2],
            "duration": p[3],
            "description": p[4],
            "image_path": p[5],
            "day_id": p[6],
            "stage_id": p[7],
            "genre_id": p[8],
            "organizer_id": p[9],
            "is_published": p[10],
            "created_at": p[11],
            "updated_at": p[12],
            "is_featured": p[13],
        }
        for p in performances
    ]


def check_artist_exists(artist_name: str) -> bool:
    """
    Verifica se un artista esiste già

    Parameters:
        artist_name (str): Nome dell'artista

    Returns:
        bool: True se l'artista esiste già, False altrimenti
    """

    query = "SELECT COUNT(*) FROM performances WHERE artist_name = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (artist_name,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return count > 0


def check_time_slot_available(
    day_id: int,
    stage_id: int,
    start_time: str,
    duration: int,
    exclude_performance_id: Optional[int] = None,
) -> Tuple[bool, str]:
    """
    Verifica se un time slot è disponibile per un palco in un giorno specifico

    Parameters:
        day_id (int): ID del giorno
        stage_id (int): ID del palco
        start_time (str): Orario di inizio (formato HH:MM)
        duration (int): Durata in minuti
        exclude_performance_id (int, optional): ID della performance da escludere dal controllo

    Returns:
        bool: True se il time slot è disponibile, False altrimenti
        str: Messaggio di errore (se disponibile=False)
    """

    start_hour, start_minute = map(int, start_time.split(":"))
    start_minutes = start_hour * 60 + start_minute
    end_minutes = start_minutes + duration

    day = event_days_dao.get_day_by_id(day_id)

    # Verifica che l'orario d'inizio non sia prima dell'orario di apertura del festival
    if day and day.get("start_time"):
        opening_hour, opening_minute = map(int, day["start_time"].split(":"))
        opening_minutes = opening_hour * 60 + opening_minute

        if start_minutes < opening_minutes:
            return (
                False,
                f"La performance inizia alle {start_hour:02d}:{start_minute:02d}, prima dell'orario di apertura del festival ({day['start_time']})",
            )

    # Verifica che l'orario di fine non superi l'orario di chiusura del festival
    if day and day.get("end_time"):
        closing_hour, closing_minute = map(int, day["end_time"].split(":"))
        closing_minutes = closing_hour * 60 + closing_minute

        if end_minutes > closing_minutes:
            return (
                False,
                f"La performance finisce alle {end_minutes//60:02d}:{end_minutes%60:02d}, oltre l'orario di chiusura del festival ({day['end_time']})",
            )
            
    query = """
    SELECT 
        id, 
        start_time, 
        duration 
    FROM performances 
    WHERE 
        day_id = ? AND 
        stage_id = ? AND 
        is_published = 1
    """

    if exclude_performance_id:
        query += " AND id != ?"
        params = (day_id, stage_id, exclude_performance_id)
    else:
        params = (day_id, stage_id)

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    performances = cursor.fetchall()
    cursor.close()
    conn.close()

    for p in performances:
        p_start_hour, p_start_minute = map(int, p[1].split(":"))
        p_start_minutes = p_start_hour * 60 + p_start_minute
        p_end_minutes = p_start_minutes + p[2]

        # Verifica sovrapposizione
        if not (end_minutes <= p_start_minutes or start_minutes >= p_end_minutes):
            return (
                False,
                "Esiste già una performance in questo slot orario sul palco selezionato",
            )

    return True, ""


def add_performance(
    artist_name: str,
    start_time: str,
    duration: int,
    description: str,
    image_path: str,
    day_id: int,
    stage_id: int,
    genre_id: int,
    organizer_id: int,
    is_published: int = 0,
    is_featured: int = 0,
) -> Tuple[int, str]:
    """
    Aggiunge una nuova performance

    Parameters:
        artist_name (str): Nome dell'artista
        start_time (str): Orario di inizio (formato HH:MM)
        duration (int): Durata in minuti
        description (str): Descrizione della performance
        image_path (str): Percorso dell'immagine dell'artista
        day_id (int): ID del giorno
        stage_id (int): ID del palco
        genre_id (int): ID del genere
        organizer_id (int): ID dell'organizzatore
        is_published (int): 0=bozza, 1=pubblicata (default: 0)
        is_featured (int): 0=normale, 1=in evidenza (default: 0)

    Returns:
        int: ID della nuova performance, -1 se c'è stato un errore
        str: Messaggio di errore o successo
    """

    if check_artist_exists(artist_name):
        return -1, "Questo artista ha già una performance programmata nel festival"

    if is_published == 1:
        is_available, error_message = check_time_slot_available(
            day_id, stage_id, start_time, duration
        )
        if not is_available:
            return -1, error_message

    query = """
    INSERT INTO performances (
        artist_name, start_time, duration, description, image_path,
        day_id, stage_id, genre_id, organizer_id, is_published, is_featured
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            query,
            (
                artist_name,
                start_time,
                duration,
                description,
                image_path,
                day_id,
                stage_id,
                genre_id,
                organizer_id,
                is_published,
                is_featured,
            ),
        )
        conn.commit()

        performance_id = cursor.lastrowid
        return (
            performance_id if performance_id is not None else -1
        ), "Performance aggiunta con successo"

    except Exception as e:
        conn.rollback()
        logger.error(f"Errore durante l'inserimento della performance: {e}")
        return -1, f"Errore durante l'inserimento della performance: {e}"

    finally:
        cursor.close()
        conn.close()


def update_performance(
    performance_id: int,
    artist_name: str,
    start_time: str,
    duration: int,
    description: str,
    image_path: str,
    day_id: int,
    stage_id: int,
    genre_id: int,
    is_published: int = 0,
    is_featured: int = 0,
) -> Tuple[bool, str]:
    """
    Aggiorna una performance esistente

    Parameters:
        performance_id (int): ID della performance da aggiornare
        artist_name (str): Nome dell'artista
        start_time (str): Orario di inizio (formato HH:MM)
        duration (int): Durata in minuti
        description (str): Descrizione della performance
        image_path (str): Percorso dell'immagine dell'artista
        day_id (int): ID del giorno
        stage_id (int): ID del palco
        genre_id (int): ID del genere
        is_published (int): 0=bozza, 1=pubblicata (default: 0)
        is_featured (int): 0=normale, 1=in evidenza (default: 0)

    Returns:
        bool: True se l'aggiornamento è andato a buon fine, False altrimenti
        str: Messaggio di errore o successo
    """

    current_performance = get_performance_by_id(performance_id)
    if not current_performance:
        return False, "Performance non trovata"

    if current_performance["is_published"] == 1:
        return False, "Non è possibile modificare una performance già pubblicata"

    if artist_name != current_performance["artist_name"]:
        if check_artist_exists(artist_name):
            return (
                False,
                "Questo artista ha già una performance programmata nel festival",
            )

    if is_published == 1:
        is_available, error_message = check_time_slot_available(
            day_id, stage_id, start_time, duration, performance_id
        )
        if not is_available:
            return False, error_message

    query = """
    UPDATE performances 
    SET artist_name = ?, start_time = ?, duration = ?, description = ?, 
        image_path = CASE WHEN ? != '' THEN ? ELSE image_path END,
        day_id = ?, stage_id = ?, genre_id = ?, is_published = ?, 
        is_featured = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            query,
            (
                artist_name,
                start_time,
                duration,
                description,
                image_path,
                image_path,
                day_id,
                stage_id,
                genre_id,
                is_published,
                is_featured,
                performance_id,
            ),
        )
        conn.commit()
        return True, "Performance aggiornata con successo"

    except Exception as e:
        conn.rollback()
        logger.error(f"Errore durante l'aggiornamento della performance: {e}")
        return False, f"Errore durante l'aggiornamento della performance: {e}"

    finally:
        cursor.close()
        conn.close()


def delete_performance(performance_id: int) -> Tuple[bool, str]:
    """
    Elimina una performance

    Parameters:
        performance_id (int): ID della performance da eliminare

    Returns:
        bool: True se l'eliminazione è andata a buon fine, False altrimenti
    """

    current_performance = get_performance_by_id(performance_id)
    if not current_performance:
        return False, "Performance non trovata"

    if current_performance["is_published"] == 1:
        return False, "Non è possibile eliminare una performance già pubblicata"

    query = "DELETE FROM performances WHERE id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (performance_id,))
        conn.commit()
        return True, "Performance eliminata con successo"

    except Exception as e:
        conn.rollback()
        logger.error(f"Errore durante l'eliminazione della performance: {e}")
        return False, f"Errore durante l'eliminazione della performance: {e}"

    finally:
        cursor.close()
        conn.close()
