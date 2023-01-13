"""Pelican Configuration

For a simple conference 
"""
AUTHOR = 'Huan He'
SITENAME = 'VAHC'

# just set this to relative path due to deployment issue
SITEURL = './'

# where to store the markdown contents and other materials
PATH = 'content'

# I'm here
TIMEZONE = 'America/Chicago'

# by default
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget if needed.
SOCIAL = (('https://twitter.com/', '#'),
          ('https://facebook.com/', '#'),)

# we don't need pagination as there is no blog
DEFAULT_PAGINATION = False

# put all contents under year folder
ARTICLE_URL = "{category}/{slug}.html"
ARTICLE_SAVE_AS = "{category}/{slug}.html"

# for page
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# for conference site author category is not needed
AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""

# no need for tags page
TAGS_SAVE_AS = ""

# no need for archive page
ARCHIVES_SAVE_AS = ""

# no need for categorys page
CATEGORY_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""

# default conf year
DEFAULT_YEAR = '2022'

# for past events
PAST_EVENTS = [
    # year, location, date, 
    ['2022', 'Washington, D.C.'],
    ['2021', 'Virtual'],
    ['2020', 'Virtual'],
    ['2019', 'Vancouver, BC, Canada'],
    ['2018', 'San Francisco, CA'],
    ['2017', 'Phoenix, AZ'],
    ['2016', 'Chicago, IL'],
    ['2015', 'Chicago, IL'],
    ['2014', 'Washington, D.C.'],
    ['2013', 'Washington, D.C.'],
    ['2012', 'Seattle, WA'],
    ['2011', 'Providence, RI'],
    ['2010', 'Salt Lake City, GA'],
]

# specify the customized theme
THEME = "./themes/vahc-theme"