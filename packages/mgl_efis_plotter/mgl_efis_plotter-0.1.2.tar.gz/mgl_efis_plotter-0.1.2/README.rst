================
MGL EFIS Plotter
================

The MGL EFIS Plotter package parses the flight data logs from
MGL EFIS products, such as the iEFIS.
It can read both ``IEFISBB.DAT`` files and ``IEFISS.REC`` files.

The package is intended to be used inside a Jupyter Notebook
to create graphs. It can also save subsets of the data as CSV files.


Installation
------------

``pip install mgl_efis_plotter``


Sample Usage
------------

Jupyter Notebook cell::

    from mgl_efis_plotter import *

    config = Config()

    flights = createFlights('IEFIS.REC', config)

    p = Plot(flights[0])

    p.plot2(['pAltitude', 'densityAltitude', 'oat']).show()


Author
------

Art Zemon art@zemon.name

Copyright
---------
(c) Copyright 2019 Art Zemon

License
-------

MIT
