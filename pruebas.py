from chatbot import simular

CONVERSACIONES = [
    ("C01 - Saludo y menú de ayuda", ["Hola, buenos días", "¿Qué puedes hacer?"]),
    ("C02 - Definición de discrepancia", ["¿Qué significa discrepancia de impresiones?"]),
    ("C03 - Causas de la diferencia", ["¿Por qué no coinciden los números entre sistemas?"]),
    ("C04 - Porcentaje aceptable", ["¿Cuál es el porcentaje aceptable de diferencia?"]),
    ("C05 - Verificador vs DSP", ["¿Cuál es la diferencia entre IAS y el DSP?"]),
    ("C06 - Datos para un ticket", ["¿Qué información necesito para abrir un ticket?"]),
    ("C07 - Escalamiento urgente", ["Tengo un caso urgente, ¿con quién puedo hablar?"]),
    ("C08 - Tiempos de respuesta", ["¿Cuánto tarda en responder el equipo?", "Perfecto, gracias"]),
    ("C09 - Flujo guiado completo (datos ficticios)",
        ["Guíame para armar el resumen", "DV360", "1 al 7 de octubre", "1,250,000", "1,050,000"]),
    ("C10 - Flujo guiado con dato inválido y cancelación",
        ["Ayúdame a preparar el resumen", "TTD", "ayer", "muchas", "cancelar"]),
    ("C11 - Consulta fuera de alcance (fallback)", ["¿Cuál es la capital de Francia?"]),
    ("C12 - Mensaje vacío y despedida", ["   ", "Adiós"]),
]

if __name__ == "__main__":
    for titulo, turnos in CONVERSACIONES:
        simular(turnos, titulo)
