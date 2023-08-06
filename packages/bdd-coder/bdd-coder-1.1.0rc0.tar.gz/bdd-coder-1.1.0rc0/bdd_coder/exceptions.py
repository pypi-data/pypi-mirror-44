import os


class FeaturesSpecError(Exception):
    """Inconsistency in provided YAML specifications"""


class DocException(Exception):
    def __init__(self, *args, **kwargs):
        self.text = ' '.join(list(filter(None, map(str.strip, self.__doc__.format(
            *args, **kwargs).splitlines()))))

    def __str__(self):
        return self.text


class OverwriteError(DocException):
    """
    Cannot overwrite {path} (--overwrite not set). {error}
    """


def makedirs(path, exist_ok):
    try:
        os.makedirs(path, exist_ok=exist_ok)
    except OSError as error:
        raise OverwriteError(path=path, error=error)


class InconsistentClassStructure(DocException):
    """
    Expected class structure from docs does not match the defined one: {error}
    """


class BaseTesterRetrievalError(DocException):
    """Raised in the base tester retrieval process"""


class StoriesModuleNotFoundError(BaseTesterRetrievalError):
    """Test module {test_module} not found"""


class BaseModuleNotFoundError(BaseTesterRetrievalError):
    """Test module {test_module} should have a `base` module imported"""


class BaseTesterNotFoundError(BaseTesterRetrievalError):
    """
    Imported base test module {test_module}.base should have a single
    BddTester subclass - found {set}
    """
