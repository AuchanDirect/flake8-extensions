import tokenize


def is_noqa_line(token):
    if token[0] == tokenize.COMMENT:
        return (token[1].endswith('noqa') or
                isinstance(token[0], str) and token[0].endswith('noqa'))


def get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda l=iter(code): next(l))
    return [token[2][0] for token in tokens if is_noqa_line(token)]
