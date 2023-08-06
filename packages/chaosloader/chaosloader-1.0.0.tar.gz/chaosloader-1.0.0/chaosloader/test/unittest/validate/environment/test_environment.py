from click.testing import CliRunner
from chaosloader.src.cli import cli


class TestClass(object):

    def test_environment(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['validate', 'environment'])
        assert result.exit_code == 0
        assert 'command apply works!' in result.output
