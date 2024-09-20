
import io
from typing import List
import numpy as np
import pandas as pd
from requests.packages import urllib3

from src.domain.enum.headers import Headers
from src.logic.baseScreaper import BaseScrapper
from src.domain.enum.pathexpresion import XPathExpressionsSenesyt


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url='https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml'

listas=[]

class SenesytScrapper(BaseScrapper):

    def __init__(self):
        super().__init__()
        self.result=self.get(url=url,verify=False)
#        self.cookies=self.result.cookies.get_dict()
        self.ViewState=self.result.html.xpath(XPathExpressionsSenesyt.VIEW_STATE.value)[0].attrs['value']
        captchaSellerInput=self.result.html.xpath(XPathExpressionsSenesyt.CAPIMG.value)[0].attrs['src'].split(';')[0]
        
        self.imgcapchar=self.get(f'https://www.senescyt.gob.ec{captchaSellerInput}',verify=False,)

    def processo(self,cedula)->pd.DataFrame:

        new_string = self.processar_capchar(self.imgcapchar)

        data={
            'formPrincipal':'formPrincipal',
            'formPrincipal:apellidos':'',
            'formPrincipal:identificacion':	cedula,
            'formPrincipal:captchaSellerInput': new_string,
            'formPrincipal:boton-buscar':'',
            'javax.faces.ViewState':self.ViewState
        }

        datos=self.post( url=url,
                        data=data,
                        cookies=self.cookies,
                        verify=False,
                        headers=Headers.get_headers(cookies=self.cookies,url=url)
                        )
        error=datos.html.xpath(XPathExpressionsSenesyt.MESSAGES.value) #capchar
        mensaje=datos.html.xpath(XPathExpressionsSenesyt.DIVPOSICIONTRES.value) #mensaje 
        
        if mensaje:
            if 'msg-rojo' == mensaje[0].attrs['class'][0]:
                print('Servidor No tiene REGISTRO EN LA senescyt')
                return [pd.DataFrame( [{'CEDULA':cedula,
                                        'Titulo CUARTONIVEL':'N/A',
                                        'Titulo TERCERNIVEL':'N/A',
                                        'TituloTecnologico':'N/A',
                                        'Observacion':mensaje[0].text
                                        }])
                        ]

        if not error:
            ttable=datos.html.xpath(XPathExpressionsSenesyt.GROUPDATOS.value)
            if ttable:
                dataframes=pd.read_html( io.StringIO(ttable[0].html))
                dataframes.pop(0)
                dataframes.pop(0)

                headers=ttable[0].find('div.panel-heading')
                headers.pop(0)

                target_text = 'Título(s)'
                for index in range(len(headers)):
                    if  target_text in headers[index].text.strip():
                        header = headers[index].text.strip()
                        dataframes[index]['NIVEL']=header
                return dataframes  
            else:
                return [pd.DataFrame([
                                        {
                                            'CEDULA': cedula,
                                            'Titulo CUARTONIVEL': 'N/A',
                                            'Titulo TERCERNIVEL': 'N/A',
                                            'TituloTecnologico': 'N/A',
                                            'Observacion': 'la persona solo tiene certificado '
                                        }
                                    ])
                        ]
        else:
            return processo(cedula)

    def opcion_dos(_,path,File):
        pd.set_option('display.max_colwidth', None)
        archivo = pd.read_excel(File, dtype=str, usecols=['cedulas'])
        for i in archivo['cedulas']:
            print(f"buscando registro para la cedula: {i}")
            cont = pd.concat([frame for frame in processo(i)])
            TituloCuartoNivel = np.where(cont['NIVEL'].str.contains('cuarto nivel'), cont["Título"].str.replace('0    ', ''), None)
            TituloTercerNivel = np.where(cont['NIVEL'].str.contains('tercer nivel'), cont['NIVEL'].str.contains('técnico-tecnológico'), cont["Título"].str.replace('0    ', ''), None)
            TituloTecnologico = np.where(cont['NIVEL'].str.contains('técnico-tecnológico'), cont["Título"].str.replace('0    ', ''), None)
            listas.append(pd.DataFrame({'CEDULA': i, 
                                        'Titulo CUARTONIVEL':[np.array2string(TituloCuartoNivel, separator=', ')], 
                                        'Titulo TERCERNIVEL':[np.array2string(TituloTercerNivel, separator=', ')], 
                                        'TituloTecnologico': [np.array2string(TituloTecnologico, separator=', ')]
                                        }, 
                                        index=[0]))

    def procesomio(_,path,File):
        pd.set_option('display.max_colwidth', None)

        archivo=pd.read_excel(File,dtype=str )    
        for i in archivo['cedulas']:  
            TituloCuartoNivel:str=None
            TituloTercerNivel:str=None    
            TituloTecnologico:str=None
            print(f"buscando registro para la cedula: {i}")

            cont:List[pd.DataFrame]=processo(i)
            for frame in cont:
                if  frame['NIVEL'].str.contains('cuarto nivel').any():
                    TituloCuartoNivel=frame["Título"].str.replace('0    ', '').to_string(name=False)
                if frame['NIVEL'].str.contains('tercer nivel').any() and not frame['NIVEL'].str.contains('técnico-tecnológico').any() :
                    TituloTercerNivel=frame["Título"].str.replace('0    ', '').to_string(name=False)
                if frame['NIVEL'].str.contains('técnico-tecnológico').any():
                    TituloTecnologico=frame["Título"].str.replace('0    ', '').to_string(name=False)
            listas.append( pd.DataFrame([
                                        {'CEDULA':i,
                                        'Titulo CUARTONIVEL':TituloCuartoNivel,
                                        'Titulo TERCERNIVEL':TituloTercerNivel,
                                        'TituloTecnologico':TituloTecnologico
                                        }
                                    ])
                                    )

    def processodatos(_,path,File):
        try:
            procesomio(_,path,File)
            #opcion_dos(_,path,File)
        except BaseException as e:
            raise Exception(f'Se encontro un error general {e}')
        finally:
            df = pd.concat(listas, ignore_index=True)
            df.to_csv('ar.csv',index=False)
            df.to_excel('consolidado.xlsx',index=False)
