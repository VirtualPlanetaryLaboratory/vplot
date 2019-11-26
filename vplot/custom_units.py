# -*- coding: utf-8 -*-
import astropy.units as u

# Alias for second
sec = u.def_unit("sec", u.second)

# TODO: Unit in BINARY
F_FEarth = u.def_unit("F/F_Earth", u.Unit(""))

# Register the units
u.add_enabled_units([sec, F_FEarth])
