# Esame 16/06/2025

[https://elite.polito.it/teaching/01dxu-iaw/esame](https://elite.polito.it/teaching/01dxu-iaw/esame)

[https://docs.google.com/document/d/1P5qTU0oU2jlxHHxbXlDaB2t9CdrUOKS0w3HIMpGg9QY/edit?usp=sharing](https://docs.google.com/document/d/1P5qTU0oU2jlxHHxbXlDaB2t9CdrUOKS0w3HIMpGg9QY/edit?usp=sharing)

## Requisiti
<!-- TODO: commentare il codice -->

## Design

### DB

- **Giorni**:
  - id
  - nome giorno
  - data
  - numero di partecipanti
  - massimo partecipanti
  - ora inizio
  - ora fine
  
  ```sql
  CREATE TABLE "event_days" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "date" TEXT NOT NULL,
    "current_attendees" INTEGER NOT NULL DEFAULT 0,
    "max_attendees" INTEGER NOT NULL DEFAULT 200,
    "start_time" TEXT NOT NULL,
    "end_time" TEXT NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
  )
  ```

- **Utenti**:
  - id
  - nome utente
  - nome
  - cognome
  - email
  - password
  - ruolo (organizzatore, partecipante)
  - pfp
  
  ```sql
  CREATE TABLE "users" (
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
  ```

- **Palchi**:
  - id
  - nome palco
  - descrizione
  - immagine
  
  ```sql
  CREATE TABLE "stages" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "image" TEXT NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
  )
  ```

- **Generi Musicali**:
  - id
  - nome genere
  
  ```sql
  CREATE TABLE "genres" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT)
  )
  ```

- **Performance**:
  - id
  - nome artista/gruppo
  - giorno (venerdì, sabato, domenica)
  - ora inizio
  - durata in minuti
  - descrizione breve
  - palco
  - genere musicale
  - immagini promozionali
  - stato di pubblicazione (pubblicata/bozza)
  - organizzatore
  - timestamp creazione
  - timestamp aggiornamento
  - featured (se famoso/da mostrare in homepage)
  
  ```sql
  CREATE TABLE "performances" (
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
  ```

- **Tipi Biglietti**:
  - id
  - nome tipo biglietto (Giornaliero, Pass 2 Giorni, Full Pass)
  - descrizione
  - prezzo
  - numero di giorni inclusi (1, 2 o 3)

  ```sql
  CREATE TABLE "ticket_types" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT,
    "price" REAL NOT NULL,
    "days_count" INTEGER NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
  )
  ```

- **Biglietti**:
  - id
  - id utente (partecipante)
  - id tipo biglietto
  - data acquisto
  - giorno evento
  - validità
  - venerdì
  - sabato
  - domenica
  
  ```sql
  CREATE TABLE "tickets" (
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
  ```

## Utenti disponibili

### Organizzatori (nomi utente - password)

- **Organizzatore 1**: musicmaestro - Admin2025!
- **Organizzatore 2**: soundwizard - Stage2025!
- **Organizzatore 3**: beatmaker - Plan2025!
- **Organizzatore 4**: rhythmking - Music2025!

### Partecipanti (nomi utente - password)

- **Partecipante 1**: music_fan - Fan2025!
- **Partecipante 2**: rock_lover - Rock2025!
- **Partecipante 3**: pop_enthusiast - Pop2025!
- **Partecipante 4**: festival_goer - Fest2025!
- **Partecipante 5**: concert_junkie - Concert2025!

## Indirizzo pubblico

[https://bunz.pythonanywhere.com](https://bunz.pythonanywhere.com)
