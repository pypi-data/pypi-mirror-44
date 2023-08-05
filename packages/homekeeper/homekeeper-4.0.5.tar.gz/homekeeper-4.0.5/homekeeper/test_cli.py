import click.testing
import homekeeper
import homekeeper.cli
import homekeeper.test_case
import mock


# pylint: disable=attribute-defined-outside-init
# pylint: disable=maybe-no-member
class TestCli(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestCli, self).setup_method()
        self.runner = click.testing.CliRunner()
        self.mock_instance = mock.MagicMock()
        self.patcher = mock.patch('homekeeper.Homekeeper')
        self.mock_class = self.patcher.start()
        self.mock_class.return_value = self.mock_instance

    def teardown_method(self):
        self.patcher.stop()

    def run(self, *args, **kwargs):
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.exit_code == 0
        if 'output' in kwargs:
            assert result.output == kwargs['output']
        else:
            assert result.output == ''

    def test_cleanup(self):
        self.run('cleanup')
        self.mock_class.cleanup.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == True
        assert self.mock_instance.overwrite == False
        self.mock_instance.cleanup.assert_called_with()

    def test_cleanup_ignores_no_cleanup_and_overwrite(self):
        self.run('--no-cleanup-symlinks', '--overwrite', 'cleanup')
        self.mock_class.cleanup.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == True
        assert self.mock_instance.overwrite == False
        self.mock_instance.cleanup.assert_called_with()

    def test_init_with_custom_config(self, os):
        dotfiles_directory = os.getcwd()
        config_path = os.path.join(dotfiles_directory, '.config.json')
        self.run('--config-path', config_path, 'init')
        self.mock_class.assert_called_once_with(config_path=config_path)
        self.mock_class.init.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == False
        assert self.mock_instance.overwrite == False
        self.mock_instance.init.assert_called_with()

    def test_init_cannot_cleanup_or_overwrite(self):
        self.run('--cleanup-symlinks', '--overwrite', 'init')
        self.mock_class.assert_called_once_with(config_path=None)
        self.mock_class.init.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == False
        assert self.mock_instance.overwrite == False
        self.mock_instance.init.assert_called_with()

    def test_keep_with_default_options(self):
        self.run('keep')
        self.mock_class.assert_called_once_with(config_path=None)
        self.mock_class.keep.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == True
        assert self.mock_instance.overwrite == True
        self.mock_instance.keep.assert_called_with()

    def test_keep_with_custom_options(self):
        self.run('--no-cleanup-symlinks', '--no-overwrite', 'keep')
        self.mock_class.assert_called_once_with(config_path=None)
        self.mock_class.keep.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == False
        assert self.mock_instance.overwrite == False
        self.mock_instance.keep.assert_called_with()

    def test_unkeep_with_default_options(self):
        self.run('unkeep')
        self.mock_class.assert_called_once_with(config_path=None)
        self.mock_class.keep.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == True
        assert self.mock_instance.overwrite == True
        self.mock_instance.unkeep.assert_called_with()

    def test_unkeep_with_custom_options(self):
        self.run('--no-cleanup-symlinks', '--no-overwrite', 'unkeep')
        self.mock_class.assert_called_once_with(config_path=None)
        self.mock_class.keep.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == False
        assert self.mock_instance.overwrite == False
        self.mock_instance.unkeep.assert_called_with()

    def test_version(self):
        output = 'Homekeeper version %s\n' % homekeeper.__version__
        self.run('version', output=output)
        self.mock_class.assert_not_called()
