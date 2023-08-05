import io
import os
import sys
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path
import pytest
from mode.utils.mocks import patch

sys.path.append(str(Path(__file__).parent))

from proj import main  # noqa


def test_main():
    stdout = io.StringIO()
    stderr = io.StringIO()
    environ = dict(os.environ)
    try:
        with ExitStack() as stack:
            stack.enter_context(patch('sys.argv', ['proj', 'foo']))
            stack.enter_context(pytest.raises(SystemExit))
            stack.enter_context(redirect_stdout(stdout))
            stack.enter_context(redirect_stderr(stderr))

            main()
    finally:
        os.environ.clear()
        os.environ.update(environ)
    print(stdout.getvalue())
    print(stderr.getvalue())
    assert 'HELLO WORLD' in stdout.getvalue()
