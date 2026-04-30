from datetime import datetime
from typing import Optional


DEFAULT_WELCOME_SUBJECT = "Dziękujemy za kontakt"
DEFAULT_WELCOME_BODY = (
    "Dzień dobry {name},\n\n"
    "Dziękuję za kontakt. Czy mogę doprecyzować:\n"
    "- budżet?\n"
    "- lokalizację?\n\n"
    "Odpowiem jak najszybciej.\n\n"
    "Pozdrawiam,\n{company}"
)
DEFAULT_FOLLOWUP_1_SUBJECT = "Przypomnienie: czy temat jest nadal aktualny?"
DEFAULT_FOLLOWUP_1_BODY = (
    "Dzień dobry {name},\n\n"
    "wracam do zapytania – czy temat jest nadal aktualny?\n\n"
    "Jeśli tak, chętnie przygotuję pierwsze propozycje.\n\n"
    "Pozdrawiam,\n{company}"
)
DEFAULT_FOLLOWUP_2_SUBJECT = "Drugie przypomnienie: mogę przesłać dopasowane oferty"
DEFAULT_FOLLOWUP_2_BODY = (
    "Dzień dobry {name},\n\n"
    "jeśli nadal poszukuje Pan nieruchomości, mogę podesłać dopasowane oferty.\n\n"
    "Daj proszę znać, czy mogę przygotować więcej propozycji.\n\n"
    "Pozdrawiam,\n{company}"
)


def render_template(template: Optional[str], default_template: str, name: str, company: str) -> str:
    text = template or default_template
    return text.format(name=name, company=company or "Zespół")


def sheet_row_for_lead(email: str, name: str, source: str, message: str) -> list[str]:
    return [
        datetime.utcnow().isoformat(),
        email,
        name,
        source,
        message,
    ]
