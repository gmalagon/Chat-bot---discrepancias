 Asistente de discrepancias de impresiones (Avance 1)

Chatbot basado en reglas hecho con Python 3.10 o superior y NLTK, para la materia
Programación para la Inteligencia Artificial.

## Problema
Las áreas de Atención a Clientes, Ventas y Account Management hacen muchas veces las
mismas preguntas sobre discrepancias de impresiones en publicidad programática. El chatbot
responde las dudas más comunes y ayuda a reunir los datos para abrir un ticket.

## Qué puede hacer
- Explicar qué es una discrepancia de impresiones y sus causas comunes
- Indicar el porcentaje de diferencia que suele considerarse aceptable
- Explicar la diferencia entre un verificador (IAS, DV) y un DSP
- Decir qué datos se necesitan para abrir un ticket, escalar y tiempos de respuesta
- Armar el resumen del ticket paso a paso (escribe "guíame") y calcular la discrepancia

## Archivos
- `chatbot.py`: código del chatbot (preprocesamiento, base de conocimiento y funciones)
- `pruebas.py`: 12 conversaciones de prueba
- `chatbot_discrepancias.ipynb`: notebook para Google Colab con todo lo anterior
- `requirements.txt`: dependencias

## Cómo ejecutarlo
En Google Colab: abre `chatbot_discrepancias.ipynb` y ejecuta todas las celdas.

En tu computadora:
```
pip install -r requirements.txt
python pruebas.py
```

Para conversar con el chatbot:
```
python -c "import chatbot; chatbot.chatear()"
```

## Limitaciones de esta versión
No corrige errores de ortografía, atiende una sola intención por mensaje, no entiende
negaciones y solo funciona en español. Se mejorará en los siguientes avances con
procesamiento de lenguaje natural, clasificación de imágenes e integración web.

Todos los datos de ejemplo son ficticios.
