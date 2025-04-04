from chat_downloader import ChatDownloader
import pyttsx3
import time
import threading

# Función para la síntesis de voz con pyttsx3
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"✗ Error al reproducir el texto: {e}")

class ChatReader:
    def __init__(self, callback=None):
        self.processed_messages = set()
        self.is_reading = False
        self.chat_thread = None
        self.callback = callback  # Función para notificar mensajes a la interfaz
    
    def start_reading(self, url):
        # Iniciar el hilo para leer el chat
        self.is_reading = True
        self.chat_thread = threading.Thread(target=self.read_chat, args=(url,))
        self.chat_thread.daemon = True
        self.chat_thread.start()
        
    def stop_reading(self):
        self.is_reading = False
        if self.chat_thread and self.chat_thread.is_alive():
            self.chat_thread.join(1)
        if self.callback:
            self.callback("Sistema", "Lector de chat detenido")
    
    def read_chat(self, url):
        try:
            chat = ChatDownloader().get_chat(url)
            
            if chat is None:
                if self.callback:
                    self.callback("Sistema", "Error: No se pudo obtener el chat. Verifica la URL o tu conexión a internet.")
                return
            
            if self.callback:
                self.callback("Sistema", "Iniciando lector de chat de YouTube...")
            
            for chat_YT in chat:
                if not self.is_reading:
                    break
                    
                message = chat_YT.get('message', '')
                author_name = chat_YT.get('author', {}).get('name', 'Desconocido')
                
                # Crear un identificador único para el mensaje
                message_id = f"{author_name}:{message}"
                
                if message and message_id not in self.processed_messages:
                    chat_text = f"{author_name} dice: {message}"
                    
                    # Notificar a la interfaz
                    if self.callback:
                        self.callback(author_name, message)
                    else:
                        print(chat_text)
                    
                    # Leer el mensaje en voz alta
                    speak(chat_text)
                    
                    # Marcar el mensaje como procesado
                    self.processed_messages.add(message_id)
                    
                    # Pequeña pausa para evitar solapamiento
                    time.sleep(0.5)
                    
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if self.callback:
                self.callback("Sistema", error_msg)
            else:
                print(error_msg)

# Función principal para uso en modo consola
def main():
    url = input("Introduce la URL del video de YouTube: ")
    reader = ChatReader()
    reader.start_reading(url)
    
    try:
        # Mantener el programa en ejecución
        while reader.is_reading:
            time.sleep(1)
    except KeyboardInterrupt:
        reader.stop_reading()
        print("Programa terminado por el usuario.")

# Only run the main function if this file is executed directly
if __name__ == "__main__":
    main()