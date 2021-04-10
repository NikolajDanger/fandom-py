Getting started
===============

You can start by installing the package with:

.. code-block::

    $ pip install fandom-py


Example use case
----------------

We start by importing fandom into our project.

.. code-block:: python

    import fandom

Now let's say we want to know about `Kvothe`_ from the *Kingkiller Chronicles* book series by Pattrick Rothfuss. We should start by setting the wiki to the *kingkiller wiki* using :class:`fandom.set_wiki`. We can also set the wiki using a parameter each time we use a fandom function, but since we're going to be calling several different fandom functions, setting it now is probably a good idea:

.. code-block:: python

    fandom.set_wiki("kingkiller")

.. note::

    Not setting a wiki will result in all your fandom function calls going to the *runescape wiki*.

We don't need to use the :class:`fandom.set_lang` function, since the language defaults to english, which is the language we want the page in.

Now Kvothe has a lot of names, and we're not sure which one is used on his wiki page. So we can search for *Kvothe* on the wiki, and his page should probably come up first. Setting the ``results`` parameter to 1 ensures that we only get the top result for our search:

.. code-block:: python

    fandom.search("Kvothe", results = 1)
    # ['Kvothe']

Seems like Kvothe's wiki page just has the title *Kvothe*. We can use this information to initiate a :class:`fandom.FandomPage` object for the wiki page. The :class:`fandom.FandomPage` object contains all usable information about the given page.

.. code-block:: python

    page = fandom.page(title = "Kvothe")

Here we used the page title to initialize the page object, but if we had the page-id, we could also have used that:

.. code-block:: python

    page.pageid
    # 2230
    page2 = fandom.page(pageid = 2230)
    page2.title
    # Kvothe
    page == page2
    # True

Now we have the page for Kvothe, we can gain information from it. We can start by getting the first part of the page, which we can get with the :class:`fandom.FandomPage.summary` property:

.. code-block:: python

    page.summary
    # 'Kvothe is the main character in the Kingkiller Chronicle. His name is pronounced kəˈvōTH, much like the word quoth but beginning the same as the Yiddish term "Kvetch." '

Names are pretty important in *The Kingkiller Chronicles*, so we probably shouldn't be surprised that the pronounciation of his name is the first thing the wiki wants us to know.

But what if we want to know something else? Like his physical appearance. Well we can get a list of all sections on a page with the :class:`fandom.FandomPage.sections` property:

.. code-block:: python

    page.sections
    # ['Description', 'In The Chronicle', 'Early life', 'Tarbean', 'The University', 'First Term (Spring)', 'Second Term (Summer)', 'Third Term (Fall)', 'Fourth Term (Fall)', 'Vintas', 'The Faen Realm', 'Ademre', 'Return to the University', 'Fifth Term (Winter)', 'Sixth Term (Spring)', 'Seventh Term (Summer)', 'The present', 'Other Names', 'Kote', 'Reshi', 'Maedre', 'Dulator', 'Shadicar', 'Lightfinger', 'Six-String', 'Kvothe the Bloodless', 'Kvothe the Arcane', 'Kvothe Kingkiller', 'Speculation', 'Naming', 'Identity', 'Rings', 'Kvothe and Kote', 'Fan arts', 'References']

All sections and subsections are included in the list, which explains the long list of names after the "other names" section title.

"Description" seems like the section with the biggest potential of telling us how he looks, so let's try getting the text from that, using the :class:`fandom.FandomPage.section` method:

.. code-block:: python

    page.section("Description")
    # "Description
    # Kvothe has pale skin and green eyes, though the intensity of this color is often noted as changing throughout the series. His eyes are similar to the description of his mother's eyes. He has extremely red hair often compared to a flame.
    # He is exceptionally intelligent, quick-witted, sharp-tongued and clever, as well as a talented musician. He is also very curious, a quality that often gets him into trouble. He has a nasty temper, is reckless and often thoughtless.
    # In the books, some evidence (mostly cover illustrations) suggest that he is left-handed."

If we want more information about the structure of sections and subsections, we can use the `fandom.FandomPage.content` property, which returns a dict structured like this:

.. code-block::

    {
        'title' : 'The page title'
        'content' : 'The text before the first section starts'
        'infobox' : 'The text contained in the page's infobox'
        'sections' : [
            {
                'title' : 'The section title'
                'content' : 'The text in the section before the first subsection starts'
                'sections' : [
                    {
                        'title' : 'The subsection title'
                        'content' : 'The text in the subsection'
                    },
                    ...
                ]
            },
            ...
        ]
    }

Finally, we need a good picture of Kvothe. We can use the :class:`fandom.FandomPage.images` property for that:

.. code-block:: python

    page.images[0]
    # 'https://static.wikia.nocookie.net/nameofthewind/images/6/68/The_kingkiller_chronicle_kvothe_by_shilesque-d8m6yzz.jpg/revision/latest?cb=20190916153424'

And now you have a basic understanding of what you can do with fandom-py. Do check out the rest of the documentation if you want to know more.

.. _Kvothe: https://kingkiller.fandom.com/wiki/Kvothe