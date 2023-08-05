#
# This file is part of TransportMaps.
#
# TransportMaps is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TransportMaps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with TransportMaps.  If not, see <http://www.gnu.org/licenses/>.
#
# Transport Maps Library
# Copyright (C) 2015-2018 Massachusetts Institute of Technology
# Uncertainty Quantification group
# Department of Aeronautics and Astronautics
#
# Author: Transport Map Team
# Website: transportmaps.mit.edu
# Support: transportmaps.mit.edu/qa/
#

import logging
import dill
import numpy as np
import numpy.linalg as npla
import scipy.optimize as sciopt

from TransportMaps import get_mpi_pool, mpi_map, mpi_map_alloc_dmem, mpi_alloc_dmem
from TransportMaps.Distributions.TransportMapDistributions import \
    PullBackTransportMapDistribution, PushForwardTransportMapDistribution
from TransportMaps.Functionals.MonotonicFunctionApproximations import \
    MonotonicIntegratedExponentialApproximation, \
    MonotonicIntegratedSquaredApproximation, \
    MonotonicLinearSpanApproximation
from TransportMaps.Functionals.LinearSpanApproximationBase import \
    LinearSpanApproximation

from TransportMaps.Maps.TriangularTransportMapBase import *

__all__ = ['IntegratedExponentialTriangularTransportMap',
           'CommonBasisIntegratedExponentialTriangularTransportMap',
           'IntegratedSquaredTriangularTransportMap',
           'LinearSpanTriangularTransportMap',
           'CommonBasisLinearSpanTriangularTransportMap',
           'MonotonicLinearSpanTriangularTransportMap',
           'MonotonicCommonBasisLinearSpanTriangularTransportMap']

nax = np.newaxis

class IntegratedExponentialTriangularTransportMap(MonotonicTriangularTransportMap):
    r""" Triangular transport map where each component is represented by an :class:`IntegratedExponential<TransportMaps.MonotonicApproximation.IntegratedExponential>` function.

    Args:
       active_vars (:class:`list<list>` [:math:`d`] of :class:`list<list>`): for
         each dimension lists the active variables.
       approx_list (:class:`list<list>` [:math:`d`] of :class:`FunctionalApproximations.MonotonicFunctionApproximation`):
         list of monotonic functional approximations for each dimension
       full_c_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of the constant part of each component for a full triangular map
         (this is needed for some adaptivity algorithm)
       full_h_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of the constant part of each component for a full triangular map
         (this is needed for some adaptivity algorithm)
    """
    def __init__(self, active_vars, approx_list,
                 full_c_basis_list=None, full_h_basis_list=None):
        super(IntegratedExponentialTriangularTransportMap,
              self).__init__(active_vars, approx_list)
        self.full_c_basis_list = full_c_basis_list
        self.full_h_basis_list = full_h_basis_list
        if not all( [ isinstance(a, MonotonicIntegratedExponentialApproximation)
                      for a in approx_list ] ):
            raise ValueError("All the approximation functions must be instances " +
                             "of the class MonotonicIntegratedExponentialApproximation")

    def get_identity_coeffs(self):
        r""" Returns the coefficients corresponding to the identity map

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`N`]): coefficients
        """
        return np.zeros( self.n_coeffs )

    def get_default_init_values_minimize_kl_divergence(self):
        return self.get_identity_coeffs()

class IntegratedSquaredTriangularTransportMap(MonotonicTriangularTransportMap):
    r""" Triangular transport map where each component is represented by an :class:`IntegratedSquaredLinearSpanApproximation` function.

    Args:
       active_vars (:class:`list<list>` [:math:`d`] of :class:`list<list>`): for
         each dimension lists the active variables.
       approx_list (:class:`list<list>` [:math:`d`] of :class:`FunctionalApproximations.MonotonicFunctionApproximation`):
         list of monotonic functional approximations for each dimension
       full_c_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of the constant part of each component for a full triangular map
         (this is needed for some adaptivity algorithm)
       full_h_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of the constant part of each component for a full triangular map
         (this is needed for some adaptivity algorithm)
    """
    def __init__(self, active_vars, approx_list,
                 full_c_basis_list=None, full_h_basis_list=None):
        super(IntegratedSquaredTriangularTransportMap,
              self).__init__(active_vars, approx_list)
        self.full_c_basis_list = full_c_basis_list
        self.full_h_basis_list = full_h_basis_list
        if not all( [ isinstance(a, MonotonicIntegratedSquaredApproximation)
                      for a in approx_list ] ):
            raise ValueError("All the approximation functions must be instances " +
                             "of the class MonotonicIntegratedSquaredApproximation")

    def get_identity_coeffs(self):
        r""" Returns the coefficients corresponding to the identity map

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`N`]): coefficients
        """
        # Define the identity map
        coeffs = []
        for a in self.approx_list:
            coeffs.append( np.zeros(a.c.n_coeffs) )
            ch = np.zeros(a.h.n_coeffs)
            idx = next(i for i,x in enumerate(a.h.multi_idxs) if x == tuple([0]*a.h.dim))
            ch[idx] = 1.
            coeffs.append(ch)
        return np.hstack(coeffs)

    def get_default_init_values_minimize_kl_divergence(self):
        return self.get_identity_coeffs()
                                
class LinearSpanTriangularTransportMap(TriangularTransportMap):
    r""" Triangular transport map where each component is represented by an :class:`FunctionalApproximations.LinearSpanApproximation` function.

    Args:
       active_vars (:class:`list<list>` [:math:`d`] of :class:`list<list>`): for
         each dimension lists the active variables.
       approx_list (:class:`list<list>` [:math:`d`] of :class:`FunctionalApproximations.LinearSpanApproximation`):
         list of functional approximations for each dimension
       full_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of each component for a full triangular map
         (this is needed for some adaptivity algorithm)
    """
    def __init__(self, active_vars, approx_list, full_basis_list=None):
        self.set_logger()
        if not all( [ isinstance(a, LinearSpanApproximation)
                      for a in approx_list ] ):
            raise ValueError("All the approximation functions must be instances " +
                             "of the class LinearSpanApproximation")
        super(LinearSpanTriangularTransportMap,
              self).__init__(active_vars, approx_list)
        self.full_basis_list = full_basis_list

    def minimize_kl_divergence_complete(self, *args, **kwargs):
        raise NotImplementedError("This function is not implemented for non-monotonic maps")

class MonotonicLinearSpanTriangularTransportMap(LinearSpanTriangularTransportMap,
                                                MonotonicTriangularTransportMap):
    r""" Triangular transport map where each component is represented by an :class:`FunctionalApproximations.MonotonicLinearSpanApproximation` function.

    Args:
       active_vars (:class:`list<list>` [:math:`d`] of :class:`list<list>`): for
         each dimension lists the active variables.
       approx_list (:class:`list<list>` [:math:`d`] of :class:`FunctionalApproximations.MonotonicLinearSpanApproximation`):
         list of monotonic functional approximations for each dimension
       full_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of each component for a full triangular map
         (this is needed for some adaptivity algorithm)
    """
    def __init__(self, active_vars, approx_list, full_basis_list=None):
        self.set_logger()
        if not all( [ isinstance(a, MonotonicLinearSpanApproximation)
                      for a in approx_list ] ):
            raise ValueError("All the approximation functions must be instances " +
                             "of the class MonotonicLinearSpanApproximation")
        super(MonotonicLinearSpanTriangularTransportMap,
              self).__init__(active_vars, approx_list)
        self.full_basis_list = full_basis_list
    
    def minimize_kl_divergence_complete(self, d1, d2,
                                        x=None, w=None,
                                        params_d1=None, params_d2=None,
                                        x0=None,
                                        regularization=None,
                                        tol=1e-4, maxit=100, ders=1,
                                        fungrad=False, hessact=False,
                                        precomp_type='uni',
                                        batch_size=None,
                                        mpi_pool=None,
                                        grad_check=False, hess_check=False):
        r""" Compute: :math:`{\bf a}^* = \arg\min_{\bf a}\mathcal{D}_{KL}\left(\pi_1, \pi_{2,{\bf a}}\right)`

        Args:
          d1 (Distribution): distribution :math:`\pi_1`
          d2 (Distribution): distribution :math:`\pi_2`
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): quadrature points
          w (:class:`ndarray<numpy.ndarray>` [:math:`m`]): quadrature weights
          params_d1 (dict): parameters for distribution :math:`\pi_1`
          params_d2 (dict): parameters for distribution :math:`\pi_2`
          x0 (:class:`ndarray<numpy.ndarray>` [:math:`N`]): coefficients to be used
            as initial values for the optimization
          regularization (dict): defines the regularization to be used.
            If ``None``, no regularization is applied.
            If key ``type=='L2'`` then applies Tikonhov regularization with
            coefficient in key ``alpha``.
          tol (float): tolerance to be used to solve the KL-divergence problem.
          maxit (int): maximum number of iterations
          ders (int): order of derivatives available for the solution of the
            optimization problem. 0 -> derivative free (SLSQP), 1 -> gradient (SLSQP).
          fungrad (bool): whether the target distribution provides the method
            :func:`Distribution.tuple_grad_x_log_pdf` computing the evaluation and the
            gradient in one step. This is used only for ``ders==1``.
          hessact (bool): this option is disabled for linear span maps (no Hessian used)
          precomp_type (str): whether to precompute univariate Vandermonde matrices 'uni' or
            multivariate Vandermonde matrices 'multi'
          batch_size (:class:`list<list>` [2] of :class:`int<int>`): the list contains the
            size of the batch to be used for each iteration. A size ``1`` correspond
            to a completely non-vectorized evaluation. A size ``None`` correspond to a
            completely vectorized one.
            If the target distribution is a :class:`ProductDistribution`, then
            the optimization problem decouples and
            ``batch_size`` is a list of lists containing the batch sizes to be
            used for each component of the map.
          mpi_pool (:class:`mpi_map.MPI_Pool` or :class:`list<list>` of ``mpi_pool``):
            pool of processes to be used, ``None`` stands for one process.
            If the target distribution is a :class:`ProductDistribution`, then
            the minimization problem decouples and ``mpi_pool`` is a list containing
            ``mpi_pool``s for each component of the map.
          grad_check (bool): whether to use finite difference to check the correctness of
            of the gradient
          hess_check (bool): whether to use finite difference to check the correctenss of
            the Hessian

        Returns:
          log (dict): log informations from the solver

        .. note:: The parameters ``(qtype,qparams)`` and ``(x,w)`` are mutually
          exclusive, but one pair of them is necessary.
        """
        if ders < 0:
            self.logger.warning("Value for ders too low (%d). Set to 0." % ders)
            ders = 0
        if ders > 1:
            self.logger.warning("Value for ders too high (%d). Set to 1." % ders)
            ders = 1
        
        self.logger.debug("minimize_kl_divergence(): Precomputation started")

        if batch_size is None:
            batch_size = [None] * 2

        # Distribute objects
        d2_distr = dill.loads( dill.dumps(d2) )
        d2_distr.reset_counters() # Reset counters on copy to avoid couting twice
        mpi_alloc_dmem(d2=d2_distr, mpi_pool=mpi_pool)
        # Link tm to d2.transport_map
        def link_tm_d2(d2):
            return (d2.transport_map,)
        (tm,) = mpi_map_alloc_dmem(
            link_tm_d2, dmem_key_in_list=['d2'], dmem_arg_in_list=['d2'],
            dmem_val_in_list=[d2], dmem_key_out_list=['tm'],
            mpi_pool=mpi_pool)
            
        if isinstance(d2, PullBackTransportMapDistribution):
            # Init memory
            params2 = {
                'params_pi': params_d2,
                'params_t': {'components': [{} for i in range(self.dim)]} }
            mpi_alloc_dmem(params2=params2, mpi_pool=mpi_pool)
            
            # precomp_minimize_kl_divergence
            bcast_tuple = (['precomp_type'],[precomp_type])
            mpi_map("precomp_minimize_kl_divergence",
                    bcast_tuple=bcast_tuple,
                    dmem_key_in_list=['params2', 'x'],
                    dmem_arg_in_list=['params', 'x'],
                    dmem_val_in_list=[params2, x],
                    obj='tm', obj_val=tm,
                    mpi_pool=mpi_pool, concatenate=False)
            # allocate_cache_minimize_kl_divergence
            (cache, ) = mpi_map_alloc_dmem(
                "allocate_cache_minimize_kl_divergence",
                dmem_key_in_list=['x'],
                dmem_arg_in_list=['x'],
                dmem_val_in_list=[x],
                dmem_key_out_list=['cache'],
                obj='tm', obj_val=tm,
                mpi_pool=mpi_pool, concatenate=False)
        elif isinstance(d2, PushForwardTransportMapDistribution):
            # Init memory
            params2 = { 'params_pi': params_d2,
                        'params_t': {} }
            mpi_alloc_dmem(params2=params2, mpi_pool=mpi_pool)
            # allocate cache
            (cache, ) = mpi_map_alloc_dmem(
                "allocate_cache_minimize_kl_divergence",
                dmem_key_in_list=['x'],
                dmem_arg_in_list=['x'],
                dmem_val_in_list=[x],
                dmem_key_out_list=['cache'],
                obj='tm', obj_val=tm,
                mpi_pool=mpi_pool, concatenate=False)
        else:
            raise AttributeError("Not recognized distribution type")
        # Append the slices indices
        if self.logger.getEffectiveLevel() <= logging.DEBUG:
            self.logger.debug("minimize_kl_divergence(): Precomputation ended")
        params = {}
        params['nobj'] = 0
        params['nda_obj'] = 0
        params['nda2_obj'] = 0
        params['nda2_obj_dot'] = 0
        params['x'] = x
        params['w'] = w
        params['d1'] = d1
        params['d2'] = d2
        params['params1'] = params_d1
        params['params2'] = params2
        params['cache'] = cache
        params['batch_size'] = batch_size
        params['regularization'] = regularization
        params['grad_check'] = grad_check
        params['hess_check'] = hess_check
        params['mpi_pool'] = mpi_pool

        # Link params_t on the first level of params
        # (this is needed for the MPI implementation of the constraints)
        def link_params_t(params):
            return (params['params_t'],)
        (params['params_t'],) = mpi_map_alloc_dmem(
            link_params_t,
            dmem_key_in_list = ['params2'],
            dmem_arg_in_list = ['params'],
            dmem_val_in_list = [params2],
            dmem_key_out_list = ['params_t'],
            mpi_pool=mpi_pool)

        cons = ({'type': 'ineq',
                 'fun': self.minimize_kl_divergence_constraints,
                 'jac': self.minimize_kl_divergence_da_constraints,
                 'args': (params,)})

        if x0 is None:
            x0 = self.get_default_init_values_minimize_kl_divergence()
            
        params['objective_cache_coeffs'] = x0 - 1.

        # Callback variables
        self.it_callback = 0
        self.ders_callback = ders
        self.params2_callback = params2

        # Options for optimizer
        options = {'maxiter': maxit,
                   'disp': False}

        # Solve
        if ders == 0:
            res = sciopt.minimize(self.minimize_kl_divergence_objective,
                                  args=params,
                                  x0=x0,
                                  constraints=cons,
                                  method='SLSQP',
                                  tol=tol, 
                                  options=options,
                                  callback=self.minimize_kl_divergence_callback)
        elif ders == 1:
            if fungrad:
                res = sciopt.minimize(self.minimize_kl_divergence_tuple_grad_a_objective,
                                      args=params, x0=x0,
                                      jac=True,
                                      constraints=cons,
                                      method='SLSQP',
                                      tol=tol, 
                                      options=options,
                                      callback=self.minimize_kl_divergence_callback)
            else:
                res = sciopt.minimize(self.minimize_kl_divergence_objective, args=params,
                                      x0=x0,
                                      jac=self.minimize_kl_divergence_grad_a_objective,
                                      constraints=cons,
                                      method='SLSQP',
                                      tol=tol, 
                                      options=options,
                                      callback=self.minimize_kl_divergence_callback)

        # Clean up callback stuff
        del self.it_callback
        del self.ders_callback
        del self.params2_callback

        # Get d2 from children processes and update counters
        if mpi_pool is not None:
            d2_child_list = mpi_pool.get_dmem('d2')
            d2.update_ncalls_tree( d2_child_list[0][0] )
            for (d2_child,) in d2_child_list:
                d2.update_nevals_tree(d2_child)
                d2.update_teval_tree(d2_child)

        # Log
        log = {}
        log['success'] = res['success']
        log['message'] = res['message']
        log['fval'] = res['fun']
        log['nit'] = res['nit']
        log['n_fun_ev'] = params['nobj']
        if ders >= 1:
            log['n_jac_ev'] = params['nda_obj']
            log['jac'] = res['jac']

        # Attach cache to log
        if mpi_pool is None:
            log['cache'] = cache
        else:
            log['cache'] = mpi_pool.get_dmem('cache')
        
        # Display stats
        if log['success']:
            self.logger.info("minimize_kl_divergence: Optimization terminated successfully")
        else:
            self.logger.warn("minimize_kl_divergence: Minimization of KL-divergence failed.")
            self.logger.warn("minimize_kl_divergence: Message: %s" % log['message'])
        self.logger.info("minimize_kl_divergence:   Function value:          %6f" % log['fval'])
        if ders >= 1:
            self.logger.info("minimize_kl_divergence:   Norm of the Jacobian:    %6f" % npla.norm(log['jac']))
        self.logger.info("minimize_kl_divergence:   Number of iterations:    %6d" % log['nit'])
        self.logger.info("minimize_kl_divergence:   N. function evaluations: %6d" % log['n_fun_ev'])
        if ders >= 1:
            self.logger.info("minimize_kl_divergence:   N. Jacobian evaluations: %6d" % log['n_jac_ev'])

        # Clear mpi_pool and detach object
        if mpi_pool is not None:
            mpi_pool.clear_dmem()
            
        # Set coefficients
        d2.coeffs = res['x'] 
        return log

    def get_identity_coeffs(self):
        r""" Returns the coefficients corresponding to the identity map

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`N`]): coefficients
        """
        # Define the identity map
        coeffs = []
        for a in self.approx_list:
            cc = np.zeros(a.n_coeffs)
            idx = next(i for i,x in enumerate(a.multi_idxs)
                       if x == tuple([0]*(a.dim-1)+[1]))
            cc[idx] = 1.
            coeffs.append(cc)
        return np.hstack(coeffs)

    def get_default_init_values_minimize_kl_divergence(self):
        return self.get_identity_coeffs()

    def minimize_kl_divergence_constraints(self, a, params):
        mpi_pool = params['mpi_pool']
        # Update distribution coefficients
        bcast_tuple = (['coeffs'],[a])
        mpi_map("_set_coeffs", bcast_tuple=bcast_tuple,
                obj='tm', obj_val=self,
                mpi_pool=mpi_pool, concatenate=False)
        # Evaluate
        x = params['x']
        dmem_key_in_list = ['params_t', 'x']
        dmem_arg_in_list = ['precomp', 'x']
        dmem_val_in_list = [ params['params_t'], x ]
        out = mpi_map("partial_xd", 
                      dmem_key_in_list=dmem_key_in_list,
                      dmem_arg_in_list=dmem_arg_in_list,
                      dmem_val_in_list=dmem_val_in_list,
                      obj='tm', obj_val=self,
                      mpi_pool=mpi_pool)
        return out.reshape( out.shape[0] * out.shape[1] )

    def minimize_kl_divergence_da_constraints(self, a, params):
        mpi_pool = params['mpi_pool']
        # Update distribution coefficients
        bcast_tuple = (['coeffs'],[a])
        mpi_map("_set_coeffs", bcast_tuple=bcast_tuple,
                obj='tm', obj_val=self,
                mpi_pool=mpi_pool, concatenate=False)
        # Evaluate
        x = params['x']
        dmem_key_in_list = ['params_t', 'x']
        dmem_arg_in_list = ['precomp', 'x']
        dmem_val_in_list = [ params['params_t'], x ]
        out = mpi_map("grad_a_partial_xd", 
                      dmem_key_in_list=dmem_key_in_list,
                      dmem_arg_in_list=dmem_arg_in_list,
                      dmem_val_in_list=dmem_val_in_list,
                      obj='tm', obj_val=self,
                      mpi_pool=mpi_pool)
        return out.reshape( (out.shape[0]*out.shape[1], self.n_coeffs) )

class CommonBasisLinearSpanTriangularTransportMap(LinearSpanTriangularTransportMap):
    r""" Triangular transport map :math:`T` where the beases of each component :math:`T_i` are the same for corresponding dimensions.

    The advantage of using this class with respect to
    :class:`LinearSpanTriangularTransportMap` is that the Vandermonde matrices necessary
    for the evaluation are shared among every component :math:`T_i`.
    
    Args:
       active_vars (:class:`list<list>` [:math:`d`] of :class:`list<list>`): for
         each dimension lists the active variables.
       approx_list (:class:`list<list>` [:math:`d`] of :class:`FunctionalApproximations.LinearSpanApproximation`):
         list of functional approximations for each dimension
       full_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of each component for a full triangular map
         (this is needed for some adaptivity algorithm)

    .. seealso:: :class:`LinearSpanTriangularTransportMap`
    """

    def __init__(self, active_vars, approx_list, full_basis_list=None):
        # Super class constructor
        super(CommonBasisLinearSpanTriangularTransportMap,
              self).__init__(active_vars, approx_list)
        self.full_basis_list = full_basis_list
        # Checks
        self.basis_list = [None for i in range(self.dim)]
        for a,avars in zip(self.approx_list, self.active_vars):
            for b, avar in zip(a.basis_list,avars):
                if self.basis_list[avar] is None:
                    self.basis_list[avar] = b
                if not( self.basis_list[avar] is b ):
                    raise ValueError("Fixed a dimension, all the basis for " +
                                     "this dimension must be of the same object " +
                                     "for all T_i")
        # Init
        self.max_orders = np.zeros(self.dim, dtype=int)
        for a,avar in zip(self.approx_list, self.active_vars):
            a_max_ord = a.get_directional_orders()
            idxs = tuple( np.where( self.max_orders[avar] < a_max_ord )[0] )
            for i in idxs: self.max_orders[avar[i]] = a_max_ord[i]

    def precomp_evaluate(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`T({\bf x},{\bf a})`

        This returns a list of uni-variate Vandermonde matrices with order maximum among the components :math:`T_i`.

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        to_compute_flag = False
        for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
            try: tmp = p['V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            vand = [ b.GradVandermonde(x[:,i], int(o)) for i,(o,b) in
                     enumerate(zip(self.max_orders,self.basis_list)) ]
            for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
                # Vandermonde matrices
                p['V_list'] = [ vand[var] for var in avar ]
        return precomp

    def precomp_grad_x(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla_{\bf x}T({\bf x},{\bf a})`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
            :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # precomp_evaluate part
        self.precomp_evaluate(x, precomp)
        # precomp_grad_x part
        to_compute_flag = False
        for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
            try: tmp = p['partial_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            vand = [ b.GradVandermonde(x[:,i], int(o), k=1) for i,(o,b) in
                     enumerate(zip(self.max_orders,self.basis_list)) ]
            for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
                p['partial_x_V_list'] = [ vand[var] for var in avar ]
        return precomp

    def precomp_hess_x(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla^2_{\bf x}T({\bf x},{\bf a})`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # precomp_evaluate and precomp_grad_x parts
        self.precomp_evaluate(x, precomp)
        self.precomp_grad_x(x, precomp)
        # precomp_hess_x part
        to_compute_flag = False
        for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
            try: tmp = p['partial2_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            vand = [ b.GradVandermonde(x[:,i], int(o), k=2) for i,(o,b) in
                     enumerate(zip(self.max_orders,self.basis_list)) ]
            for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
                p['partial2_x_V_list'] = [ vand[var] for var in avar ]
        return precomp

    def precomp_nabla3_x(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla^3_{\bf x}T({\bf x},{\bf a})`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # precomp_evaluate precomp_grad_x precomp_hess_x parts
        self.precomp_evaluate(x, precomp)
        self.precomp_grad_x(x, precomp)
        self.precomp_hess_x(x, precomp)
        # precomp_nabla3_x
        to_compute_flag = False
        for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
            try: tmp = p['partial3_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            vand = [ b.GradVandermonde(x[:,i], int(o), k=3) for i,(o,b) in
                     enumerate(zip(self.max_orders, self.basis_list)) ]
            for i,(avar,p) in enumerate(zip(self.active_vars, precomp['components'])):
                p['partial3_x_V_list'] = [ vand[var] for var in avar ]
        return precomp

    def precomp_partial_xd(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\partial_{x_k}T_k({\bf x},{\bf a})` for :math:`k=1,\ldots,d`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # precomp_evaluate and precomp_grad_x parts
        self.precomp_evaluate(x, precomp)
        self.precomp_grad_x(x, precomp)
        # Generate partial_xd_V_last fields
        for p in precomp['components']:
            p['partial_xd_V_last'] = p['partial_x_V_list'][-1]
        return precomp

    def precomp_grad_x_partial_xd(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla_{\bf x}\partial_{x_k}T_k({\bf x},{\bf a})` for :math:`k=1,\ldots,d`

        Enriches the dictionaries in the ``precomp`` list if necessary.
        
        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`dict<dict>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # precomp_evaluate, precomp_grad_x and precomp_hess_x parts
        self.precomp_evaluate(x, precomp)
        self.precomp_grad_x(x, precomp)
        self.precomp_hess_x(x, precomp)
        # Generate partial2_xd_V_last fields
        for p in precomp['components']:
            p['partial2_xd_V_last'] = p['partial2_x_V_list'][-1]
        return precomp

    def precomp_hess_x_partial_xd(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla^2_{\bf x}\partial_{x_k}T_k({\bf x},{\bf a})` for :math:`k=1,\ldots,d`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`dict<dict>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # precomp_evaluate, precomp_grad_x, precomp_hess_x, precomp_nabla3_x parts
        self.precomp_evaluate(x, precomp)
        self.precomp_grad_x(x, precomp)
        self.precomp_hess_x(x, precomp)
        self.precomp_nabla3_x(x, precomp)
        # Generate partial3_xd_V_last fields
        for p in precomp['components']:
            p['partial3_xd_V_last'] = p['partial3_x_V_list'][-1]
        return precomp

class MonotonicCommonBasisLinearSpanTriangularTransportMap(
        CommonBasisLinearSpanTriangularTransportMap,
        MonotonicLinearSpanTriangularTransportMap):
    r""" Triangular transport map :math:`T` where the beases of each component :math:`T_i` are the same for corresponding dimensions.

    The advantage of using this class with respect to :class:`LinearSpanTriangularTransportMap` is that the Vandermonde matrices necessary for the evaluation are shared among every component :math:`T_i`.
    
    Args:
       active_vars (:class:`list<list>` [:math:`d`] of :class:`list<list>`): for
         each dimension lists the active variables.
       approx_list (:class:`list<list>` [:math:`d`] of :class:`FunctionalApproximations.MonotonicLinearSpanApproximation`):
         list of monotonic functional approximations for each dimension
       full_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of each component for a full triangular map
         (this is needed for some adaptivity algorithm)

    .. seealso:: :class:`LinearSpanTriangularTransportMap`
    """
    def __init__(self, active_vars, approx_list, full_basis_list=None):
        super(MonotonicCommonBasisLinearSpanTriangularTransportMap,
              self).__init__( active_vars, approx_list, full_basis_list )
        
class CommonBasisIntegratedExponentialTriangularTransportMap(
        IntegratedExponentialTriangularTransportMap):
    r""" Triangular transport map :math:`T` where the beases of each component :math:`T_i` are the same for corresponding dimensions.

    The advantage of using this class with respect to :class:`IntegratedExponentialTriangularTransportMap` is that the Vandermonde matrices necessary for the evaluation are shared among every component :math:`T_i`.

    Args:
       active_vars (:class:`list<list>` [:math:`d`] of :class:`list<list>`): for
         each dimension lists the active variables.
       approx_list (:class:`list<list>` [:math:`d`] of :class:`FunctionalApproximations.LinearSpanApproximation`):
         list of monotonic functional approximations for each dimension
       full_c_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of the constant part of each component for a full triangular map
         (this is needed for some adaptivity algorithm)
       full_h_basis_list (:class:`list` of :class:`list`): list of basis for each input
         of the constant part of each component for a full triangular map
         (this is needed for some adaptivity algorithm)

    .. seealso:: :class:`IntegratedExponentialTriangularTransportMap`
    """

    def __init__(self, active_vars, approx_list,
                 full_c_basis_list=None, full_h_basis_list=None):
        # Super class constructor
        super(CommonBasisIntegratedExponentialTriangularTransportMap,
              self).__init__(active_vars, approx_list)
        self.full_c_basis_list = full_c_basis_list
        self.full_h_basis_list = full_h_basis_list
        # Checks
        self.const_basis_list = [None for i in range(self.dim)]
        self.exp_basis_list = [None for i in range(self.dim)]
        for a,avars in zip(self.approx_list, self.active_vars):
            const_approx = a.c
            exp_approx = a.h
            for const_basis, exp_basis, avar in zip(const_approx.basis_list,
                                                    exp_approx.basis_list, avars):
                if self.const_basis_list[avar] is None:
                    self.const_basis_list[avar] = const_basis
                if self.exp_basis_list[avar] is None:
                    self.exp_basis_list[avar] = exp_basis
                if ( not( self.const_basis_list[avar] is const_basis ) or
                     not( self.exp_basis_list[avar] is exp_basis ) ):
                    raise ValueError("Fixed a dimension, all the basis for " +
                                     "this dimension must be of the same object " +
                                     "for all T_i")
        # Init
        self.const_max_orders = np.zeros(self.dim, dtype=int)
        self.exp_max_orders = np.zeros(self.dim, dtype=int)
        for a,avar in zip(self.approx_list, self.active_vars):
            const_approx = a.c
            const_max_ord = const_approx.get_directional_orders()
            const_idxs = tuple( np.where( self.const_max_orders[avar] < const_max_ord )[0] )
            for i in const_idxs: self.const_max_orders[avar[i]] = const_max_ord[i]
            exp_approx = a.h
            exp_max_ord = exp_approx.get_directional_orders()
            exp_idxs = tuple( np.where( self.exp_max_orders[avar] < exp_max_ord )[0] )
            for i in exp_idxs: self.exp_max_orders[avar[i]] = exp_max_ord[i]

    def minimize_kl_divergence(self, d1, d2,
                               qtype=None, qparams=None,
                               x=None, w=None,
                               params_d1=None, params_d2=None,
                               x0=None,
                               regularization=None,
                               tol=1e-4, maxit=100, ders=2,
                               fungrad=False, hessact=False,
                               precomp_type='uni',
                               batch_size=[None,None,None],
                               mpi_pool=None,
                               grad_check=False, hess_check=False):
        r""" Compute: :math:`{\bf a}^* = \arg\min_{\bf a}\mathcal{D}_{KL}\left(\pi_1, \pi_{2,{\bf a}}\right)`

        Args:
          d1 (Distribution): distribution :math:`\pi_1`
          d2 (Distribution): distribution :math:`\pi_2`
          qtype (int): quadrature type number provided by :math:`\pi`
          qparams (object): inputs necessary to the generation of the selected
            quadrature
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): quadrature points
          w (:class:`ndarray<numpy.ndarray>` [:math:`m`]): quadrature weights
          params_d1 (dict): parameters for distribution :math:`\pi_1`
          params_d2 (dict): parameters for distribution :math:`\pi_2`
          x0 (:class:`ndarray<numpy.ndarray>` [:math:`N`]): coefficients to be used
            as initial values for the optimization
          regularization (dict): defines the regularization to be used.
            If ``None``, no regularization is applied.
            If key ``type=='L2'`` then applies Tikonhov regularization with
            coefficient in key ``alpha``.
          tol (float): tolerance to be used to solve the KL-divergence problem.
          maxit (int): maximum number of iterations
          ders (int): order of derivatives available for the solution of the
            optimization problem. 0 -> derivative free, 1 -> gradient, 2 -> hessian.
          fungrad (bool): whether the target distribution provides the method
            :func:`Distribution.tuple_grad_x_log_pdf` computing the evaluation and the
            gradient in one step. This is used only for ``ders==1``.
          hessact (bool): use the action of the Hessian. The target distribution must
            implement the function :func:`Distribution.action_hess_x_log_pdf`.
          precomp_type (str): whether to precompute univariate Vandermonde matrices 'uni' or
            multivariate Vandermonde matrices 'multi'
          batch_size (:class:`list<list>` [3 or 2] of :class:`int<int>`): the list contains the
            size of the batch to be used for each iteration. A size ``1`` correspond
            to a completely non-vectorized evaluation. A size ``None`` correspond to a
            completely vectorized one.
          mpi_pool (:class:`mpi_map.MPI_Pool`): pool of processes to be used
          grad_check (bool): whether to use finite difference to check the correctness of
            of the gradient
          hess_check (bool): whether to use finite difference to check the correctenss of
            the Hessian

        Returns:
          log (dict): log informations from the solver

        .. note:: The parameters ``(qtype,qparams)`` and ``(x,w)`` are mutually
          exclusive, but one pair of them is necessary.
        """
        return super(CommonBasisIntegratedExponentialTriangularTransportMap,
                     self).minimize_kl_divergence(
                         d1, d2, qtype=qtype, qparams=qparams, x=x, w=w,
                         params_d1=params_d1, params_d2=params_d2, x0=x0,
                         regularization=regularization,
                         tol=tol, maxit=maxit, ders=ders, fungrad=fungrad,
                         hessact=hessact,
                         batch_size=batch_size, 
                         mpi_pool=mpi_pool, 
                         grad_check=grad_check, hess_check=hess_check)
    
    def precomp_evaluate(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`T({\bf x},{\bf a})`

        This returns a list of uni-variate Vandermonde matrices with order maximum among the components :math:`T_i`.

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # Constant part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const = prec['const']
            except KeyError:
                to_compute_flag = True
                break
            try: prec_const_V_list = prec['const']['V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            const_vand = [ b.GradVandermonde(x[:,i], int(o)) for i,(o,b) in
                           enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const = prec['const']
                except KeyError: prec['const'] = {}
                # Vandermonde matrices
                try: prec_const_V_list = prec['const']['V_list']
                except KeyError:
                    prec['const']['V_list'] = [ const_vand[var] for var in avar ]
        # Integrated exponential part
        to_compute_flag = False
        for i,(approx,avar,prec) in enumerate(zip(self.approx_list, self.active_vars,
                                                  precomp['components'])):
            try: prec_intexp = prec['intexp']
            except KeyError:
                to_compute_flag = True
                break
            try:
                xjsc_list = prec['intexp']['xjsc_list']
                wjsc_list = prec['intexp']['wjsc_list']
            except KeyError:
                to_compute_flag = True
                break
            try: precomp_intexp_list = prec['intexp']['prec_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            exp_vand = [ b.GradVandermonde(x[:,i], int(o)) for i,(o,b) in
                         enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(approx,avar,prec) in enumerate(zip(self.approx_list, self.active_vars,
                                                      precomp['components'])):
                try: prec_intexp = prec['intexp']
                except KeyError: prec['intexp'] = {}
                # Generate points and weights
                try:
                    xjsc_list = prec['intexp']['xjsc_list']
                    wjsc_list = prec['intexp']['wjsc_list']
                except KeyError:
                    prec['intexp']['xjsc_list'] = []
                    prec['intexp']['wjsc_list'] = []
                    xapprox = x[:,avar]
                    xd_order = (approx.h.get_directional_orders())[-1]
                    (xj,wj) = approx.P_JAC.Quadrature( approx.integ_ord_mult * xd_order, norm=True )
                    xj = xj / 2. + 0.5  # Mapped to [0,1]
                    for idx in range(x.shape[0]):
                        wjsc = wj * xapprox[idx,-1]
                        xjsc = xj * xapprox[idx,-1]
                        xother = np.tile( xapprox[idx,:-1], (len(xjsc), 1) )
                        xeval = np.hstack( (xother, xjsc[:,nax]) )
                        # Append values
                        prec['intexp']['xjsc_list'].append( xeval )
                        prec['intexp']['wjsc_list'].append( wjsc )
                # Generate Vandermonde matrices
                try: precomp_intexp_list = prec['intexp']['prec_list']
                except KeyError: prec['intexp']['prec_list'] = [{} for i in range(x.shape[0])]
                for idx, (xeval, pp) in enumerate(zip(prec['intexp']['xjsc_list'],
                                                      prec['intexp']['prec_list'])):
                    # Vandermonde matrices
                    try: prec_intexp_V_list = pp['V_list']
                    except KeyError:
                        pp['V_list'] = [ np.tile( exp_vand[var][idx,:], (xeval.shape[0],1) )
                                         for var in avar[:-1] ]
                        pp['V_list'].append(
                            self.exp_basis_list[avar[-1]].GradVandermonde(
                                xeval[:,-1], self.exp_max_orders[avar[-1]]) )
        return precomp

    def precomp_grad_x(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla_{\bf x}T({\bf x},{\bf a})`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
            :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        # precomp_evaluate part
        precomp = self.precomp_evaluate(x, precomp, precomp_type)
        # Constant part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const_partial_x_V_list = prec['const']['partial_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            const_vand = [ b.GradVandermonde(x[:,i], int(o), k=1) for i,(o,b) in
                           enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const_partial_x_V_list = prec['const']['partial_x_V_list']
                except KeyError:
                    prec['const']['partial_x_V_list'] = [ const_vand[var] for var in avar ]
        # Integrated exponential part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            for idx, (xeval, pp) in enumerate(zip(prec['intexp']['xjsc_list'],
                                                  prec['intexp']['prec_list'])):
                try: prec_intexp_partial_x_V_list = pp['partial_x_V_list']
                except KeyError:
                    to_compute_flag = True
                    break
            if to_compute_flag: break
        if to_compute_flag:
            partial_x_exp_vand = [ b.GradVandermonde(x[:,i], int(o), k=1) for i,(o,b) in
                                   enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                # Generate Vandermonde matrices
                for idx, (xeval, pp) in enumerate(zip(prec['intexp']['xjsc_list'],
                                                      prec['intexp']['prec_list'])):
                    try: prec_intexp_partial_x_V_list = pp['partial_x_V_list']
                    except KeyError:
                        pp['partial_x_V_list'] = [
                            np.tile( partial_x_exp_vand[var][idx,:], (xeval.shape[0],1) )
                            for var in avar[:-1] ]
                        pp['partial_x_V_list'].append(
                            self.exp_basis_list[avar[-1]].GradVandermonde(
                                xeval[:,-1], self.exp_max_orders[avar[-1]], k=1) )
        # precomp_partial_xd part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_exp = prec['exp']
            except KeyError:
                to_compute_flag = True
                break
            try: prec_exp_V_list = prec['exp']['V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            exp_vand = [ b.GradVandermonde(x[:,i], int(o)) for i,(o,b) in
                         enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_exp = prec['exp']
                except KeyError: prec['exp'] = {}
                try: prec_exp_V_list = prec['exp']['V_list']
                except KeyError:
                    prec['exp']['V_list'] = [ exp_vand[var] for var in avar ]
        return precomp

    def precomp_hess_x(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla^2_{\bf x}T({\bf x},{\bf a})`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        # precomp_grad_x part (and precomp_evaluate)
        precomp = self.precomp_grad_x(x, precomp, precomp_type)
        # Constant part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const_partial2_x_V_list = prec['const']['partial2_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            const_vand = [ b.GradVandermonde(x[:,i], int(o), k=2) for i,(o,b) in
                           enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const_partial2_x_V_list = prec['const']['partial2_x_V_list']
                except KeyError:
                    prec['const']['partial2_x_V_list'] = [ const_vand[var] for var in avar ]
        # Integrated exponential part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            for idx, (xeval, pp) in enumerate(zip(prec['intexp']['xjsc_list'],
                                                  prec['intexp']['prec_list'])):
                try: prec_intexp_partial2_x_V_list = pp['partial2_x_V_list']
                except KeyError:
                    to_compute_flag = True
                    break
            if to_compute_flag: break
        if to_compute_flag:
            partial2_x_exp_vand = [ b.GradVandermonde(x[:,i], int(o), k=2) for i,(o,b) in
                                   enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                # Generate Vandermonde matrices
                for idx, (xeval, pp) in enumerate(zip(prec['intexp']['xjsc_list'],
                                                      prec['intexp']['prec_list'])):
                    try: prec_intexp_partial2_x_V_list = pp['partial2_x_V_list']
                    except KeyError:
                        pp['partial2_x_V_list'] = [
                            np.tile( partial2_x_exp_vand[var][idx,:], (xeval.shape[0],1) )
                            for var in avar[:-1] ]
                        pp['partial2_x_V_list'].append(
                            self.exp_basis_list[avar[-1]].GradVandermonde(
                                xeval[:,-1], self.exp_max_orders[avar[-1]], k=2) )
        # precomp_partial2_xd part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_exp_partial_xd_V_last = prec['exp']['partial_xd_V_last']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            partial_x_exp_vand = [ b.GradVandermonde(x[:,i], int(o), k=1) for i,(o,b) in
                                   enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_exp_partial_xd_V_last = prec['exp']['partial_xd_V_last']
                except KeyError:
                    prec['exp']['partial_xd_V_last'] = partial_x_exp_vand[avar[-1]]
        return precomp

    def precomp_nabla3_x(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla^3_{\bf x}T({\bf x},{\bf a})`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        # precomp_hess_x part (and precomp_evaluate, precomp_grad_x)
        precomp = self.precomp_hess_x(x, precomp, precomp_type)
        # Constant part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const_partial3_x_V_list = prec['const']['partial3_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            const_vand = [ b.GradVandermonde(x[:,i], int(o), k=3) for i,(o,b) in
                           enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const_partial3_x_V_list = prec['const']['partial3_x_V_list']
                except KeyError:
                    prec['const']['partial3_x_V_list'] = [ const_vand[var] for var in avar ]
        # Integrated exponential part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            for idx, (xeval, pp) in enumerate(zip(prec['intexp']['xjsc_list'],
                                                  prec['intexp']['prec_list'])):
                try: prec_intexp_partial3_x_V_list = pp['partial3_x_V_list']
                except KeyError:
                    to_compute_flag = True
                    break
        if to_compute_flag:
            partial3_x_exp_vand = [ b.GradVandermonde(x[:,i], int(o), k=3) for i,(o,b) in
                                   enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                # Generate Vandermonde matrices
                for idx, (xeval, pp) in enumerate(zip(prec['intexp']['xjsc_list'],
                                                      prec['intexp']['prec_list'])):
                    try: prec_intexp_partial3_x_V_list = pp['partial3_x_V_list']
                    except KeyError:
                        pp['partial2_x_V_list'] = [
                            np.tile( partial3_x_exp_vand[var][idx,:], (xeval.shape[0],1) )
                            for var in avar[:-1] ]
                        pp['partial2_x_V_list'].append(
                            self.exp_basis_list[avar[-1]].GradVandermonde(
                                xeval[:,-1], self.exp_max_orders[avar[-1]], k=3) )
        # precomp_partial3_xd part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_exp_partial2_xd_V_last = prec['exp']['partial2_xd_V_last']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            partial2_x_exp_vand = [ b.GradVandermonde(x[:,i], int(o), k=2) for i,(o,b) in
                                    enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_exp_partial2_xd_V_last = prec['exp']['partial2_xd_V_last']
                except KeyError:
                    prec['exp']['partial2_xd_V_last'] = partial2_x_exp_vand[avar[-1]]
        return precomp

    def precomp_partial_xd(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\partial_{x_k}T_k({\bf x},{\bf a})` for :math:`k=1,\ldots,d`

        Enriches the dictionaries in the ``precomp`` list if necessary.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`ndarray<numpy.ndarray>`) -- necessary structures
        """
        if precomp_type != 'uni':
            raise ValueError("Only option 'uni' is allowed for CommonBasisTransportMaps")
        if precomp is None:
            precomp = {'components': [{} for i in range(self.dim)]}
        # Constant part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const = prec['const']
            except KeyError:
                to_compute_flag = True
                break
            try: prec_const_V_list = prec['const']['V_list']
            except KeyError:
                to_compute_flag = True
                break
            try: prec_const_partial_xd_V_last = prec['const']['partial_xd_V_last']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            const_vand = [ b.GradVandermonde(x[:,i], int(o)) for i,(o,b) in
                           enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            const_partial_x_vand = [ b.GradVandermonde(x[:,i], int(o), k=1) for i,(o,b) in
                                     enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const = prec['const']
                except KeyError: prec['const'] = {}
                try: prec_const_V_list = prec['const']['V_list']
                except KeyError: prec['const']['V_list'] = [ const_vand[var] for var in avar ]
                try: prec_const_partial_xd_V_last = prec['const']['partial_xd_V_last']
                except KeyError: prec['const']['partial_xd_V_last'] = const_partial_x_vand[avar[-1]]
        # Exponential part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const = prec['exp']
            except KeyError:
                to_compute_flag = True
                break
            try: prec_exp_V_list = prec['exp']['V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            exp_vand = [ b.GradVandermonde(x[:,i], int(o)) for i,(o,b) in
                         enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const = prec['exp']
                except KeyError: prec['exp'] = {}
                try: prec_exp_V_list = prec['exp']['V_list']
                except KeyError: prec['exp']['V_list'] = [ exp_vand[var] for var in avar ]
        return precomp

    def precomp_grad_x_partial_xd(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla_{\bf x}\partial_{x_k}T_k({\bf x},{\bf a})` for :math:`k=1,\ldots,d`

        Enriches the dictionaries in the ``precomp`` list if necessary.
        
        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`dict<dict>`) -- necessary structures
        """
        # precomp_partial_xd part
        precomp = self.precomp_partial_xd(x, precomp, precomp_type)
        # Constant part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const_partial_xd_V_list = prec['const']['partial_xd_V_list']
            except KeyError:
                to_compute_flag = True
                break
            try: prec_const_partial2_xd_V_last = prec['const']['partial2_xd_V_last']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            const_partial_x_vand = [ b.GradVandermonde(x[:,i], int(o), k=1) for i,(o,b) in
                                     enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            const_partial2_x_vand = [ b.GradVandermonde(x[:,i], int(o), k=2) for i,(o,b) in
                                      enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const_partial_xd_V_list = prec['const']['partial_xd_V_list']
                except KeyError:
                    prec['const']['partial_xd_V_list'] = [ const_partial_x_vand[var] for var in avar ]
                try: prec_const_partial2_xd_V_last = prec['const']['partial2_xd_V_last']
                except KeyError: prec['const']['partial2_xd_V_last'] = const_partial2_x_vand[avar[-1]]
        # Exponential part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_exp_partial_x_V_list = prec['exp']['partial_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            partial_x_exp_vand = [ b.GradVandermonde(x[:,i], int(o), k=1) for i,(o,b) in
                                   enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_exp_partial_x_V_list = prec['exp']['partial_x_V_list']
                except KeyError:
                    prec['exp']['partial_x_V_list'] = [ partial_x_exp_vand[var] for var in avar ]
        return precomp

    def precomp_hess_x_partial_xd(self, x, precomp=None, precomp_type='uni'):
        r""" Precompute necessary structures for the evaluation of :math:`\nabla^2_{\bf x}\partial_{x_k}T_k({\bf x},{\bf a})` for :math:`k=1,\ldots,d`

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          precomp (dict): list of dictionaries of precomputed values
          precomp_type (str): only option 'uni' is allowed for this TransportMap

        Returns:
           (:class:`dict<dict>` of :class:`list<list>` [:math:`d`]
             :class:`dict<dict>`) -- necessary structures
        """
        # precomp_grad_x_partial_xd (and precomp_partial_xd) parts
        precomp = self.precomp_grad_x_partial_xd(x, precomp, precomp_type)
        # Constant part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_const_partial2_xd_V_list = prec['const']['partial2_xd_V_list']
            except KeyError:
                to_compute_flag = True
                break
            try: prec_const_partial3_xd_V_last = prec['const']['partial3_xd_V_last']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            const_partial2_x_vand = [ b.GradVandermonde(x[:,i], int(o), k=2) for i,(o,b) in
                                      enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            const_partial3_x_vand = [ b.GradVandermonde(x[:,i], int(o), k=3) for i,(o,b) in
                                      enumerate(zip(self.const_max_orders,self.const_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_const_partial2_xd_V_list = prec['const']['partial2_xd_V_list']
                except KeyError:
                    prec['const']['partial2_xd_V_list'] = [ const_partial2_x_vand[var] for var in avar ]
                try: prec_const_partial3_xd_V_last = prec['const']['partial3_xd_V_last']
                except KeyError: prec['const']['partial3_xd_V_last'] = const_partial3_x_vand[avar[-1]]
        # Exponential part
        to_compute_flag = False
        for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
            try: prec_exp_partial2_x_V_list = prec['exp']['partial2_x_V_list']
            except KeyError:
                to_compute_flag = True
                break
        if to_compute_flag:
            partial2_x_exp_vand = [ b.GradVandermonde(x[:,i], int(o), k=2) for i,(o,b) in
                                    enumerate(zip(self.exp_max_orders,self.exp_basis_list)) ]
            for i,(avar,prec) in enumerate(zip(self.active_vars, precomp['components'])):
                try: prec_exp_partial2_x_V_list = prec['exp']['partial2_x_V_list']
                except KeyError:
                    prec['exp']['partial2_x_V_list'] = [ partial2_x_exp_vand[var] for var in avar ]
        return precomp
