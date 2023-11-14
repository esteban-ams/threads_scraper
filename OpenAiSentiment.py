import os
import openai
import sys
import json
import requests
import time
import re
import pandas as pd

openai.api_key = os.environ("OPENAI_KEY")

sentimientos_permitidos = [
        "abandono", "abatimiento", "abrumamiento", "aburrimiento", "abuso", "aceptación",
        "acompañamiento", "admiración", "adoración", "afectación", "afecto", "aflicción",
        "agobio", "agradecimiento", "agravio", "agresión", "alarma", "alborozo", "alegría",
        "alivio", "alteración", "amabilidad", "amargura", "ambivalencia", "amor", "angustia",
        "anhelo", "ansiedad", "añoranza", "apatía", "apego", "apoyo", "aprobación", "armonía",
        "arrepentimiento", "arrogancia", "arrojo", "asco", "asombro", "atracción", "ausencia",
        "autonomía", "aversión", "benevolencia", "bondad", "calma", "cansancio", "cariño",
        "celos", "censura", "cercanía", "cólera", "compasión", "competencia", "comprensión",
        "compromiso", "concentración", "condescendencia", "confianza", "confusión", "congoja",
        "consideración", "consuelo", "contento", "contrariedad", "correspondencia", "cuidado",
        "culpa", "curiosidad", "decepción", "dependencia", "depresión", "derrota", "desaliento",
        "desamor", "desamparo", "desánimo", "desasosiego", "desconcierto", "desconfianza",
        "desconsideración", "desconsuelo", "desdén", "desdicha", "desencanto", "deseo",
        "desesperación", "desgano", "desidia", "desilusión", "desmotivación", "desolación",
        "desorientación", "desprecio", "desprestigio", "desprotección", "destrucción",
        "desvalimiento", "desventura", "devaluación", "dicha", "dignidad", "disforia",
        "disgusto", "diversión", "dolor", "dominación", "duda", "duelo", "ecuanimidad",
        "embelesamiento", "emoción", "empatía", "enamoramiento", "encanto", "enfado",
        "engaño", "enjuiciamiento", "enojo", "enternecimiento", "entusiasmo", "envidia",
        "espanto", "esperanza", "estima", "estremecimiento", "estupor", "euforia",
        "exaltación", "exasperación", "excitación", "expectativa", "éxtasis", "extrañeza",
        "fastidio", "felicidad", "fervor", "firmeza", "fobia", "fortaleza", "fracaso",
        "fragilidad", "frenesí", "frustración", "furia", "generosidad", "gozo", "gratitud",
        "hastío", "herida", "honestidad", "honorabilidad", "horror", "hostilidad", "humildad",
        "humillación", "ilusión", "impaciencia", "imperturbabilidad", "impotencia", "impresión",
        "incapacidad", "incomodidad", "incompatibilidad", "incomprensión", "inconformidad",
        "incongruencia", "incredulidad", "indiferencia", "indignación", "inestabilidad",
        "infelicidad", "inferioridad", "injusticia", "inquietud", "insatisfacción", "inseguridad",
        "insuficiencia", "integridad", "interés", "intimidad", "intolerancia", "intranquilidad",
        "intrepidez", "intriga", "invasión", "ira", "irritación", "jocosidad", "júbilo", "justicia",
        "lamento", "lástima", "libertad", "logro", "lujuria", "manipulación", "melancolía",
        "menosprecio", "mezquindad", "miedo", "molestia", "motivación", "necesidad", "nerviosismo",
        "nostalgia", "obligación", "obnubilación", "obstinación", "odio", "omnipotencia",
        "opresión", "optimismo", "orgullo", "ostentación", "paciencia", "pánico", "parálisis",
        "pasión", "pavor", "paz", "pena", "pereza", "persecución", "pertenencia", "pesadumbre",
        "pesimismo", "placer", "plenitud", "preocupación", "prepotencia", "pudor", "rabia",
        "rebeldía", "recelo", "rechazo", "regocijo", "remordimiento", "rencor", "repudio",
        "resentimiento", "reserva", "resignación", "respeto", "resquemor", "revelarse", "romance",
        "satisfacción", "seguridad", "serenidad", "simpatía", "soledad", "solidaridad", "sometimiento",
        "sorpresa", "sosiego", "suficiencia", "sumisión", "susto", "temor", "templanza", "tentación",
        "ternura", "terquedad", "terror", "timidez", "tolerancia", "traición", "tranquilidad",
        "tristeza", "triunfo", "turbación", "unidad", "vacilación", "vacío", "valentía", "valoración",
        "venganza", "verguenza", "violencia", "vulnerabilidad"
]

conversation_history = []
url = 'https://dragonnext-unicorn-proxy.hf.space/proxy/openai/v1/chat/completions'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer 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'}

def openaiInit():
    try:
        # Texto que deseas enviar a ChatGPT
        input_text = "Por favor, de un texto dado responde con un solo sentimiento de una lista que te daré, es decir, tu respuesta debe ser solo UNA PALABRA. Puede ser cualquier sentimiento de la lista de emociones proporcionada. El texto son comentarios o posts de Threads, una red social.\nLista de emociones:\n"+str(sentimientos_permitidos)+"\nPor ejemplo, si el texto es 'Estoy muy feliz', tu respuesta debe ser 'alegría'.\nSi no sabes que responder, solo escribe 'No sé'."
        
        # Agrega el mensaje del usuario al historial de conversación
        conversation_history.append({"role": "user", "content": input_text})
        
        # Llamada a la API de OpenAI para obtener la respuesta
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=conversation_history
        # )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        if response.choices:
            print("Error en la llamada a la API de OpenAI")
            tiempo = re.search(r'Please try again in (\d+) seconds.', response['error']['message']).group(1)
            time.sleep(int(tiempo)+1)
        
        # Agrega la respuesta del asistente al historial de conversación
        conversation_history.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        # Extraer el texto de la respuesta
        print("Inicialización exitosa")
        time.sleep(45)
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

# Función para obtener el sentimiento de un texto
def obtener_sentimiento(texto):
    try:
        global conversation_history  # Accede a la variable global conversation_history

        # Agrega el mensaje del usuario al historial de conversación
        conversation_history.append({"role": "user", "content": texto})

        # Llamada a la API de OpenAI para obtener la respuesta
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=conversation_history
        # )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        print(response, type(response))
        if response.choices:
            print("Error en la llamada a la API de OpenAI")
            tiempo = re.search(r'Please try again in (\d+) seconds.', response['error']['message']).group(1)
            time.sleep(int(tiempo)+1)
            return obtener_sentimiento(texto)
        # Extrae el texto de la respuesta del asistente
        respuesta_asistente = response['choices'][0]['message']['content'].lower()

        # Agrega la respuesta del asistente al historial de conversación
        conversation_history.append({"role": "assistant", "content": respuesta_asistente})

        return respuesta_asistente

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

def procesar_csv(nombre_archivo):
    try:
        # Lee el archivo CSV en un DataFrame
        df = pd.read_csv(nombre_archivo, sep=',')

        # Verifica si la columna 'Texto' existe en el DataFrame
        if 'Texto' not in df.columns:
            print("El archivo CSV no tiene una columna 'Texto'.")
            return

        # Itera a través de cada fila del DataFrame
        for index, row in df.iterrows():
            texto = row['Texto']
            sentimiento = row['Concepto']
            if sentimiento == 'False' or sentimiento is False or pd.isnull(sentimiento):
                print(f"Procesando fila {index}...")
                # Obtén el sentimiento del texto
                sentimiento = obtener_sentimiento(texto)

                # Agrega el sentimiento a la columna 'Concepto'
                df.at[index, 'Concepto'] = sentimiento
                print(f"Texto: {texto}\nSentimiento: {sentimiento}")

        # Guarda el DataFrame actualizado en un nuevo archivo CSV o sobrescribe el original
        df.to_csv(nombre_archivo, index=False)
        df.to_excel(f"{nombre_archivo.split('.csv')[0]}" + '.xlsx', index=False)

    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        df.to_csv(nombre_archivo, encoding="utf-8", index=False)
        df.to_excel(f"{nombre_archivo.split('.csv')[0]}" + '.xlsx', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py archivo_json")
    else:
        input_file = sys.argv[1]
        openaiInit()
        procesar_csv(input_file)
