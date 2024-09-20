


import io
import pandas as pd
from src.logic.baseScreaper import BaseScrapper
from src.domain.enum.pathexpresion import XPathExpressionsBachillerato



class BachilleratoScraper(BaseScrapper):
    
    url ='https://servicios.educacion.gob.ec/titulacion25-web/faces/paginas/consulta-titulos-refrendados.xhtml'


    def __init__(self):
        super().__init__()
        self.result=self.get(url=self.url,verify=False)

        self.ViewState=self.result.html.xpath(XPathExpressionsBachillerato.VIEW_STATE.value)[0].attrs['value']
        captchaSellerInput=self.result.html.xpath(XPathExpressionsBachillerato.CAPIMG.value)[0].attrs['src']
        self.imgcapchar=self.get(f'https://servicios.educacion.gob.ec{captchaSellerInput}',verify=False)


    def processo(self,cedula):

        header={
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-Encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'cache-control':'max-age=0',
        'connection': 'keep-alive',
        'content-length': '212',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': f'JSESSIONID={self.cookies.get('JSESSIONID')}',
        'faces-request': 'partial/ajax',
        'host': 'servicios.educacion.gob.ec',
        'origin': 'https://servicios.educacion.gob.ec',
        'referer': 'https://servicios.educacion.gob.ec/titulacion25-web/faces/paginas/consulta-titulos-refrendados.xhtml',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'sec-ch-ua-mobile':'?0',
        'secch-ua-platform': "Windows",
        'sec-fetch-Dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }
        new_string = self.processar_capchar(self.imgcapchar)

        data = {
            'formBusqueda': 'formBusqueda',
            'formBusqueda:j_idt18': 1,
            'formBusqueda:cedula':cedula,
            'formBusqueda:captcha': new_string,
            'formBusqueda:clBuscar': 'Consultar',
            'javax.faces.ViewState': self.ViewState,
            }

        datados = {
            'formBusqueda': 'formBusqueda',
            'formBusqueda:j_idt18': 1,
            'formBusqueda:cedula':cedula,
            'formBusqueda:captcha': '',
            'formBusqueda:clBuscar': 'Consultar',
            'javax.faces.ViewState': self.ViewState,
            'javax.faces.source': 'formBusqueda:cedula',
            'javax.faces.partial.event': 'change',
            'javax.faces.partial.execute': 'formBusqueda:cedula @component',
            'javax.faces.partial.render':'@component',
            'javax.faces.behavior.event':'valueChange',
            'org.richfaces.ajax.component': 'formBusqueda:cedula',
            'rfExt': 'null',
            'AJAX:EVENTS_COUNT': 1,
            'javax.faces.partial.ajax': 'true'
            }

        datosdos=self.post( url=self.url,
                         data=datados,
                         verify=False,
                         headers=header
                        )
        
        
        datos=self.post( url=self.url,
                         data=data,
                         verify=False,
                         headers=header
                        )
        
        
        #self.result.html.raw_html = datosdos.text
        self.result.html.render()

        result=datos.html.xpath(XPathExpressionsBachillerato.GROUPDATOS.value)
        results=datosdos.html.xpath(XPathExpressionsBachillerato.GROUPDATOS.value)

        ttable=self.result.html.xpath(XPathExpressionsBachillerato.GROUPDATOS.value)
        
        #dataframes=pd.read_html( io.StringIO(ttable[0].html))

        #print(dataframes)