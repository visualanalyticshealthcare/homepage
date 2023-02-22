import re
from pelican import signals

REGEX_YEAR = r"\b(\d{4})\b"

###########################################################
# Filters
###########################################################

def filter_get_year(date_str):
    '''
    Get the year in a string
    '''
    ms = re.findall(REGEX_YEAR, date_str)

    if len(ms) == 0:
        return ''
    else:
        return ms[0]


def filter_pg2path(page_name):
    '''
    Get the path according to page_name
    '''
    if page_name == 'index':
        # ok it's the homepage
        return '.'
    else:
        return '..'


def add_all_filters(pelican):
    """Add (register) all filters to Pelican."""
    pelican.env.filters.update({"pg2path": filter_pg2path})


###########################################################
# Plugin for make special pages
###########################################################


def register():
    """Plugin registration."""
    signals.generator_init.connect(add_all_filters)