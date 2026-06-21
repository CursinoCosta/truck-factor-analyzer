import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch
from src.git_loader import load_commits

# Garante que a raiz do projeto esteja no sys.path antes de importar o src
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
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

@patch("src.git_loader.Repository")
def test_load_commits_com_unificacao(mock_repository):
    # Criação de commits simulados (mocks) para evitar download na CI
    commit1 = MagicMock()
    commit1.author.name = "Jane Doe"
    commit1.author.email = "jane@example.com"
    commit1.hash = "abc1"
    mod1 = MagicMock()
    mod1.new_path = "src/main.py"
    commit1.modified_files = [mod1]

    commit2 = MagicMock()
    commit2.author.name = "J. Doe"
    commit2.author.email = "jane@example.com"
    commit2.hash = "abc2"
    mod2 = MagicMock()
    mod2.new_path = "src/utils.py"
    commit2.modified_files = [mod2]

    # Configura o mock do Repository para retornar nossos commits simulados
    instancia_mock = mock_repository.return_value
    instancia_mock.traverse_commits.return_value = [commit1, commit2]

    # Executa a função integrada
    commits_resultado = load_commits("caminho_falso")

    # Verifica se os arquivos foram lidos corretamente
    assert len(commits_resultado) == 2
    
    # Verifica se a integração com unificar_autores funcionou (o nome deve ser padronizado)
    assert commits_resultado[0].author == "Jane Doe"
    assert commits_resultado[1].author == "Jane Doe"  # O nome "J. Doe" deve ter sido corrigido pelo e-mail