from urlextract import URLExtract

def Find(Text):
    return URLExtract().find_urls(str(Text))

def Parse(Url):

    Uri = {}
    if not Url or not '.' in Url:return
    if ('://' in Url.lower()) and (not 'http://' in Url.lower()) and (not 'https://' in Url.lower()): return

    Uri['Url'] = {}
    if '://' in Url:Uri['Url']['Full'], Uri['Url']['Medium'] = Url[Url.lower().find('http'):], Url.split('://')[1]
    else:Uri['Url']['Full'], Uri['Url']['Medium'] = f'https://{Url}', Url
    Uri['Url']['Short'] = Uri['Url']['Medium'].split('/')[0]

    Uri['Domain'] = {}
    Uri['Domain']['Full'] = '.'.join(Uri['Url']['Short'].split('.')[-2:]).lower()
    Uri['Domain']['Name'] = Uri['Domain']['Full'].split('.')[-2].lower()
    Uri['Domain']['Zone'] = Uri['Domain']['Full'].split('.')[-1].lower()

    Uri['Subdomains'] = Uri['Url']['Short'].split('.')[:-2]
    Uri['Path'] = Uri['Url']['Medium'].split('/')[1:]

    Uri['Www'] = Uri['Url']['Short'].startswith('www.')
    Uri['Protocol'] = Uri['Url']['Full'].split('://')[0].lower()

    return Uri