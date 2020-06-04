""" quotesapp context processor
"""
from .models import UserQuote


def header_quote(request):
    """ add header quote to context
    """
    random_quote = UserQuote.objects.filter(header=True).order_by('?').first()
    return {'header_quote': random_quote}
