def get_percentage(count, total):
    return f'{round(count/total*100, 2)}%'


def format_database_column_name(name):
    if name == 'header_dnt':
        return 'DNT'

    words = name.split('_')

    if words[0] == 'header':
        return '-'.join(word.capitalize() for word in words[1:])

    assert words[0] == 'js'

    if words[1] == 'webgl':
        words[1] = 'WebGL'
        return ' '.join(words[1:])

    return ' '.join(words[1:]).capitalize()
