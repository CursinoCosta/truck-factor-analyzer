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

def test_diretorios_ignorados():
    # Caminhos com pastas que devem ser ignoradas (retornam True)
    assert ignorar_arquivo("node_modules/express/index.js") is True
    assert ignorar_arquivo("venv/lib/python3.11/site-packages/typer.py") is True
    assert ignorar_arquivo("projeto/build/saida.py") is True
    
def test_diretorios_nao_ignorados():
    # Caminhos válidos que têm palavras parecidas no nome do arquivo (retornam False)
    # Isso garante que a função verifica as pastas e não apenas o texto do caminho
    assert ignorar_arquivo("src/utils/node_modules_handler.py") is False
    assert ignorar_arquivo("src/scripts/gerar_build.py") is False