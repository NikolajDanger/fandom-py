from __future__ import unicode_literals

import requests
import re
import time
import mimetypes
from datetime import timedelta

from fandom.error import RedirectError, HTTPTimeoutError, FandomError
from fandom import FandomPage
import fandom.util as u

# Generate all extensions from the OS
mimetypes.init()

LANG = ""
SUBFANDOM = ""

def default_url():
  subfandom = SUBFANDOM+"." if SUBFANDOM != "" else ""
  language = LANG+"/" if LANG != "" else ""
  return f"https://{subfandom}fandom.com/{language}"

def set_subfandom(subfandom : str):
  """
  Sets the global subfandom variable

  :param subfandom: The subfandom to set as the global subfandom variable
  :type subfandom: str
  """
  global SUBFANDOM
  SUBFANDOM = subfandom.lower() if subfandom else SUBFANDOM

  for cached_func in (search, summary):
    cached_func.clear_cache()

def set_lang(language):
  """
  Sets the global language variable

  :param language: The language to set as the global language variable
  :type language: str
  """
  global LANG
  LANG = language.lower() if language else LANG

  for cached_func in (search, summary):
    cached_func.clear_cache()

def set_rate_limiting(rate_limit : bool, min_wait : int = 50):
  """
  Enable or disable rate limiting on requests to the fandom servers.
  If rate limiting is not enabled, under some circumstances (depending on
  load on fandom, the number of requests you and other `fandom` users
  are making, and other factors), fandom may return an HTTP timeout error.

  .. note::
    Enabling rate limiting generally prevents that issue, but please note that HTTPTimeoutError still might be raised.

  :param rate_limit: Whether to enable rate limiting or not
  :param min_wait: If rate limiting is enabled, `min_wait` is the minimum time to wait before requests in milliseconds.
  :type min_wait: int
  :type rate_limit: bool
  """

  min_wait = timedelta(milliseconds=min_wait)
  u.RATE_LIMIT = rate_limit
  if not rate_limit:
    u.RATE_LIMIT_MIN_WAIT = None
  else:
    u.RATE_LIMIT_MIN_WAIT = min_wait

  u.RATE_LIMIT_LAST_CALL = None

def set_user_agent(user_agent_string):
  """
  Set the User-Agent string to be used for all requests.

  :param user_agent_string: A string specifying the User-Agent header
  :type user_agent_string: str
  """
  u.USER_AGENT = user_agent_string

@u.cache
def search(query : str, subfandom : str = SUBFANDOM, language: str = LANG, results : str = 10):
  """
  Do a fandom search.

  :param query: What to search for
  :param subfandom: The subfandom to search in (defaults to the global subfandom variable)
  :param language: The language to search in (defaults to the global language variable)
  :param results: The maximum number of results to be returned
  :type query: str
  :type subfandom: str
  :type language: str
  :type results: int

  :returns: :class:`list`
  """
  subfandom = subfandom if subfandom != "" else (SUBFANDOM if SUBFANDOM != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")

  search_params = {
    'action': 'query',
    'subfandom': subfandom,
    'lang': language,
    'srlimit': results,
    "list" : "search",
    'srsearch': query
  }

  raw_results = u._wiki_request(search_params)

  try:
    search_results = (d['title'] for d in raw_results['query']["search"])
  except KeyError:
    raise FandomError(query, subfandom, language)
  return list(search_results)


def random(pages : int = 1, subfandom : str = SUBFANDOM, language : str = LANG):
  """
  Get a list of random fandom article titles.

  .. note:: Random only gets articles from namespace 0, meaning only articles

  :param pages: the number of random pages returned (max of 10)
  :param subfandom: The subfandom to search (defaults to the global subfandom variable. If the global subfandom variable is not set, defaults to "runescape")
  :param language: The language to search in (defaults to the global language variable. If  the global language variable is not set, defaults to english)
  :type pages: int
  :type subfandom: str
  :type language: str

  :returns: :class:`str` or :class:`list` of :class:`str`
  """
  subfandom = subfandom if subfandom != "" else (SUBFANDOM if SUBFANDOM != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")
  
  query_params = {
    'action': 'query',
    'subfandom': subfandom,
    'lang': language,
    'list': 'random',
    'rnlimit':pages,
    'rnnamespace':0
  }

  request = u._wiki_request(query_params)
  titles = [page['title'] for page in request['query']['random']]

  if len(titles) == 1:
    return titles[0]

  return titles


@u.cache
def summary(title : str, subfandom : str = SUBFANDOM, language : str = LANG, sentences : int = -1, redirect : bool = True):
  """
  Plain text summary of the page with the requested title.
  Is just an implementation of :class:`FandomPage.summary`, but with the added
  functionality of requesting a specific amount of sentences.
  
  :param title: The title of the page to get the summary of
  :param subfandom: The subfandom to search (defaults to the global subfandom variable. If the global subfandom variable is not set, defaults to "runescape")
  :param language: The language to search in (defaults to the global language variable. If  the global language variable is not set, defaults to english)
  :param sentences: The maximum number of sentences to output. Defaults to the whole summary
  :param redirect: Allow redirection without raising RedirectError
  :type title: str
  :type subfandom: str
  :type language: str
  :type sentences: int
  :type redirect: bool
  """
  subfandom = subfandom if subfandom != "" else (SUBFANDOM if SUBFANDOM != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")

  page_info = page(title, subfandom = subfandom, language = language, redirect=redirect)
  summary = page_info.summary

  if sentences != -1:
    periods = [m.start() for m in re.finditer(r'\. [A-Z]', summary)] 
    if len(periods) >= sentences:
      summary = summary[:periods[sentences-1]+1]

  return summary


def page(title : str = "", pageid : int = -1, subfandom : str = SUBFANDOM, language : str = LANG, redirect : bool = True, preload : bool = False):
  """
  Get a FandomPage object for the page in the sub fandom with title or the pageid (mutually exclusive).

  :param title: - the title of the page to load
  :param pageid: The numeric pageid of the page to load
  :param subfandom: The subfandom to search (defaults to the global subfandom variable. If the global subfandom variable is not set, defaults to "runescape")
  :param language: The language to search in (defaults to the global language variable. If  the global language variable is not set, defaults to english)
  :param redirect: Allow redirection without raising RedirectError
  :param preload: Load content, summary, images, references, and links during initialization
  :type title: str
  :type pageid: int
  :type subfandom: str
  :type language: str
  :type redirect: bool
  :type preload: bool
  """

  subfandom = subfandom if subfandom != "" else (SUBFANDOM if SUBFANDOM != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")
  
  if title != "":
    return FandomPage(subfandom, language, title=title, redirect=redirect, preload=preload)
  elif pageid != -1:
    return FandomPage(subfandom, language, pageid=pageid, preload=preload)
  else:
    raise ValueError("Either a title or a pageid must be specified")
