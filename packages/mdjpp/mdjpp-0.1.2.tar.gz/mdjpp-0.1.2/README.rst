Journal PreProcessor
--------------------

Journal PreProcessor - mdJPP - is a preporcessor for plain text documents that
supports tagging.

Use case
========

Suppose that you are obliged (or you want to) log progress of your work.
One of the simplest way to do it is to put notes into some plain text file.
The more you work, the more notes you write. Finally, the file can be use as a
basis for some kind of report or even as a report itself. If you decide to use
markup, let it be `Markdown <https://daringfireball.net/projects/markdown>`_, your notes may look quite elegant.

Imagine now, that you are *dr. No* and you work in *ACME* company as a member of
*Y-man support team*. You did some work. Each day you put some notes and
used some tags. Your work log may look following::

    **ACME**

    Y-man support team
    dr No

    Work log.

    20181022
    --------

    *X-substance*

    Testing alternative synthesis:

    * Z + Y -> X
    * Z + V + U -> X + W

    *garden*

    Singing to the flowers.

    20181023
    --------

    *X-substance* *IT*

    Simulation of X-substance stability.

    *garden*

    Taking care of bees.

    20181024
    --------

    *X-substance*

    Purification.
    
    **It's alive!**

Although, markup languages are nice and allows to produce nice looking documents 
or web pages, they lack of convenient support for tagging. In the above example
*X-substance* annotation was consequently used to mark actions related to *X-substance* development etc.

Obvious question emerges, how to get a report on *X-substance* only?

Solution
========

The above log can be annotated according to mdJPP tagging syntax. It cane be later
submitted to mdJPP preprocessor that can produce document extracts according to
tags and dates.

Syntax
^^^^^^

mdJPP tags, including dates, starts always with double ``@@`` character.
In the current version only one tag can be used in one line so there is no
inline tags (not yet!). There are two types of tags:

#. Date tags, for example ``@@20181103``.
#. (Normal) tags, for example ``@@X-substance``.

Please note, that dates are always written as YYYYMMDD.

Normal tags can be joined. If particular note is related with *X-substance*
development and *IT* work, it can be annotated with two tags::

    @@X-substance
    @@IT
    
Tags written one after another without blank lines are joined and note that
follows is tagged with *X-substance* and *IT*.

Structure
^^^^^^^^^

mdJPP annotated documents **always** have following structure:

* Plain text (optional)
* Global normal tags that annotate all that follows (optional)
    * Plain text (optional)
    * Date tag (optional)
        * Plain text (optional)
        * Normal tag that annotate text note that follows (optional)
            * Plain text (optional)
        * Normal tag that annotate text note that follows (optional)
            * ...
    * Date tag (optional)
        * ...

Please note two facts:

#. All elements of the document's structure are optional.
#. All mdJPP documents have **always** the same structure.

Example
^^^^^^^

Let's use mdJPP tagging for *dr. No* notes::

    **ACME**

    @@Y-man support team
    @@dr No

    Work log.

    @@20181022

    @@X-substance

    Testing alternative synthesis:

    * Z + Y -> X
    * Z + V + U -> X + W

    @@garden

    Singing to the flowers.

    @@20181023

    @@X-substance
    @@IT

    Simulation of X-substance stability.

    @@garden

    Taking care of bees.

    @@20181024

    @@X-substance

    Purification.

    **It's alive!**

Usage
=====

Once the log is annotated with mdJPP tags, prepocessor can be used to produce nice
looking document by redirecting its output to, say, `pandoc <https://pandoc.org/>`_::

    mdjpp dr_no_log.mdj | pandoc > dr_no_log.html

This is all unless you want to do some filtering.

Filters
^^^^^^^

**ACME** boss wants you to report progress on *X-substance* development since October 23rd?
::

    mdjpp dr_no_log.mdj --only-tag X-substance --date-from 20181023
    
Want to do more?
::
   
    mdjpp --help
    
   
Index
^^^^^

If several files are submitted to mdJPP and one of them ends with `index.mdj` it
is processed first.

This allows to put all global tags and other titles to the index and real work
logs can be kept in other files.

Example
^^^^^^^

So, how it looks like? It depends on rendering options. Currently, three rendering engines
are available:

#. *Null* - This render engine does not render at all. Useful when you want to do filtering only. This is default render engine.
#. *Markdown* - Changes global, date, and normal tags to header level 1, 2, and 3 accordingly. Uses some emphasis for tags strings. To switch it on use ``--md`` option. It is useful when you want to produce PDF or ODT documents.
#. *HTML* - Renders global and normal tags as *nice* boxes with coloured text. Uses emphasis for date tags and uses some horizontal lines. To switch it on use ``--html`` option.

Here are examples of HTML documents created with `HTML rendering engine <https://tljm.github.io/mdjpp/test_journal.html>`_, and with
`Markdown rendering engine <https://tljm.github.io/mdjpp/test_journal_md.html>`_.

Look also at this `PDF document created with Markdown rendering engine <https://tljm.github.io/mdjpp/test_journal.pdf>`_.

**Please note** that the above examples are done with `pandoc <https://pandoc.org/>`_ ``--metadata="title:Your smart title"``. The title is, therefore, added at the beginning of documents.


Installation
============

mdJPP can be installed with following command::

    pip install mdjpp
    
Question & Answer
=================

#. *Hey dude, why don't you put all that notes to some database and use SQL to query DB and get what you want?*
   
   That's a very good question. Well, may be, may be... 
