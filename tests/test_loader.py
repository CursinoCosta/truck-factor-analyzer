import pytest
from src.git_loader import ignorar_arquivo

def test_extensoes_ignoradas():
    # Extensões que devem ser ignoradas (retornam True)
    assert ignorar_arquivo("README.md") is True
    assert ignorar_arquivo("config/settings.json") is True
    assert ignorar_arquivo("dados.csv") is True
    assert ignorar_arquivo("imagem.png") is True

def test_extensoes_nao_ignoradas(): 
    # Arquivos que devem ser processados (retornam False)
    assert ignorar_arquivo("src/main.py") is False
    assert ignorar_arquivo("Makefile") is False
    assert ignorar_arquivo("src/analise.java") is False