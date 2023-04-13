import re
from pelican import signals

REGEX_YEAR = r"\b(\d{4})\b"
PTN_IMPT_DATES = '<h1>IMPORTANT DATES</h1>'

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


def filter_cut_sec_important_dates(content, flag_dates=True):
    '''
    Cut the important_dates_section from a given article
    '''
    # find the pattern of index
    idx = -1
    try:
        idx = content.index(PTN_IMPT_DATES)
    except:
        if flag_dates:
            return '<p>NA</p>'
        else:
            return content

    if flag_dates:
        return content[idx:]
    else:
        return content[:idx]


def add_all_filters(pelican):
    """Add (register) all filters to Pelican."""
    pelican.env.filters.update({"get_year": filter_get_year})
    pelican.env.filters.update({"pg2path": filter_pg2path})
    pelican.env.filters.update({"cut_sec_important_dates": filter_cut_sec_important_dates})


###########################################################
# Plugin for make special pages
###########################################################


def register():
    """Plugin registration."""
    signals.generator_init.connect(add_all_filters)