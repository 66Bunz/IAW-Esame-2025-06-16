import sqlite3
from typing import Any, Dict, Optional

from utils.logger import get_logger
from utils.vars import DB_PATH, ROOT_PATH

logger = get_logger()


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Restituisce un utente dato il suo ID

    Parameters:
        user_id (int): ID dell'utente

    Returns:
        dict: Dizionario contenente i dettagli dell'utente, o None se non trovato
    """

    query = "SELECT * FROM users WHERE id = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return {
            "id": user[0],
            "username": user[1],
            "name": user[2],
            "surname": user[3],
            "email": user[4],
            "password": user[5],
            "role": user[6],
            "pfp": user[7],
        }

    return None


def user_from_nickname(username: str) -> Optional[Dict[str, Any]]:
    """
    Restituisce un utente dato il suo nome utente

    Parameters:
        username (str): Il nome utente dell'utente

    Returns:
        dict: Dizionario contenente i dettagli dell'utente, o None se non trovato
    """

    username = username.lower()

    query = "SELECT * FROM users WHERE username = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return {
            "id": user[0],
            "username": user[1],
            "name": user[2],
            "surname": user[3],
            "email": user[4],
            "password": user[5],
            "role": user[6],
            "pfp": user[7],
        }

    return None


def user_from_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Restituisce un utente data la sua email

    Parameters:
        email (str): L'email dell'utente

    Returns:
        dict: Dizionario contenente i dettagli dell'utente, o None se non trovato
    """

    email = email.lower()

    query = "SELECT * FROM users WHERE email = ?"

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return {
            "id": user[0],
            "username": user[1],
            "name": user[2],
            "surname": user[3],
            "email": user[4],
            "password": user[5],
            "role": user[6],
            "pfp": user[7],
        }

    return None


def new_user(
    username: str,
    name: str,
    surname: str,
    email: str,
    password: str,
    pfp_path: str,
    role: int = 0,
) -> int:
    """
    Registra un nuovo utente nel database

    Parameters:
        username (str): Nome utente
        name (str): Nome
        surname (str): Cognome
        email (str): Email
        password (str): Password
        pfp_path (str): Percorso dell'immagine profilo
        role (int): Ruolo dell'utente (0=partecipante, 1=organizzatore) (default: 0)

    Returns:
        int: L'ID del nuovo utente
    """

    username = username.lower()
    email = email.lower()

    query = "INSERT INTO users (username, name, surname, email, password, pfp, role) VALUES (?, ?, ?, ?, ?, ?, ?)"

    try:
        conn = sqlite3.connect(ROOT_PATH + DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            query, (username, name, surname, email, password, pfp_path, role)
        )
        conn.commit()

        user_id = cursor.lastrowid
        cursor.close()
        conn.close()

        logger.info(f"Nuovo utente creato: {username} (ID: {user_id})")
        return user_id if user_id is not None else -1

    except Exception as e:
        logger.error(f"Errore durante la creazione dell'utente {username}: {e}")
        return -1


def update_user(
    user_id: int,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
):
    """
    Aggiorna i dati di un utente nel database

    Parameters:
        user_id (int): ID dell'utente
        name (str, optional): Nuovo nome
        surname (str, optional): Nuovo cognome
        email (str, optional): Nuova email
        password (str, optional): Nuova password (hash)
    """

    update_fields = []
    params = []

    if name is not None:
        update_fields.append("name = ?")
        params.append(name)

    if surname is not None:
        update_fields.append("surname = ?")
        params.append(surname)

    if email is not None:
        email = email.lower()
        update_fields.append("email = ?")
        params.append(email)

    if password is not None:
        update_fields.append("password = ?")
        params.append(password)

    if not update_fields:
        return

    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
    params.append(user_id)

    try:
        conn = sqlite3.connect(ROOT_PATH + DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Dati utente aggiornati per ID: {user_id}")

    except Exception as e:
        logger.error(f"Errore durante l'aggiornamento dell'utente ID {user_id}: {e}")


def update_user_pfp(user_id: int, pfp_path: str):
    """
    Aggiorna l'immagine profilo di un utente

    Parameters:
        user_id (int): ID dell'utente
        pfp_path (str): Percorso della nuova immagine profilo
    """

    query = "UPDATE users SET pfp = ? WHERE id = ?"

    try:
        conn = sqlite3.connect(ROOT_PATH + DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, (pfp_path, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Immagine profilo aggiornata per utente ID: {user_id}")

    except Exception as e:
        logger.error(
            f"Errore durante l'aggiornamento dell'immagine profilo per utente ID {user_id}: {e}"
        )
