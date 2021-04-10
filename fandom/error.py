"""
Global fandom exception and warning classes.
"""

import sys


ODD_ERROR_MESSAGE = "This shouldn't happen. Please report on GitHub: github.com/goldsmith/fandom"


class FandomException(Exception):
  """Base fandom exception class."""

  def __init__(self, error):
    self.error = error

  def __unicode__(self):
    return "An unknown error occurred: \"{0}\". Please report it on GitHub!".format(self.error)

  if sys.version_info > (3, 0):
    def __str__(self):
      return self.__unicode__()

  else:
    def __str__(self):
      return self.__unicode__().encode('utf8')


class PageError(FandomException):
  """Exception raised when no fandom matched a query."""

  def __init__(self, pageid=None, *args):
    if pageid:
      self.pageid = pageid
    else:
      self.title = args[0]

  def __unicode__(self):
    if hasattr(self, 'title'):
      return u"\"{0}\" does not match any pages. Try another query!".format(self.title)
    else:
      return u"Page id \"{0}\" does not match any pages. Try another id!".format(self.pageid)

class RedirectError(FandomException):
  """Exception raised when a page title unexpectedly resolves to a redirect."""

  def __init__(self, title):
    self.title = title

  def __unicode__(self):
    return u"\"{0}\" resulted in a redirect. Set the redirect property to True to allow automatic redirects.".format(self.title)


class HTTPTimeoutError(FandomException):
  """Exception raised when a request to the Mediawiki servers times out."""

  def __init__(self, query):
    self.query = query

  def __unicode__(self):
    return u"Searching for \"{0}\" resulted in a timeout. Try again in a few seconds, and make sure you have rate limiting set to True.".format(self.query)

class FandomError(FandomException):
  """Exception raised when the requested query can't be found"""
  def __init__(self, query, wiki, language):
    self.query = query
    self.wiki = wiki
    self.language = language

  def __unicode__(self):
    return u"Could not locate page \"{}\" on wiki \"{}\" with language \"{}\"".format(self.query, self.wiki, self.language)

class RequestError(FandomException):
  """
  Exception raised when the request does not return usable data.
  Usually raised when the wiki doesn't exist in the requested language
  """
  def __init__(self, url, params):
    self.url = url
    self.params = params

  def __unicode__(self):
    return u"Your request to the url \"{url}\" with the paramaters \"{params}\" either returned nothing or returned data in a format other than JSON. Please check your input data.".format(url=self.url, params=self.params)