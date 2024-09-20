import flet as ft
from logic.SenesytScrapper import  buscar_tesesseract, processodatos
import logging

dlg = ft.AlertDialog(title=ft.Text("EL ARCHIVO DEBE TENER COMO NOMBRE 'FILE',validar el nombre"), on_dismiss=lambda e: ft.Text("ARCHIVO CARGADO EXITOSAMENTE"))
logger = logging.getLogger(__name__)


logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.ERROR)

class Formulario:

    def __init__(self,page):
        self.page=page
        self.pr()

    def open_dlg(self,e:ft.FilePickerResultEvent):
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def dialog_picker(self,e:ft.FilePickerResultEvent):
        for file  in e.files:
           self. ruta.value=file.path
           self.page.update()

    def dialog_file(self,e:ft.FilePickerResultEvent):
        for file  in e.files:
            if file.name !="FILE.xlsx":
                self.open_dlg(e)
            else:
                self.archivo.value=file.path
                self.page.update()

    def sn(self,_):
        loading_indicator = ft.ProgressBar(  width=400 )
        self.page.add(loading_indicator)

        try:

            if processodatos(_,self.ruta.value,self.archivo.value):

                dialog = ft.AlertDialog(
                    content=ft.Text("OPERACION TERMINADA"),
                    on_dismiss=lambda e: self.page.add(ft.Text("Operación exitosa!")),
                )
                self.page.dialog = dialog
                dialog.open = True
                logging.info("ESTADO OK")

        except Exception as e:
            self.page.remove(loading_indicator)

            dialog = ft.AlertDialog(
                content=ft.Text("OPERACION TERMINADA"),
                on_dismiss=lambda e: _.page.add(ft.Text("Error: " + str(e))),
            )
            self.page.dialog = dialog
            dialog.open = True
            logging.error(  str(e))
        self.page.remove(loading_indicator)
        self.page.update()


    def pr(self):

        tesseract_cmd=buscar_tesesseract()
        self.filefile=ft.FilePicker( on_result=self.dialog_file)
        self.file=ft.FilePicker( on_result=self.dialog_picker)

        self.ruta=ft.TextField(hint_text="ingrese el path",
                            value= tesseract_cmd ,
                            icon=  ft.icons.PAYMENT_SHARP,
                            read_only=True,
                            suffix=ft.IconButton(
                                icon=ft.icons.FILE_UPLOAD,
                                on_click=lambda _:self.file.pick_files(),
                                disabled=True
                                ),
                                disabled=True
                                )

        self.archivo= ft.TextField(hint_text= "Cargar Archivo",
                                    icon=ft.icons.FILE_OPEN,
                                    read_only=True,
                                    suffix=ft.IconButton(
                                        icon=ft.icons.FILE_UPLOAD, 
                                        on_click=lambda _:self.filefile.pick_files()))
