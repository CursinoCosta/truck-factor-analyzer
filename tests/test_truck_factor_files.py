import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.models import CommitInfo
from src.strategies.files import FileAuthorshipTracker


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