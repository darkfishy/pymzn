"""
PyMzn is a Python library that wraps and enhances the MiniZinc tools for CSP
modelling and solving. It is built on top of the libminizinc library
(version 2.0) and provides a number of off-the-shelf functions to readily
solve problems encoded in MiniZinc and parse the solutions into Python objects.
"""
import ast
import yaml
import appdirs
import logging

from . import _utils
from . import bin
from . import _dzn
from ._dzn import *
from . import _mzn
from ._mzn import *

__version__ = '0.10.8'
__all__ = ['debug', 'config', 'bin', 'gecode']
__all__.extend(_dzn.__all__)
__all__.extend(_mzn.__all__)

# TODO: update python2 branch
# TODO: config solver function and default arguments to solver
# TODO: mzn2doc
# TODO: check the import of other files in minizinc
# TODO: make it work on windows
# TODO: check the ctrl+C thing which seems to not work anymore

_debug_handler = None
_pymzn_logger = logging.getLogger(__name__)
_pymzn_logger.addHandler(logging.NullHandler())

def debug(dbg=True):
    global _debug_handler
    if dbg and _debug_handler is None:
        _debug_handler = logging.StreamHandler()
        _pymzn_logger.addHandler(_debug_handler)
        _pymzn_logger.setLevel(logging.DEBUG)
    elif not dbg and _debug_handler is not None:
        _pymzn_logger.removeHandler(_debug_handler)
        _debug_handler = None
        _pymzn_logger.setLevel(logging.WARNING)


config = {}
cfg_file = os.path.join(appdirs.user_config_dir(__name__), 'config.yml')
if os.path.isfile(cfg_file):
    with open(cfg_file) as f:
        config = yaml.load(f)


# Solvers
gecode = Gecode(path=config.get('gecode'))


def main():
    import argparse

    desc = 'PyMzn is a wrapper for the MiniZinc tool pipeline.'
    p = argparse.ArgumentParser(description=desc)
    p.add_argument('--debug', action='store_true',
                   help='display debug messages on standard output')
    p.add_argument('mzn', help='the mzn file to solve')
    p.add_argument('dzn_files', nargs='*', help='additional dzn files')
    p.add_argument('--data', type=ast.literal_eval,
                   help='additional inline data')
    p.add_argument('-k', '--keep', action='store_true',
                   help='whether to keep generated files')
    p.add_argument('-o', '--output-base',
                   help='base name for generated files')
    p.add_argument('-G', '--mzn-globals-dir',
                   help='directory of global files in the standard library')
    p.add_argument('-f', '--fzn-fn',
                   help='name of proxy function for the solver')
    p.add_argument('--fzn-args', type=ast.literal_eval, default={},
                   help='arguments to pass to the solver')
    args = p.parse_args()

    if args.debug:
        debug()

    other_args = {**{'data': args.data, 'keep': args.keep,
                     'output_base': args.output_base,
                     'mzn_globals_dir': args.mzn_globals_dir,
                     'fzn_fn': args.fzn_fn}, **args.fzn_args}

    print(minizinc(args.mzn, *args.dzn_files, raw_output=True, **other_args))
