from enum import Enum


class XPathExpressionsSenesyt(Enum):
    VIEW_STATE = "//*[@id='j_id1:javax.faces.ViewState:0']"
    CAPIMG="//*[@id='formPrincipal:capimg']"
    MESSAGES='//*[@id="formPrincipal:messages"]/div/ul/li/span[2]'
    DIVPOSICIONTRES="//*[@id='formPrincipal']/div/div[3]"
    GROUPDATOS="//*[@id='formPrincipal:groupDatos']"

class XPathExpressionsBachillerato(Enum):
    #TODO 
    #TOCA BUSCAR LOS PATH DE ESTOS COMPONENTES.
    VIEW_STATE = "//*[@id='javax.faces.ViewState']"
    CAPIMG="//*[@id='formBusqueda:capimg']"

    MESSAGES='//*[@id="formPrincipal:messages"]/div/ul/li/span[2]'
    DIVPOSICIONTRES="//*[@id='formPrincipal']/div/div[3]"
    GROUPDATOS="//*[@id='formBusqueda:j_idt63']"
    