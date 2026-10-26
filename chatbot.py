# Chatbot basado en reglas para consultas sobre discrepancias de impresiones
# Python 3.10 o superior y NLTK

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)


# ---------------------------------------------------------------
# 1. Preprocesamiento del texto
# ---------------------------------------------------------------
def quitar_acentos(texto):
    cambios = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u"}
    for letra in cambios:
        texto = texto.replace(letra, cambios[letra])
    return texto


stemmer = SnowballStemmer("spanish")
palabras_vacias = [quitar_acentos(p) for p in stopwords.words("spanish")]


def preprocesar(texto):
    # minusculas, sin acentos, tokenizar, quitar stopwords y sacar la raiz
    texto = quitar_acentos(texto.lower())
    tokens = word_tokenize(texto, language="spanish")
    raices = []
    for t in tokens:
        if t.isalnum() and t not in palabras_vacias:
            raices.append(stemmer.stem(t))
    return raices


# ---------------------------------------------------------------
# 2. Base de conocimiento: palabras clave y respuesta de cada intencion
# ---------------------------------------------------------------
base_conocimiento = {
    "saludo": {
        "palabras": ["hola", "buenas", "buenos", "dias", "tardes", "noches", "saludos", "hey"],
        "respuesta": "¡Hola! Soy el asistente de discrepancias de impresiones. Puedo explicarte "
                     "qué es una discrepancia, sus causas, qué porcentaje es normal y qué datos "
                     "reunir para abrir un ticket. ¿Qué necesitas?",
    },
    "ayuda": {
        "palabras": ["ayuda", "ayudar", "puedes", "funciones", "haces", "eres", "menu", "opciones"],
        "respuesta": "Puedo ayudarte con: (1) qué es una discrepancia de impresiones, (2) causas "
                     "comunes, (3) porcentaje aceptable, (4) diferencia entre verificadores y DSP, "
                     "(5) datos para abrir un ticket (o armar el resumen contigo, escribe 'guíame'), "
                     "(6) cómo escalar y (7) tiempos de respuesta.",
    },
    "definicion": {
        "palabras": ["discrepancia", "definicion", "significa", "concepto", "explica", "explicar", "entender"],
        "respuesta": "Una discrepancia de impresiones es la diferencia entre el número de impresiones "
                     "que reporta un sistema (por ejemplo, el ad server o la plataforma propia) y el "
                     "que reporta otro (el DSP o un verificador externo) para la misma campaña y "
                     "periodo. Que existan diferencias es normal; lo importante es saber si están "
                     "dentro de un margen razonable.",
    },
    "causas": {
        "palabras": ["causa", "causas", "motivo", "razon", "porque", "origen", "coinciden", "cuadran",
                     "difieren", "distintos", "distintas", "ivt", "latencia", "provoca", "genera"],
        "respuesta": "Causas comunes: (1) definiciones distintas de 'impresión' (al servir, al "
                     "renderizar o al ser visible); (2) filtrado de tráfico inválido (IVT) en un "
                     "sistema y no en el otro; (3) latencia o abandono antes de que el anuncio cargue; "
                     "(4) zonas horarias o cortes de reporte diferentes; (5) bloqueadores de anuncios "
                     "o fallas en la etiqueta de medición.",
    },
    "porcentaje": {
        "palabras": ["porcentaje", "aceptable", "normal", "margen", "tolerancia", "limite", "umbral",
                     "rango", "excesiva"],
        "respuesta": "Como referencia general en la industria, una diferencia de hasta ~10% entre "
                     "sistemas suele considerarse normal. Aun así, el umbral exacto depende del "
                     "acuerdo con el cliente y del tipo de medición, así que úsalo como guía y no "
                     "como regla. Si pasa de ese margen, conviene abrir un ticket con los datos de "
                     "la campaña.",
    },
    "verificacion_vs_dsp": {
        "palabras": ["ias", "dv", "doubleverify", "verificacion", "verificador", "verificadores", "dsp",
                     "tercero", "terceros", "etiqueta", "tag", "viewability", "visibilidad", "dv360", "ttd"],
        "respuesta": "El DSP (por ejemplo DV360 o The Trade Desk) cuenta lo que compró y sirvió; un "
                     "verificador de terceros (como IAS o DV) mide lo que ocurrió en la página "
                     "mediante una etiqueta propia. Como cada uno mide en un momento y con reglas "
                     "distintas, sus números casi nunca coinciden al 100%. Para comparar, usa el "
                     "mismo periodo y la misma definición de impresión.",
    },
    "datos_ticket": {
        "palabras": ["ticket", "datos", "informacion", "adjuntar", "abrir", "reportar", "reporte",
                     "caso", "solicitud", "enviar", "incluir"],
        "respuesta": "Para abrir un ticket completo reúne: (1) plataforma o DSP involucrado, (2) rango "
                     "de fechas, (3) impresiones según tu plataforma, (4) impresiones según la otra "
                     "plataforma o verificador, (5) ID de campaña o deal y (6) una captura del "
                     "reporte. Si quieres, escribe 'guíame' y armamos el resumen paso a paso.",
    },
    "escalamiento": {
        "palabras": ["escalar", "escalamiento", "contacto", "contactar", "urgente", "urgencia", "humano",
                     "persona", "hablar", "techops", "responsable", "supervisor"],
        "respuesta": "Si es urgente (por ejemplo, una campaña en vuelo con una diferencia muy alta), "
                     "abre el ticket marcándolo como urgente y avisa al equipo de TechOps por el "
                     "canal de soporte interno. Para casos no urgentes basta con el ticket; el equipo "
                     "lo priorizará según la fecha de fin de la campaña.",
    },
    "tiempos": {
        "palabras": ["tiempo", "tiempos", "tardan", "tarda", "demora", "demoran", "sla", "plazo",
                     "responden", "respuesta"],
        "respuesta": "Los tiempos dependen de la prioridad y de que el ticket llegue con la "
                     "información completa. En general, un ticket completo se atiende más rápido "
                     "porque evita preguntas de seguimiento. Para tiempos exactos, consulta el "
                     "acuerdo de servicio vigente de tu equipo.",
    },
    "despedida": {
        "palabras": ["gracias", "adios", "chao", "bye", "perfecto", "excelente", "listo", "entendido"],
        "respuesta": "¡Con gusto! Si surge otra duda sobre discrepancias, aquí estaré. ¡Hasta pronto!",
    },
    "inicio_guia": {
        "palabras": ["guiame", "guiar", "guia", "paso", "pasos", "armar", "preparar", "resumen", "ayudame"],
        "respuesta": "",  # esta intencion inicia el flujo guiado
    },
}

mensaje_fallback = ("No estoy seguro de haber entendido. Puedo ayudarte con: definición de "
                    "discrepancia, causas, porcentaje aceptable, IAS/DV vs DSP, datos para un "
                    "ticket, escalamiento o tiempos de respuesta. ¿Sobre cuál quieres saber?")

# Preguntas del flujo guiado (arman el resumen del ticket)
pasos_guia = [
    ["plataforma", "Paso 1/4: ¿Con qué plataforma o verificador comparas? (ej. DV360, TTD, IAS)"],
    ["fechas", "Paso 2/4: ¿Qué rango de fechas revisas? (ej. 1 al 7 de octubre)"],
    ["propia", "Paso 3/4: ¿Cuántas impresiones reporta tu plataforma? (solo el número)"],
    ["otra", "Paso 4/4: ¿Cuántas impresiones reporta la otra plataforma? (solo el número)"],
]
margen_referencia = 10  # porcentaje de referencia, no es una regla fija

# Estado de la conversacion (paso None = conversacion normal)
estado = {"paso": None, "datos": {}}


def reiniciar():
    estado["paso"] = None
    estado["datos"] = {}


# ---------------------------------------------------------------
# 3. Funciones del chatbot
# ---------------------------------------------------------------
def detectar_intencion(texto):
    raices_usuario = preprocesar(texto)
    mejor_intencion = None
    mejor_puntaje = 0
    for intencion in base_conocimiento:
        puntaje = 0
        for palabra in base_conocimiento[intencion]["palabras"]:
            raiz = preprocesar(palabra)
            if len(raiz) > 0 and raiz[0] in raices_usuario:
                puntaje = puntaje + 1
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_intencion = intencion
    return mejor_intencion


def convertir_numero(texto):
    limpio = texto.replace(",", "").replace(".", "").replace(" ", "")
    if limpio.isdigit():
        return int(limpio)
    return None


def paso_guia(texto):
    if texto.strip().lower() == "cancelar":
        reiniciar()
        return "Listo, cancelé el resumen. ¿En qué más te ayudo?"

    nombre = pasos_guia[estado["paso"]][0]
    valor = texto.strip()
    if nombre == "propia" or nombre == "otra":
        valor = convertir_numero(texto)
        if valor is None or valor <= 0:
            return "Necesito solo un número mayor que cero (ej. 1250000). " + pasos_guia[estado["paso"]][1]

    estado["datos"][nombre] = valor
    estado["paso"] = estado["paso"] + 1

    if estado["paso"] < len(pasos_guia):
        return pasos_guia[estado["paso"]][1]
    return armar_resumen()


def armar_resumen():
    d = estado["datos"]
    diferencia = abs(d["propia"] - d["otra"]) / d["propia"] * 100
    if diferencia <= margen_referencia:
        comentario = "dentro del margen de referencia"
    else:
        comentario = "por encima del margen de referencia; conviene abrir el ticket"
    reiniciar()
    return ("Resumen para tu ticket:\n"
            "  - Plataforma: " + d["plataforma"] + "\n"
            "  - Fechas: " + d["fechas"] + "\n"
            "  - Impresiones de tu plataforma: " + format(d["propia"], ",") + "\n"
            "  - Impresiones de la otra plataforma: " + format(d["otra"], ",") + "\n"
            "  - Discrepancia: " + str(round(diferencia, 1)) + "% (" + comentario + ").\n"
            "Recuerda añadir el ID de campaña o deal y una captura del reporte.")


def responder(texto):
    if texto.strip() == "":
        return "Escribe tu pregunta y con gusto te ayudo."
    if estado["paso"] is not None:
        return paso_guia(texto)

    intencion = detectar_intencion(texto)
    if intencion is None:
        return mensaje_fallback
    if intencion == "inicio_guia":
        estado["paso"] = 0
        estado["datos"] = {}
        return "Perfecto, armemos el resumen. (Escribe 'cancelar' para salir.)\n" + pasos_guia[0][1]
    return base_conocimiento[intencion]["respuesta"]


def chatear():
    # conversacion interactiva, se termina escribiendo "salir"
    reiniciar()
    print("Bot: Hola, soy el asistente de discrepancias. Escribe 'salir' para terminar.")
    while True:
        entrada = input("Tú: ")
        if entrada.strip().lower() == "salir" and estado["paso"] is None:
            print("Bot: ¡Hasta pronto!")
            break
        print("Bot:", responder(entrada))


def simular(turnos, titulo=""):
    # ejecuta una conversacion de prueba y muestra lo que pasa
    reiniciar()
    print("=" * 70)
    print(titulo)
    for t in turnos:
        print("Usuario:", t)
        print("Bot:", responder(t))
    print()
