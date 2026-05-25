"""
Mapeo de las 73 variables de la ECP 2023 (DANE) usadas por el modelo.

Cada entrada incluye:
- label: pregunta legible en español
- section: agrupador temático para el formulario
- options: dict {valor_código: texto_legible}  (None = input numérico libre)
- default: valor por defecto sensible

Escalas estándar reutilizadas:
- SI_NO: 1=Sí, 2=No
- CONFIANZA_5: 1=Mucha, 2=Algo, 3=Poca, 4=Ninguna, 5=No conoce
- ACUERDO_5: 1=Totalmente de acuerdo ... 5=Totalmente en desacuerdo
- NS_NR: 99=No sabe / No responde
"""

SI_NO = {1: "Sí", 2: "No"}
SI_NO_NSR = {1: "Sí", 2: "No", 99: "No sabe/No responde"}
CONFIANZA_5 = {
    1: "Mucha confianza",
    2: "Alguna confianza",
    3: "Poca confianza",
    4: "Ninguna confianza",
    5: "No conoce",
    99: "No sabe/No responde",
}
ACUERDO_5 = {
    1: "Totalmente de acuerdo",
    2: "De acuerdo",
    3: "Ni de acuerdo ni en desacuerdo",
    4: "En desacuerdo",
    5: "Totalmente en desacuerdo",
    99: "No sabe/No responde",
}

SEXO = {1: "Hombre", 2: "Mujer"}

ESTADO_CIVIL = {
    1: "Unión libre (<2 años)",
    2: "Unión libre (2+ años)",
    3: "Casado(a)",
    4: "Separado(a)/Divorciado(a)",
    5: "Viudo(a)",
    6: "Soltero(a)",
}

NIVEL_EDUC = {
    1: "Ninguno",
    2: "Preescolar",
    3: "Básica primaria",
    4: "Básica secundaria",
    5: "Media",
    6: "Técnico/Tecnológico",
    7: "Universitario/Posgrado",
    99: "No sabe/No responde",
}

ESTRATO = {i: f"Estrato {i}" for i in range(1, 11)}
ESTRATO[99] = "No sabe/No responde"

INTERES_POLITICA = {
    1: "Mucho",
    2: "Algo",
    3: "Poco",
    4: "Nada",
    5: "No sabe",
}

SATISFACCION_5 = {
    1: "Muy satisfecho",
    2: "Satisfecho",
    3: "Ni satisfecho ni insatisfecho",
    4: "Insatisfecho",
    5: "Muy insatisfecho",
    99: "No sabe/No responde",
}

IDEAL_GOBIERNO = {
    1: "La democracia es preferible a cualquier otra forma de gobierno",
    2: "Da igual un régimen democrático que uno no democrático",
    3: "En algunas circunstancias un gobierno autoritario puede ser preferible",
    99: "No sabe/No responde",
}


FEATURES = {
    # ============ Demografía / sociodemográficas ============
    "P220": {
        "label": "Sexo",
        "section": "Demografía",
        "options": SEXO,
        "default": 1,
    },
    "P2057": {
        "label": "¿Se considera campesino(a)?",
        "section": "Demografía",
        "options": SI_NO_NSR,
        "default": 2,
    },
    "P605": {
        "label": "Estado civil",
        "section": "Demografía",
        "options": ESTADO_CIVIL,
        "default": 6,
    },
    "P6210": {
        "label": "Nivel educativo más alto alcanzado",
        "section": "Demografía",
        "options": NIVEL_EDUC,
        "default": 5,
    },
    "P6945": {
        "label": "Estrato de la vivienda",
        "section": "Demografía",
        "options": ESTRATO,
        "default": 2,
    },
    "P3039": {
        "label": "Interés en la política",
        "section": "Demografía",
        "options": INTERES_POLITICA,
        "default": 3,
    },

    # ============ Participación en organizaciones (P2001S*) ============
    "P2001S1": {
        "label": "¿Participa en juntas de acción comunal?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S2": {
        "label": "¿Participa en organizaciones religiosas?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S3": {
        "label": "¿Participa en organizaciones de caridad?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S4": {
        "label": "¿Participa en sindicatos?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S17": {
        "label": "¿Participa en organizaciones LGBTIQ+?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S7": {
        "label": "¿Participa en organizaciones culturales/artísticas?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S12": {
        "label": "¿Participa en organizaciones ambientales?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S13": {
        "label": "¿Participa en organizaciones de víctimas?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S14": {
        "label": "¿Participa en organizaciones de mujeres?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S15": {
        "label": "¿Participa en organizaciones étnicas?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S18": {
        "label": "¿Participa en colectivos juveniles?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2001S10": {
        "label": "¿Participa en partidos o movimientos políticos?",
        "section": "Participación en organizaciones",
        "options": SI_NO, "default": 2,
    },

    # ============ Confianza en organizaciones (P2003S*) ============
    "P2003S4": {
        "label": "Confía en los sindicatos",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2003S17": {
        "label": "Confía en las organizaciones LGBTIQ+",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2003S7": {
        "label": "Confía en las organizaciones culturales/artísticas",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 1,
    },
    "P2003S10": {
        "label": "Confía en los partidos o movimientos políticos",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 2,
    },
    "P2003S12": {
        "label": "Confía en las organizaciones ambientales",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 1,
    },
    "P2003S13": {
        "label": "Confía en las organizaciones de víctimas",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 1,
    },
    "P2003S14": {
        "label": "Confía en las organizaciones de mujeres",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 1,
    },
    "P2003S15": {
        "label": "Confía en las organizaciones étnicas",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 1,
    },
    "P2003S18": {
        "label": "Confía en los colectivos juveniles",
        "section": "Confianza en organizaciones",
        "options": SI_NO, "default": 1,
    },

    # ============ Participación electoral (P5373S*) ============
    "P5373S4": {
        "label": "¿Votó en la última elección presidencial?",
        "section": "Participación electoral",
        "options": SI_NO, "default": 1,
    },
    "P5373S5": {
        "label": "¿Votó en las elecciones de Congreso?",
        "section": "Participación electoral",
        "options": SI_NO, "default": 1,
    },
    "P5373S6": {
        "label": "¿Votó en las elecciones locales (alcalde/gobernador)?",
        "section": "Participación electoral",
        "options": SI_NO, "default": 1,
    },

    # ============ Mecanismos de participación (P5306S*) ============
    "P5306S1": {
        "label": "¿Ha firmado peticiones o cartas a autoridades?",
        "section": "Mecanismos de participación",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5306S2": {
        "label": "¿Ha participado en marchas o manifestaciones pacíficas?",
        "section": "Mecanismos de participación",
        "options": SI_NO_NSR, "default": 2,
    },

    # ============ Democracia ============
    "P2019": {
        "label": "Satisfacción con el funcionamiento de la democracia en Colombia",
        "section": "Percepción de democracia",
        "options": SATISFACCION_5, "default": 4,
    },

    # ============ Confianza en instituciones (P2016S*) ============
    "P2016S1": {
        "label": "Confianza en el Presidente",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 3,
    },
    "P2016S2": {
        "label": "Confianza en el Congreso",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 4,
    },
    "P2016S3": {
        "label": "Confianza en el sistema judicial",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 3,
    },
    "P2016S4": {
        "label": "Confianza en los partidos políticos",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 4,
    },
    "P2016S5": {
        "label": "Confianza en la Policía Nacional",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 3,
    },
    "P2016S6": {
        "label": "Confianza en las Fuerzas Militares",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 2,
    },
    "P2016S7": {
        "label": "Confianza en la Iglesia",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 2,
    },
    "P2016S8": {
        "label": "Confianza en los medios de comunicación",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 3,
    },
    "P2016S9": {
        "label": "Confianza en las organizaciones sociales",
        "section": "Confianza institucional",
        "options": CONFIANZA_5, "default": 3,
    },

    # ============ Acuerdos políticos (P2017S*) ============
    "P2017S1": {
        "label": "¿Está de acuerdo con que las mujeres participen en política?",
        "section": "Actitudes políticas",
        "options": SI_NO_NSR, "default": 1,
    },
    "P2017S2": {
        "label": "¿Está de acuerdo con que los jóvenes participen en política?",
        "section": "Actitudes políticas",
        "options": SI_NO_NSR, "default": 1,
    },
    "P2017S3": {
        "label": "¿Está de acuerdo con la participación de población LGBTIQ+ en política?",
        "section": "Actitudes políticas",
        "options": SI_NO_NSR, "default": 1,
    },
    "P2017S4": {
        "label": "¿Está de acuerdo con la participación de grupos étnicos en política?",
        "section": "Actitudes políticas",
        "options": SI_NO_NSR, "default": 1,
    },
    "P2017S5": {
        "label": "¿Está de acuerdo con la participación de personas con discapacidad en política?",
        "section": "Actitudes políticas",
        "options": SI_NO_NSR, "default": 1,
    },
    "P2017S6": {
        "label": "¿Está de acuerdo con la participación de víctimas del conflicto en política?",
        "section": "Actitudes políticas",
        "options": SI_NO_NSR, "default": 1,
    },
    "P2017S7": {
        "label": "¿Está de acuerdo con la participación de excombatientes en política?",
        "section": "Actitudes políticas",
        "options": SI_NO_NSR, "default": 2,
    },

    # ============ Preferencias de gobierno ============
    "P2021": {
        "label": "Forma de gobierno preferida",
        "section": "Percepción de democracia",
        "options": IDEAL_GOBIERNO, "default": 1,
    },
    "P1754": {
        "label": "¿Cómo califica la situación económica actual de su hogar?",
        "section": "Percepción económica",
        "options": {
            1: "Buena",
            2: "Regular",
            3: "Mala",
            99: "No sabe/No responde",
        },
        "default": 2,
    },

    # ============ Información política (P5376S*) ============
    "P5376S1": {
        "label": "¿Se informa sobre política por televisión?",
        "section": "Fuentes de información",
        "options": SI_NO, "default": 1,
    },
    "P5376S2": {
        "label": "¿Se informa sobre política por radio?",
        "section": "Fuentes de información",
        "options": SI_NO, "default": 2,
    },
    "P5376S3": {
        "label": "¿Se informa sobre política por prensa escrita?",
        "section": "Fuentes de información",
        "options": SI_NO, "default": 2,
    },
    "P5376S4": {
        "label": "¿Se informa sobre política por redes sociales?",
        "section": "Fuentes de información",
        "options": SI_NO, "default": 1,
    },
    "P5376S5": {
        "label": "¿Se informa sobre política por internet (portales/blogs)?",
        "section": "Fuentes de información",
        "options": SI_NO, "default": 1,
    },
    "P5376S6": {
        "label": "¿Se informa sobre política por conversaciones con familiares/amigos?",
        "section": "Fuentes de información",
        "options": SI_NO, "default": 1,
    },

    # ============ Identificación y simpatía política (P5317S*) ============
    "P5317S4": {
        "label": "¿Se identifica con algún partido o movimiento político?",
        "section": "Identidad política",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5317S5": {
        "label": "¿Ha trabajado para algún partido o candidato?",
        "section": "Identidad política",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5317S1": {
        "label": "¿Asiste a reuniones políticas o mítines?",
        "section": "Identidad política",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5317S9": {
        "label": "¿Ha contactado autoridades por algún problema público?",
        "section": "Identidad política",
        "options": SI_NO_NSR, "default": 2,
    },

    # ============ Participación cívica (P5307S*) ============
    "P5307S1": {
        "label": "¿Conoce los mecanismos de participación ciudadana?",
        "section": "Cultura cívica",
        "options": SI_NO, "default": 2,
    },
    "P5307S2": {
        "label": "¿Conoce el derecho de petición?",
        "section": "Cultura cívica",
        "options": SI_NO, "default": 1,
    },
    "P5307S3": {
        "label": "¿Conoce las veedurías ciudadanas?",
        "section": "Cultura cívica",
        "options": SI_NO, "default": 2,
    },
    "P5307S4": {
        "label": "¿Conoce los cabildos abiertos?",
        "section": "Cultura cívica",
        "options": SI_NO, "default": 2,
    },
    "P5307S5": {
        "label": "¿Conoce los referendos o consultas populares?",
        "section": "Cultura cívica",
        "options": SI_NO, "default": 2,
    },

    # ============ Valores sociales (P5314S*) ============
    "P5314S2": {
        "label": "¿Está de acuerdo con la igualdad de derechos para parejas del mismo sexo?",
        "section": "Valores sociales",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5314S3": {
        "label": "¿Está de acuerdo con la adopción por parejas del mismo sexo?",
        "section": "Valores sociales",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5314S4": {
        "label": "¿Está de acuerdo con la despenalización del aborto?",
        "section": "Valores sociales",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5314S5": {
        "label": "¿Está de acuerdo con la legalización de drogas recreativas?",
        "section": "Valores sociales",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5314S6": {
        "label": "¿Está de acuerdo con la eutanasia?",
        "section": "Valores sociales",
        "options": SI_NO_NSR, "default": 2,
    },
    "P5314S7": {
        "label": "¿Está de acuerdo con el matrimonio igualitario?",
        "section": "Valores sociales",
        "options": SI_NO_NSR, "default": 2,
    },

    # ============ Otra ============
    "P2009S9": {
        "label": "¿Cree que la corrupción ha aumentado en los últimos años?",
        "section": "Percepción institucional",
        "options": SI_NO_NSR, "default": 1,
    },
}


SECTION_ORDER = [
    "Demografía",
    "Percepción económica",
    "Percepción de democracia",
    "Confianza institucional",
    "Percepción institucional",
    "Identidad política",
    "Participación electoral",
    "Mecanismos de participación",
    "Participación en organizaciones",
    "Confianza en organizaciones",
    "Actitudes políticas",
    "Valores sociales",
    "Fuentes de información",
    "Cultura cívica",
]


FEATURE_ORDER = [
    "P220", "P2057", "P605", "P6210", "P6945", "P3039",
    "P2001S1", "P2001S2", "P2001S3", "P2001S4", "P2001S17", "P2001S7",
    "P2001S12", "P2001S13", "P2001S14", "P2001S15", "P2001S18",
    "P2003S4", "P2001S10", "P2003S17", "P2003S7", "P2003S10",
    "P2003S12", "P2003S13", "P2003S14", "P2003S15", "P2003S18",
    "P5373S4", "P5373S5", "P5373S6",
    "P5306S1", "P5306S2",
    "P2019",
    "P2016S1", "P2016S2", "P2016S3", "P2016S4", "P2016S5",
    "P2016S6", "P2016S7", "P2016S8", "P2016S9",
    "P2017S1", "P2017S2", "P2017S3", "P2017S4", "P2017S5", "P2017S6",
    "P2021", "P1754",
    "P5376S1", "P5376S2", "P5376S3", "P5376S4", "P5376S5", "P5376S6",
    "P5317S4", "P5317S5",
    "P5307S1", "P5307S2", "P5307S3", "P5307S4", "P5307S5",
    "P2017S7",
    "P5314S2", "P5314S3", "P5314S4", "P5314S5", "P5314S6", "P5314S7",
    "P5317S1", "P5317S9", "P2009S9",
]


def get_default_row() -> dict:
    return {code: meta["default"] for code, meta in FEATURES.items()}


def get_sections() -> dict:
    sections = {s: [] for s in SECTION_ORDER}
    for code in FEATURE_ORDER:
        sec = FEATURES[code]["section"]
        sections.setdefault(sec, []).append(code)
    return sections
