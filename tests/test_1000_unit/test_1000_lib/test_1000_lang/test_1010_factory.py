from myutils import pytest

def test_1000_factory():

    from myutils.lib.lang.factory import Factory

    config = {
        'root': 1
    }
    f = Factory.Default(config)

    assert f.config is config
