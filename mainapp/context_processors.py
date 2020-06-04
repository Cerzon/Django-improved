""" mainapp context processors
"""


def site_set(request):
    """ add site name, top menu template and stuff
    """
    site_name = 'Рога и Копыта'
    top_menu = 'includes/topmenu.html'
    show_quote = True
    if 'adminapp' in request.resolver_match.namespaces:
        site_name = 'Администрирование сайта'
        top_menu = 'adminapp/includes/topmenu.html'
        show_quote = False
    return {
        'site_name': site_name,
        'top_menu': top_menu,
        'show_quote': show_quote,
    }
