import flet as ft
from flet import (
    Page, 
    AppBar, 
    Text, 
    TextField, 
    ElevatedButton, 
    Column, 
    Container, 
    ListView, 
    ListTile, 
    Row, 
    MainAxisAlignment, 
    CrossAxisAlignment, 
    colors, 
    border_radius
)
from main import ChatReader  # Importar la clase ChatReader del archivo main.py

class ChatSpeechApp:
    def __init__(self):
        self.chat_reader = None
    
    def main(self, page: Page):
        # Store the page reference for use in other methods
        self.page = page
        
        # Set window size to a vertical format using the window property
        page.window.width = 500
        page.window.height = 920
        page.window.resizable = True
        
        page.title = "Chat Speech"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        
        # Store TextField reference
        self.url_field = TextField(
            label="URL del video",
            hint_text="https://www.youtube.com/watch?v=...",
            width=380,  # Adjusted width to fit better in narrow window
            border_radius=10,
        )
        
        # Pantalla de bienvenida
        self.welcome_view = Column(
            controls=[
                Container(
                    content=Text("Bienvenido a Chat Speech", size=30, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(top=50, bottom=200),
                ),
                Container(
                    content=Column(
                        controls=[
                            Text("Introduce la URL del live de YouTube para comenzar", size=20, text_align=ft.TextAlign.CENTER),
                            self.url_field,
                            ElevatedButton(
                                content=Text("Comenzar", size=16, weight=ft.FontWeight.BOLD),
                                width=170,
                                height=50,
                                on_click=self.start_chat_reader,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                        ],
                        spacing=20,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
                Text("@biglexdev", size=12, color=colors.GREY_400),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        )
        
        # Pantalla principal con mensajes
        self.chat_list = ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True
        )
        
        self.main_view = Column(
            visible=False,
            controls=[
                Container(
                    content=Text("Chat Speech for Biglex Dev", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    margin=ft.margin.only(top=10),
                    alignment=ft.alignment.center,
                ),
                Container(
                    content=self.chat_list,
                    border_radius=10,
                    bgcolor=colors.SURFACE_VARIANT,
                    expand=True,
                    padding=10
                ),
                Row(
                    controls=[
                        ElevatedButton(
                            "Detener",
                            on_click=self.stop_chat_reader,
                            style=ft.ButtonStyle(
                                bgcolor=colors.RED_400,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                        ElevatedButton(
                            "Volver",
                            on_click=self.go_back,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=20,
            expand=True,
            horizontal_alignment=CrossAxisAlignment.CENTER  # Add this line to center the text
        )
        
        # Añadir vistas a la página
        page.add(self.welcome_view, self.main_view)
        
        # Crear el objeto ChatReader con un callback para recibir mensajes
        self.chat_reader = ChatReader(callback=self.add_message)
    
    def start_chat_reader(self, e):
        url = self.url_field.value
        
        if not url:
            self.url_field.error_text = "Por favor, introduce una URL válida"
            self.welcome_view.update()
            return
        
        # Ensure chat_reader is initialized
        if self.chat_reader is None:
            self.chat_reader = ChatReader(callback=self.add_message)
        
        # Ocultar pantalla de bienvenida y mostrar pantalla principal
        self.welcome_view.visible = False
        self.main_view.visible = True
        self.welcome_view.update()
        self.main_view.update()
        
        # Iniciar el lector de chat
        self.chat_reader.start_reading(url)
    
    def add_message(self, author, message):
        # Create the message container
        message_container = Container(
            content=ListTile(
                leading=Container(
                    width=40,
                    height=40,
                    bgcolor=colors.BLUE_400,
                    border_radius=border_radius.all(20),
                    content=Text(author[0].upper() if author else "?", color=colors.WHITE, size=16, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                ),
                title=Text(author, weight=ft.FontWeight.BOLD),
                subtitle=Text(message),
            ),
            bgcolor=colors.SURFACE,
            border_radius=10,
            padding=5,
        )
        
        # Add the message to the chat list
        self.chat_list.controls.append(message_container)
        
        # Update the UI
        self.page.update()
    
    def stop_chat_reader(self, e):
        if self.chat_reader:
            self.chat_reader.stop_reading()
    
    def go_back(self, e):
        self.stop_chat_reader(None)
        self.chat_list.controls.clear()
        self.main_view.visible = False
        self.welcome_view.visible = True
        self.welcome_view.update()
        self.main_view.update()

def main():
    app = ChatSpeechApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()