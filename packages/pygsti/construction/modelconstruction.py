"""Functions for the construction of new models."""
from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************

import numpy as _np
import itertools as _itertools
import collections as _collections
import scipy.linalg as _spl
import warnings as _warnings


from ..tools import optools as _gt
from ..tools import basistools as _bt
from ..tools import compattools as _compat
from ..objects import operation as _op
from ..objects import spamvec as _spamvec
from ..objects import povm as _povm
from ..objects import model as _mdl
from ..objects import gaugegroup as _gg
from ..objects import labeldicts as _ld
from ..objects import qubitgraph as _qubitgraph
from ..objects.localnoisemodel import LocalNoiseModel as _LocalNoiseModel
from ..baseobjs import label as _label
from ..baseobjs import Basis as _Basis
from ..baseobjs import Dim as _Dim


#############################################
# Build gates based on "standard" gate names
############################################

def basis_build_vector(vecExpr, basis):
    """
    Build a rho or E vector from an expression.

    Parameters
    ----------
    vecExpr : string
        the expression which determines which vector to build.  Currenlty, only
        integers are allowed, which specify a the vector for the pure state of
        that index.  For example, "1" means return vectorize(``|1><1|``).  The
        index labels the absolute index of the state within the entire state
        space, and is independent of the direct-sum decomposition of density
        matrix space.

    basis : Basis object
        The basis of the returned vector.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).

    Returns
    -------
    numpy array
        The vector specified by vecExpr in the desired basis.
    """
    _, opDim, blockDims = basis.dim
    vecInReducedStdBasis = _np.zeros( (opDim,1), 'd' ) # assume index given as vecExpr refers to a
                                                         #Hilbert-space state index, so "reduced-std" basis

    #So far just allow integer prepExpressions that give the index of state (within the state space) that we prep/measure
    try:
        index = int(vecExpr)
    except:
        raise ValueError("Expression must be the index of a state (as a string)")

    start = 0; vecIndex = 0
    for blockDim in blockDims:
        for i in range(start,start+blockDim):
            for j in range(start,start+blockDim):
                if (i,j) == (index,index):
                    vecInReducedStdBasis[ vecIndex, 0 ] = 1.0  #set diagonal element of density matrix
                    break
                vecIndex += 1
        start += blockDim

    return _bt.change_basis(vecInReducedStdBasis, 'std', basis)

def build_vector(stateSpaceDims, stateSpaceLabels, vecExpr, basis="gm"):
    """
    DEPRECATED: use :func:`basis_build_vector` instead.
    """
    _warnings.warn(("This function is deprecated and will be removed in the"
                    " future.  Please use `basis_build_vector` instead."))
    return basis_build_vector(vecExpr, _Basis(basis, stateSpaceDims))

def basis_build_identity_vec(basis):
    """
    Build a the identity vector for a given space and basis.

    Parameters
    ----------
    basis : Basis object
        The basis of the returned vector.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).

    Returns
    -------
    numpy array
        The identity vector in the desired basis.
    """
    _, opDim, blockDims = basis.dim 
    vecInReducedStdBasis = _np.zeros( (opDim,1), 'd' ) # assume index given as vecExpr refers to a Hilbert-space state index, so "reduced-std" basis

    #set all diagonal elements of density matrix to 1.0 (end result = identity density mx)
    start = 0; vecIndex = 0
    for blockDim in blockDims:
        for i in range(start,start+blockDim):
            for j in range(start,start+blockDim):
                if i == j: vecInReducedStdBasis[ vecIndex, 0 ] = 1.0  #set diagonal element of density matrix
                vecIndex += 1
        start += blockDim
    return _bt.change_basis(vecInReducedStdBasis, "std", basis)

def build_identity_vec(stateSpaceDims, basis="gm"):
    """
    Build the identity vector given a certain density matrix struture.

    Parameters
    ----------
    stateSpaceDims : list
        A list of integers specifying the dimension of each block
        of a block-diagonal the density matrix.

    basis : str, optional
        The string abbreviation of the basis of the returned vector.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt).

    Returns
    -------
    numpy array
    """
    return basis_build_identity_vec(_Basis(basis, stateSpaceDims))

def _oldBuildGate(stateSpaceDims, stateSpaceLabels, opExpr, basis="gm"):
#coherentStateSpaceBlockDims
    """
    Build a operation matrix from an expression

    Parameters
    ----------
    stateSpaceDims : a list of integers specifying the dimension of each block
    of a block-diagonal the density matrix
    stateSpaceLabels : a list of tuples, each one corresponding to a block of
    the density matrix.  Elements of the tuple are user-defined labels
    beginning with "L" (single level) or "Q" (two-level; qubit) which interpret
    the states within the block as a tensor product structure between the
    labelled constituent systems.

    opExpr : string containing an expression for the gate to build

    basis : {'std', 'gm', 'pp', 'qt'} or Basis object
        The source and destination basis, respectively.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).
    """
    # opExpr can contain single qubit ops: X(theta) ,Y(theta) ,Z(theta)
    #                      two qubit ops: CNOT
    #                      clevel qubit ops: Leak
    #                      two clevel opts: Flip
    #  each of which is given additional parameters specifying which indices it acts upon


    #LinearOperator matrix will be in matrix unit basis, which we order by vectorizing
    # (by concatenating rows) each block of coherent states in the order given.
    dmDim, _ , _ = _Dim(stateSpaceDims)
    fullOpDim = dmDim**2

    #Working with a StateSpaceLabels object gives us access to all the info we'll need later
    sslbls = _ld.StateSpaceLabels(stateSpaceLabels)
    if sslbls.dim != _Dim(stateSpaceDims):
        raise ValueError("Dimension mismatch!")

    #Store each tensor product block's start index (within the density matrix)
    startIndex = []; M = 0
    for tpb_dim in sslbls.dim.blockDims:
        startIndex.append(M); M += tpb_dim

    #print "DB: dim = ",dim, " dmDim = ",dmDim
    opInStdBasis = _np.identity( fullOpDim, 'complex' )
      # in full basis of matrix units, which we later reduce to the
      # that basis of matrix units corresponding to the allowed non-zero
      #  elements of the density matrix.

    exprTerms = opExpr.split(':')
    for exprTerm in exprTerms:

        opTermInStdBasis = _np.identity( fullOpDim, 'complex' )
        l = exprTerm.index('('); r = exprTerm.index(')')
        opName = exprTerm[0:l]
        argsStr = exprTerm[l+1:r]
        args = argsStr.split(',')

        if opName == "I":
            pass

        elif opName in ('X','Y','Z'): #single-qubit gate names
            assert(len(args) == 2) # theta, qubit-index
            theta = eval( args[0], {"__builtins__":None}, {'pi': _np.pi})
            label = args[1].strip(); assert(sslbls.labeldims[label] == 2)

            if opName == 'X': ex = -1j * theta*_bt.sigmax/2
            elif opName == 'Y': ex = -1j * theta*_bt.sigmay/2
            elif opName == 'Z': ex = -1j * theta*_bt.sigmaz/2
            Uop = _spl.expm(ex) # 2x2 unitary matrix operating on single qubit in [0,1] basis

            iTensorProdBlk = sslbls.tpb_index[label] # index of tensor product block (of state space) this bit label is part of
            cohBlk = sslbls.labels[iTensorProdBlk]
            basisInds = []
            for l in cohBlk:
                basisInds.append(list(range(sslbls.labeldims[l])))

            tensorBlkBasis = list(_itertools.product(*basisInds))
            K = cohBlk.index(label)
            N = len(tensorBlkBasis)
            UcohBlk = _np.identity( N, 'complex' ) # unitary matrix operating on relevant tensor product block part of state
            for i,b1 in enumerate(tensorBlkBasis):
                for j,b2 in enumerate(tensorBlkBasis):
                    if (b1[:K]+b1[K+1:]) == (b2[:K]+b2[K+1:]):   #if all part of tensor prod match except for qubit we're operating on
                        UcohBlk[i,j] = Uop[ b1[K], b2[K] ] # then fill in element

            opBlk = _gt.unitary_to_process_mx(UcohBlk) # N^2 x N^2 mx operating on vectorized tensor product block of densty matrix

            #Map opBlk's basis into final gate basis
            mapBlk = []
            s = startIndex[iTensorProdBlk] #within state space (i.e. row or col of density matrix)
            cohBlkSize = UcohBlk.shape[0]
            for i in range(cohBlkSize):
                for j in range(cohBlkSize):
                    vec_ij_index = (s+i)*dmDim + (s+j) #vectorize by concatenating rows
                    mapBlk.append( vec_ij_index ) #build list of vector indices of each element of opBlk mx
            for i,fi in enumerate(mapBlk):
                for j,fj in enumerate(mapBlk):
                    opTermInStdBasis[fi,fj] = opBlk[i,j]


        elif opName in ('CX','CY','CZ','CNOT','CPHASE'): #two-qubit gate names

            if opName in ('CX','CY','CZ'):
                assert(len(args) == 3) # theta, qubit-label1, qubit-label2
                theta = eval( args[0], {"__builtins__":None}, {'pi': _np.pi})
                label1, label2 = args[1:]

                if opName == 'CX': ex = -1j * theta*_bt.sigmax/2
                elif opName == 'CY': ex = -1j * theta*_bt.sigmay/2
                elif opName == 'CZ': ex = -1j * theta*_bt.sigmaz/2
                Utarget = _spl.expm(ex) # 2x2 unitary matrix operating on target qubit
                
            else: # opName in ('CNOT','CPHASE')
                assert(len(args) == 2) # qubit-label1, qubit-label2
                label1, label2 = args
                if opName == 'CNOT':
                    Utarget = _np.array( [[0, 1],
                                          [1, 0]], 'd')
                elif opName == 'CPHASE':
                    Utarget = _np.array( [[1, 0],
                                          [0,-1]], 'd')

            Uop = _np.identity(4, 'complex'); Uop[2:,2:] = Utarget #4x4 unitary matrix operating on isolated two-qubit space

            assert(sslbls.labeldims[label1] == 2 and sslbls.labeldims[label2] == 2)
            iTensorProdBlk = sslbls.tpb_index[label1] # index of tensor product block (of state space) this bit label is part of
            assert( iTensorProdBlk == sslbls.tpb_index[label2] ) #labels must be members of the same tensor product block
            cohBlk = sslbls.labels[iTensorProdBlk]
            basisInds = []
            for l in cohBlk:
                basisInds.append(list(range(sslbls.labeldims[l])))

            tensorBlkBasis = list(_itertools.product(*basisInds))
            K1 = cohBlk.index(label1)
            K2 = cohBlk.index(label2)
            N = len(tensorBlkBasis)
            UcohBlk = _np.identity( N, 'complex' ) # unitary matrix operating on relevant tensor product block part of state
            for i,b1 in enumerate(tensorBlkBasis):
                for j,b2 in enumerate(tensorBlkBasis):
                    b1p = list(b1); del b1p[max(K1,K2)]; del b1p[min(K1,K2)] # b1' -- remove basis indices for tensor
                    b2p = list(b2); del b2p[max(K1,K2)]; del b2p[min(K1,K2)] # b2'      product parts we operate on
                    if b1p == b2p:   #if all parts of tensor product match except for qubits we're operating on
                        UcohBlk[i,j] = Uop[ 2*b1[K1]+b1[K2], 2*b2[K1]+b2[K2] ] # then fill in element

            #print "UcohBlk = \n",UcohBlk

            opBlk = _gt.unitary_to_process_mx(UcohBlk) # N^2 x N^2 mx operating on vectorized tensor product block of densty matrix

            #Map opBlk's basis into final gate basis
            mapBlk = []
            s = startIndex[iTensorProdBlk] #within state space (i.e. row or col of density matrix)
            cohBlkSize = UcohBlk.shape[0]
            for i in range(cohBlkSize):
                for j in range(cohBlkSize):
                    vec_ij_index = (s+i)*dmDim + (s+j) #vectorize by concatenating rows
                    mapBlk.append( vec_ij_index ) #build list of vector indices of each element of opBlk mx
            for i,fi in enumerate(mapBlk):
                for j,fj in enumerate(mapBlk):
                    opTermInStdBasis[fi,fj] = opBlk[i,j]

        elif opName == "LX":  #TODO - better way to describe leakage?
            assert(len(args) == 3) # theta, dmIndex1, dmIndex2 - X rotation between any two density matrix basis states
            theta = eval( args[0], {"__builtins__":None}, {'pi': _np.pi})
            i1 = int(args[1])
            i2 = int(args[2])
            ex = -1j * theta*_bt.sigmax/2
            Uop = _spl.expm(ex) # 2x2 unitary matrix operating on the i1-th and i2-th states of the state space basis
            Utot = _np.identity(dmDim, 'complex')
            Utot[ i1,i1 ] = Uop[0,0]
            Utot[ i1,i2 ] = Uop[0,1]
            Utot[ i2,i1 ] = Uop[1,0]
            Utot[ i2,i2 ] = Uop[1,1]

            opBlk = _gt.unitary_to_process_mx(Utot) # N^2 x N^2 mx operating on vectorized tensor product block of densty matrix

            #Map opBlk's basis (vectorized 2x2) into final gate basis
            mapBlk = [] #note: "start index" is effectively zero since we're mapping all the blocs
            for i in range(dmDim):
                for j in range(dmDim):
                    vec_ij_index = (i)*dmDim + (j) #vectorize by concatenating rows
                    mapBlk.append( vec_ij_index ) #build list of vector indices of each element of opBlk mx
            for i,fi in enumerate(mapBlk):
                for j,fj in enumerate(mapBlk):
                    opTermInStdBasis[fi,fj] = opBlk[i,j]

            #sq = startIndex[qbIndex]; sc = startIndex[clIndex]  #sq,sc are density matrix start indices
            #vsq = dmiToVi[ (sq,sq) ]; vsc = dmiToVi[ (sc,sc) ]  # vector indices of (sq,sq) and (sc,sc) density matrix elements
            #vsq1 = dmiToVi[ (sq,sq+1) ]; vsq2 = dmiToVi[ (sq+1,sq) ]  # vector indices of qubit coherences
            #
            ## action = swap (sq,sq) and (sc,sc) elements of a d.mx. and destroy coherences within qubit
            #opTermInStdBasis[vsq,vsc] = opTermInStdBasis[vsc,vsq] = 1.0
            #opTermInStdBasis[vsq,vsq] = opTermInStdBasis[vsc,vsc] = 0.0
            #opTermInStdBasis[vsq1,vsq1] = opTermInStdBasis[vsq2,vsq2] = 0.0


#        elif opName == "Flip":
#            assert(len(args) == 2) # clevel-index0, clevel-index1
#            indx0 = int(args[0])
#            indx1 = int(args[1])
#            assert(indx0 != indx1)
#            assert(bitLabels[indx0] == 'L' and bitLabels[indx1] == 'L')
#
#            s0 = startIndex[indx0]; s1 = startIndex[indx1] #density matrix indices
#            vs0 = dmiToVi[ (s0,s0) ]; vs1 = dmiToVi[ (s1,s1) ]  # vector indices of (s0,s0) and (s1,s1) density matrix elements
#
#            # action = swap (s0,s0) and (s1,s1) elements of a d.mx.
#            opTermInStdBasis[vs0,vs1] = opTermInStdBasis[vs1,vs0] = 1.0
#            opTermInStdBasis[vs0,vs0] = opTermInStdBasis[vs1,vs1] = 0.0

        else: raise ValueError("Invalid gate name: %s" % opName)

        opInStdBasis = _np.dot(opInStdBasis, opTermInStdBasis)

    #Pare down opInStdBasis to only include those matrix unit basis elements that are allowed to be nonzero
    opInReducedStdBasis = _bt.resize_mx(opInStdBasis, stateSpaceDims, resize='contract')

    #Change from std (mx unit) basis to another if requested
    opMxInFinalBasis = _bt.change_basis(opInReducedStdBasis, "std", basis, stateSpaceDims)
    
    return _op.FullyParameterizedOp(opMxInFinalBasis)

def basis_build_operation(stateSpaceLabels, opExpr, basis="gm", parameterization="full", unitaryEmbedding=False):
    """
    Build a LinearOperator object from an expression.

    Parameters
    ----------
    stateSpaceLabels : a list of tuples
        Each tuple corresponds to a block of a density matrix in the standard
        basis (and therefore a component of the direct-sum density matrix
        space). Elements of a tuple are user-defined labels beginning with "L"
        (single level) or "Q" (two-level; qubit) which interpret the
        d-dimensional state space corresponding to a d x d block as a tensor
        product between qubit and single level systems.

    opExpr : string
        expression for the gate to build.  String is first split into parts
        delimited by the colon (:) character, which are composed together to
        create the final gate.  Each part takes on of the allowed forms:

        - I(ssl_0, ...) = identity operation on one or more state space labels
          (ssl_i)
        - X(theta, ssl) = x-rotation by theta radians of qubit labeled by ssl
        - Y(theta, ssl) = y-rotation by theta radians of qubit labeled by ssl
        - Z(theta, ssl) = z-rotation by theta radians of qubit labeled by ssl
        - CX(theta, ssl0, ssl1) = controlled x-rotation by theta radians.  Acts
          on qubit labeled by ssl1 with ssl0 being the control.
        - CY(theta, ssl0, ssl1) = controlled y-rotation by theta radians.  Acts
          on qubit labeled by ssl1 with ssl0 being the control.
        - CZ(theta, ssl0, ssl1) = controlled z-rotation by theta radians.  Acts
          on qubit labeled by ssl1 with ssl0 being the control.
        - CNOT(ssl0, ssl1) = standard controlled-not gate.  Acts on qubit
          labeled by ssl1 with ssl0 being the control.
        - CPHASE(ssl0, ssl1) = standard controlled-phase gate.  Acts on qubit
          labeled by ssl1 with ssl0 being the control.
        - LX(theta, i0, i1) = leakage between states i0 and i1.  Implemented as
          an x-rotation between states with integer indices i0 and i1 followed
          by complete decoherence between the states.

    basis : {'std', 'gm', 'pp', 'qt'} or Basis object
        The source and destination basis, respectively.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).

    parameterization : {"full","TP","static","linear","linearTP"}, optional
        How to parameterize the resulting gate.

        - "full" = return a FullyParameterizedOp.
        - "TP" = return a TPParameterizedOp.
        - "static" = return a StaticOp.
        - "linear" = if possible, return a LinearlyParameterizedOp that
          parameterizes only the pieces explicitly present in opExpr.
        - "linearTP" = if possible, return a LinearlyParameterizedOp that
          parameterizes only the TP pieces explicitly present in opExpr.

    unitaryEmbedding : bool, optional
        An interal switch determining how the gate is constructed.  Should have
        no bearing on the output except in determining how to parameterize a
        non-FullyParameterizedOp.  It's best to leave this to False unless
        you really know what you're doing.  Currently, only works for
        parameterization == 'full'.

    Returns
    -------
    LinearOperator
        A gate object representing the gate given by opExpr in the desired
        basis.
    """
    # opExpr can contain single qubit ops: X(theta) ,Y(theta) ,Z(theta)
    #                      two qubit ops: CNOT
    #                      clevel qubit ops: Leak
    #                      two clevel opts: Flip
    #  each of which is given additional parameters specifying which indices it acts upon
    dmDim, opDim, blockDims = basis.dim
      #fullOpDim = dmDim**2
    
    #Working with a StateSpaceLabels object gives us access to all the info we'll need later
    sslbls = _ld.StateSpaceLabels(stateSpaceLabels)
    assert(sslbls.dim == basis.dim), \
        "State space labels dim (%s) != basis dim (%s)" % (sslbls.dim, basis.dim)


    # ----------------------------------------------------------------------------------------------------------------------------------------
    # -- Helper Functions --------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------------

    def equals_except(list1, list2, exemptIndices):
        """ Test equivalence of list1 and list2 except for certain indices """
        for i,(l1,l2) in enumerate(zip(list1,list2)):
            if i in exemptIndices: continue
            if l1 != l2: return False
        return True

    def embed_operator_unitary(Uop, labels):
        """ Use the "unitary method" to embed a gate within it's larger Hilbert space """
        # Note: Uop should be in std basis (really no other basis it could be
        # since gm and pp are only for acting on dm space)
        iTensorProdBlks = [ sslbls.tpb_index[label] for label in labels ] # index of tensor product block (of state space) a bit label is part of
        if len(set(iTensorProdBlks)) > 1:
            raise ValueError("All qubit labels of a multi-qubit gate must correspond to the same tensor-product-block of the state space")

        iTensorProdBlk = iTensorProdBlks[0] #because they're all the same (tested above)
        tensorProdBlkLabels = sslbls.labels[iTensorProdBlk]
        basisInds = [] # list of *state* indices of each component of the tensor product block
        for l in tensorProdBlkLabels:
            basisInds.append( list(range(sslbls.labeldims[l])) ) # e.g. [0,1] for qubits

        tensorBlkBasis = list(_itertools.product(*basisInds)) #state-space basis (remember tensor-prod-blocks are in state space)
        N = len(tensorBlkBasis) #size of state space (not density matrix space, which is N**2)

        labelIndices = [ tensorProdBlkLabels.index(label) for label in labels ]
        labelMultipliers = []; stateSpaceDim = 1
        for l in reversed(labels):
            labelMultipliers.append(stateSpaceDim)
            stateSpaceDim *= sslbls.labeldims[l]
        labelMultipliers.reverse() #reverse back to labels order (labels was reversed in loop above)
        labelMultipliers = _np.array(labelMultipliers,_np.int64) #so we can use _np.dot below
        assert(stateSpaceDim == Uop.shape[0] == Uop.shape[1])

        # Unitary op approach: build unitary acting on state space than use kron => map acting on vec(density matrix) space
        UcohBlk = _np.identity( N, 'complex' ) # unitary matrix operating on relevant tensor product block part of state
        for i,b1 in enumerate(tensorBlkBasis):
            for j,b2 in enumerate(tensorBlkBasis):
                if equals_except(b1,b2,labelIndices): #if all parts of tensor prod match except for qubit(s) we're operating on
                    op_b1 = _np.array([ b1[K] for K in labelIndices ],_np.int64) #basis indices for just the qubits we're operating on
                    op_b2 = _np.array([ b2[K] for K in labelIndices ],_np.int64) # - i.e. those corresponding to the given Uop
                    op_i = _np.dot(labelMultipliers, op_b1)
                    op_j = _np.dot(labelMultipliers, op_b2)
                    UcohBlk[i,j] = Uop[ op_i, op_j ] # fill in element
                    #FUTURE: could keep track of what Uop <-> UcohBlk elements for parameterization here

        opBlk = _gt.unitary_to_process_mx(UcohBlk) # N^2 x N^2 mx operating on vectorized tensor product block of densty matrix

        #print "DEBUG: Uop = \n", Uop
        #print "DEBUG: UcohBlk = \n", UcohBlk

        #Map opBlk's basis into final gate basis (shift basis indices due to the composition of different direct-sum
        # blocks along diagonal of final gate mx)
        offset = sum( [ blockDims[i]**2 for i in range(0,iTensorProdBlk) ] ) #number of basis elements preceding our block's elements
        finalGateInStdBasis = _np.identity( opDim, 'complex' )             # operates on entire state space (direct sum of tensor prod. blocks)
        finalGateInStdBasis[offset:offset+N**2,offset:offset+N**2] = opBlk # opBlk gets offset along diagonal by the numer of preceding basis elements

        if parameterization != "full":
            raise ValueError("Unitary embedding is only implemented for parmeterization='full'")

        finalOpInFinalBasis = _bt.change_basis(finalGateInStdBasis, "std", basis.name, blockDims)
        return _op.FullyParameterizedOp(finalOpInFinalBasis)


    def embed_operation(opmx, labels, indicesToParameterize="all"):
        """ Embed "local" operation matrix into gate for larger Hilbert space using
            our standard method """
        #print "DEBUG: embed_operation opmx = \n", opmx
        iTensorProdBlks = [  sslbls.tpb_index[label] for label in labels ] # index of tensor product block (of state space) a bit label is part of
        if len(set(iTensorProdBlks)) != 1:
            raise ValueError("All qubit labels of a multi-qubit gate must correspond to the" + \
                             " same tensor-product-block of the state space -- checked previously")

        iTensorProdBlk = iTensorProdBlks[0] #because they're all the same (tested above)
        tensorProdBlkLabels = stateSpaceLabels[iTensorProdBlk]
        basisInds = [] # list of possible *density-matrix-space* indices of each component of the tensor product block
        for l in tensorProdBlkLabels:
            basisInds.append( list(range(sslbls.labeldims[l]**2)) ) # e.g. [0,1,2,3] for qubits (I, X, Y, Z)

        tensorBlkEls = list(_itertools.product(*basisInds)) #dm-space basis
        lookup_blkElIndex = { tuple(b):i for i,b in enumerate(tensorBlkEls) } # index within vec(tensor prod blk) of each basis el
        N = len(tensorBlkEls) #size of density matrix space
        assert( N == blockDims[iTensorProdBlk]**2 )

        # LinearOperator matrix approach: insert elements of opmx into map acting on vec(density matrix) space
        opBlk = _np.identity( N, 'd' ) # matrix operating on vec(tensor product block), (tensor prod blk is a part of the total density mx)
          #Note: because we're in the Pauil-product basis this is a *real* matrix (and opmx should have only real elements and be in the pp basis)

        # Separate the components of the tensor product that are not operated on, i.e. that our final map just acts as identity w.r.t.
        basisInds_noop = basisInds[:]
        labelIndices = [ tensorProdBlkLabels.index(label) for label in labels ]
        for labelIndex in sorted(labelIndices,reverse=True):
            del basisInds_noop[labelIndex]
        tensorBlkEls_noop = list(_itertools.product(*basisInds_noop)) #dm-space basis for noop-indices only
        parameterToBaseIndicesMap = {}

        def decomp_op_index(indx):
            """ Decompose index of a Pauli-product matrix into indices of each
            Pauli in the product """
            ret = []; divisor = 1; divisors = []
            #print "Decomp %d" % indx,
            for l in labels:
                divisors.append(divisor)
                divisor *= sslbls.labeldims[l]**2 # E.g. "4" for qubits
            for d in reversed(divisors):
                ret.append( indx // d )
                indx = indx % d
            #print " => %s (div = %s)" % (str(ret), str(divisors))
            return ret

        def merge_op_and_noop_bases(op_b, noop_b):
            """
            Merge the Pauli basis indices for the "gate"-parts of the total
            basis contained in op_b (i.e. of the components of the tensor
            product space that are operated on) and the "noop"-parts contained
            in noop_b.  Thus, len(op_b) + len(noop_b) == len(basisInds), and
            this function merges together basis indices for the operated-on and
            not-operated-on tensor product components.
            Note: return value always have length == len(basisInds) == number
            of componens
            """
            ret = list(noop_b[:])    #start with noop part...
            for li,b_el in sorted( zip(labelIndices,op_b), key=lambda x: x[0]):
                ret.insert(li, b_el) #... and insert gate parts at proper points
            return ret


        for op_i in range(opmx.shape[0]):     # rows ~ "output" of the gate map
            for op_j in range(opmx.shape[1]): # cols ~ "input"  of the gate map
                if indicesToParameterize == "all":
                    iParam = op_i*opmx.shape[1] + op_j #index of (i,j) gate parameter in 1D array of parameters (flatten opmx)
                    parameterToBaseIndicesMap[ iParam ] = []
                elif indicesToParameterize == "TP":
                    if op_i > 0:
                        iParam = (op_i-1)*opmx.shape[1] + op_j
                        parameterToBaseIndicesMap[ iParam ] = []
                    else:
                        iParam = None
                elif (op_i,op_j) in indicesToParameterize:
                    iParam = indicesToParameterize.index( (op_i,op_j) )
                    parameterToBaseIndicesMap[ iParam ] = []
                else:
                    iParam = None #so we don't parameterize below

                op_b1 = decomp_op_index(op_i) # op_b? are lists of dm basis indices, one index per
                op_b2 = decomp_op_index(op_j) #  tensor product component that the gate operates on (2 components for a 2-qubit gate)

                for b_noop in tensorBlkEls_noop: #loop over all state configurations we don't operate on - so really a loop over diagonal dm elements
                    b_out = merge_op_and_noop_bases(op_b1, b_noop)  # using same b_noop for in and out says we're acting
                    b_in  = merge_op_and_noop_bases(op_b2, b_noop)  #  as the identity on the no-op state space
                    out_vec_index = lookup_blkElIndex[ tuple(b_out) ] # index of output dm basis el within vec(tensor block basis)
                    in_vec_index  = lookup_blkElIndex[ tuple(b_in) ]  # index of input dm basis el within vec(tensor block basis)

                    opBlk[ out_vec_index, in_vec_index ] = opmx[ op_i, op_j ]
                    if iParam is not None:
                        # keep track of what opBlk <-> opmx elements for parameterization
                        parameterToBaseIndicesMap[ iParam ].append( (out_vec_index, in_vec_index) )


        #Map opBlk's basis into final gate basis (shift basis indices due to the composition of different direct-sum
        # blocks along diagonal of final gate mx)
        offset = sum( [ blockDims[i]**2 for i in range(0,iTensorProdBlk) ] ) #number of basis elements preceding our block's elements
        finalOp = _np.identity( opDim, 'd' )              # operates on entire state space (direct sum of tensor prod. blocks)
        finalOp[offset:offset+N,offset:offset+N] = opBlk  # opBlk gets offset along diagonal by the number of preceding basis elements
        # Note: final is a *real* matrix whose basis is the pauli-product basis in the iTensorProdBlk-th block, concatenated with
        #   bases for the other blocks - say the "std" basis (which one does't matter since the identity is the same for std, gm, and pp)

        #print "DEBUG: embed_operation opBlk = \n", opBlk
        tensorDim = blockDims[iTensorProdBlk]
        startBasis = _Basis('pp',  tensorDim)
        finalBasis = _Basis(basis.name, tensorDim)

        d = slice(offset, offset+N)

        full_ppToFinal       = _np.identity(opDim, 'complex')
        full_ppToFinal[d, d] = startBasis.transform_matrix(finalBasis)

        full_finalToPP       = _np.identity(opDim, 'complex')
        full_finalToPP[d, d] = finalBasis.transform_matrix(startBasis)

        finalOpInFinalBasis = _np.dot(full_ppToFinal,
                                        _np.dot( finalOp, full_finalToPP))
        if parameterization == "full":
            return _op.FullyParameterizedOp(
                _np.real(finalOpInFinalBasis)
                if finalBasis.real else finalOpInFinalBasis, "densitymx" )

        if parameterization == "static":
            return _op.StaticOp(
                _np.real(finalOpInFinalBasis)
                if finalBasis.real else finalOpInFinalBasis, "densitymx" )

        if parameterization == "TP":
            if not finalBasis.real:
                raise ValueError("TP gates must be real. Failed to build gate!") # pragma: no cover
            return _op.TPParameterizedOp(_np.real(finalOpInFinalBasis))

        elif parameterization in ("linear","linearTP"):
            #OLD (INCORRECT) -- but could give this as paramArray if gave zeros as base matrix instead of finalOp
            # paramArray = opmx.flatten() if indicesToParameterize == "all" else _np.array([opmx[t] for t in indicesToParameterize])

            #Set all params to *zero* since base matrix contains all initial elements -- parameters just give deviation
            if indicesToParameterize == "all":
                paramArray = _np.zeros(opmx.size, 'd')
            elif indicesToParameterize == "TP":
                paramArray = _np.zeros(opmx.size - opmx.shape[1], 'd')
            else:
                paramArray = _np.zeros(len(indicesToParameterize), 'd' )

            return _op.LinearlyParameterizedOp(
                finalOp, paramArray, parameterToBaseIndicesMap,
                full_ppToFinal, full_finalToPP, finalBasis.real )


        else:
            raise ValueError("Invalid 'parameterization' parameter: " +
                             "%s (must by 'full', 'TP', 'static', 'linear' or 'linearTP')"
                             % parameterization)


    # ----------------------------------------------------------------------------------------------------------------------------------------
    # -- End Helper Functions ----------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------------


    #print "DB: dim = ",dim, " dmDim = ",dmDim
    opInFinalBasis = None #what will become the final operation matrix
    defaultI2P = "all" if parameterization != "linearTP" else "TP"
      #default indices to parameterize (I2P) - used only when 
      # creating parameterized gates

    exprTerms = opExpr.split(':')
    for exprTerm in exprTerms:

        l = exprTerm.index('('); r = exprTerm.rindex(')')
        opName = exprTerm[0:l]
        argsStr = exprTerm[l+1:r]
        args = argsStr.split(',')

        if opName == "I":
            labels = args # qubit labels (TODO: what about 'L' labels? -- not sure if they work with this...)
            stateSpaceDim = sslbls.product_dim(labels)

            if unitaryEmbedding:
                Uop = _np.identity(stateSpaceDim, 'complex') #complex because in std state space basis
                opTermInFinalBasis = embed_operator_unitary(Uop, tuple(labels)) #Uop assumed to be in std basis (really the only option)
            else:
                pp_opMx = _np.identity(stateSpaceDim**2, 'd') # *real* 4x4 mx in Pauli-product basis -- still just the identity!
                opTermInFinalBasis = embed_operation(pp_opMx, tuple(labels), defaultI2P) # pp_opMx assumed to be in the Pauli-product basis

        elif opName == "D":  #like 'I', but only parameterize the diagonal elements - so can be a depolarization-type map
            labels = args # qubit labels (TODO: what about 'L' labels? -- not sure if they work with this...)
            stateSpaceDim = sslbls.product_dim(labels)

            if unitaryEmbedding or parameterization not in ("linear","linearTP"):
                raise ValueError("'D' gate only makes sense to use when unitaryEmbedding is False and parameterization == 'linear'")

            if defaultI2P == "TP":
                indicesToParameterize = [ (i,i) for i in range(1,stateSpaceDim**2) ] #parameterize only the diagonals els after the first
            else:
                indicesToParameterize = [ (i,i) for i in range(0,stateSpaceDim**2) ] #parameterize only the diagonals els
            pp_opMx = _np.identity(stateSpaceDim**2, 'd') # *real* 4x4 mx in Pauli-product basis -- still just the identity!
            opTermInFinalBasis = embed_operation(pp_opMx, tuple(labels), indicesToParameterize) # pp_opMx assumed to be in the Pauli-product basis


        elif opName in ('X','Y','Z'): #single-qubit gate names
            assert(len(args) == 2) # theta, qubit-index
            theta = eval( args[0], {"__builtins__":None}, {'pi': _np.pi})
            label = args[1].strip()
            assert(sslbls.labeldims[label] == 2), "%s gate must act on qubits!" % opName

            if opName == 'X': ex = -1j * theta*_bt.sigmax/2
            elif opName == 'Y': ex = -1j * theta*_bt.sigmay/2
            elif opName == 'Z': ex = -1j * theta*_bt.sigmaz/2

            Uop = _spl.expm(ex) # 2x2 unitary matrix operating on single qubit in [0,1] basis
            #print("CDBG Uop = \n",Uop)
            if unitaryEmbedding:
                opTermInFinalBasis = embed_operator_unitary(Uop, (label,)) #Uop assumed to be in std basis (really the only option)
            else:
                operationMx = _gt.unitary_to_process_mx(Uop) # complex 4x4 mx operating on vectorized 1Q densty matrix in std basis
                pp_opMx = _bt.change_basis(operationMx, 'std', 'pp') # *real* 4x4 mx in Pauli-product basis -- better for parameterization
                opTermInFinalBasis = embed_operation(pp_opMx, (label,), defaultI2P) # pp_opMx assumed to be in the Pauli-product basis

        elif opName == 'N': #more general single-qubit gate
            assert(len(args) == 5) # theta, sigmaX-coeff, sigmaY-coeff, sigmaZ-coeff, qubit-index
            theta = eval( args[0], {"__builtins__":None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            sxCoeff = eval( args[1], {"__builtins__":None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            syCoeff = eval( args[2], {"__builtins__":None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            szCoeff = eval( args[3], {"__builtins__":None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            label = args[4].strip()
            assert(sslbls.labeldims[label] == 2), "%s gate must act on qubits!" % opName

            ex = -1j * theta * ( sxCoeff * _bt.sigmax/2. + syCoeff * _bt.sigmay/2. + szCoeff * _bt.sigmaz/2.)
            Uop = _spl.expm(ex) # 2x2 unitary matrix operating on single qubit in [0,1] basis
            if unitaryEmbedding:
                opTermInFinalBasis = embed_operator_unitary(Uop, (label,)) #Uop assumed to be in std basis (really the only option)
            else:
                operationMx = _gt.unitary_to_process_mx(Uop) # complex 4x4 mx operating on vectorized 1Q densty matrix in std basis
                pp_opMx = _bt.change_basis(operationMx, 'std', 'pp') # *real* 4x4 mx in Pauli-product basis -- better for parameterization
                opTermInFinalBasis = embed_operation(pp_opMx, (label,), defaultI2P) # pp_opMx assumed to be in the Pauli-product basis

                
        elif opName in ('CX','CY','CZ','CNOT','CPHASE'): #two-qubit gate names

            if opName in ('CX','CY','CZ'):
                assert(len(args) == 3) # theta, qubit-label1, qubit-label2
                theta = eval( args[0], {"__builtins__":None}, {'pi': _np.pi})
                label1 = args[1].strip(); label2 = args[2].strip()

                if opName == 'CX': ex = -1j * theta*_bt.sigmax/2
                elif opName == 'CY': ex = -1j * theta*_bt.sigmay/2
                elif opName == 'CZ': ex = -1j * theta*_bt.sigmaz/2
                Utarget = _spl.expm(ex) # 2x2 unitary matrix operating on target qubit
                
            else: # opName in ('CNOT','CPHASE')
                assert(len(args) == 2) # qubit-label1, qubit-label2
                label1 = args[0].strip(); label2 = args[1].strip()

                if opName == 'CNOT':
                    Utarget = _np.array( [[0, 1],
                                          [1, 0]], 'd')
                elif opName == 'CPHASE':
                    Utarget = _np.array( [[1, 0],
                                          [0,-1]], 'd')

            Uop = _np.identity(4, 'complex'); Uop[2:,2:] = Utarget #4x4 unitary matrix operating on isolated two-qubit space

            assert(sslbls.labeldims[label1] == 2 and sslbls.labeldims[label2] == 2), \
                "%s gate must act on qubits!" % opName
            
            if unitaryEmbedding:
                opTermInFinalBasis = embed_operator_unitary(Uop, (label1,label2)) #Uop assumed to be in std basis (really the only option)
            else:
                operationMx = _gt.unitary_to_process_mx(Uop) # complex 16x16 mx operating on vectorized 2Q densty matrix in std basis
                pp_opMx = _bt.change_basis(operationMx, 'std', 'pp') # *real* 16x16 mx in Pauli-product basis -- better for parameterization
                opTermInFinalBasis = embed_operation(pp_opMx, (label1,label2), defaultI2P) # pp_opMx assumed to be in the Pauli-product basis

        elif opName == "LX":  #TODO - better way to describe leakage?
            assert(len(args) == 3) # theta, dmIndex1, dmIndex2 - X rotation between any two density matrix basis states
            theta = eval( args[0], {"__builtins__":None}, {'pi': _np.pi})
            i1 = int(args[1])  # row/column index of a single *state* within the density matrix
            i2 = int(args[2])  # row/column index of a single *state* within the density matrix
            ex = -1j * theta*_bt.sigmax/2
            Uop = _spl.expm(ex) # 2x2 unitary matrix operating on the i1-th and i2-th states of the state space basis

            Utot = _np.identity(dmDim, 'complex')
            Utot[ i1,i1 ] = Uop[0,0]
            Utot[ i1,i2 ] = Uop[0,1]
            Utot[ i2,i1 ] = Uop[1,0]
            Utot[ i2,i2 ] = Uop[1,1]
            opTermInStdBasis = _gt.unitary_to_process_mx(Utot) # dmDim^2 x dmDim^2 mx operating on vectorized total densty matrix
            print(blockDims)
            # contract [3] to [2, 1]
            opTermInReducedStdBasis = _bt.resize_std_mx(opTermInStdBasis, 
                                                             'contract', 
                                                             _Basis('std', 3), 
                                                             _Basis('std', blockDims))

            opMxInFinalBasis = _bt.change_basis(opTermInReducedStdBasis, "std", basis.name, blockDims)
            opTermInFinalBasis = _op.FullyParameterizedOp(opMxInFinalBasis)

        else: raise ValueError("Invalid gate name: %s" % opName)
        
        if opInFinalBasis is None:
            opInFinalBasis = opTermInFinalBasis
        else:
            opInFinalBasis = _op.compose( opInFinalBasis, opTermInFinalBasis, basis)

    return opInFinalBasis # a LinearOperator object

def build_operation(stateSpaceDims, stateSpaceLabels, opExpr, basis="gm", parameterization="full", unitaryEmbedding=False):
    """
    DEPRECATED: use :func:`basis_build_operation` instead.
    """
    _warnings.warn(("This function is deprecated and will be removed in the"
                    " future.  Please use `basis_build_operation` instead."))
    return basis_build_operation(stateSpaceLabels, opExpr, _Basis(basis, stateSpaceDims), parameterization, unitaryEmbedding)


def basis_build_explicit_model(stateSpaceLabels, basis,
                        opLabels, opExpressions,
                        prepLabels=('rho0',), prepExpressions=('0',),
                        effectLabels='standard', effectExpressions='labels',
                        povmLabels='Mdefault', parameterization="full"):
    """
    Build a new Model given lists of operation labels and expressions.

    Parameters
    ----------
    stateSpaceLabels : a list of tuples
        Each tuple corresponds to a block of a density matrix in the standard
        basis (and therefore a component of the direct-sum density matrix
        space). Elements of a tuple are user-defined labels beginning with "L"
        (single level) or "Q" (two-level; qubit) which interpret the
        d-dimensional state space corresponding to a d x d block as a tensor
        product between qubit and single level systems.

    basis : Basis object
        The source and destination basis, respectively.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).

    opLabels : list of strings
       A list of labels for each created gate in the final model.  To
        conform with text file parsing conventions these names should begin
        with a capital G and can be followed by any number of lowercase
        characters, numbers, or the underscore character.

    opExpressions : list of strings
        A list of gate expressions, each corresponding to a operation label in
        opLabels, which determine what operation each gate performs (see
        documentation for :meth:`build_operation`).

    prepLabels : list of string, optional
        A list of labels for each created state preparation in the final
        model.  To conform with conventions these labels should begin with
        "rho".

    prepExpressions : list of strings, optional
        A list of vector expressions for each state preparation vector (see
        documentation for :meth:`build_vector`).

    effectLabels : list, optional
        If `povmLabels` is a string, then this is just a list of the effect
        (outcome) labels for the single POVM.  If `povmLabels` is a tuple, 
        then `effectLabels` must be a list of lists of effect labels, each
        list corresponding to a POVM.  If set to the special string `"standard"`
        then the labels `"0"`, `"1"`, ... `"<dim>"` are used, where `<dim>`
        is the dimension of the state space.

    effectExpressions : list, optional
        A list or list-of-lists of (string) vector expressions for each POVM
        effect vector (see documentation for :meth:`build_vector`).  Expressions
        correspond to labels in `effectLabels`.  If set to the special string
        `"labels"`, then the values of `effectLabels` are also used as 
        expressions (which works well for integer-as-a-string labels).

    povmLabels : list or string, optional
        A list of POVM labels, or a single (string) label.  In the latter case,
        only a single POVM is created and the format of `effectLabels` and
        `effectExpressions` is simplified (see above).

    parameterization : {"full","TP","linear","linearTP"}, optional
        How to parameterize the gates of the resulting Model (see
        documentation for :meth:`build_operation`).

    Returns
    -------
    Model
        The created model.
    """
    dmDim, _, blockDims = basis.dim #don't need opDim
    defP = "TP" if (parameterization in ("TP","linearTP")) else "full"
    ret = _mdl.ExplicitOpModel(default_param=defP)
                 #prep_prefix="rho", effect_prefix="E", gate_prefix="G")

    for label,rhoExpr in zip(prepLabels, prepExpressions):
        ret.preps[label] = basis_build_vector(rhoExpr, basis)

    if _compat.isstr(povmLabels):
        povmLabels = [ povmLabels ]
        effectLabels = [ effectLabels ]
        effectExpressions = [ effectExpressions ]

    for povmLbl, ELbls, EExprs in zip(povmLabels,
                                      effectLabels, effectExpressions):
        effects = []
        
        if ELbls == "standard":
            ELbls = list(map(str,range(dmDim))) #standard labels
        if EExprs == "labels":
            EExprs = ELbls #use labels as expressions

        for label,EExpr in zip(ELbls,EExprs):
            effects.append( (label,basis_build_vector(EExpr, basis)) )

        if defP == "TP":
            ret.povms[povmLbl] = _povm.TPPOVM(effects)
        else:
            ret.povms[povmLbl] = _povm.UnconstrainedPOVM(effects)

    for (opLabel,opExpr) in zip(opLabels, opExpressions):
        ret.operations[opLabel] = basis_build_operation(stateSpaceLabels,
                                          opExpr, basis, parameterization)

    if len(blockDims) == 1:
        basisDims = blockDims[0]
    else:
        basisDims = blockDims 

    ret.basis = _Basis(basis, basisDims)

    if parameterization == "full":
        ret.default_gauge_group = _gg.FullGaugeGroup(ret.dim)
    elif parameterization == "TP":
        ret.default_gauge_group = _gg.TPGaugeGroup(ret.dim)
    else:
        ret.default_gauge_group = None #assume no gauge freedom

    return ret

def build_explicit_model(stateSpaceDims, stateSpaceLabels,
                  opLabels, opExpressions,
                  prepLabels=('rho0',), prepExpressions=('0',),
                  effectLabels='standard', effectExpressions='labels',
                  povmLabels='Mdefault', basis="auto", parameterization="full"):
    """
    Build a new Model given lists of labels and expressions.

    Parameters
    ----------
    stateSpaceDims : list of ints
       Dimensions specifying the structure of the density-matrix space.
        Elements correspond to block dimensions of an allowed density matrix in
        the standard basis, and the density-matrix space is the direct sum of
        linear spaces of dimension block-dimension^2.

    stateSpaceLabels : a list of tuples
        Each tuple corresponds to a block of a density matrix in the standard
        basis (and therefore a component of the direct-sum density matrix
        space). Elements of a tuple are user-defined labels beginning with "L"
        (single level) or "Q" (two-level; qubit) which interpret the
        d-dimensional state space corresponding to a d x d block as a tensor
        product between qubit and single level systems.

    opLabels : list of strings
       A list of labels for each created gate in the final model.  To
        conform with text file parsing conventions these names should begin
        with a capital G and can be followed by any number of lowercase
        characters, numbers, or the underscore character.

    opExpressions : list of strings
        A list of gate expressions, each corresponding to a operation label in
        opLabels, which determine what operation each gate performs (see
        documentation for :meth:`build_operation`).

    prepLabels : list of string
        A list of labels for each created state preparation in the final
        model.  To conform with conventions these labels should begin with
        "rho".

    prepExpressions : list of strings
        A list of vector expressions for each state preparation vector (see
        documentation for :meth:`build_vector`).

    effectLabels : list, optional
        If `povmLabels` is a string, then this is just a list of the effect
        (outcome) labels for the single POVM.  If `povmLabels` is a tuple, 
        then `effectLabels` must be a list of lists of effect labels, each
        list corresponding to a POVM.  If set to the special string `"standard"`
        then the labels `"0"`, `"1"`, ... `"<dim>"` are used, where `<dim>`
        is the dimension of the state space.

    effectExpressions : list, optional
        A list or list-of-lists of (string) vector expressions for each POVM
        effect vector (see documentation for :meth:`build_vector`).  Expressions
        correspond to labels in `effectLabels`.  If set to the special string
        `"labels"`, then the values of `effectLabels` are also used as 
        expressions (which works well for integer-as-a-string labels).

    povmLabels : list or string, optional
        A list of POVM labels, or a single (string) label.  In the latter case,
        only a single POVM is created and the format of `effectLabels` and
        `effectExpressions` is simplified (see above).

    basis : {'gm','pp','std','qt','auto'}, optional
        the basis of the matrices in the returned Model

        - "std" = operation matrix operates on density mx expressed as sum of matrix
          units
        - "gm"  = operation matrix operates on dentity mx expressed as sum of
          normalized Gell-Mann matrices
        - "pp"  = operation matrix operates on density mx expresses as sum of
          tensor-product of Pauli matrices
        - "qt"  = operation matrix operates on density mx expressed as sum of
          Qutrit basis matrices
        - "auto" = "pp" if possible (integer num of qubits), "qt" if density
          matrix dim == 3, and "gm" otherwise.

    parameterization : {"full","TP","linear","linearTP"}, optional
        How to parameterize the gates of the resulting Model (see
        documentation for :meth:`build_operation`).

    Returns
    -------
    Model
        The created model.
    """
    if basis == "auto":
        if len(stateSpaceDims) == 1 and \
           _np.isclose(_np.log2(stateSpaceDims[0]),
                       round(_np.log2(stateSpaceDims[0]))):
            basis = "pp"
        elif len(stateSpaceDims) == 1 and stateSpaceDims[0] == 3:
            basis = "qt"
        else: basis = "gm"

    return basis_build_explicit_model(stateSpaceLabels,
                  _Basis(basis, stateSpaceDims),
                  opLabels, opExpressions,
                  prepLabels, prepExpressions,
                  effectLabels, effectExpressions,
                  povmLabels, parameterization=parameterization)

def build_explicit_alias_model(mdl_primitives, alias_dict):
    """
    Creates a new model by composing the gates of an existing `Model`,
    `mdl_primitives`, according to a dictionary of `Circuit`s, `alias_dict`.
    The keys of `alias_dict` are the operation labels of the returned `Model`.
    SPAM vectors are unaltered, and simply copied from `mdl_primitives`.

    Parameters
    ----------
    mdl_primitives : Model
        A Model containing the "primitive" gates (those used to compose
        the gates of the returned model).
    
    alias_dict : dictionary
        A dictionary whose keys are strings and values are Circuit objects
        specifying sequences of primitive gates.  Each key,value pair specifies
        the composition rule for a creating a gate in the returned model.
    
    Returns
    -------
    Model
        A model whose gates are compositions of primitive gates and whose
        spam operations are the same as those of `mdl_primitives`.
    """
    mdl_new = mdl_primitives.copy()
    for gl in mdl_primitives.operations.keys():
        del mdl_new.operations[gl] #remove all gates from mdl_new

    for gl,opstr in alias_dict.items():
        mdl_new.operations[gl] = mdl_primitives.product(opstr)
          #Creates fully parameterized gates by default...
    return mdl_new


def build_standard_localnoise_model(nQubits, gate_names, nonstd_gate_unitaries={}, availability={}, 
                                    qubit_labels=None, geometry="line", parameterization='static',
                                    evotype="auto", sim_type="auto", on_construction_error='raise'):
    """
    TODO: docstring - add geometry
    Creates a "standard" n-qubit model, usually of ideal gates.

    The returned model is "standard", in that the following standard gate
    names may be specified as elements to `gate_names` without the need to
    supply their corresponding unitaries (as one must when calling
    the constructor directly):

    - 'Gi' : the 1Q idle operation
    - 'Gx','Gy','Gz' : 1Q pi/2 rotations
    - 'Gxpi','Gypi','Gzpi' : 1Q pi rotations
    - 'Gh' : Hadamard
    - 'Gp' : phase
    - 'Gcphase','Gcnot','Gswap' : standard 2Q gates

    Furthermore, if additional "non-standard" gates are needed,
    they are specified by their *unitary* gate action, even if
    the final model propagates density matrices (as opposed
    to state vectors).

    Parameters
    ----------
    nQubits : int
        The total number of qubits.

    gate_names : list
        A list of string-type gate names (e.g. `"Gx"`) either taken from
        the list of builtin "standard" gate names given above or from the
        keys of `nonstd_gate_unitaries`.  These are the typically 1- and 2-qubit
        gates that are repeatedly embedded (based on `availability`) to form
        the resulting model.

    nonstd_gate_unitaries : dict, optional 
        A dictionary of numpy arrays which specifies the unitary gate action
        of the gate names given by the dictionary's keys.

    availability : dict, optional
        A dictionary whose keys are gate names and whose values are lists of 
        qubit-label-tuples.  See constructor docstring for more details.

    parameterization : {"full", "TP", "CPTP", "H+S", "S", "static", "H+S terms",
                        "H+S clifford terms", "clifford"}
        The type of parameterizaton to use for each gate value before it is
        embedded. See :method:`Model.set_all_parameterizations` for more
        details.

    evotype : {"auto","densitymx","statevec","stabilizer","svterm","cterm"}
        The evolution type.  Often this is determined by the choice of 
        `parameterization` and can be left as `"auto"`, which prefers
        `"densitymx"` (full density matrix evolution) when possible. In some
        cases, however, you may want to specify this manually.  For instance,
        if you give unitary maps instead of superoperators in `gatedict`
        you'll want to set this to `"statevec"`.

    sim_type : {"auto", "matrix", "map", "termorder:<N>"} 
        The simulation method used to compute predicted probabilities for the
        resulting :class:`Model`.  Usually `"auto"` is fine, the default for
        each `evotype` is usually what you want.  Setting this to something
        else is expert-level tuning.

    on_construction_error : {'raise','warn',ignore'}
        What to do when the creation of a gate with the given 
        `parameterization` fails.  Usually you'll want to `"raise"` the error.
        In some cases, for example when converting as many gates as you can
        into `parameterization="clifford"` gates, `"warn"` or even `"ignore"`
        may be useful.

    Returns
    -------
    Model
        A model with `"rho0"` prep, `"Mdefault"` POVM, and gates labeled by
        gate name (keys of `gatedict`) and qubit labels (from within
        `availability`).  For instance, the operation label for the `"Gx"` gate on
        qubit 2 might be `Label("Gx",1)`.
    """
    return _LocalNoiseModel.build_standard(nQubits, gate_names, nonstd_gate_unitaries, availability,
                                           qubit_labels, geometry, parameterization, evotype,
                                           sim_type, on_construction_error, independent_gates=False,
                                           ensure_composed_gates=False)


###SCRATCH
# Old from embed_operation:
#        for op_i in range(opmx.shape[0]):     # rows ~ "output" of the gate map
#            for op_j in range(opmx.shape[1]): # cols ~ "input"  of the gate map
#                op_b1_ket, op_b2_bra = decomp_op_index(op_i) # op_b* are lists of state indices, one index per
#                op_b2_ket, op_b2_bra = decomp_op_index(op_j) #  tensor product component that the gate operates on (2 components for a 2-qubit gate)
#
#                for i,b_noop in enumerate(tensorBlkBasis_noop): #loop over all state configurations we don't operate on - so really a loop over diagonal dm elements
#
#                    out_ket = insert_op_basis(op_b1_ket, b_noop)  # using same b_noop for ket & bra says we're acting
#                    out_bra = insert_op_basis(op_b1_bra, b_noop)  #  as the identity on the no-op state space
#                    out_blkBasis_i = lookup_blkBasisIndex[ tuple(out_ket) ] # row index of ket within tensor block basis (state space basis)
#                    out_blkBasis_j = lookup_blkBasisIndex[ tuple(out_bra) ] # col index of ket within tensor block basis (state space basis)
#                    out_vec_index = N*out_blkBasis_i + out_blkBasis_j  # index of (row,col) tensor block element (vectorized row,col)
#
#                    in_ket = insert_op_basis(op_b2_ket, b_noop)  # using same b_noop for ket & bra says we're acting
#                    in_bra = insert_op_basis(op_b2_bra, b_noop)  #  as the identity on the no-op state space
#                    in_blkBasis_i = lookup_blkBasisIndex[ tuple(in_ket) ] # row index of ket within tensor block basis (state space basis)
#                    in_blkBasis_j = lookup_blkBasisIndex[ tuple(in_bra) ] # col index of ket within tensor block basis (state space basis)
#                    in_vec_index = N*in_blkBasis_i + in_blkBasis_j  # index of (row,col) tensor block element (vectorized row,col)
#
#                    opBlk[ out_vec_index, in_vec_index ] = opmx[ op_i, op_j ]