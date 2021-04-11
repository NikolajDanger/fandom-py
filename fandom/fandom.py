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
WIKI = ""

def default_url():
  wiki = WIKI+"." if WIKI != "" else ""
  language = LANG+"/" if LANG != "" else ""
  return f"https://{wiki}fandom.com/{language}"

def set_wiki(wiki : str):
  """
  Sets the global wiki variable

  :param wiki: The wiki to set as the global wiki variable
  :type wiki: str
  """
  global WIKI
  WIKI = wiki.lower() if wiki else WIKI

  for cached_func in (search, summary):
    cached_func.clear_cache()

def set_lang(language : str):
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

def set_user_agent(user_agent_string : str):
  """
  Set the User-Agent string to be used for all requests.

  :param user_agent_string: A string specifying the User-Agent header
  :type user_agent_string: str
  """
  u.USER_AGENT = user_agent_string

@u.cache
def search(query : str, wiki : str = WIKI, language: str = LANG, results : int = 10):
  """
  Do a fandom search.

  The search returns a list of tuples, with the page title and the page id.

  :param query: What to search for
  :param wiki: The wiki to search in (defaults to the global wiki variable)
  :param language: The language to search in (defaults to the global language variable)
  :param results: The maximum number of results to be returned
  :type query: str
  :type wiki: str
  :type language: str
  :type results: int

  :returns: :class:`list` of :class:`tuple`
  """
  wiki = wiki if wiki != "" else (WIKI if WIKI != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")

  search_params = {
    'action': 'query',
    'wiki': wiki,
    'lang': language,
    'srlimit': results,
    "list" : "search",
    'srsearch': query
  }

  raw_results = u._wiki_request(search_params)

  try:
    search_results = [(d['title'], d['pageid']) for d in raw_results['query']['search']]
  except KeyError:
    raise FandomError(query, wiki, language)
  return list(search_results)


def random(pages : int = 1, wiki : str = WIKI, language : str = LANG):
  """
  Get a list of random fandom article titles.

  Returns the results as tuples with the title and page id.

  .. note:: Random only gets articles from namespace 0, meaning only articles

  :param pages: the number of random pages returned (max of 10)
  :param wiki: The wiki to search (defaults to the global wiki variable. If the global wiki variable is not set, defaults to "runescape")
  :param language: The language to search in (defaults to the global language variable. If  the global language variable is not set, defaults to english)
  :type pages: int
  :type wiki: str
  :type language: str

  :returns: :class:`tuple` if the pages parameter was 1, :class:`list` of :class:`tuple` if it was larger
  """
  wiki = wiki if wiki != "" else (WIKI if WIKI != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")

  query_params = {
    'action': 'query',
    'wiki': wiki,
    'lang': language,
    'list': 'random',
    'rnlimit':pages,
    'rnnamespace':0
  }

  request = u._wiki_request(query_params)
  titles = [(page['title'], page['id']) for page in request['query']['random']]

  if len(titles) == 1:
    return titles[0]

  return titles


@u.cache
def summary(title : str, wiki : str = WIKI, language : str = LANG, sentences : int = -1, redirect : bool = True):
  """
  Plain text summary of the page with the requested title.
  Is just an implementation of :class:`FandomPage.summary`, but with the added
  functionality of requesting a specific amount of sentences.

  :param title: The title of the page to get the summary of
  :param wiki: The wiki to search (defaults to the global wiki variable. If the global wiki variable is not set, defaults to "runescape")
  :param language: The language to search in (defaults to the global language variable. If  the global language variable is not set, defaults to english)
  :param sentences: The maximum number of sentences to output. Defaults to the whole summary
  :param redirect: Allow redirection without raising RedirectError
  :type title: str
  :type wiki: str
  :type language: str
  :type sentences: int
  :type redirect: bool
  """
  wiki = wiki if wiki != "" else (WIKI if WIKI != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")

  page_info = page(title, wiki = wiki, language = language, redirect=redirect)
  summary = page_info.summary

  if sentences != -1:
    periods = [m.start() for m in re.finditer(r'\. [A-Z]', summary)]
    if len(periods) >= sentences:
      summary = summary[:periods[sentences-1]+1]

  return summary


def page(title : str = "", pageid : int = -1, wiki : str = WIKI, language : str = LANG, redirect : bool = True, preload : bool = False):
  """
  Get a FandomPage object for the page in the sub fandom with title or the pageid (mutually exclusive).

  :param title: - the title of the page to load
  :param pageid: The numeric pageid of the page to load
  :param wiki: The wiki to search (defaults to the global wiki variable. If the global wiki variable is not set, defaults to "runescape")
  :param language: The language to search in (defaults to the global language variable. If  the global language variable is not set, defaults to english)
  :param redirect: Allow redirection without raising RedirectError
  :param preload: Load content, summary, images, references, and links during initialization
  :type title: str
  :type pageid: int
  :type wiki: str
  :type language: str
  :type redirect: bool
  :type preload: bool
  """

  wiki = wiki if wiki != "" else (WIKI if WIKI != "" else "runescape")
  language = language if language != "" else (LANG if LANG != "" else "en")

  if title != "":
    return FandomPage(wiki, language, title=title, redirect=redirect, preload=preload)
  elif pageid != -1:
    return FandomPage(wiki, language, pageid=pageid, preload=preload)
  else:
    raise ValueError("Either a title or a pageid must be specified")
