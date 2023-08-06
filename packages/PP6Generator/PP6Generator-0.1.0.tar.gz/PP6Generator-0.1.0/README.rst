PP6Generator
============

A toolkit for generating ProPresenter6 files.

Getting started
---------------

Install with ``pip``:

.. code:: bash

   $ pip install PP6Generator

Then:

.. code:: python

   from PP6Generator import Presentation, Slide, Text

   t1 = Text()
   t1.add_text(['Hello there!'])
   t2 = Text()
   t2.add_text(['General Kenobi!'])

   s1 = Slide()
   s1.add_display_element(t)
   s2 = Slide()
   s2.add_display_element(t)

   p = Presentation()
   p.add_slides([s1, s2])
   p.set_title('Hello')

   # Generate a file called Hellop.pro6
   p.generate_file()
