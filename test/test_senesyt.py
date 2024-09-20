
from src.logic.SenesytScrapper import SenesytScrapper

def test_inicio_senesyt():
    senesyt=SenesytScrapper()
    assert isinstance (senesyt,SenesytScrapper)