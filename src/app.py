import flet as ft

from src.ui.dialog.scraper_dialog import Formulario



def main(page:ft.Page):

    formumario=Formulario(page)

    page.window_width=500
    page.window_height=300
    page.title='Stract Titulos'
    page.theme_mode=ft.ThemeMode.LIGHT

    page.overlay.append(formumario.file)
    page.overlay.append(formumario.filefile)

    page.add(
        ft.Container(
            content=ft.Column(controls=[
                                        formumario.ruta,
                                        formumario.archivo,                           
                                        ft.FilledButton(
                                            "EJECUTAR",
                                            on_click = formumario.sn
                                            )
            ])
        )
    )

    page.update()

