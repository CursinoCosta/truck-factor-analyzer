import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.git_loader import CommitInfo
from src.aliases import unificar_autores, distancia_levenshtein

def test_distancia_levenshtein():
    assert distancia_levenshtein("Bob Rob", "Bob.Rob") == 1
    assert distancia_levenshtein("Jane", "Jane") == 0
    assert distancia_levenshtein("Mateus", "Matheus") == 1
    assert distancia_levenshtein("Izadora", "Iza") == 4

def test_unificacao_por_email():
    commits = [
        CommitInfo(author="Jane Doe", email="jane@email.com", commit_hash="1", modified_files=[]),
        CommitInfo(author="J. Doe", email="jane@email.com", commit_hash="2", modified_files=[])
    ]
    commits_unificados = unificar_autores(commits)
    assert commits_unificados[0].author == commits_unificados[1].author

def test_unificacao_por_levenshtein():
    commits = [
        CommitInfo(author="Bob Rob", email="bob1@email.com", commit_hash="1", modified_files=[]),
        CommitInfo(author="Bob.Rob", email="bob2@email.com", commit_hash="2", modified_files=[])
    ]
    commits_unificados = unificar_autores(commits)
    assert commits_unificados[0].author == commits_unificados[1].author