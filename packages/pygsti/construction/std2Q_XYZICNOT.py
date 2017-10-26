from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
"""
Variables for working with the 2-qubit gate set containing the gates
I*X(pi/2), I*Y(pi/2), I*Z(pi/2), X(pi/2)*I, Y(pi/2)*I, Z(pi/2)*I and CNOT.
"""

import numpy as _np
from . import gatestringconstruction as _strc
from . import gatesetconstruction as _setc
from . import spamspecconstruction as _spamc
from ..tools import gatetools as _gt

description = "I*X(pi/2), I*Y(pi/2), I*Z(pi/2), X(pi/2)*I, Y(pi/2)*I, Z(pi/2)*I and CNOT gates"

gates = ['Gix','Giy','Giz','Gxi','Gyi','Gzi','Gcnot']

fiducials16 = _strc.gatestring_list(
    [ (), ('Gix',), ('Giy',), ('Gix','Gix'),
      ('Gxi',), ('Gxi','Gix'), ('Gxi','Giy'), ('Gxi','Gix','Gix'),
      ('Gyi',), ('Gyi','Gix'), ('Gyi','Giy'), ('Gyi','Gix','Gix'),
      ('Gxi','Gxi'), ('Gxi','Gxi','Gix'), ('Gxi','Gxi','Giy'), ('Gxi','Gxi','Gix','Gix') ] )

fiducials36 = _strc.gatestring_list(
    [ (), ('Gix',), ('Giy',), ('Gix','Gix'), ('Gix','Gix','Gix'), ('Giy','Giy','Giy'),
      ('Gxi',), ('Gxi','Gix'), ('Gxi','Giy'), ('Gxi','Gix','Gix'), ('Gxi','Gix','Gix','Gix'), ('Gxi','Giy','Giy','Giy'),
      ('Gyi',), ('Gyi','Gix'), ('Gyi','Giy'), ('Gyi','Gix','Gix'), ('Gyi','Gix','Gix','Gix'), ('Gyi','Giy','Giy','Giy'),
      ('Gxi','Gxi'), ('Gxi','Gxi','Gix'), ('Gxi','Gxi','Giy'), ('Gxi','Gxi','Gix','Gix'), ('Gxi','Gxi','Gix','Gix','Gix'),
      ('Gxi','Gxi','Giy','Giy','Giy'), ('Gxi','Gxi','Gxi'), ('Gxi','Gxi','Gxi','Gix'), ('Gxi','Gxi','Gxi','Giy'),
      ('Gxi','Gxi','Gxi','Gix','Gix'), ('Gxi','Gxi','Gxi','Gix','Gix','Gix'), ('Gxi','Gxi','Gxi','Giy','Giy','Giy'),
      ('Gyi','Gyi','Gyi'), ('Gyi','Gyi','Gyi','Gix'), ('Gyi','Gyi','Gyi','Giy'), ('Gyi','Gyi','Gyi','Gix','Gix'),
      ('Gyi','Gyi','Gyi','Gix','Gix','Gix'), ('Gyi','Gyi','Gyi','Giy','Giy','Giy') ] )

fiducials = fiducials16
prepStrs = fiducials16

effectStrs = _strc.gatestring_list(
    [(), ('Gix',), ('Giy',), 
     ('Gix','Gix'), ('Gxi',), 
     ('Gyi',), ('Gxi','Gxi'), 
     ('Gxi','Gix'), ('Gxi','Giy'), 
     ('Gyi','Gix'), ('Gyi','Giy')] )

germs = _strc.gatestring_list( [
        ('Gii',),
        ('Gxi',),
        ('Gyi',),
        ('Gzi',),
        ('Gix',),
        ('Giy',),
        ('Giz',),
        ('Gxi', 'Gyi'),
        ('Gix', 'Giy'),
        ('Gyi', 'Gcnot'),
        ('Gix', 'Gyi'),
        ('Giy', 'Gxi'),
        ('Gix', 'Gxi'),
        ('Gii', 'Gcnot'),
        ('Giz', 'Gyi'),
        ('Gxi', 'Gxi', 'Gyi'),
        ('Gxi', 'Gxi', 'Gzi'),
        ('Gxi', 'Gyi', 'Gyi'),
        ('Gxi', 'Gyi', 'Gzi'),
        ('Gxi', 'Gzi', 'Gzi'),
        ('Gyi', 'Gyi', 'Gzi'),
        ('Gyi', 'Gzi', 'Gzi'),
        ('Gix', 'Gix', 'Giy'),
        ('Gix', 'Gix', 'Giz'),
        ('Gix', 'Giy', 'Giy'),
        ('Gix', 'Giy', 'Giz'),
        ('Gix', 'Giz', 'Giz'),
        ('Giy', 'Giy', 'Giz'),
        ('Giy', 'Giz', 'Giz'),
        ('Gxi', 'Gyi', 'Gii'),
        ('Gxi', 'Gii', 'Gyi'),
        ('Gxi', 'Gii', 'Gii'),
        ('Gyi', 'Gii', 'Gii'),
        ('Gix', 'Giy', 'Gii'),
        ('Gix', 'Gii', 'Giy'),
        ('Gix', 'Gii', 'Gii'),
        ('Giy', 'Gii', 'Gii'),
        ('Giy', 'Gxi', 'Gcnot'),
        ('Giy', 'Gcnot', 'Gxi'),
        ('Gix', 'Gix', 'Gcnot'),
        ('Giy', 'Gcnot', 'Gyi'),
        ('Gix', 'Gyi', 'Gxi'),
        ('Giy', 'Gyi', 'Gcnot'),
        ('Gxi', 'Gcnot', 'Gcnot'),
        ('Gix', 'Giy', 'Gcnot'),
        ('Gii', 'Gcnot', 'Gcnot'),
        ('Gii', 'Gxi', 'Giy'),
        ('Giy', 'Gyi', 'Gxi'),
        ('Gii', 'Gyi', 'Gix'),
        ('Gii', 'Gzi', 'Giy'),
        ('Giz', 'Gcnot', 'Gxi'),
        ('Gzi', 'Gzi', 'Gcnot'),
        ('Gxi', 'Gzi', 'Gcnot'),
        ('Giz', 'Gcnot', 'Gyi'),
        ('Gii', 'Gzi', 'Giz'),
        ('Gix', 'Gcnot', 'Gzi'),
        ('Giz', 'Gxi', 'Gcnot'),
        ('Gyi', 'Gcnot', 'Gzi'),
        ('Gxi', 'Gxi', 'Gii', 'Gyi'),
        ('Gxi', 'Gyi', 'Gyi', 'Gii'),
        ('Gix', 'Gix', 'Gii', 'Giy'),
        ('Gix', 'Giy', 'Giy', 'Gii'),
        ('Gcnot', 'Gcnot', 'Giy', 'Gcnot'),
        ('Giy', 'Gix', 'Gyi', 'Giy'),
        ('Gii', 'Gxi', 'Gxi', 'Gcnot'),
        ('Gxi', 'Gyi', 'Gcnot', 'Gcnot'),
        ('Giy', 'Gcnot', 'Gxi', 'Giy'),
        ('Giz', 'Gzi', 'Gxi', 'Giz'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gzi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Giz'),
        ('Gxi', 'Gii', 'Gcnot', 'Giy', 'Gix'),
        ('Gyi', 'Gyi', 'Giy', 'Gcnot', 'Giy'),
        ('Gyi', 'Gcnot', 'Giy', 'Gix', 'Giy'),
        ('Giy', 'Gxi', 'Gcnot', 'Gxi', 'Gxi'),
        ('Giy', 'Gyi', 'Gii', 'Giy', 'Gyi'),
        ('Gix', 'Gcnot', 'Gxi', 'Gxi', 'Giy'),
        ('Gyi', 'Gcnot', 'Gix', 'Gyi', 'Gxi'),
        ('Gyi', 'Gix', 'Gix', 'Giy', 'Giy'),
        ('Giz', 'Giz', 'Gyi', 'Gzi', 'Gyi'),
        ('Gyi', 'Gyi', 'Giz', 'Gcnot', 'Giz'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gxi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gxi', 'Gzi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gyi', 'Gzi'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gix'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Gix', 'Giz'),
        ('Gii', 'Gii', 'Gii', 'Gii', 'Giy', 'Giz'),
        ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
        ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
        ('Gii', 'Gyi', 'Giy', 'Gyi', 'Gcnot', 'Gxi'),
        ('Gxi', 'Giy', 'Giy', 'Gyi', 'Giy', 'Gcnot'),
        ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gcnot', 'Gyi'),
        ('Gix', 'Gyi', 'Giy', 'Giy', 'Gxi', 'Gxi'),
        ('Gcnot', 'Gii', 'Gxi', 'Gyi', 'Gyi', 'Giy'),
        ('Gcnot', 'Gii', 'Gxi', 'Gcnot', 'Gix', 'Gxi'),
        ('Gyi', 'Gix', 'Gxi', 'Gix', 'Giy', 'Giy'),
        ('Gix', 'Giy', 'Giy', 'Giy', 'Giy', 'Gcnot'),
        ('Gyi', 'Gcnot', 'Gii', 'Gcnot', 'Gix', 'Giy'),
        ('Gii', 'Gzi', 'Giz', 'Gyi', 'Gcnot', 'Gxi'),
        ('Gzi', 'Gxi', 'Giz', 'Gzi', 'Gcnot', 'Gyi'),
        ('Gcnot', 'Gcnot', 'Gcnot', 'Gxi', 'Gix', 'Gii', 'Giy'),
        ('Gii', 'Gyi', 'Gxi', 'Gcnot', 'Gcnot', 'Gix', 'Gcnot'),
        ('Giy', 'Gxi', 'Gyi', 'Gxi', 'Gcnot', 'Gyi', 'Gix'),
        ('Gxi', 'Gyi', 'Gyi', 'Gcnot', 'Gix', 'Gix', 'Giy'),
        ('Gxi', 'Giy', 'Gix', 'Gcnot', 'Giy', 'Gix', 'Gii'),
        ('Gix', 'Giy', 'Gix', 'Gyi', 'Gxi', 'Gii', 'Gxi'),
        ('Gii', 'Gii', 'Gxi', 'Gcnot', 'Gii', 'Giy', 'Gcnot'),
        ('Giy', 'Gix', 'Gxi', 'Gix', 'Gii', 'Gxi', 'Gii'),
        ('Giy', 'Giy', 'Gix', 'Gii', 'Gix', 'Gxi', 'Gxi'),
        ('Giy', 'Gxi', 'Giy', 'Gxi', 'Gxi', 'Gyi', 'Gyi'),
        ('Gzi', 'Gii', 'Giz', 'Gzi', 'Gcnot', 'Gxi', 'Gii'),
        ('Gzi', 'Gcnot', 'Gzi', 'Gxi', 'Gix', 'Gii', 'Giz'),
        ('Gxi', 'Giy', 'Gix', 'Gcnot', 'Gii', 'Gyi', 'Gyi', 'Giy'),
        ('Gcnot', 'Gix', 'Gix', 'Gcnot', 'Gcnot', 'Gyi', 'Giy', 'Giy'),
        ('Gxi', 'Gix', 'Gcnot', 'Gix', 'Gxi', 'Giy', 'Gyi', 'Giy'),
        ('Giy', 'Gcnot', 'Gxi', 'Gcnot', 'Gix', 'Gxi', 'Gxi', 'Gyi'),
        ('Gxi', 'Gcnot', 'Gix', 'Giy', 'Gyi', 'Gyi', 'Gyi', 'Gcnot'),
        ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcnot', 'Gix', 'Gyi', 'Gyi'),
        ('Gix', 'Gix', 'Gix', 'Gyi', 'Giy', 'Gxi', 'Giy', 'Giy'),
        ('Gcnot', 'Gyi', 'Gxi', 'Gyi', 'Giy', 'Gyi', 'Gyi', 'Giy'),
        ('Gii', 'Gzi', 'Gzi', 'Giz', 'Gii', 'Gzi', 'Gyi', 'Gcnot'),
        ('Gxi', 'Giz', 'Giz', 'Giz', 'Gzi', 'Gix', 'Gyi', 'Gyi'),
        ('Gcnot', 'Gyi', 'Gxi', 'Gyi', 'Giz', 'Gyi', 'Gzi', 'Giz') 
        ])

#Construct the target gateset
gs_target = _setc.build_gateset(
    [4], [('Q0','Q1')],['Gii', 'Gix','Giy','Giz','Gxi','Gyi','Gzi','Gcnot'],
    [  "I(Q0):I(Q1)", "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "I(Q0):Z(pi/2,Q1)",
       "X(pi/2,Q0):I(Q1)", "Y(pi/2,Q0):I(Q1)", "Z(pi/2,Q0):I(Q1)", "CNOT(Q0,Q1)"],
    prepLabels=['rho0'], prepExpressions=["0"],
    effectLabels=['E0','E1','E2'], effectExpressions=["0","1","2"],
    spamdefs={'00': ('rho0','E0'), '01': ('rho0','E1'),
              '10': ('rho0','E2'), '11': ('rho0','remainder') }, basis="pp")


specs16x10 = _spamc.build_spam_specs(
    prepStrs=prepStrs,
    effectStrs=effectStrs,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs16 = _spamc.build_spam_specs(
    fiducials16,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs36 = _spamc.build_spam_specs(
    fiducials36,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs = specs16x10 #use smallest specs set as "default"


global_fidPairs =  [
    (1, 1), (2, 7), (3, 3), (4, 5), (4, 10), (5, 10), (6, 3), 
    (6, 4), (6, 9), (7, 3), (7, 7), (8, 3), (9, 6), (10, 10), 
    (12, 4), (14, 9)]

pergerm_fidPairsDict = {
  ('Gzi',): [
        (0, 2), (0, 5), (0, 6), (0, 8), (1, 1), (1, 5), (1, 6), 
        (1, 7), (2, 6), (3, 1), (3, 3), (3, 5), (3, 6), (3, 8), 
        (3, 10), (4, 1), (4, 2), (4, 4), (4, 5), (4, 9), (5, 0), 
        (5, 7), (6, 7), (6, 8), (6, 9), (8, 0), (8, 5), (8, 6), 
        (9, 4), (9, 6), (9, 7), (10, 3), (10, 7), (10, 8), (11, 0), 
        (11, 10), (12, 0), (12, 8), (13, 6), (13, 9), (14, 0), 
        (14, 2), (14, 4), (14, 7), (15, 0), (15, 1)],
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
  ('Giz',): [
        (0, 7), (2, 2), (3, 2), (3, 4), (3, 7), (3, 10), (4, 1), 
        (4, 3), (4, 4), (4, 8), (5, 7), (6, 4), (6, 6), (6, 7), 
        (6, 9), (7, 0), (8, 0), (8, 7), (9, 2), (9, 3), (10, 5), 
        (10, 6), (10, 9), (10, 10), (11, 5), (11, 8), (12, 2), 
        (12, 4), (12, 6), (12, 8), (13, 2), (13, 3), (14, 2), 
        (14, 5), (14, 7), (14, 9), (15, 8)],
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
  ('Giy', 'Gxi'): [
        (1, 1), (2, 8), (3, 0), (3, 2), (3, 6), (4, 7), (7, 2), 
        (8, 6), (9, 1), (9, 7), (9, 9), (10, 2), (10, 10), (11, 8), 
        (12, 6), (13, 2), (13, 7), (14, 2), (15, 5)],
  ('Gix', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Gii', 'Gcnot'): [
        (0, 7), (1, 0), (2, 4), (4, 3), (5, 5), (5, 10), (6, 1), 
        (6, 10), (7, 8), (8, 2), (8, 5), (8, 6), (9, 0), (9, 4), 
        (9, 6), (9, 9), (10, 2), (10, 4), (10, 5), (11, 5), (12, 2), 
        (13, 7), (14, 1), (14, 2), (14, 3), (14, 6), (15, 8), 
        (15, 10)],
  ('Gix', 'Gxi'): [
        (0, 0), (1, 5), (2, 4), (3, 3), (3, 5), (5, 2), (6, 1), 
        (6, 8), (6, 10), (8, 6), (10, 2), (10, 8), (10, 10), 
        (11, 8), (12, 1), (13, 1), (13, 4), (13, 6), (13, 10), 
        (14, 8), (15, 3)],
  ('Gix', 'Gyi'): [
        (0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4), 
        (6, 0), (6, 8), (9, 7), (10, 9), (11, 1), (11, 4), (14, 4), 
        (14, 9), (15, 5), (15, 7)],
  ('Gyi', 'Gcnot'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gxi', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Giz', 'Gyi'): [
        (0, 6), (1, 6), (2, 3), (2, 9), (2, 10), (4, 7), (4, 9), 
        (5, 2), (5, 5), (5, 7), (7, 4), (9, 2), (10, 2), (12, 5), 
        (12, 6), (12, 10), (13, 1), (14, 9)],
  ('Gii', 'Gzi', 'Giz'): [
        (0, 0), (0, 4), (0, 9), (1, 1), (1, 6), (2, 0), (2, 1), 
        (2, 7), (3, 7), (4, 2), (4, 10), (5, 4), (5, 7), (5, 9), 
        (5, 10), (6, 8), (7, 2), (7, 4), (7, 5), (8, 0), (8, 6), 
        (9, 8), (9, 10), (10, 2), (10, 3), (10, 4), (10, 5), 
        (10, 9), (11, 10), (12, 1), (12, 8), (13, 9), (14, 7), 
        (14, 10), (15, 0), (15, 3), (15, 8)],
  ('Gyi', 'Gyi', 'Gzi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gyi', 'Gii', 'Gii'): [
        (3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 7), (6, 0), 
        (6, 8), (7, 2), (7, 4), (7, 9), (8, 0), (8, 7), (9, 2), 
        (9, 3), (10, 9), (10, 10), (14, 7), (14, 9), (15, 10)],
  ('Gix', 'Gix', 'Giz'): [
        (0, 0), (0, 6), (1, 5), (2, 7), (4, 4), (6, 4), (7, 4), 
        (7, 10), (9, 2), (9, 5), (10, 10), (11, 2), (12, 0), 
        (13, 10), (14, 0)],
  ('Giy', 'Gcnot', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Giy', 'Gii'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Gxi', 'Gyi', 'Gzi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Gcnot', 'Gzi'): [
        (0, 1), (0, 5), (1, 5), (2, 5), (2, 7), (4, 4), (5, 0), 
        (6, 0), (6, 10), (7, 0), (7, 5), (8, 5), (10, 10), (11, 9), 
        (12, 7), (12, 9), (14, 2), (15, 5)],
  ('Gix', 'Gyi', 'Gxi'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0), 
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2), 
        (14, 1)],
  ('Gyi', 'Gzi', 'Gzi'): [
        (3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 4), (5, 7), 
        (6, 0), (6, 8), (7, 4), (7, 9), (8, 0), (8, 7), (8, 8), 
        (9, 2), (10, 9), (14, 7), (15, 10)],
  ('Gii', 'Gxi', 'Giy'): [
        (1, 1), (2, 8), (3, 0), (3, 2), (3, 6), (4, 7), (7, 2), 
        (8, 6), (9, 1), (9, 7), (9, 9), (10, 2), (10, 10), (11, 8), 
        (12, 6), (13, 2), (13, 7), (14, 2), (15, 5)],
  ('Gxi', 'Gii', 'Gii'): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), 
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1), 
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), 
        (15, 2), (15, 3)],
  ('Gii', 'Gcnot', 'Gcnot'): [
        (0, 8), (1, 0), (1, 1), (1, 3), (1, 10), (2, 5), (2, 9), 
        (3, 3), (3, 9), (4, 3), (4, 8), (5, 0), (5, 5), (5, 7), 
        (6, 4), (6, 6), (6, 8), (6, 10), (7, 0), (7, 2), (7, 3), 
        (7, 4), (7, 6), (7, 10), (8, 3), (8, 5), (9, 3), (9, 4), 
        (9, 5), (9, 6), (9, 8), (9, 9), (10, 3), (10, 9), (10, 10), 
        (11, 1), (11, 5), (12, 5), (12, 7), (12, 9), (13, 0), 
        (13, 10), (14, 0), (14, 1), (14, 2), (14, 6), (15, 0), 
        (15, 5), (15, 6), (15, 7), (15, 8)],
  ('Gxi', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gzi', 'Gzi', 'Gcnot'): [
        (0, 7), (1, 0), (2, 4), (4, 3), (5, 5), (5, 10), (6, 1), 
        (6, 10), (7, 8), (8, 2), (8, 5), (8, 6), (9, 0), (9, 4), 
        (9, 6), (9, 9), (10, 2), (10, 4), (10, 5), (11, 5), (12, 2), 
        (13, 7), (14, 1), (14, 2), (14, 3), (14, 6), (15, 8), 
        (15, 10)],
  ('Gix', 'Giy', 'Giz'): [
        (0, 6), (0, 8), (0, 10), (1, 0), (1, 1), (1, 3), (2, 9), 
        (3, 8), (4, 4), (4, 7), (5, 7), (6, 1), (7, 0), (7, 8), 
        (9, 10), (10, 5), (11, 5), (12, 5), (12, 6), (14, 0), 
        (15, 0), (15, 6), (15, 8)],
  ('Gxi', 'Gii', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Gix', 'Gcnot'): [
        (0, 6), (0, 7), (2, 2), (2, 3), (2, 5), (2, 9), (4, 4), 
        (4, 9), (6, 1), (8, 10), (12, 3), (12, 9), (13, 3), (14, 10), 
        (15, 3)],
  ('Gii', 'Gzi', 'Giy'): [
        (0, 7), (1, 1), (2, 6), (3, 2), (5, 9), (6, 3), (6, 4), 
        (6, 5), (7, 3), (8, 1), (8, 6), (8, 10), (9, 0), (9, 5), 
        (9, 6), (9, 9), (10, 4), (10, 7), (10, 8), (10, 9), (11, 0), 
        (12, 0), (12, 9), (14, 5), (14, 10), (15, 3)],
  ('Gix', 'Giz', 'Giz'): [
        (0, 9), (2, 2), (2, 5), (3, 4), (3, 6), (4, 3), (4, 5), 
        (4, 9), (5, 4), (5, 5), (5, 10), (6, 8), (8, 3), (8, 6), 
        (9, 9), (10, 8), (10, 10), (11, 8), (12, 0), (12, 4), 
        (12, 6), (13, 0), (13, 7), (14, 7), (15, 8)],
  ('Gix', 'Gii', 'Gii'): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3), 
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10), 
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8), 
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8), 
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3), 
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8), 
        (15, 9)],
  ('Gxi', 'Gyi', 'Gii'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Giy', 'Gyi', 'Gxi'): [
        (0, 9), (1, 1), (1, 9), (2, 7), (3, 4), (4, 4), (4, 10), 
        (6, 0), (6, 3), (7, 0), (9, 4), (11, 5), (12, 4), (13, 7), 
        (14, 0)],
  ('Giy', 'Gii', 'Gii'): [
        (0, 0), (0, 7), (1, 1), (3, 5), (3, 6), (4, 2), (4, 4), 
        (4, 5), (5, 3), (5, 7), (7, 1), (7, 8), (8, 5), (9, 4), 
        (9, 5), (9, 9), (10, 5), (11, 5), (11, 6), (11, 8), (11, 10), 
        (12, 0), (12, 3), (13, 10), (14, 0), (14, 5), (14, 6), 
        (14, 7), (15, 0), (15, 6), (15, 9)],
  ('Gix', 'Gix', 'Giy'): [
        (0, 0), (0, 6), (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), 
        (4, 8), (5, 5), (6, 7), (7, 6), (8, 9), (9, 9), (10, 2), 
        (10, 8), (11, 10), (12, 6), (12, 9), (13, 1), (13, 9), 
        (15, 1)],
  ('Gxi', 'Gzi', 'Gcnot'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giz', 'Gcnot', 'Gxi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (7, 8), (9, 3), (9, 9), (9, 10), 
        (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 4), 
        (15, 5)],
  ('Gii', 'Gyi', 'Gix'): [
        (0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4), 
        (6, 0), (6, 8), (9, 7), (10, 9), (11, 1), (11, 4), (14, 4), 
        (14, 9), (15, 5), (15, 7)],
  ('Gxi', 'Gzi', 'Gzi'): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), 
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1), 
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), 
        (15, 2), (15, 3)],
  ('Giy', 'Giz', 'Giz'): [
        (0, 5), (0, 9), (1, 1), (1, 7), (2, 3), (3, 5), (3, 9), 
        (4, 4), (4, 7), (4, 8), (5, 7), (6, 2), (6, 5), (7, 7), 
        (7, 9), (7, 10), (8, 0), (9, 9), (10, 3), (10, 7), (11, 3), 
        (12, 9), (13, 3), (13, 4), (14, 6), (14, 10)],
  ('Giy', 'Gcnot', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (7, 8), (9, 3), (9, 9), (9, 10), 
        (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 4), 
        (15, 5)],
  ('Giz', 'Gxi', 'Gcnot'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Giy', 'Gcnot'): [
        (0, 3), (1, 0), (1, 4), (3, 10), (4, 3), (5, 7), (7, 2), 
        (7, 4), (7, 7), (7, 8), (8, 1), (8, 5), (8, 7), (8, 9), 
        (9, 2), (9, 6), (10, 3), (14, 10), (15, 4)],
  ('Gyi', 'Gcnot', 'Gzi'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (2, 4), (2, 10), (4, 3), 
        (7, 4), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), (10, 3), 
        (15, 4)],
  ('Giy', 'Gyi', 'Gcnot'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (7, 8), (9, 3), (9, 9), (9, 10), 
        (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 4), 
        (15, 5)],
  ('Giz', 'Gcnot', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Giy', 'Giy', 'Giz'): [
        (0, 1), (0, 5), (3, 7), (3, 9), (4, 2), (4, 7), (6, 7), 
        (7, 3), (8, 3), (9, 2), (9, 10), (11, 9), (12, 0), (14, 1), 
        (14, 3), (15, 1)],
  ('Gxi', 'Gcnot', 'Gcnot'): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), 
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1), 
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), 
        (15, 2), (15, 3)],
  ('Gix', 'Gii', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Gix', 'Giy', 'Giy'): [
        (0, 4), (0, 5), (0, 7), (1, 1), (1, 6), (2, 3), (4, 10), 
        (5, 4), (6, 8), (7, 4), (7, 10), (8, 8), (8, 9), (10, 5), 
        (11, 5), (11, 6), (11, 9), (13, 10), (14, 1), (14, 9)],
  ('Giy', 'Gxi', 'Gcnot'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Gxi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Gxi', 'Gzi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giz', 'Gzi', 'Gxi', 'Giz'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0), 
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2), 
        (14, 1)],
  ('Gii', 'Gxi', 'Gxi', 'Gcnot'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Gyi', 'Gcnot', 'Gcnot'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Giy', 'Gcnot', 'Gxi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gix', 'Gyi', 'Giy'): [
        (2, 0), (2, 1), (3, 0), (3, 9), (5, 4), (5, 7), (7, 6), 
        (7, 8), (8, 8), (11, 1), (11, 4), (12, 3), (12, 6), (14, 9), 
        (15, 3)],
  ('Gix', 'Giy', 'Giy', 'Gii'): [
        (0, 4), (0, 5), (0, 7), (1, 1), (1, 6), (2, 3), (4, 10), 
        (5, 4), (6, 8), (7, 4), (7, 10), (8, 8), (8, 9), (10, 5), 
        (11, 5), (11, 6), (11, 9), (13, 10), (14, 1), (14, 9)],
  ('Gcnot', 'Gcnot', 'Giy', 'Gcnot'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gix', 'Gix', 'Gii', 'Giy'): [
        (0, 0), (0, 6), (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), 
        (4, 8), (5, 5), (6, 7), (7, 6), (8, 9), (9, 9), (10, 2), 
        (10, 8), (11, 10), (12, 6), (12, 9), (13, 1), (13, 9), 
        (15, 1)],
  ('Gxi', 'Gyi', 'Gyi', 'Gii'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Gxi', 'Gii', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giz', 'Giz', 'Gyi', 'Gzi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Gzi'): [
        (0, 2), (0, 5), (0, 6), (0, 8), (1, 1), (1, 5), (1, 6), 
        (1, 7), (2, 6), (3, 1), (3, 3), (3, 5), (3, 6), (3, 8), 
        (3, 10), (4, 1), (4, 2), (4, 4), (4, 5), (4, 9), (5, 0), 
        (5, 7), (6, 7), (6, 8), (6, 9), (8, 0), (8, 5), (8, 6), 
        (9, 4), (9, 6), (9, 7), (10, 3), (10, 7), (10, 8), (11, 0), 
        (11, 10), (12, 0), (12, 8), (13, 6), (13, 9), (14, 0), 
        (14, 2), (14, 4), (14, 7), (15, 0), (15, 1)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Giz'): [
        (0, 7), (2, 2), (3, 2), (3, 4), (3, 7), (3, 10), (4, 1), 
        (4, 3), (4, 4), (4, 8), (5, 7), (6, 4), (6, 6), (6, 7), 
        (6, 9), (7, 0), (8, 0), (8, 7), (9, 2), (9, 3), (10, 5), 
        (10, 6), (10, 9), (10, 10), (11, 5), (11, 8), (12, 2), 
        (12, 4), (12, 6), (12, 8), (13, 2), (13, 3), (14, 2), 
        (14, 5), (14, 7), (14, 9), (15, 8)],
  ('Giy', 'Gxi', 'Gcnot', 'Gxi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gyi', 'Gcnot', 'Giy', 'Gix', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Gii', 'Gcnot', 'Giy', 'Gix'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gyi', 'Gii', 'Giy', 'Gyi'): [
        (0, 10), (1, 9), (4, 8), (5, 1), (5, 7), (6, 1), (6, 8), 
        (7, 8), (9, 4), (9, 5), (9, 10), (10, 1), (10, 2), (10, 4), 
        (13, 5)],
  ('Gyi', 'Gyi', 'Giy', 'Gcnot', 'Giy'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gyi', 'Gix', 'Gix', 'Giy', 'Giy'): [
        (0, 8), (1, 3), (1, 9), (2, 3), (2, 5), (5, 3), (5, 7), 
        (6, 0), (6, 5), (6, 7), (7, 7), (8, 6), (8, 8), (9, 2), 
        (9, 8), (12, 0), (15, 6)],
  ('Gix', 'Gcnot', 'Gxi', 'Gxi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gyi', 'Gyi', 'Giz', 'Gcnot', 'Giz'): [
        (0, 3), (1, 0), (1, 4), (3, 10), (4, 3), (5, 7), (7, 2), 
        (7, 4), (7, 7), (7, 8), (8, 1), (8, 5), (8, 7), (8, 9), 
        (9, 2), (9, 6), (10, 3), (14, 10), (15, 4)],
  ('Gyi', 'Gcnot', 'Gix', 'Gyi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcnot', 'Gii', 'Gxi', 'Gcnot', 'Gix', 'Gxi'): [
        (1, 5), (3, 3), (4, 1), (6, 1), (6, 6), (6, 8), (8, 6), 
        (10, 10), (11, 8), (13, 1), (13, 4), (13, 6), (13, 10), 
        (14, 8), (15, 3)],
  ('Gxi', 'Giy', 'Giy', 'Gyi', 'Giy', 'Gcnot'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Gxi', 'Gzi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcnot', 'Gii', 'Gxi', 'Gyi', 'Gyi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gzi', 'Gxi', 'Giz', 'Gzi', 'Gcnot', 'Gyi'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gii', 'Gyi', 'Giy', 'Gyi', 'Gcnot', 'Gxi'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gix'): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3), 
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10), 
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8), 
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8), 
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3), 
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8), 
        (15, 9)],
  ('Gyi', 'Gix', 'Gxi', 'Gix', 'Giy', 'Giy'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0), 
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2), 
        (14, 1)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Gix', 'Giz'): [
        (0, 1), (0, 3), (3, 0), (3, 6), (5, 5), (5, 8), (6, 8), 
        (7, 0), (8, 3), (8, 9), (9, 9), (10, 9), (10, 10), (11, 6), 
        (15, 0)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Gii', 'Gxi'): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), 
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1), 
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), 
        (15, 2), (15, 3)],
  ('Gyi', 'Gcnot', 'Gii', 'Gcnot', 'Gix', 'Giy'): [
        (3, 0), (4, 4), (5, 1), (5, 8), (6, 5), (7, 3), (8, 6), 
        (8, 7), (9, 5), (10, 3), (11, 4), (14, 0), (14, 6), (14, 9), 
        (15, 5)],
  ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gcnot', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Giy', 'Giy', 'Giy', 'Giy', 'Gcnot'): [
        (2, 2), (3, 1), (4, 5), (4, 7), (4, 8), (5, 3), (5, 4), 
        (8, 5), (9, 4), (9, 6), (10, 10), (12, 0), (13, 0), (14, 5), 
        (15, 1), (15, 7), (15, 10)],
  ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Gyi', 'Giy', 'Giy', 'Gxi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Gyi', 'Gzi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Gii', 'Gii', 'Gii', 'Gii', 'Giy', 'Giz'): [
        (0, 2), (0, 6), (3, 4), (4, 7), (5, 5), (6, 7), (7, 6), 
        (8, 5), (10, 2), (10, 8), (11, 6), (11, 10), (12, 6), 
        (14, 1), (14, 4)],
  ('Gii', 'Gzi', 'Giz', 'Gyi', 'Gcnot', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Giy', 'Gix', 'Gyi', 'Gxi', 'Gii', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gix', 'Gxi', 'Gix', 'Gii', 'Gxi', 'Gii'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Giy', 'Gix', 'Gii', 'Gix', 'Gxi', 'Gxi'): [
        (0, 4), (0, 6), (1, 1), (2, 2), (3, 5), (4, 9), (6, 10), 
        (8, 0), (8, 2), (10, 7), (11, 1), (12, 1), (14, 6), (15, 6), 
        (15, 9)],
  ('Giy', 'Gxi', 'Giy', 'Gxi', 'Gxi', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gii', 'Gyi', 'Gxi', 'Gcnot', 'Gcnot', 'Gix', 'Gcnot'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gcnot', 'Gcnot', 'Gcnot', 'Gxi', 'Gix', 'Gii', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gii', 'Gii', 'Gxi', 'Gcnot', 'Gii', 'Giy', 'Gcnot'): [
        (0, 3), (1, 0), (1, 4), (3, 10), (4, 3), (5, 7), (7, 2), 
        (7, 4), (7, 7), (7, 8), (8, 1), (8, 5), (8, 7), (8, 9), 
        (9, 2), (9, 6), (10, 3), (14, 10), (15, 4)],
  ('Gzi', 'Gcnot', 'Gzi', 'Gxi', 'Gix', 'Gii', 'Giz'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Giy', 'Gix', 'Gcnot', 'Giy', 'Gix', 'Gii'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Gyi', 'Gyi', 'Gcnot', 'Gix', 'Gix', 'Giy'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (7, 8), (9, 3), (9, 9), (9, 10), 
        (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 4), 
        (15, 5)],
  ('Gzi', 'Gii', 'Giz', 'Gzi', 'Gcnot', 'Gxi', 'Gii'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Giy', 'Gxi', 'Gyi', 'Gxi', 'Gcnot', 'Gyi', 'Gix'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcnot', 'Gix', 'Gix', 'Gcnot', 'Gcnot', 'Gyi', 'Giy', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gcnot', 'Gxi', 'Gcnot', 'Gix', 'Gxi', 'Gxi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Giz', 'Giz', 'Giz', 'Gzi', 'Gix', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Gix', 'Gix', 'Gyi', 'Giy', 'Gxi', 'Giy', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gii', 'Gzi', 'Gzi', 'Giz', 'Gii', 'Gzi', 'Gyi', 'Gcnot'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcnot', 'Gix', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Gix', 'Gcnot', 'Gix', 'Gxi', 'Giy', 'Gyi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcnot', 'Gyi', 'Gxi', 'Gyi', 'Giz', 'Gyi', 'Gzi', 'Giz'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Giy', 'Gix', 'Gcnot', 'Gii', 'Gyi', 'Gyi', 'Giy'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Gcnot', 'Gix', 'Giy', 'Gyi', 'Gyi', 'Gyi', 'Gcnot'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcnot', 'Gyi', 'Gxi', 'Gyi', 'Giy', 'Gyi', 'Gyi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
}