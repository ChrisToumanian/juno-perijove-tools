# Juno Perijove Tools
A selection of tools to help with Jovian observations during the Juno orbiter's perijoves.

# Installation and Requirements
Juno Perijove Tools works with Python 3 and later.

# Using Juno Perijove Tools
Perijove.py provides an up-to-date list of Juno's predicted orbits. Select a perijove to view the optimimum estimated observation time.

Horizons.py assists with queries to JPL HORIZONS, an on-line solar system data and ephemeris computation service. Include horizons.py and use the class HorizonsRequest to select a center, target, time, and quantities matching to what is available on the HORIZONS system's web-interface (https://ssd.jpl.nasa.gov/horizons.cgi). Keys can be added and modified. After the request has been sent you can retrieve a list of all lines of the response or a dictionary with the results of the query.
