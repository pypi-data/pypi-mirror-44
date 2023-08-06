================
MGL EFIS Plotter
================

The MGL EFIS Plotter package parses the flight data logs from
MGL EFIS products, such as the iEFIS.
It can read both ``IEFISS.REC`` and ``IEFISBB.DAT`` files.

The package is intended to be used inside a Jupyter Notebook
to create graphs. It can also save subsets of the data as CSV files.


Installation
------------

Install with pip or your favorite Python package manager::

  pip install mgl_efis_plotter


Sample Usage
------------

Jupyter Notebook cell:

.. code-block:: python

    from mgl_efis_plotter import *

    config = Config()
    flights = create_flights('IEFIS.REC', config)

    p = Plot(flights[0])
    p.plot2(['pAltitude', 'densityAltitude', 'oat']).show()

Author
------

| Art Zemon
| art@zemon.name
| https://cheerfulcurmudgeon.com/

Copyright and MIT License
-------------------------

|copy| Copyright 2019 Art Zemon.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. |copy| unicode:: U+000A9 .. COPYRIGHT SIGN
