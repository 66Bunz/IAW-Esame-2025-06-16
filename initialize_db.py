import os
import sqlite3
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

from utils.vars import DB_PATH, ROOT_PATH


table_schemas = [
    """
    CREATE TABLE IF NOT EXISTS "event_days" (
        "id" INTEGER NOT NULL UNIQUE,
        "name" TEXT NOT NULL,
        "date" TEXT NOT NULL,
        "current_attendees" INTEGER NOT NULL DEFAULT 0,
        "max_attendees" INTEGER NOT NULL DEFAULT 200,
        "start_time" TEXT NOT NULL,
        "end_time" TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "users" (
        "id" INTEGER NOT NULL UNIQUE,
        "username" TEXT NOT NULL UNIQUE,
        "name" TEXT NOT NULL,
        "surname" TEXT NOT NULL,
        "email" TEXT NOT NULL UNIQUE,
        "password" TEXT NOT NULL,
        "role" INTEGER NOT NULL,
        "pfp" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "stages" (
        "id" INTEGER NOT NULL UNIQUE,
        "name" TEXT NOT NULL UNIQUE,
        "description" TEXT NOT NULL,
        "image" TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "genres" (
        "id" INTEGER NOT NULL UNIQUE,
        "name" TEXT NOT NULL UNIQUE,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "performances" (
        "id" INTEGER NOT NULL UNIQUE,
        "artist_name" TEXT NOT NULL,
        "start_time" TEXT NOT NULL,
        "duration" INTEGER NOT NULL,
        "description" TEXT,
        "image_path" TEXT,
        "day_id" INTEGER NOT NULL,
        "stage_id" INTEGER NOT NULL,
        "genre_id" INTEGER NOT NULL,
        "organizer_id" INTEGER NOT NULL,
        "is_published" INTEGER NOT NULL DEFAULT 0,
        "created_at" TEXT DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TEXT DEFAULT CURRENT_TIMESTAMP,
        "is_featured" INTEGER DEFAULT 0,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("day_id") REFERENCES "event_days"("id"),
        FOREIGN KEY("stage_id") REFERENCES "stages"("id"),
        FOREIGN KEY("genre_id") REFERENCES "genres"("id"),
        FOREIGN KEY("organizer_id") REFERENCES "users"("id")
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "ticket_types" (
        "id" INTEGER NOT NULL UNIQUE,
        "name" TEXT NOT NULL UNIQUE,
        "description" TEXT,
        "price" REAL NOT NULL,
        "days_count" INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "tickets" (
        "id" INTEGER NOT NULL UNIQUE,
        "user_id" INTEGER NOT NULL,
        "ticket_type_id" INTEGER NOT NULL,
        "purchase_date" TEXT DEFAULT CURRENT_TIMESTAMP,
        "is_valid" INTEGER DEFAULT 1,
        "friday" INTEGER DEFAULT 0,
        "saturday" INTEGER DEFAULT 0,
        "sunday" INTEGER DEFAULT 0,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("user_id") REFERENCES "users"("id"),
        FOREIGN KEY("ticket_type_id") REFERENCES "ticket_types"("id")
    )
    """,
]

table_names = [
    "event_days",
    "users",
    "stages",
    "genres",
    "performances",
    "ticket_types",
    "tickets",
]

default_users = [
    ("musicmaestro", "Marco", "Rossi", "marco.rossi@example.com", "Admin2025!", "", 1),
    (
        "soundwizard",
        "Laura",
        "Bianchi",
        "laura.bianchi@example.com",
        "Stage2025!",
        "images/pfp/2.webp",
        1,
    ),
    ("beatmaker", "Paolo", "Verdi", "paolo.verdi@example.com", "Plan2025!", "", 1),
    (
        "rhythmking",
        "Sara",
        "Neri",
        "sara.neri@example.com",
        "Music2025!",
        "images/pfp/4.webp",
        1,
    ),
    ("music_fan", "Luca", "Romano", "luca.romano@example.com", "Fan2025!", "", 0),
    (
        "rock_lover",
        "Elena",
        "Ferrari",
        "elena.ferrari@example.com",
        "Rock2025!",
        "images/pfp/6.webp",
        0,
    ),
    (
        "pop_enthusiast",
        "Andrea",
        "Marino",
        "andrea.marino@example.com",
        "Pop2025!",
        "images/pfp/7.webp",
        0,
    ),
    (
        "festival_goer",
        "Chiara",
        "Costa",
        "chiara.costa@example.com",
        "Fest2025!",
        "",
        0,
    ),
    (
        "concert_junkie",
        "Matteo",
        "Rizzo",
        "matteo.rizzo@example.com",
        "Concert2025!",
        "",
        0,
    ),
]

default_days = [
    ("Venerdì", "2025-06-20", 0, 200, "14:00", "24:00"),
    ("Sabato", "2025-06-21", 0, 200, "14:00", "24:00"),
    ("Domenica", "2025-06-22", 0, 200, "14:00", "24:00"),
]

default_stages = [
    (
        "Main Stage",
        "Il palco principale con artisti di fama internazionale.",
        "images/assets/main_stage.webp",
    ),
    (
        "Secondary Stage",
        "Un palco più intimo per performance alternative.",
        "images/assets/secondary_stage.webp",
    ),
    (
        "Experimental Stage",
        "Un palco dedicato alla musica sperimentale.",
        "images/assets/experimental_stage.webp",
    ),
]

default_genres = [
    "Rock",
    "Pop",
    "Electronic",
    "Hip-Hop",
    "R&B",
    "Jazz",
    "Blues",
    "Metal",
    "Folk",
    "Indie",
    "Techno",
    "Reggae",
]

default_ticket_types = [
    ("Biglietto Giornaliero", "Accesso per un singolo giorno del festival", 59.99, 1),
    ("Pass 2 Giorni", "Accesso per due giorni consecutivi del festival", 99.99, 2),
    ("Full Pass", "Valido per tutti e tre i giorni del festival", 139.99, 3),
]

default_performances = [
    (
        1,
        "Lunar Echo",
        "18:00",
        60,
        "Un viaggio elettronico attraverso atmosfere lunari e pulsazioni ritmiche profonde",
        "images/performances/performance_1_20250610224310.webp",
        1,
        1,
        3,
        1,
        1,
        "2025-06-10 20:43:10",
        "2025-06-10 20:44:38",
        1,
    ),
    (
        2,
        "Mystic Voyage",
        "23:00",
        60,
        "Una fusione di blues tradizionale e psichedelia moderna",
        "images/performances/performance_2_20250610224602.webp",
        3,
        3,
        7,
        1,
        1,
        "2025-06-10 20:46:02",
        "2025-06-10 20:59:16",
        0,
    ),
    (
        3,
        "Aurora Groove",
        "14:00",
        30,
        "Pop elettronico con influenze nordiche e vocalizzi eterei",
        "images/performances/performance_3_20250610225521.webp",
        2,
        3,
        2,
        1,
        1,
        "2025-06-10 20:55:21",
        "2025-06-10 20:59:24",
        0,
    ),
    (
        4,
        "Velvet Thunder",
        "21:00",
        60,
        "Power metal con influenze sinfoniche e una potente voce femminile",
        "images/performances/performance_4_20250610225737.webp",
        2,
        1,
        8,
        1,
        0,
        "2025-06-10 20:57:37",
        "2025-06-10 20:57:37",
        0,
    ),
    (
        5,
        "Midnight Mirage",
        "18:30",
        45,
        "Indie pop etereo con testi poetici e melodie sognanti",
        "images/performances/performance_5_20250610225901.webp",
        1,
        3,
        10,
        1,
        1,
        "2025-06-10 20:59:01",
        "2025-06-10 20:59:45",
        1,
    ),
    (
        6,
        "Quantum Flux",
        "14:00",
        60,
        "Progressive metal tecnico con cambi di tempo complessi e virtuosismo strumentale",
        "images/performances/performance_6_20250610230139.webp",
        2,
        1,
        8,
        1,
        1,
        "2025-06-10 21:01:39",
        "2025-06-10 21:02:35",
        0,
    ),
    (
        7,
        "Rhapsody in Blue",
        "14:00",
        60,
        "Un quartetto jazz che reinterpreta classici in chiave moderna e presenta composizioni originali",
        "images/performances/performance_7_20250610231525.webp",
        3,
        2,
        6,
        1,
        1,
        "2025-06-10 21:15:25",
        "2025-06-10 21:15:37",
        0,
    ),
    (
        8,
        "The Crystal Waves",
        "15:00",
        60,
        "Rock alternativo con influenze progressive e testi introspettivi",
        "images/performances/performance_8_20250610232310.webp",
        1,
        2,
        1,
        3,
        1,
        "2025-06-10 21:23:10",
        "2025-06-10 21:23:23",
        1,
    ),
    (
        9,
        "Neon Syndrome",
        "14:00",
        45,
        "Synthwave con influenze cinematiche e un estetica retrofuturistica",
        "images/performances/performance_9_20250610232439.webp",
        2,
        2,
        3,
        3,
        1,
        "2025-06-10 21:24:39",
        "2025-06-10 21:24:50",
        0,
    ),
    (
        10,
        "Ethereal Whispers",
        "14:45",
        45,
        "Folk moderno che intreccia melodie tradizionali con arrangiamenti contemporanei",
        "images/performances/performance_10_20250610232556.webp",
        2,
        2,
        9,
        3,
        1,
        "2025-06-10 21:25:56",
        "2025-06-10 21:26:02",
        0,
    ),
    (
        11,
        "Electric Oasis",
        "15:30",
        30,
        "Fusion di elettronica e world music che crea paesaggi sonori immersivi",
        "images/performances/performance_11_20250610232702.webp",
        2,
        2,
        3,
        3,
        1,
        "2025-06-10 21:27:02",
        "2025-06-10 21:27:53",
        0,
    ),
    (
        12,
        "Soul Ignition",
        "17:30",
        60,
        "R&B contemporaneo che fonde tradizione soul con produzioni moderne",
        "images/performances/performance_12_20250610233004.webp",
        1,
        3,
        5,
        3,
        0,
        "2025-06-10 21:30:04",
        "2025-06-10 21:30:04",
        0,
    ),
    (
        13,
        "Nebula Dreams",
        "23:00",
        60,
        "Un ensemble di jazz sperimentale che fonde sonorità tradizionali con elettronica ambient",
        "images/performances/performance_13_20250610233440.webp",
        3,
        1,
        6,
        4,
        1,
        "2025-06-10 21:34:40",
        "2025-06-10 21:34:48",
        1,
    ),
    (
        14,
        "Eternal Echoes",
        "14:00",
        60,
        "Ambient sperimentale che esplora le intersezioni tra suono, spazio e percezione",
        "images/performances/performance_14_20250610233606.webp",
        3,
        1,
        6,
        4,
        1,
        "2025-06-10 21:36:06",
        "2025-06-10 21:36:46",
        0,
    ),
    (
        15,
        "Digital Horizons",
        "17:00",
        60,
        "Techno sperimentale con visual art sincronizzata",
        "images/performances/performance_15_20250610233750.webp",
        3,
        3,
        11,
        4,
        1,
        "2025-06-10 21:37:50",
        "2025-06-10 21:38:14",
        1,
    ),
    (
        16,
        "Crimson Tide",
        "18:00",
        40,
        "Una band rock emergente con sonorità vintage e una energia contagiosa sul palco",
        "images/performances/performance_16_20250610233929.webp",
        3,
        3,
        1,
        4,
        1,
        "2025-06-10 21:39:29",
        "2025-06-10 21:39:35",
        0,
    ),
]

default_tickets = [
    (1, 5, 3, "2025-06-10 21:55:08", 1, 1, 1, 1),
    (2, 6, 1, "2025-06-10 21:55:50", 1, 0, 1, 0),
    (3, 8, 2, "2025-06-10 21:57:06", 1, 1, 1, 0),
    (4, 9, 2, "2025-06-10 21:57:37", 1, 0, 1, 1),
]


def ensure_db_directory():
    """Assicura che la directory del database esista"""
    os.makedirs(os.path.dirname(ROOT_PATH + DB_PATH), exist_ok=True)
    return os.path.exists(os.path.dirname(ROOT_PATH + DB_PATH))


def check_db_exists():
    """Verifica se il database esiste"""
    return os.path.exists(ROOT_PATH + DB_PATH)


def create_database_structure():
    """
    Crea la struttura del database come definita nel README
    """
    ensure_db_directory()

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    tables_created = 0
    for schema in table_schemas:
        try:
            cursor.execute(schema)
            tables_created += 1
        except Exception as e:
            print(f"Errore durante la creazione della tabella: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    if tables_created == len(table_schemas):
        print("Tutte le tabelle create con successo")
        return True
    else:
        print(f"Create {tables_created}/{len(table_schemas)} tabelle")
        return False


def initialize_default_data():
    """
    Inizializza il database con i dati predefiniti
    """
    if not check_db_exists():
        print("Database non trovato. Crea prima la struttura del database.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    success = True

    try:
        cursor.execute("SELECT COUNT(*) FROM event_days")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO event_days (name, date, current_attendees, max_attendees, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?)",
                default_days,
            )
            print("Giorni dell'evento inizializzati con successo")
        else:
            print("La tabella event_days contiene già dati, inizializzazione saltata")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inizializzazione dei giorni: {e}")
        success = False

    try:
        cursor.execute("SELECT COUNT(*) FROM stages")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO stages (name, description, image) VALUES (?, ?, ?)",
                default_stages,
            )
            print("Palchi inizializzati con successo")
        else:
            print("La tabella stages contiene già dati, inizializzazione saltata")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inizializzazione dei palchi: {e}")
        success = False

    try:
        cursor.execute("SELECT COUNT(*) FROM genres")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO genres (name) VALUES (?)",
                [(genre,) for genre in default_genres],
            )
            print("Generi musicali inizializzati con successo")
        else:
            print("La tabella genres contiene già dati, inizializzazione saltata")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inizializzazione dei generi: {e}")
        success = False

    try:
        cursor.execute("SELECT COUNT(*) FROM ticket_types")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO ticket_types (name, description, price, days_count) VALUES (?, ?, ?, ?)",
                default_ticket_types,
            )
            print("Tipi di biglietti inizializzati con successo")
        else:
            print("La tabella ticket_types contiene già dati, inizializzazione saltata")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inizializzazione dei tipi di biglietti: {e}")
        success = False

    conn.commit()
    cursor.close()
    conn.close()

    if success and not initialize_default_users():
        print("Errore durante l'inizializzazione degli utenti.")
        success = False

    if success and not initialize_default_performances():
        print("Errore durante l'inizializzazione delle performance.")
        success = False
    
    if success and not initialize_default_tickets():
        print("Errore durante l'inizializzazione dei biglietti.")
        success = False

    return success


def initialize_default_users():
    """
    Crea gli utenti di default nel database.
    """
    if not check_db_exists():
        print("Database non trovato. Crea prima la struttura del database.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]

    if users_count > 0:
        print(
            f"Ci sono già {users_count} utenti nel database. Inizializzazione utenti saltata."
        )
        cursor.close()
        conn.close()
        return True

    os.makedirs(f"{ROOT_PATH}static/images/pfp", exist_ok=True)

    insert_query = """
    INSERT INTO users (username, name, surname, email, password, pfp, role)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    inserted_users = 0
    success = True

    try:
        for user in default_users:
            username, name, surname, email, plain_password, pfp, role = user

            password_hash = generate_password_hash(plain_password, method="scrypt")

            cursor.execute(
                insert_query,
                (
                    username.lower(),
                    name,
                    surname,
                    email.lower(),
                    password_hash,
                    pfp,
                    role,
                ),
            )
            inserted_users += 1

        conn.commit()
        print(f"Inizializzati {inserted_users} utenti di default con successo")

    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inizializzazione degli utenti: {e}")
        success = False

    finally:
        cursor.close()
        conn.close()

    return success


def initialize_default_performances():
    """
    Inizializza le performance predefinite nel database
    """
    if not check_db_exists():
        print("Database non trovato. Crea prima la struttura del database.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    success = True

    try:
        cursor.execute("SELECT COUNT(*) FROM performances")
        if cursor.fetchone()[0] == 0:
            os.makedirs(f"{ROOT_PATH}static/images/performances", exist_ok=True)

            cursor.execute("DELETE FROM sqlite_sequence WHERE name='performances'")

            cursor.executemany(
                """INSERT INTO performances 
                (id, artist_name, start_time, duration, description, image_path, 
                day_id, stage_id, genre_id, organizer_id, is_published, 
                created_at, updated_at, is_featured) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                default_performances,
            )
            print("Performance inizializzate con successo")
        else:
            print("La tabella performances contiene già dati, inizializzazione saltata")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inizializzazione delle performance: {e}")
        success = False

    conn.commit()
    cursor.close()
    conn.close()

    return success


def initialize_default_tickets():
    """
    Inizializza i biglietti predefiniti nel database
    """
    if not check_db_exists():
        print("Database non trovato. Crea prima la struttura del database.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    success = True

    try:
        cursor.execute("SELECT COUNT(*) FROM tickets")
        if cursor.fetchone()[0] == 0:
            # Resetta la sequenza per permettere ID specifici
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='tickets'")
            
            # Inserisci i biglietti
            cursor.executemany(
                """INSERT INTO tickets 
                (id, user_id, ticket_type_id, purchase_date, is_valid, 
                friday, saturday, sunday) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                default_tickets
            )
            print("Biglietti inizializzati con successo")
        else:
            print("La tabella tickets contiene già dati, inizializzazione saltata")
    except Exception as e:
        conn.rollback()
        print(f"Errore durante l'inizializzazione dei biglietti: {e}")
        success = False

    conn.commit()
    cursor.close()
    conn.close()

    return success


def drop_tables():
    """
    Elimina tutte le tabelle del database
    """
    if not check_db_exists():
        print("Database non trovato.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = OFF")

    success = True
    for table_name in reversed(table_names):
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Tabella {table_name} eliminata con successo")
        except Exception as e:
            print(f"Errore durante l'eliminazione della tabella {table_name}: {e}")
            success = False

    cursor.execute("PRAGMA foreign_keys = ON")

    conn.commit()
    cursor.close()
    conn.close()

    return success


def truncate_tables():
    """
    Svuota tutte le tabelle del database mantenendo la struttura
    """
    if not check_db_exists():
        print("Database non trovato.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = OFF")

    success = True
    for table_name in reversed(table_names):
        try:
            cursor.execute(f"DELETE FROM {table_name}")
            print(f"Tabella {table_name} svuotata con successo")
        except Exception as e:
            print(f"Errore durante lo svuotamento della tabella {table_name}: {e}")
            success = False

    cursor.execute("PRAGMA foreign_keys = ON")

    conn.commit()
    cursor.close()
    conn.close()

    return success


def reset_auto_increment():
    """
    Resetta i contatori di auto-incremento per tutte le tabelle
    """
    if not check_db_exists():
        print("Database non trovato.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    success = True
    for table_name in table_names:
        try:
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")
            print(f"Contatore auto-incremento per {table_name} resettato con successo")
        except Exception as e:
            print(f"Errore durante il reset del contatore per {table_name}: {e}")
            success = False

    conn.commit()
    cursor.close()
    conn.close()

    return success


def count_records():
    """
    Conta il numero di record in ogni tabella
    """
    if not check_db_exists():
        print("Database non trovato.")
        return False

    conn = sqlite3.connect(ROOT_PATH + DB_PATH)
    cursor = conn.cursor()

    print("\nNumero di record per tabella:")
    print("-" * 40)

    for table_name in table_names:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"{table_name}: {count} record")
        except Exception as e:
            print(f"{table_name}: Errore - {e}")

    print("-" * 40)

    cursor.close()
    conn.close()
    return True


def backup_database():
    """
    Crea un backup del database
    """
    if not check_db_exists():
        print("Database non trovato.")
        return False

    backup_dir = "db/backup"
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{backup_dir}/sonosphere_backup_{timestamp}.db"

    try:
        with open(ROOT_PATH + DB_PATH, "rb") as src, open(backup_path, "wb") as dst:
            dst.write(src.read())

        print(f"Backup creato con successo: {backup_path}")
        print(f"Backup creato: {backup_path}")
        return True
    except Exception as e:
        print(f"Errore durante la creazione del backup: {e}")
        return False


def restore_database():
    """
    Ripristina un backup del database
    """
    backup_dir = "db/backup"

    if not os.path.exists(backup_dir):
        print("Directory di backup non trovata.")
        return False

    backups = [
        f
        for f in os.listdir(backup_dir)
        if f.startswith("sonosphere_backup_") and f.endswith(".db")
    ]

    if not backups:
        print("Nessun backup trovato.")
        return False

    print("\nBackup disponibili:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")

    choice = input(
        "\nSeleziona il numero del backup da ripristinare (0 per annullare): "
    )

    try:
        choice = int(choice)
        if choice == 0:
            return False
        if choice < 1 or choice > len(backups):
            print("Scelta non valida.")
            return False

        selected_backup = backups[choice - 1]
        backup_path = f"{backup_dir}/{selected_backup}"

        if check_db_exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pre_restore_backup = f"{backup_dir}/pre_restore_{timestamp}.db"
            with open(ROOT_PATH + DB_PATH, "rb") as src, open(
                pre_restore_backup, "wb"
            ) as dst:
                dst.write(src.read())
            print(f"Backup pre-ripristino creato: {pre_restore_backup}")

        with open(backup_path, "rb") as src, open(ROOT_PATH + DB_PATH, "wb") as dst:
            dst.write(src.read())

        print(f"Database ripristinato dal backup: {selected_backup}")
        print(f"Database ripristinato con successo dal backup: {selected_backup}")
        return True
    except ValueError:
        print("Input non valido.")
        return False
    except Exception as e:
        print(f"Errore durante il ripristino del backup: {e}")
        return False


def print_menu():
    """
    Stampa il menu principale
    """
    print("\n" + "=" * 60)
    print("SONOSPHERE DATABASE MANAGER".center(60))
    print("=" * 60)

    print("\nOPERAZIONI DISPONIBILI:")
    print("1. Crea struttura del database (tabelle)")
    print("2. Popola database con dati predefiniti")
    print("3. Inizializza utenti predefiniti")
    print("4. Elimina tutte le tabelle")
    print("5. Svuota tutte le tabelle (mantiene struttura)")
    print("6. Reset contatori auto-incremento")
    print("7. Visualizza conteggio record")
    print("8. Crea backup del database")
    print("9. Ripristina database da backup")
    print("10. Inizializzazione completa (crea + popola + utenti)")
    print("0. Esci")

    print("\nStato database:", end=" ")
    if check_db_exists():
        print("PRESENTE ✓")
    else:
        print("NON PRESENTE ✗")


def main():
    """
    Funzione principale interattiva
    """
    while True:
        print_menu()

        choice = input("\nSeleziona un'operazione [0-10]: ")

        if choice == "1":
            print("\nCreazione struttura del database...")
            if create_database_structure():
                print("Struttura del database creata con successo!")
            else:
                print("Si sono verificati errori durante la creazione della struttura.")

        elif choice == "2":
            print("\nPopolamento database con dati predefiniti...")
            if initialize_default_data():
                print("Database popolato con successo!")
            else:
                print("Si sono verificati errori durante il popolamento del database.")

        elif choice == "3":
            print("\nInizializzazione utenti predefiniti...")
            if initialize_default_users():
                print("Utenti inizializzati con successo!")
            else:
                print(
                    "Si sono verificati errori durante l'inizializzazione degli utenti."
                )

        elif choice == "4":
            confirm = input(
                "\nATTENZIONE: Questa operazione eliminerà tutte le tabelle e i dati.\nSei sicuro di voler procedere? (s/n): "
            )
            if confirm.lower() == "s":
                if drop_tables():
                    print("Tutte le tabelle sono state eliminate con successo!")
                else:
                    print(
                        "Si sono verificati errori durante l'eliminazione delle tabelle."
                    )

        elif choice == "5":
            confirm = input(
                "\nATTENZIONE: Questa operazione svuoterà tutte le tabelle.\nSei sicuro di voler procedere? (s/n): "
            )
            if confirm.lower() == "s":
                if truncate_tables():
                    print("Tutte le tabelle sono state svuotate con successo!")
                else:
                    print(
                        "Si sono verificati errori durante lo svuotamento delle tabelle."
                    )

        elif choice == "6":
            if reset_auto_increment():
                print("Contatori auto-incremento resettati con successo!")
            else:
                print("Si sono verificati errori durante il reset dei contatori.")

        elif choice == "7":
            count_records()

        elif choice == "8":
            if backup_database():
                print("Backup completato con successo!")
            else:
                print("Si sono verificati errori durante la creazione del backup.")

        elif choice == "9":
            if not restore_database():
                print("Ripristino annullato o non riuscito.")

        elif choice == "10":
            print("\nInizializzazione completa del database...")

            success = True

            print("1. Creazione struttura...")
            if not create_database_structure():
                print("Errore durante la creazione della struttura!")
                success = False

            if success:
                print("2. Popolamento dati predefiniti...")
                if not initialize_default_data():
                    print("Errore durante il popolamento dei dati!")
                    success = False

            if success:
                print("\nInizializzazione completa terminata con successo!")
            else:
                print("\nL'inizializzazione completa ha incontrato errori.")

        elif choice == "0":
            print("\nUscita dal programma. Arrivederci!")
            break

        else:
            print("\nScelta non valida. Riprova.")

        input("\nPremi INVIO per continuare...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperazione interrotta. Uscita dal programma.")
        sys.exit(0)
