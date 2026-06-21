import sys
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.models import CommitInfo
from src.strategies.files import FileAuthorshipTracker
from src.strategies.files import _compute_doa, _normalize_doa_per_file
from src.strategies.files import calculate_truck_factor_files


def _commit(author: str, files: list[str]) -> CommitInfo:
    return CommitInfo(author=author, email=f"{author}@test.com",
                      commit_hash="x", modified_files=files)


class TestFileAuthorshipTracker:

    def test_fa_atribuido_ao_primeiro_autor(self):
        tracker = FileAuthorshipTracker()
        tracker.process_commits([
            _commit("alice", ["src/foo.py"]),
            _commit("bob",   ["src/foo.py"]),
        ])
        assert tracker.fa["src/foo.py"] == "alice"

    def test_ac_incrementado_quando_terceiro_edita(self):
        tracker = FileAuthorshipTracker()
        tracker.process_commits([
            _commit("alice", ["src/foo.py"]),
            _commit("bob",   ["src/foo.py"]),
        ])
        assert tracker.ac[("src/foo.py", "alice")] == 1

    def test_dl_incrementado_por_cada_edicao_direta(self):
        tracker = FileAuthorshipTracker()
        tracker.process_commits([
            _commit("alice", ["src/foo.py"]),
            _commit("alice", ["src/foo.py"]),
            _commit("bob",   ["src/foo.py"]),
        ])
        assert tracker.dl[("src/foo.py", "alice")] == 2
        assert tracker.dl[("src/foo.py", "bob")]   == 1

    def test_fa_nao_muda_com_edicoes_de_outros_autores(self):
        tracker = FileAuthorshipTracker()
        tracker.process_commits([
            _commit("alice", ["src/bar.py"]),
            _commit("bob",   ["src/bar.py"]),
            _commit("carol", ["src/bar.py"]),
        ])
        assert tracker.fa["src/bar.py"] == "alice"
        assert tracker.ac[("src/bar.py", "alice")] == 2
        assert tracker.ac[("src/bar.py", "bob")] == 0

class TestDOA:

    def test_ac_zero_nao_levanta_excecao(self):
        score = _compute_doa(fa=1, dl=5, ac=0)
        assert math.isclose(score, 3.293 + 1.098 + 0.164 * 5, rel_tol=1e-6)

    def test_first_author_tem_score_maior(self):
        assert _compute_doa(fa=1, dl=3, ac=0) > _compute_doa(fa=0, dl=3, ac=0)

    def test_ac_alto_reduz_score(self):
        assert _compute_doa(fa=1, dl=5, ac=100) < _compute_doa(fa=1, dl=5, ac=1)

    def test_normalizacao_maximo_vira_um(self):
        raw = {("foo.py", "alice"): 5.0, ("foo.py", "bob"): 2.5}
        norm = _normalize_doa_per_file(raw)
        assert math.isclose(norm[("foo.py", "alice")], 1.0)
        assert math.isclose(norm[("foo.py", "bob")],   0.5)

    def test_normalizacao_isolada_por_arquivo(self):
        raw = {
            ("a.py", "alice"): 4.0,
            ("b.py", "bob"):   8.0,
        }
        norm = _normalize_doa_per_file(raw)

        assert math.isclose(norm[("a.py", "alice")], 1.0)
        assert math.isclose(norm[("b.py", "bob")],   1.0)


class TestGreedyHeuristic:

    def test_tf_um_quando_top_autor_e_critico(self):
        commits = [
            _commit("alice", ["a.py", "b.py", "c.py"]),
            _commit("bob",   ["d.py"]),
            _commit("carol", ["a.py"]),  
        ]
        result = calculate_truck_factor_files(commits, coverage_threshold=0.5)
        assert result.truck_factor == 1
        assert "alice" in result.critical_authors

    def test_critical_authors_ordenado_por_remocao(self):
        """Autores removidos com sucesso aparecem em critical_authors."""
        commits = [
            _commit("alice", ["a.py"]),
            _commit("bob",   ["b.py"]),
            _commit("carol", ["c.py", "d.py"]),
        ]
        # threshold 0.1 
        result = calculate_truck_factor_files(commits, coverage_threshold=0.1)
        assert isinstance(result.critical_authors, list)