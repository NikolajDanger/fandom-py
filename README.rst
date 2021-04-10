fandom-py
=========

**fandom-py** is a Python library that makes it easy to access and parse
data from any `Fandom website <https://www.fandom.com>`_

Search a Fandom, get article summaries, get data like links and images
from a page, and more. *fandom-py* wraps the Fandom API so you can focus on using
Fandom data, not getting it.´

.. code:: python

  >>> import fandom
  >>> print(fandom.summary("Banshee", "Runescape"))
  # Banshees are Slayer monsters that require level 15 Slayer to kill. They frequently drop 13 noted pure essence, making them an alternative source of essence. Additionally, banshees tend to frequently drop many different types of herbs. Mighty banshees are a higher-levelled alternative, if this is given as your Slayer assignment.

  >>> fandom.search("Forest", "Runescape")
  # ['Forest', "Forester's Arms", 'Forester (Burgh de Rott Ramble)', 'Forester', 'Forest Beyond', 'Nemi Forest', 'Dense forest', 'Jungle forester', 'Freaky Forester', "Bartender (Forester's Arms)"]

  >>> fandom.set_subfandom("Runescape")
  >>> drakan = fandom.page("Castle Drakan")
  >>> drakan.title
  # u'Castle Drakan'
  >>> drakan.url
  # u'http://runescape.fandom.com/wiki/Castle_Drakan'
  >>> drakan.plain_text
  # u'Castle Drakan is the home of Lord Drakan, the vampyre lord of Morytania. Found just north of Meiyerditch, it looms over the Sanguinesti region'...

  >>> fandom.set_lang("nl") # Dutch
  >>> fandom.summary("Runes", "Runescape", sentences=1)
  # Runes, of Magische runes zijn kleine gewichtloze steentjes waarmee spelers een spreuk kunnen uitvoeren.

Note: this library was designed for ease of use and simplicity, not for advanced use.

Installation
------------

To install fandom-py, simply run:

::

  $ pip install fandom-py

fandom-py is compatible with Python 3.9+.

Tests
-------------

To run tests, clone the `respository on GitHub <https://github.com/NikolajDanger/fandom-py>`__, then run:

::

  $ pip install -r requirements.txt
  $ bash runtests.bat  # will run tests for python
  $ runtests.bat # will run tests for python (windows)
  $ python3 -m unittest discover -s fandom/tests -p '*test.py'  # manual style

in the root project directory.

License
-------

MIT licensed. See the `LICENSE
file <https://github.com/NikolajDanger/fandom-py/blob/master/LICENSE>`__ for
full details.

Credits
-------

-  `wiki-api <https://github.com/richardasaurus/wiki-api>`__ by
   @richardasaurus for inspiration
-  @nmoroze and @themichaelyang for feedback and suggestions
-  The `Wikimedia
   Foundation <http://wikimediafoundation.org/wiki/Home>`__ for giving
   the world free access to data
-  @goldsmith for making such a fantastic library to fork
-  /u/captainmeta4 for giving the idea for a reddit bot to post game wiki info
   like auto-wiki bot
-  @timidger for writing the wikia code this is based on

