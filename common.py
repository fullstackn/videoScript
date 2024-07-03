import urllib


def get_full_caption(title, caption, tags):
    full_caption = ''
    if title is not None and title != '':
        full_caption += title + '\n'

    full_caption += caption + '\n' + ' '.join([f'#{t}' for t in tags])
    return urllib.parse.quote(full_caption)
