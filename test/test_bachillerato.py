from src.logic.bachillerato import BachilleratoScraper

def test_bachi():
    bachillerato=BachilleratoScraper()
    assert isinstance (bachillerato,BachilleratoScraper)

def test_proceso():
    bachillerato=BachilleratoScraper()
    bachillerato.processo('0952461093')    
    assert isinstance (bachillerato,BachilleratoScraper)
