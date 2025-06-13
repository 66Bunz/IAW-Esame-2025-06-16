from flask_login import UserMixin


class User(UserMixin):
    """
    Rappresenta un utente del sistema.

    Attributes:
        id (int): ID univoco dell'utente.
        username (str): Nome utente.
        password (str): Password dell'utente.
        name (str): Nome reale dell'utente.
        surname (str): Cognome dell'utente.
        email (str): Indirizzo email dell'utente.
        pfp (str): Percorso del profilo dell'utente.
        role (str): Ruolo dell'utente
    """

    def __init__(
        self,
        id: int,
        username: str,
        password: str,
        name: str,
        surname: str,
        email: str,
        pfp: str,
        role: str,
    ) -> None:

        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.pfp = pfp
        self.role = role
