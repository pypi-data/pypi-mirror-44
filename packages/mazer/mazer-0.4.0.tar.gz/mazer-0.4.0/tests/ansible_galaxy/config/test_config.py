from collections import OrderedDict
import logging
import tempfile

from ansible_galaxy.config import config

log = logging.getLogger(__name__)

CONFIG_SECTIONS = ['server', 'content_path', 'global_content_path', 'options']


def assert_object(config_obj):
    assert isinstance(config_obj, config.Config)

    for attr in CONFIG_SECTIONS:
        assert hasattr(config_obj, attr), 'Config instance does not have attr "%s"' % attr


def test_config_init():
    config_ = config.Config()

    assert_object(config_)


def test_config_unknown_attr():
    config_ = config.Config()

    assert hasattr(config_, 'not_a_valid_attr') is False
    try:
        blip = config_.not_a_valid_attr
    except AttributeError as e:
        log.debug(e, exc_info=True)
        return

    assert False, 'Expected to get an AttributeError accessing an unknown attr but did not and %s was returned' % blip


def test_config_from_empty_dict():
    config_data = OrderedDict({})
    config_ = config.Config.from_dict(config_data)
    assert_object(config_)


def test_config_from_dict():
    config_data = OrderedDict([
        ('options', {'some_option': 'some_option_value'}),
    ])

    config_ = config.Config.from_dict(config_data)
    assert_object(config_)

    assert config_.options['some_option'] == 'some_option_value'


def test_config_as_dict_empty():
    config_ = config.Config()
    config_data = config_.as_dict()

    assert isinstance(config_data, dict)

    assert set(config_data) == set(CONFIG_SECTIONS)


def test_config_as_dict():
    orig_config_data = OrderedDict([
        ('server', {'url': 'some_url_value',
                    'ignore_certs': True}),
        ('content_path', None),
        ('global_content_path', None),
        ('options', {'some_option': 'some_option_value'}),
    ])

    config_ = config.Config.from_dict(orig_config_data)
    config_data = config_.as_dict()

    assert isinstance(config_data, dict)

    # verify we end up with keys in dict corresponding to each config section
    assert set(config_data) == set(CONFIG_SECTIONS)

    assert config_data == orig_config_data


def test_config_as_dict_from_partial_dict():
    orig_config_data = {
        'server': {'url': 'some_url_value'},
    }
    config_ = config.Config.from_dict(orig_config_data)
    config_data = config_.as_dict()

    assert isinstance(config_data, dict)

    assert set(config_data) == set(CONFIG_SECTIONS)

    assert config_data['server'] == orig_config_data['server']

    assert isinstance(config_data['options'], dict)
    assert config_data['options'] == {}

    assert config_data['content_path'] is None


def test_load_empty():
    yaml_fo = tempfile.NamedTemporaryFile()

    config_ = config.load(yaml_fo.name)

    assert_object(config_)
    log.debug('data: %s', config_.as_dict())


def test_save_empty():
    yaml_fo = tempfile.NamedTemporaryFile()

    config_ = config.Config()

    config.save(config_, yaml_fo.name)

    res_fo = open(yaml_fo.name, 'r')

    written_yaml = res_fo.read()
    log.debug('written_yaml: %s', written_yaml)

    assert written_yaml != ''
    assert 'server' in written_yaml
    assert 'content_path' in written_yaml


def test_save():
    yaml_fo = tempfile.NamedTemporaryFile()

    config_ = config.Config()

    config_.options['some_option'] = 'some_option_value'

    config.save(config_, yaml_fo.name)

    res_fo = open(yaml_fo.name, 'r')

    written_yaml = res_fo.read()
    log.debug('written_yaml: %s', written_yaml)

    assert written_yaml != ''
    expected_strs = [
        'some_option',
        'some_option_value',
    ]
    for expected_str in expected_strs:
        assert expected_str in written_yaml, \
            'expected to find the string "%s" in written config file but did not. file contents: %s' % (expected_str, written_yaml)
