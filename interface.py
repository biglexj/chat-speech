import flet as ft
from flet import (
    Page, 
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
    border_radius
)
from main import ChatReader

class ChatSpeechApp:
    def __init__(self):
        self.chat_reader = None
    
    def main(self, page: Page):
        self.page = page
        
        page.window.width = 500
        page.window.height = 920
        page.window.resizable = True
        
        page.title = "Chat Speech"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        
        self.is_horizontal = False
        page.on_resize = self.on_window_resize
        
        self.toggle_layout_button = ElevatedButton(
            content=Row(
                controls=[
                    ft.Icon(ft.Icons.SCREEN_ROTATION),
                    Text("Cambiar vista", size=14),
                ],
                spacing=5,
                alignment=MainAxisAlignment.CENTER,
            ),
            on_click=self.toggle_layout,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )
        
        self.url_field = TextField(
            label="URL del video",
            hint_text="https://www.youtube.com/watch?v=...",
            width=380,
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
                Text("@biglexdev", size=12, color=ft.Colors.GREY_400),
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
                    bgcolor=ft.Colors.GREY_900,
                    expand=True,
                    padding=10
                ),
                Row(
                    controls=[
                        ElevatedButton(
                            "Detener",
                            on_click=self.stop_chat_reader,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_400,
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
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        
        self.chat_reader = ChatReader(callback=self.add_message)
        
        page.add(self.welcome_view, self.main_view)
        
        self.is_horizontal = page.window.width > 700
        self.update_layout()
    
    def start_chat_reader(self, e):
        url = self.url_field.value
        
        if not url:
            self.url_field.error_text = "Por favor, introduce una URL válida"
            self.page.update()
            return
        
        if self.chat_reader is None:
            self.chat_reader = ChatReader(callback=self.add_message)
        
        self.welcome_view.visible = False
        self.main_view.visible = True
        self.page.update()
        
        self.chat_reader.start_reading(url)
    
    def add_message(self, author, message):
        message_container = Container(
            content=ListTile(
                leading=Container(
                    width=40,
                    height=40,
                    bgcolor=ft.Colors.BLUE_400,
                    border_radius=border_radius.all(20),
                    content=Text(author[0].upper() if author else "?", color=ft.Colors.WHITE, size=16, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                ),
                title=Text(author, weight=ft.FontWeight.BOLD),
                subtitle=Text(message),
            ),
            bgcolor=ft.Colors.GREY_800,
            border_radius=10,
            padding=5,
        )
        
        self.chat_list.controls.append(message_container)
        self.page.update()
    
    def stop_chat_reader(self, e):
        if self.chat_reader:
            self.chat_reader.stop_reading()
    
    def go_back(self, e):
        self.stop_chat_reader(None)
        self.chat_list.controls.clear()
        self.main_view.visible = False
        self.welcome_view.visible = True
        self.page.update()
    
    def on_window_resize(self, e):
        new_is_horizontal = self.page.window.width > 700
        
        if new_is_horizontal != self.is_horizontal:
            self.is_horizontal = new_is_horizontal
            self.update_layout()
    
    def toggle_layout(self, e):
        self.is_horizontal = not self.is_horizontal
        self.update_layout()
    
    def update_layout(self):
        if self.is_horizontal:
            self.switch_to_horizontal_layout()
        else:
            self.switch_to_vertical_layout()
        
        self.page.update()
    
    def switch_to_horizontal_layout(self):
        self.page.controls.clear()
        
        welcome_horizontal = Row(
            visible=not self.main_view.visible,
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Text("Bienvenido a Chat Speech", size=30, weight=ft.FontWeight.BOLD),
                            Text("@biglexdev", size=12, color=ft.Colors.GREY_400),
                        ],
                        spacing=10,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    width=300,
                    margin=ft.margin.only(left=20),
                    alignment=ft.alignment.center,
                ),
                Container(
                    content=Column(
                        controls=[
                            Text("Introduce la URL del live de YouTube para comenzar", size=18, text_align=ft.TextAlign.CENTER),
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
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        )
        
        main_horizontal = Row(
            visible=self.main_view.visible,
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Container(
                                content=Text("Chat Speech for Biglex Dev", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                margin=ft.margin.only(bottom=10),
                                alignment=ft.alignment.center,
                            ),
                            Column(
                                controls=[
                                    ElevatedButton(
                                        "Detener",
                                        on_click=self.stop_chat_reader,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.RED_400,
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
                                spacing=10,
                                alignment=MainAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=20,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    width=200,
                    alignment=ft.alignment.center,
                ),
                Container(
                    content=self.chat_list,
                    border_radius=10,
                    bgcolor=ft.Colors.GREY_900,
                    expand=True,
                    padding=10
                ),
            ],
            spacing=20,
            expand=True,
            alignment=MainAxisAlignment.CENTER
        )
        
        self.welcome_view = welcome_horizontal
        self.main_view = main_horizontal
        
        self.page.add(welcome_horizontal, main_horizontal)
    
    def switch_to_vertical_layout(self):
        self.page.controls.clear()
        
        welcome_vertical = Column(
            visible=not self.main_view.visible,
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
                Text("@biglexdev", size=12, color=ft.Colors.GREY_400),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
        )
        
        main_vertical = Column(
            visible=self.main_view.visible,
            controls=[
                Container(
                    content=Text("Chat Speech for Biglex Dev", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    margin=ft.margin.only(top=10),
                    alignment=ft.alignment.center,
                ),
                Container(
                    content=self.chat_list,
                    border_radius=10,
                    bgcolor=ft.Colors.GREY_900,
                    expand=True,
                    padding=10
                ),
                Row(
                    controls=[
                        ElevatedButton(
                            "Detener",
                            on_click=self.stop_chat_reader,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_400,
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
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        
        self.welcome_view = welcome_vertical
        self.main_view = main_vertical
        
        self.page.add(welcome_vertical, main_vertical)

def main():
    app = ChatSpeechApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()