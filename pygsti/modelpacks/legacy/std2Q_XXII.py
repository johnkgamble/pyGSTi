#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************
"""
Variables for working with the 2-qubit model containing the gates
I*I, I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and X(pi/2)*X(pi/2)
"""

import sys as _sys

from ...construction import circuitconstruction as _strc
from ...construction import modelconstruction as _setc
from ...construction import stdtarget as _stdtarget

description = "I*I, I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and X(pi/2)*X(pi/2) gates"

gates = ['Gii', 'Gix', 'Giy', 'Gxi', 'Gyi', 'Gxx']

fiducials16 = _strc.to_circuits(
    [(), ('Gix',), ('Giy',), ('Gix', 'Gix'),
     ('Gxi',), ('Gxi', 'Gix'), ('Gxi', 'Giy'), ('Gxi', 'Gix', 'Gix'),
     ('Gyi',), ('Gyi', 'Gix'), ('Gyi', 'Giy'), ('Gyi', 'Gix', 'Gix'),
     ('Gxi', 'Gxi'), ('Gxi', 'Gxi', 'Gix'), ('Gxi', 'Gxi', 'Giy'), ('Gxi', 'Gxi', 'Gix', 'Gix')], line_labels=('*',))

fiducials36 = _strc.to_circuits(
    [(),
     ('Gix',),
     ('Giy',),
     ('Gix', 'Gix'),
     ('Gix', 'Gix', 'Gix'),
     ('Giy', 'Giy', 'Giy'),
     ('Gxi',),
     ('Gxi', 'Gix'),
     ('Gxi', 'Giy'),
     ('Gxi', 'Gix', 'Gix'),
     ('Gxi', 'Gix', 'Gix', 'Gix'),
     ('Gxi', 'Giy', 'Giy', 'Giy'),
     ('Gyi',),
     ('Gyi', 'Gix'),
     ('Gyi', 'Giy'),
     ('Gyi', 'Gix', 'Gix'),
     ('Gyi', 'Gix', 'Gix', 'Gix'),
     ('Gyi', 'Giy', 'Giy', 'Giy'),
     ('Gxi', 'Gxi'),
     ('Gxi', 'Gxi', 'Gix'),
     ('Gxi', 'Gxi', 'Giy'),
     ('Gxi', 'Gxi', 'Gix', 'Gix'),
     ('Gxi', 'Gxi', 'Gix', 'Gix', 'Gix'),
     ('Gxi', 'Gxi', 'Giy', 'Giy', 'Giy'),
     ('Gxi', 'Gxi', 'Gxi'),
     ('Gxi', 'Gxi', 'Gxi', 'Gix'),
     ('Gxi', 'Gxi', 'Gxi', 'Giy'),
     ('Gxi', 'Gxi', 'Gxi', 'Gix', 'Gix'),
     ('Gxi', 'Gxi', 'Gxi', 'Gix', 'Gix', 'Gix'),
     ('Gxi', 'Gxi', 'Gxi', 'Giy', 'Giy', 'Giy'),
     ('Gyi', 'Gyi', 'Gyi'),
     ('Gyi', 'Gyi', 'Gyi', 'Gix'),
     ('Gyi', 'Gyi', 'Gyi', 'Giy'),
     ('Gyi', 'Gyi', 'Gyi', 'Gix', 'Gix'),
     ('Gyi', 'Gyi', 'Gyi', 'Gix', 'Gix', 'Gix'),
     ('Gyi', 'Gyi', 'Gyi', 'Giy', 'Giy', 'Giy')], line_labels=('*',))

fiducials = fiducials16
prepStrs = fiducials16

effectStrs = _strc.to_circuits(
    [(), ('Gix',), ('Giy',),
     ('Gix', 'Gix'), ('Gxi',),
     ('Gyi',), ('Gxi', 'Gxi'),
     ('Gxi', 'Gix'), ('Gxi', 'Giy'),
     ('Gyi', 'Gix'), ('Gyi', 'Giy')], line_labels=('*',))

germs = _strc.to_circuits(
    [('Gii',),
     ('Gxi',),
     ('Gyi',),
     ('Gix',),
     ('Giy',),
     ('Gxx',),
     ('Gxi', 'Gyi'),
     ('Gix', 'Giy'),
     ('Giy', 'Gyi'),
     ('Gix', 'Gxi'),
     ('Gix', 'Gyi'),
     ('Giy', 'Gxi'),
     ('Gii', 'Gix'),
     ('Gii', 'Giy'),
     ('Gii', 'Gyi'),
     ('Giy', 'Gxx'),
     ('Gyi', 'Gxx'),
     ('Gxi', 'Gxi', 'Gyi'),
     ('Gix', 'Gix', 'Giy'),
     ('Gxi', 'Gyi', 'Gyi'),
     ('Gix', 'Giy', 'Giy'),
     ('Giy', 'Gxi', 'Gxi'),
     ('Giy', 'Gxi', 'Gyi'),
     ('Gix', 'Gxi', 'Giy'),
     ('Gix', 'Gyi', 'Gxi'),
     ('Gix', 'Gyi', 'Giy'),
     ('Gix', 'Giy', 'Gyi'),
     ('Gix', 'Giy', 'Gxi'),
     ('Giy', 'Gyi', 'Gxi'),
     ('Gxi', 'Gyi', 'Gii'),
     ('Gxi', 'Gii', 'Gyi'),
     ('Gxi', 'Gii', 'Gii'),
     ('Gyi', 'Gii', 'Gii'),
     ('Gix', 'Giy', 'Gii'),
     ('Gix', 'Gii', 'Giy'),
     ('Gix', 'Gii', 'Gii'),
     ('Giy', 'Gii', 'Gii'),
     ('Gii', 'Gix', 'Gyi'),
     ('Gii', 'Giy', 'Gyi'),
     ('Gii', 'Gyi', 'Gix'),
     ('Gxi', 'Gyi', 'Gxx'),
     ('Gyi', 'Gxx', 'Gxx'),
     ('Giy', 'Gxx', 'Gxx'),
     ('Giy', 'Gyi', 'Gxx'),
     ('Gix', 'Gix', 'Gxx'),
     ('Gix', 'Giy', 'Gxx'),
     ('Gix', 'Gxx', 'Gxi'),
     ('Gii', 'Gxx', 'Gxx'),
     ('Gix', 'Gxx', 'Giy'),
     ('Giy', 'Gxx', 'Gyi'),
     ('Gxi', 'Gxi', 'Gxx'),
     ('Gyi', 'Gix', 'Gxi', 'Giy'),
     ('Gix', 'Giy', 'Gxi', 'Gyi'),
     ('Gix', 'Gix', 'Gix', 'Giy'),
     ('Gxi', 'Gyi', 'Gyi', 'Gyi'),
     ('Gyi', 'Gyi', 'Giy', 'Gyi'),
     ('Gyi', 'Gix', 'Gix', 'Gix'),
     ('Gxi', 'Gyi', 'Gix', 'Gix'),
     ('Gxi', 'Gyi', 'Gyi', 'Gii'),
     ('Gix', 'Giy', 'Giy', 'Gii'),
     ('Giy', 'Gxi', 'Gii', 'Gii'),
     ('Gix', 'Gii', 'Gii', 'Gxi'),
     ('Gxx', 'Gxx', 'Gyi', 'Gyi'),
     ('Giy', 'Gxx', 'Gxi', 'Giy'),
     ('Gxx', 'Gxx', 'Gxx', 'Gix', 'Gxi'),
     ('Giy', 'Gyi', 'Gxi', 'Gxi', 'Giy'),
     ('Gxi', 'Gxi', 'Giy', 'Gyi', 'Giy'),
     ('Giy', 'Gix', 'Gxi', 'Gix', 'Gxi'),
     ('Gyi', 'Giy', 'Gyi', 'Gix', 'Gix'),
     ('Giy', 'Gxi', 'Gix', 'Giy', 'Gyi'),
     ('Giy', 'Giy', 'Gxi', 'Gyi', 'Gxi'),
     ('Gyi', 'Gyi', 'Giy', 'Gxx', 'Giy'),
     ('Gxi', 'Gix', 'Giy', 'Gxi', 'Giy', 'Gyi'),
     ('Gxi', 'Giy', 'Gix', 'Gyi', 'Gix', 'Gix'),
     ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
     ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
     ('Gyi', 'Gxi', 'Gix', 'Giy', 'Gxi', 'Gix'),
     ('Gyi', 'Gxi', 'Gix', 'Gxi', 'Gix', 'Giy'),
     ('Gxi', 'Gix', 'Giy', 'Giy', 'Gxi', 'Gyi'),
     ('Gix', 'Giy', 'Giy', 'Gix', 'Gxi', 'Gxi'),
     ('Gyi', 'Giy', 'Gxi', 'Giy', 'Giy', 'Giy'),
     ('Gyi', 'Gyi', 'Gyi', 'Giy', 'Gyi', 'Gix'),
     ('Giy', 'Giy', 'Gxi', 'Giy', 'Gix', 'Giy'),
     ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gxx', 'Gyi'),
     ('Giy', 'Gix', 'Gyi', 'Gyi', 'Gix', 'Gxi', 'Giy'),
     ('Gii', 'Gyi', 'Gxi', 'Gxx', 'Gxx', 'Gix', 'Gxx'),
     ('Gxx', 'Gxx', 'Gxx', 'Gxi', 'Gix', 'Gii', 'Giy'),
     ('Gyi', 'Gxi', 'Giy', 'Gxi', 'Gix', 'Gxi', 'Gyi', 'Giy'),
     ('Gix', 'Gix', 'Gyi', 'Gxi', 'Giy', 'Gxi', 'Giy', 'Gyi')
     ], line_labels=('*',))

germs_lite = _strc.to_circuits(
    [('Gii',),
     ('Gxi',),
     ('Gyi',),
     ('Gix',),
     ('Giy',),
     ('Gxx',),
     ('Gxi', 'Gyi'),
     ('Gix', 'Giy'),
     ('Gxi', 'Gxi', 'Gyi'),
     ('Gix', 'Gix', 'Giy'),
     ('Gxx', 'Gxx', 'Gxx', 'Gix', 'Gxi'),
     ('Gxi', 'Gix', 'Giy', 'Gxi', 'Giy', 'Gyi'),
     ('Gxi', 'Giy', 'Gix', 'Gyi', 'Gix', 'Gix'),
     ('Gyi', 'Gxi', 'Giy', 'Gxi', 'Gix', 'Gxi', 'Gyi', 'Giy')
     ], line_labels=('*',))

#Construct the target model
_target_model = _setc.create_explicit_model(
    [('Q0', 'Q1')], ['Gii', 'Gix', 'Giy', 'Gxi', 'Gyi', 'Gxx'],
    ["I(Q0):I(Q1)", "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "X(pi/2,Q0):I(Q1)",
     "Y(pi/2,Q0):I(Q1)", "X(pi/2,Q0):X(pi/2,Q1)"],
    effect_labels=['00', '01', '10', '11'], effect_expressions=["0", "1", "2", "3"])

_gscache = {("full", "auto"): _target_model}


def target_model(parameterization_type="full", sim_type="auto"):
    """
    Returns a copy of the target model in the given parameterization.

    Parameters
    ----------
    parameterization_type : {"TP", "CPTP", "H+S", "S", ... }
        The gate and SPAM vector parameterization type. See
        :function:`Model.set_all_parameterizations` for all allowed values.

    sim_type : {"auto", "matrix", "map", "termorder:X" }
        The simulator type to be used for model calculations (leave as
        "auto" if you're not sure what this is).

    Returns
    -------
    Model
    """
    return _stdtarget._copy_target(_sys.modules[__name__], parameterization_type,
                                   sim_type, _gscache)


global_fidPairs = [
    (0, 5), (0, 8), (1, 2), (1, 5), (2, 7), (2, 8), (3, 4), (3, 9),
    (3, 10), (4, 5), (5, 0), (5, 2), (5, 7), (6, 5), (6, 7),
    (6, 8), (6, 10), (7, 7), (8, 2), (8, 9), (8, 10), (9, 4),
    (9, 9), (10, 6), (10, 7), (11, 3), (11, 4), (12, 4), (13, 3),
    (14, 1), (14, 2), (15, 1), (15, 4), (15, 7)]

pergerm_fidPairsDict = {
    ('Gix',): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3),
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10),
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8),
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8),
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3),
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8),
        (15, 9)],
    ('Gyi',): [
        (3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 7), (6, 0),
        (6, 8), (7, 2), (7, 4), (7, 9), (8, 0), (8, 7), (9, 2),
        (9, 3), (10, 9), (10, 10), (14, 7), (14, 9), (15, 10)],
    ('Gxx',): [
        (0, 0), (1, 5), (2, 4), (3, 3), (3, 5), (5, 2), (6, 1),
        (6, 8), (6, 10), (8, 6), (10, 2), (10, 8), (10, 10),
        (11, 8), (12, 1), (13, 1), (13, 4), (13, 6), (13, 10),
        (14, 8), (15, 3)],
    ('Gii',): [
        (0, 8), (1, 0), (1, 1), (1, 3), (1, 10), (2, 5), (2, 9),
        (3, 3), (3, 9), (4, 3), (4, 8), (5, 0), (5, 5), (5, 7),
        (6, 4), (6, 6), (6, 8), (6, 10), (7, 0), (7, 2), (7, 3),
        (7, 4), (7, 6), (7, 10), (8, 3), (8, 5), (9, 3), (9, 4),
        (9, 5), (9, 6), (9, 8), (9, 9), (10, 3), (10, 9), (10, 10),
        (11, 1), (11, 5), (12, 5), (12, 7), (12, 9), (13, 0),
        (13, 10), (14, 0), (14, 1), (14, 2), (14, 6), (15, 0),
        (15, 5), (15, 6), (15, 7), (15, 8)],
    ('Giy',): [
        (0, 0), (0, 7), (1, 1), (3, 5), (3, 6), (4, 2), (4, 4),
        (4, 5), (5, 3), (5, 7), (7, 1), (7, 8), (8, 5), (9, 4),
        (9, 5), (9, 9), (10, 5), (11, 5), (11, 6), (11, 8), (11, 10),
        (12, 0), (12, 3), (13, 10), (14, 0), (14, 5), (14, 6),
        (14, 7), (15, 0), (15, 6), (15, 9)],
    ('Gxi',): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4),
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1),
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7),
        (15, 2), (15, 3)],
    ('Giy', 'Gyi'): [
        (0, 6), (0, 8), (0, 10), (1, 0), (1, 1), (1, 3), (2, 9),
        (3, 8), (4, 4), (4, 7), (5, 7), (6, 1), (7, 0), (7, 8),
        (9, 10), (10, 5), (11, 5), (12, 5), (12, 6), (14, 0),
        (15, 0), (15, 6), (15, 8)],
    ('Giy', 'Gxi'): [
        (1, 1), (2, 8), (3, 0), (3, 2), (3, 6), (4, 7), (7, 2),
        (8, 6), (9, 1), (9, 7), (9, 9), (10, 2), (10, 10), (11, 8),
        (12, 6), (13, 2), (13, 7), (14, 2), (15, 5)],
    ('Gyi', 'Gxx'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0),
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2),
        (14, 1)],
    ('Gii', 'Giy'): [
        (0, 0), (0, 7), (1, 1), (3, 5), (3, 6), (4, 2), (4, 4),
        (4, 5), (5, 3), (5, 7), (7, 1), (7, 8), (8, 5), (9, 4),
        (9, 5), (9, 9), (10, 5), (11, 5), (11, 6), (11, 8), (11, 10),
        (12, 0), (12, 3), (13, 10), (14, 0), (14, 5), (14, 6),
        (14, 7), (15, 0), (15, 6), (15, 9)],
    ('Gix', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5),
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6),
        (12, 9), (13, 9), (15, 1)],
    ('Gix', 'Gxi'): [
        (0, 0), (1, 5), (2, 4), (3, 3), (3, 5), (5, 2), (6, 1),
        (6, 8), (6, 10), (8, 6), (10, 2), (10, 8), (10, 10),
        (11, 8), (12, 1), (13, 1), (13, 4), (13, 6), (13, 10),
        (14, 8), (15, 3)],
    ('Gii', 'Gyi'): [
        (3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 7), (6, 0),
        (6, 8), (7, 2), (7, 4), (7, 9), (8, 0), (8, 7), (9, 2),
        (9, 3), (10, 9), (10, 10), (14, 7), (14, 9), (15, 10)],
    ('Gix', 'Gyi'): [
        (0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4),
        (6, 0), (6, 8), (9, 7), (10, 9), (11, 1), (11, 4), (14, 4),
        (14, 9), (15, 5), (15, 7)],
    ('Gii', 'Gix'): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3),
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10),
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8),
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8),
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3),
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8),
        (15, 9)],
    ('Gxi', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Giy', 'Gxx'): [
        (0, 6), (3, 0), (5, 0), (6, 7), (7, 1), (8, 3), (9, 9),
        (10, 4), (10, 9), (12, 9), (13, 2), (14, 5), (14, 8),
        (14, 10), (15, 6)],
    ('Gyi', 'Gii', 'Gii'): [
        (3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 7), (6, 0),
        (6, 8), (7, 2), (7, 4), (7, 9), (8, 0), (8, 7), (9, 2),
        (9, 3), (10, 9), (10, 10), (14, 7), (14, 9), (15, 10)],
    ('Gxi', 'Gxi', 'Gxx'): [
        (0, 6), (1, 3), (1, 7), (1, 10), (2, 10), (4, 1), (5, 1),
        (5, 5), (7, 3), (8, 2), (8, 3), (9, 8), (10, 1), (10, 6),
        (10, 10), (11, 7), (15, 3)],
    ('Gix', 'Giy', 'Gii'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5),
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6),
        (12, 9), (13, 9), (15, 1)],
    ('Giy', 'Gxx', 'Gxx'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Gyi', 'Gxi'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0),
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2),
        (14, 1)],
    ('Gix', 'Gxi', 'Giy'): [
        (0, 6), (3, 0), (5, 0), (6, 7), (7, 1), (8, 3), (9, 9),
        (10, 4), (10, 9), (12, 9), (13, 2), (14, 5), (14, 8),
        (14, 10), (15, 6)],
    ('Gxi', 'Gii', 'Gii'): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4),
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1),
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7),
        (15, 2), (15, 3)],
    ('Gii', 'Giy', 'Gyi'): [
        (0, 6), (0, 8), (0, 10), (1, 0), (1, 1), (1, 3), (2, 9),
        (3, 8), (4, 4), (4, 7), (5, 7), (6, 1), (7, 0), (7, 8),
        (9, 10), (10, 5), (11, 5), (12, 5), (12, 6), (14, 0),
        (15, 0), (15, 6), (15, 8)],
    ('Gix', 'Giy', 'Gyi'): [
        (0, 1), (4, 2), (4, 7), (6, 7), (8, 3), (9, 5), (9, 7),
        (10, 0), (10, 4), (10, 5), (11, 2), (11, 9), (14, 6),
        (14, 8), (15, 3)],
    ('Giy', 'Gii', 'Gii'): [
        (0, 0), (0, 7), (1, 1), (3, 5), (3, 6), (4, 2), (4, 4),
        (4, 5), (5, 3), (5, 7), (7, 1), (7, 8), (8, 5), (9, 4),
        (9, 5), (9, 9), (10, 5), (11, 5), (11, 6), (11, 8), (11, 10),
        (12, 0), (12, 3), (13, 10), (14, 0), (14, 5), (14, 6),
        (14, 7), (15, 0), (15, 6), (15, 9)],
    ('Gxi', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Gxx', 'Gxi'): [
        (1, 5), (3, 3), (4, 1), (6, 1), (6, 6), (6, 8), (8, 6),
        (10, 10), (11, 8), (13, 1), (13, 4), (13, 6), (13, 10),
        (14, 8), (15, 3)],
    ('Giy', 'Gxi', 'Gxi'): [
        (1, 7), (2, 2), (4, 8), (7, 2), (7, 10), (8, 6), (9, 8),
        (9, 9), (10, 1), (11, 4), (11, 9), (12, 8), (12, 9),
        (13, 0), (13, 1), (13, 9)],
    ('Gii', 'Gix', 'Gyi'): [
        (0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4),
        (6, 0), (6, 8), (9, 7), (10, 9), (11, 1), (11, 4), (14, 4),
        (14, 9), (15, 5), (15, 7)],
    ('Giy', 'Gxx', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Giy', 'Gxx'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Gyi', 'Giy'): [
        (3, 0), (4, 4), (5, 1), (5, 8), (6, 5), (7, 3), (8, 6),
        (8, 7), (9, 5), (10, 3), (11, 4), (14, 0), (14, 6), (14, 9),
        (15, 5)],
    ('Giy', 'Gyi', 'Gxx'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Gxi', 'Gii', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Gii', 'Gxx', 'Gxx'): [
        (1, 5), (3, 3), (4, 1), (6, 1), (6, 6), (6, 8), (8, 6),
        (10, 10), (11, 8), (13, 1), (13, 4), (13, 6), (13, 10),
        (14, 8), (15, 3)],
    ('Gix', 'Giy', 'Giy'): [
        (0, 4), (0, 5), (0, 7), (1, 1), (1, 6), (2, 3), (4, 10),
        (5, 4), (6, 8), (7, 4), (7, 10), (8, 8), (8, 9), (10, 5),
        (11, 5), (11, 6), (11, 9), (13, 10), (14, 1), (14, 9)],
    ('Gxi', 'Gyi', 'Gii'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Gix', 'Gix', 'Giy'): [
        (0, 0), (0, 6), (1, 0), (1, 10), (4, 0), (4, 4), (4, 7),
        (4, 8), (5, 5), (6, 7), (7, 6), (8, 9), (9, 9), (10, 2),
        (10, 8), (11, 10), (12, 6), (12, 9), (13, 1), (13, 9),
        (15, 1)],
    ('Gix', 'Gxx', 'Giy'): [
        (0, 3), (1, 0), (1, 4), (3, 10), (4, 3), (5, 7), (7, 2),
        (7, 4), (7, 7), (7, 8), (8, 1), (8, 5), (8, 7), (8, 9),
        (9, 2), (9, 6), (10, 3), (14, 10), (15, 4)],
    ('Giy', 'Gxi', 'Gyi'): [
        (0, 9), (1, 1), (1, 9), (2, 7), (3, 4), (4, 4), (4, 10),
        (6, 0), (6, 3), (7, 0), (9, 4), (11, 5), (12, 4), (13, 7),
        (14, 0)],
    ('Giy', 'Gyi', 'Gxi'): [
        (0, 9), (1, 1), (1, 9), (2, 7), (3, 4), (4, 4), (4, 10),
        (6, 0), (6, 3), (7, 0), (9, 4), (11, 5), (12, 4), (13, 7),
        (14, 0)],
    ('Gii', 'Gyi', 'Gix'): [
        (0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4),
        (6, 0), (6, 8), (9, 7), (10, 9), (11, 1), (11, 4), (14, 4),
        (14, 9), (15, 5), (15, 7)],
    ('Gix', 'Giy', 'Gxi'): [
        (0, 6), (3, 0), (5, 0), (6, 7), (7, 1), (8, 3), (9, 9),
        (10, 4), (10, 9), (12, 9), (13, 2), (14, 5), (14, 8),
        (14, 10), (15, 6)],
    ('Gix', 'Gix', 'Gxx'): [
        (0, 0), (1, 5), (2, 4), (3, 3), (3, 5), (5, 2), (6, 1),
        (6, 8), (6, 10), (8, 6), (10, 2), (10, 8), (10, 10),
        (11, 8), (12, 1), (13, 1), (13, 4), (13, 6), (13, 10),
        (14, 8), (15, 3)],
    ('Gxi', 'Gyi', 'Gxx'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Gxx', 'Gxx'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Gii', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5),
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6),
        (12, 9), (13, 9), (15, 1)],
    ('Gix', 'Gii', 'Gii'): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3),
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10),
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8),
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8),
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3),
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8),
        (15, 9)],
    ('Gxi', 'Gxi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Gix', 'Gxi', 'Giy'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Gix', 'Gii', 'Gii', 'Gxi'): [
        (0, 0), (1, 5), (2, 4), (3, 3), (3, 5), (5, 2), (6, 1),
        (6, 8), (6, 10), (8, 6), (10, 2), (10, 8), (10, 10),
        (11, 8), (12, 1), (13, 1), (13, 4), (13, 6), (13, 10),
        (14, 8), (15, 3)],
    ('Gix', 'Giy', 'Gxi', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Giy', 'Gxi', 'Gii', 'Gii'): [
        (1, 1), (2, 8), (3, 0), (3, 2), (3, 6), (4, 7), (7, 2),
        (8, 6), (9, 1), (9, 7), (9, 9), (10, 2), (10, 10), (11, 8),
        (12, 6), (13, 2), (13, 7), (14, 2), (15, 5)],
    ('Gxx', 'Gxx', 'Gyi', 'Gyi'): [
        (0, 1), (0, 3), (0, 9), (2, 3), (2, 6), (3, 10), (5, 7),
        (6, 0), (7, 2), (7, 6), (7, 7), (8, 1), (8, 5), (9, 4),
        (14, 10)],
    ('Gyi', 'Gix', 'Gix', 'Gix'): [
        (0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4),
        (6, 0), (6, 8), (9, 7), (10, 9), (11, 1), (11, 4), (14, 4),
        (14, 9), (15, 5), (15, 7)],
    ('Gyi', 'Gyi', 'Giy', 'Gyi'): [
        (0, 2), (1, 1), (1, 4), (2, 1), (2, 10), (3, 10), (4, 0),
        (5, 3), (5, 7), (6, 4), (6, 10), (8, 2), (8, 3), (9, 0),
        (10, 8), (11, 1), (11, 7), (13, 1), (13, 8)],
    ('Gix', 'Giy', 'Giy', 'Gii'): [
        (0, 4), (0, 5), (0, 7), (1, 1), (1, 6), (2, 3), (4, 10),
        (5, 4), (6, 8), (7, 4), (7, 10), (8, 8), (8, 9), (10, 5),
        (11, 5), (11, 6), (11, 9), (13, 10), (14, 1), (14, 9)],
    ('Gxi', 'Gyi', 'Gix', 'Gix'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0),
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2),
        (14, 1)],
    ('Gxi', 'Gyi', 'Gyi', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Giy', 'Gxx', 'Gxi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Gix', 'Gix', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5),
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6),
        (12, 9), (13, 9), (15, 1)],
    ('Gxi', 'Gyi', 'Gyi', 'Gii'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Giy', 'Giy', 'Gxi', 'Gyi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Gyi', 'Giy', 'Gxx', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Giy', 'Gyi', 'Gix', 'Gix'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Giy', 'Gyi', 'Gxi', 'Gxi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Giy', 'Gxi', 'Gix', 'Giy', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gxi', 'Gxi', 'Giy', 'Gyi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gxx', 'Gxx', 'Gxx', 'Gix', 'Gxi'): [
        (1, 5), (3, 3), (4, 1), (6, 1), (6, 6), (6, 8), (8, 6),
        (10, 10), (11, 8), (13, 1), (13, 4), (13, 6), (13, 10),
        (14, 8), (15, 3)],
    ('Giy', 'Gix', 'Gxi', 'Gix', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Giy', 'Giy', 'Gix', 'Gxi', 'Gxi'): [
        (1, 1), (2, 5), (4, 3), (5, 5), (6, 3), (7, 1), (10, 2),
        (10, 5), (11, 2), (11, 5), (12, 7), (12, 10), (13, 0),
        (13, 4), (14, 5)],
    ('Gyi', 'Giy', 'Gxi', 'Giy', 'Giy', 'Giy'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Gxi', 'Giy', 'Gix', 'Gyi', 'Gix', 'Gix'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Gxi', 'Gix', 'Giy', 'Gxi', 'Giy', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gxi', 'Gix', 'Giy', 'Giy', 'Gxi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gxx', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Gyi', 'Gxi', 'Gix', 'Giy', 'Gxi', 'Gix'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Gxi', 'Gix', 'Gxi', 'Gix', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Giy', 'Giy', 'Gxi', 'Giy', 'Gix', 'Giy'): [
        (0, 4), (0, 6), (1, 1), (2, 2), (4, 1), (4, 3), (5, 1),
        (5, 3), (6, 10), (8, 2), (8, 8), (9, 4), (10, 7), (12, 1),
        (13, 2), (15, 6), (15, 9)],
    ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Gyi', 'Gyi', 'Giy', 'Gyi', 'Gix'): [
        (0, 3), (1, 0), (1, 4), (3, 10), (4, 3), (5, 7), (7, 2),
        (7, 4), (7, 7), (7, 8), (8, 1), (8, 5), (8, 7), (8, 9),
        (9, 2), (9, 6), (10, 3), (14, 10), (15, 4)],
    ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5),
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6),
        (12, 9), (13, 9), (15, 1)],
    ('Gxx', 'Gxx', 'Gxx', 'Gxi', 'Gix', 'Gii', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gii', 'Gyi', 'Gxi', 'Gxx', 'Gxx', 'Gix', 'Gxx'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10),
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
    ('Giy', 'Gix', 'Gyi', 'Gyi', 'Gix', 'Gxi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gyi', 'Gxi', 'Giy', 'Gxi', 'Gix', 'Gxi', 'Gyi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
        (15, 0), (15, 5)],
    ('Gix', 'Gix', 'Gyi', 'Gxi', 'Giy', 'Gxi', 'Giy', 'Gyi'): [
        (1, 1), (2, 5), (4, 3), (5, 5), (6, 3), (7, 1), (10, 2),
        (10, 5), (11, 2), (11, 5), (12, 7), (12, 10), (13, 0),
        (13, 4), (14, 5)],
}
