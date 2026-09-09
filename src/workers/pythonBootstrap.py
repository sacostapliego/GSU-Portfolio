"""Runs inside Pyodide once per worker.

Rewires builtins.input to the blocking JS reader the worker installs as
`_portfolio_read_line`, so student programs that call input() behave exactly
as they did in a real terminal -- no source changes, no browser dialogs.
"""

import builtins
import linecache
import sys
import traceback

# Sentinel the JS reader returns when the user pressed Ctrl+C while blocked.
_INTERRUPT = chr(0) + "__PORTFOLIO_INTERRUPT__"

# Whatever name this module was compiled under, so its frames can be stripped
# from tracebacks the student sees.
_BOOTSTRAP_FILE = sys._getframe().f_code.co_filename


def _is_plumbing(frame):
    """True for frames belonging to this runner or to the JS stdin bridge."""
    return frame.filename == _BOOTSTRAP_FILE or frame.filename.startswith(("http://", "https://"))


def _print_user_traceback(exc_type, exc_value, exc_tb):
    frames = [f for f in traceback.extract_tb(exc_tb) if not _is_plumbing(f)]
    summary = traceback.StackSummary.from_list(frames)

    sys.stderr.write("Traceback (most recent call last):\n")
    sys.stderr.write("".join(summary.format()))
    sys.stderr.write("".join(traceback.format_exception_only(exc_type, exc_value)))


def _portfolio_input(prompt=""):
    if prompt:
        sys.stdout.write(str(prompt))
        sys.stdout.flush()

    line = _portfolio_read_line()  # noqa: F821 -- injected by the worker

    if line is None:
        raise EOFError("EOF when reading a line")
    if line == _INTERRUPT:
        raise KeyboardInterrupt

    # A real terminal echoes the submitted line; the live caret line is transient.
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
    return line


builtins.input = _portfolio_input


def _portfolio_run(code, file_name):
    # The program never touches the filesystem, so register its source with
    # linecache to make tracebacks show the offending line like CPython does.
    linecache.cache[file_name] = (len(code), None, code.splitlines(True), file_name)

    scope = {"__name__": "__main__", "__file__": file_name}
    try:
        exec(compile(code, file_name, "exec"), scope)
    except SystemExit:
        pass
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys.stderr.write("\nKeyboardInterrupt\n")
    except BaseException:
        sys.stdout.flush()
        # Show only the student's own frames, so the traceback reads like CPython's.
        exc_type, exc_value, exc_tb = sys.exc_info()
        _print_user_traceback(exc_type, exc_value, exc_tb.tb_next or exc_tb)
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
