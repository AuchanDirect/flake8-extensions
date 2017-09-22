import ast

from sys import stdin

from .utils import get_noqa_lines


__version__ = '0.1.0'

ERROR_CODE = 'F8E001'
ERROR_MESSAGE = 'Forbiden import found'

FORBIDDEN_IMPORTS = frozenset([
    'django.utils.translation.ugettext',
    'django.utils.translation.ugettext_lazy',
    'django.utils.translation.ugettext_noop',
])


class ForbidenImportsChecker(object):
    name = 'flake8-forbiden_imports'
    version = __version__
    ignores = ()

    def __init__(self, tree, filename='(none)'):
        self.tree = tree
        self.filename = (filename == 'stdin' and stdin) or filename

    def run(self):
        # Get lines to ignore
        if self.filename == stdin:
            noqa = get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as file_to_check:
                noqa = get_noqa_lines(file_to_check.readlines())

        # Run the actual check
        for node in ast.walk(self.tree):
            if not isinstance(node, (ast.ImportFrom, ast.Import)):
                continue

            if node.lineno in noqa:
                continue

            if node.names is None:
                continue

            for alias in node.names:
                imp = alias.name
                if isinstance(node, ast.ImportFrom):
                    imp = '%s.%s' % (node.module, imp)

                if imp in FORBIDDEN_IMPORTS:
                    message = '{0} {1}: {2}'.format(
                        ERROR_CODE, ERROR_MESSAGE, node.names[0].name)
                    yield node.lineno, node.col_offset, message, type(self)
