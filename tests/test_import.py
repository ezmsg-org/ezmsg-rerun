from importlib.util import find_spec


def test_package_installed():
    spec = find_spec("ezmsg.rerun")
    assert spec is not None, "ezmsg.rerun is not installed."
