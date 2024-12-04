import validators


def validate(url):
    if len(url) > 255:
        return 'URL превышает 255 символов'
    elif validators.url(url) is not True:
        return 'Некорректный URL'
