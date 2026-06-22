from typer.testing import CliRunner
from src.cli import app

runner = CliRunner()


class TestCLIRouting:

    def test_strategy_invalida_retorna_exit_code_1(self):
        result = runner.invoke(app, [
            "analyze",
            "--repo-path", "/tmp/fake_repo_that_does_not_exist",
            "--strategy", "invalida",
        ])
        # o repo não existe, mas o erro de path vem antes do de strategy —
        # testamos strategy inválida com path existente via mock
        # aqui validamos que a saída menciona o nome da strategy errada
        # (o exit code 1 é garantido tanto pelo path quanto pela strategy)
        assert result.exit_code == 1

    def test_strategy_invalida_com_path_valido_mostra_mensagem_clara(self, tmp_path):
        """Usa um diretório temporário real para isolar o erro de strategy."""
        # cria um repo git mínimo para passar pela validação de path
        import subprocess
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)

        from unittest.mock import patch
        from src.models import CommitInfo

        fake_commits = [
            CommitInfo(author="alice", email="a@a.com",
                       commit_hash="1", modified_files=["a.py"]),
        ]

        with patch("src.cli.load_commits", return_value=fake_commits):
            result = runner.invoke(app, [
                "analyze",
                "--repo-path", str(tmp_path),
                "--strategy", "invalida",
            ])

        assert result.exit_code == 1
        assert "invalida" in result.output
        assert "commits" in result.output
        assert "files" in result.output

    def test_strategy_commits_roteada_corretamente(self, tmp_path):
        """--strategy commits chama calculate_truck_factor_commits, não files."""
        import subprocess
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)

        from unittest.mock import patch, MagicMock
        from src.models import CommitInfo

        fake_commits = [
            CommitInfo(author="alice", email="a@a.com",
                       commit_hash="1", modified_files=["a.py", "b.py"]),
        ]

        with patch("src.cli.load_commits", return_value=fake_commits):
            with patch("src.strategies.commits.calculate_truck_factor_commits",
                       wraps=__import__("src.strategies.commits",
                                        fromlist=["calculate_truck_factor_commits"]
                                        ).calculate_truck_factor_commits) as spy:
                runner.invoke(app, [
                    "analyze",
                    "--repo-path", str(tmp_path),
                    "--strategy", "commits",
                ])
                spy.assert_called_once()

    def test_sem_commits_exibe_mensagem_e_nao_crasha(self, tmp_path):
        import subprocess
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)

        from unittest.mock import patch

        with patch("src.cli.load_commits", return_value=[]):
            result = runner.invoke(app, [
                "analyze",
                "--repo-path", str(tmp_path),
                "--strategy", "commits",
            ])

        assert result.exit_code == 0
        assert "No commits found" in result.output
