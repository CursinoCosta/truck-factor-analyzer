import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.models import CommitInfo
from src.strategies.commits import calculate_truck_factor_commits, CommitsTruckFactorResult


def _commit(author: str, files: list[str]) -> CommitInfo:
    return CommitInfo(
        author=author,
        email=f"{author}@test.com",
        commit_hash="x",
        modified_files=files,
    )


class TestCalculateTruckFactorCommits:

    def test_corte_correto_top2_somam_mais_de_50_porcento(self):
        """
        alice: 6 modificações, bob: 3, carol: 1  → total 10
        alice sozinha já cobre 60% > 50% → TF = 1
        """
        commits = [
            _commit("alice", ["a.py", "b.py", "c.py"]),
            _commit("alice", ["d.py", "e.py", "f.py"]),
            _commit("bob",   ["g.py", "h.py", "i.py"]),
            _commit("carol", ["j.py"]),
        ]
        result = calculate_truck_factor_commits(commits, coverage_threshold=0.5)
        assert result.truck_factor == 1
        assert result.critical_authors == ["alice"]
        assert result.coverage > 0.5

    def test_dois_autores_necessarios_quando_nenhum_sozinho_ultrapassa(self):
        """
        alice: 4, bob: 4, carol: 2 → total 10
        alice = 40% (não ultrapassa 50%), alice+bob = 80% > 50% → TF = 2
        """
        commits = [
            _commit("alice", ["a.py", "b.py", "c.py", "d.py"]),
            _commit("bob",   ["e.py", "f.py", "g.py", "h.py"]),
            _commit("carol", ["i.py", "j.py"]),
        ]
        result = calculate_truck_factor_commits(commits, coverage_threshold=0.5)
        assert result.truck_factor == 2
        assert "alice" in result.critical_authors
        assert "bob" in result.critical_authors

    def test_lista_vazia_retorna_tf_zero(self):
        result = calculate_truck_factor_commits([], coverage_threshold=0.5)
        assert result.truck_factor == 0
        assert result.critical_authors == []
        assert result.coverage == 0.0

    def test_autor_unico_tf_e_sempre_um(self):
        commits = [_commit("alice", ["a.py", "b.py", "c.py"])]
        result = calculate_truck_factor_commits(commits)
        assert result.truck_factor == 1
        assert result.critical_authors == ["alice"]

    def test_threshold_customizado_0_8_exige_mais_autores(self):
        """
        alice: 5, bob: 3, carol: 2 → total 10
        threshold=0.8: alice=50%, alice+bob=80% → ultrapassa em 2 autores → TF = 2
        """
        commits = [
            _commit("alice", ["a.py", "b.py", "c.py", "d.py", "e.py"]),
            _commit("bob",   ["f.py", "g.py", "h.py"]),
            _commit("carol", ["i.py", "j.py"]),
        ]
        result = calculate_truck_factor_commits(commits, coverage_threshold=0.8)
        assert result.truck_factor == 2
        assert result.coverage >= 0.8

    def test_threshold_0_retorna_tf_um(self):
        """Qualquer autor já ultrapassa threshold=0: TF sempre 1."""
        commits = [
            _commit("alice", ["a.py"]),
            _commit("bob",   ["b.py"]),
        ]
        result = calculate_truck_factor_commits(commits, coverage_threshold=0.0)
        assert result.truck_factor == 1

    def test_ranking_ordenado_por_volume_decrescente(self):
        commits = [
            _commit("carol", ["a.py"]),
            _commit("alice", ["b.py", "c.py", "d.py"]),
            _commit("bob",   ["e.py", "f.py"]),
        ]
        result = calculate_truck_factor_commits(commits)
        authors_in_order = [a for a, _ in result.author_ranking]
        assert authors_in_order == ["alice", "bob", "carol"]
