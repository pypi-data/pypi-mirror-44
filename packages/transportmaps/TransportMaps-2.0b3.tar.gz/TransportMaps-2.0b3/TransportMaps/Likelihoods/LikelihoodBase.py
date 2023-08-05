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
# Authors: Transport Map Team
# Website: transportmaps.mit.edu
# Support: transportmaps.mit.edu/qa/
#

import numpy as np

from TransportMaps.Misc import counted, cached, cached_tuple, get_sub_cache
from TransportMaps.Functionals.FunctionBase import *
from TransportMaps.Maps.MapBase import \
    Map, ConstantMap, LinearMap, ConditionallyLinearMap
from TransportMaps.Distributions.DistributionBase import \
    ConditionalDistribution
from TransportMaps.Distributions.FrozenDistributions import \
    GaussianDistribution
from TransportMaps.Distributions.ConditionalDistributions import \
    ConditionallyGaussianDistribution

__all__ = ['LogLikelihood',
           'AdditiveLogLikelihood',
           'AdditiveLinearGaussianLogLikelihood',
           'AdditiveConditionallyLinearGaussianLogLikelihood',
           'IndependentLogLikelihood']

class LogLikelihood(Function):
    r""" Abstract class for log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})`

    Note that :math:`\log\pi:\mathbb{R}^d \rightarrow \mathbb{R}`
    is considered a function of :math:`{\bf x}`, while the
    data :math:`{\bf y}` is fixed.
    
    Args:
      y (:class:`ndarray<numpy.ndarray>`): data
      dim (int): input dimension $d$
    """
    def __init__(self, y, dim):
        super(LogLikelihood, self).__init__(dim)
        self._y = y

    @property
    def y(self):
        return self._y

    @cached()
    @counted
    def evaluate(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- function evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

    @cached()
    @counted
    def grad_x(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- gradient evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

    @cached_tuple(['evaluate', 'grad_x'])
    @counted 
    def tuple_grad_x(self, x, cache=None, **kwargs):
        r""" Evaluate :math:`\left(\log\pi({\bf y} \vert {\bf x}),\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})\right)`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`tuple`) --
            :math:`\left(\log\pi({\bf y} \vert {\bf x}),\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})\right)`
        """
        return ( self.evaluate(x, cache=cache, **kwargs),
                 self.grad_x(x, cache=cache, **kwargs) )

    @cached(caching=False)
    @counted
    def hess_x(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d,d`]) -- Hessian evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

    @cached(caching=False)
    @counted
    def action_hess_x(self, x, dx, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\langle \nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x}),\delta{\bf x}\rangle`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          dx (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): direction
            on which to evaluate the Hessian

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- Hessian evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

class AdditiveLogLikelihood(LogLikelihood):
    r""" Log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})=\log\pi({\bf y} - T({\bf x}))`

    Args:
      y (:class:`ndarray<numpy.ndarray>` :math:`[d_y]`): data
      pi (:class:`Distribution<TransportMaps.Distributions.Distribution>`):
        distribution :math:`\nu_\pi`
      T (:class:`Map<TransportMaps.Maps.Map>`): map :math:`T:\mathbb{R}^d\rightarrow\mathbb{R}^{d_y}`
    """
    def __init__(self, y, pi, T):
        if len(y) != pi.dim:
            raise ValueError("The dimension of the data must match the " + \
                             "dimension of the distribution pi")
        if len(y) != T.dim_out:
            raise ValueError("The dimension of the data must match the " + \
                             "dimension of the output of T")
        super(AdditiveLogLikelihood, self).__init__(y, T.dim_in)
        self.pi = pi
        self.T = T
        if issubclass(type(pi), ConditionalDistribution):
            self._isPiCond = True
        else:
            self._isPiCond = False

    def get_ncalls_tree(self, indent=""):
        out = super(AdditiveLogLikelihood, self).get_ncalls_tree(indent)
        out += self.pi.get_ncalls_tree(indent + '  ')
        out += self.T.get_ncalls_tree(indent + '  ')
        return out

    def get_nevals_tree(self, indent=""):
        out = super(AdditiveLogLikelihood, self).get_nevals_tree(indent)
        out += self.pi.get_nevals_tree(indent + '  ')
        out += self.T.get_nevals_tree(indent + '  ')
        return out

    def get_teval_tree(self, indent=""):
        out = super(AdditiveLogLikelihood, self).get_teval_tree(indent)
        out += self.pi.get_teval_tree(indent + '  ')
        out += self.T.get_teval_tree(indent + '  ')
        return out

    def update_ncalls_tree(self, obj):
        super(AdditiveLogLikelihood, self).update_ncalls_tree(obj)
        self.pi.update_ncalls_tree(obj.pi)
        self.T.update_ncalls_tree(obj.T)

    def update_nevals_tree(self, obj):
        super(AdditiveLogLikelihood, self).update_nevals_tree(obj)
        self.pi.update_nevals_tree(obj.pi)
        self.T.update_nevals_tree(obj.T)

    def update_teval_tree(self, obj):
        super(AdditiveLogLikelihood, self).update_teval_tree(obj)
        self.pi.update_teval_tree(obj.pi)
        self.T.update_teval_tree(obj.T)

    def reset_counters(self):
        super(AdditiveLogLikelihood, self).reset_counters()
        self.pi.reset_counters()
        self.T.reset_counters()
        
    @property
    def isPiCond(self):
        return self._isPiCond

    @cached([('pi',None),('T',None)])
    @counted
    def evaluate(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- function evaluations
        """
        pi_cache, T_cache = get_sub_cache(cache, ('pi',None), ('T',None))
        frw = self.T.evaluate(x, idxs_slice=idxs_slice, cache=T_cache)
        return self.pi.log_pdf(
            self.y - frw, idxs_slice=idxs_slice, cache=pi_cache )

    @cached([('pi',None),('T',None)])
    @counted
    def grad_x(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- gradient evaluations

        .. todo:: caching is not implemented
        """
        pi_cache, T_cache = get_sub_cache(cache, ('pi',None), ('T',None))
        frw = self.T.evaluate(x, cache=T_cache)
        gx_frw = self.T.grad_x(x, idxs_slice=idxs_slice, cache=T_cache)
        gx_lpdf = self.pi.grad_x_log_pdf(
            self.y - frw, idxs_slice=idxs_slice, cache=pi_cache )
        out = - np.einsum('...i,...ij->...j',gx_lpdf, gx_frw)
        return out

    @cached_tuple(['evaluate','grad_x'], [('pi',None),('T',None)])
    @counted
    def tuple_grad_x(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\log\pi({\bf y} \vert {\bf x}), \nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`tuple`) -- function and gradient evaluations

        .. todo:: caching is not implemented
        """
        pi_cache, T_cache = get_sub_cache(cache, ('pi',None), ('T',None))
        frw, gx_frw = self.T.tuple_grad_x(x, idxs_slice=idxs_slice, cache=T_cache)
        lpdf, gx_lpdf = self.pi.tuple_grad_x_log_pdf(
            self.y - frw, idxs_slice=idxs_slice, cache=pi_cache )
        gx = - np.einsum('...i,...ij->...j',gx_lpdf, gx_frw)
        return lpdf, gx

    @cached([('pi',None),('T',None)],False)
    @counted
    def hess_x(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d,d`]) -- Hessian evaluations

        .. todo:: caching is not implemented
        """
        pi_cache, T_cache = get_sub_cache(cache, ('pi',None), ('T',None))
        frw = self.T.evaluate(x, idxs_slice=idxs_slice, cache=T_cache) # m x d_y
        gx_frw = self.T.grad_x(x, idxs_slice=idxs_slice, cache=T_cache) # m x d_y x d_x
        hx_frw = self.T.hess_x(x, idxs_slice=idxs_slice, cache=T_cache) # m x d_y x d_x x d_x
        gx_lpdf = self.pi.grad_x_log_pdf(
            self.y - frw, idxs_slice=idxs_slice, cache=pi_cache ) # m x d_y
        hx_lpdf = self.pi.hess_x_log_pdf(
            self.y - frw, idxs_slice=idxs_slice, cache=pi_cache ) # m x d_y x d_y
        out = np.einsum('...ij,...ik,...kl->...jl', gx_frw, hx_lpdf, gx_frw)
        out -= np.einsum('...i,...ijk->...jk', gx_lpdf, hx_frw) # m x d_x x d_x
        return out

    @cached([('pi',None),('T',None)],False)
    @counted
    def action_hess_x(self, x, dx, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\langle\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x}),\delta{\bf x}\rangle`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          dx (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): direction
            on which to evaluate the Hessian
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d,`]) -- action of Hessian evaluations

        .. todo:: caching is not implemented
        """
        pi_cache, T_cache = get_sub_cache(cache, ('pi',None), ('T',None))
        
        frw = self.T.evaluate(x, idxs_slice=idxs_slice, cache=T_cache) # m x d_y
        gx_frw = self.T.grad_x(x, idxs_slice=idxs_slice, cache=T_cache) # m x d_y x d_x
        gx_lpdf = self.pi.grad_x_log_pdf(
            self.y - frw, idxs_slice=idxs_slice, cache=pi_cache ) # m x d_y

        A = np.einsum('...ij,...j->...i', -gx_frw, dx) # m x d_y
        A = self.pi.action_hess_x_log_pdf(
            self.y - frw, A, idxs_slice=idxs_slice, cache=pi_cache) # m x d_y
        A = np.einsum('...ij,...i->...j', -gx_frw, A) # m x d_x

        B = -self.T.action_hess_x(
            x, dx, idxs_slice=idxs_slice, cache=T_cache) # m x d_y x d_x
        B = np.einsum('...i,...ij->...j', gx_lpdf, B) # m x d_x

        return A + B

class AdditiveLinearGaussianLogLikelihood(AdditiveLogLikelihood):
    r""" Define the log-likelihood for the additive linear Gaussian model

    The model is

    .. math::

       {\bf y} = {\bf c} + {\bf T}{\bf x} + \varepsilon \;, \quad
       \varepsilon \sim \mathcal{N}(\mu, \Sigma)

    where :math:`T \in \mathbb{R}^{d_y \times d_x}`, :math:`\mu \in \mathbb{R}^{d_y}`
    and :math:`\Sigma \in \mathbb{R}^{d_y \times d_y}` is symmetric positve
    definite

    Args:
      y (:class:`ndarray<numpy.ndarray>` [:math:`d_y`]): data
      c (:class:`ndarray<numpy.ndarray>` [:math:`d_y`] or :class:`Map<TransportMaps.Maps.Map>`): system constant or parametric map returning the constant
      T (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_x`] or :class:`Map<TransportMaps.Maps.Map>`): system matrix or parametric map returning the system matrix
      mu (:class:`ndarray<numpy.ndarray>` [:math:`d_y`] or :class:`Map<TransportMaps.Maps.Map>`): noise mean or parametric map returning the mean
      sigma (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_y`] or :class:`Map<TransportMaps.Maps.Map>`):
        noise covariance or parametric map returning the covariance
      precision (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_y`] or :class:`Map<TransportMaps.Maps.Map>`):
        noise precision matrix or parametric map returning the precision matrix
    """
    def __init__(self, y, c, T, mu, sigma=None, precision=None):
        # INIT MAP AND DISTRIBUTION
        linmap = LinearMap(c, T)
        pi = GaussianDistribution(mu, sigma=sigma, precision=precision)
        super(AdditiveLinearGaussianLogLikelihood, self).__init__(y, pi, linmap)

class AdditiveConditionallyLinearGaussianLogLikelihood(AdditiveLogLikelihood):
    r""" Define the log-likelihood for the additive linear Gaussian model

    The model is

    .. math::

       {\bf y} = {\bf c}(\theta) + {\bf T}(\theta){\bf x} + \varepsilon \;, \quad
       \varepsilon \sim \mathcal{N}(\mu(\theta), \Sigma(\theta))

    where :math:`T \in \mathbb{R}^{d_y \times d_x}`, :math:`\mu \in \mathbb{R}^{d_y}`
    and :math:`\Sigma \in \mathbb{R}^{d_y \times d_y}` is symmetric positve
    definite

    Args:
      y (:class:`ndarray<numpy.ndarray>` [:math:`d_y`]): data
      c (:class:`ndarray<numpy.ndarray>` [:math:`d_y`] or :class:`Map<TransportMaps.Maps.Map>`): system constant or parametric map returning the constant
      T (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_x`] or :class:`Map<TransportMaps.Maps.Map>`): system matrix or parametric map returning the system matrix
      mu (:class:`ndarray<numpy.ndarray>` [:math:`d_y`] or :class:`Map<TransportMaps.Maps.Map>`): noise mean or parametric map returning the mean
      sigma (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_y`] or :class:`Map<TransportMaps.Maps.Map>`):
        noise covariance or parametric map returning the covariance
      precision (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_y`] or :class:`Map<TransportMaps.Maps.Map>`):
        noise precision matrix or parametric map returning the precision matrix
      active_vars_system (:class:`list` of :class:`int`): active variables
        identifying the parameters for for :math:`c(\theta), T(\theta)`.
      active_vars_distribution (:class:`list` of :class:`int`): active variables
        identifying the parameters for for :math:`\mu(\theta), \Sigma(\theta)`.
      coeffs (:class:`ndarray<numpy.ndarray>`): initialization coefficients
    """
    def __init__(self, y, c, T, mu, sigma=None, precision=None,
                 active_vars_system=[], active_vars_distribution=[],
                 coeffs=None):
        # SYSTEM
        if c.dim_in != T.dim_in:
            raise ValueError("Input dimension c and T don't match")
        # DISTRIBUTION
        if isinstance(mu, np.ndarray) and (
                (sigma is not None and isinstance(sigma, np.ndarray)) or
                (precision is not None and isinstance(precision, np.ndarray)) ):
            pi = GaussianDistribution(mu, sigma=sigma, precision=precision)
        else:
            if mu.dim_in != c.dim_in:
                raise ValueError("Input dimension c and mu don't match")
            if sigma is not None and mu.dim_in != sigma.dim_in:
                raise ValueError("Input dimension mu and sigma don't match")
            if precision is not None and mu.dim_in != precision.dim_in:
                raise ValueError("Input dimension mu and precision don't match")
            pi = ConditionallyGaussianDistribution(mu, sigma=sigma, precision=precision)
        # SETUP AUXILIARY VARIABLES
        self._n_coeffs = c.dim_in
        # INIT MAP AND DISTRIBUTION
        linmap = ConditionallyLinearMap(c, T)
        super(AdditiveConditionallyLinearGaussianLogLikelihood, self).__init__(y, pi, linmap)
        self.coeffs = coeffs

    @property
    def n_coeffs(self):
        return self._n_coeffs
        
    @property
    def coeffs(self):
        return self._coeffs

    @coeffs.setter
    def coeffs(self, coeffs):
        if coeffs is not None:
            self.T.coeffs = coeffs
            if self.isPiCond:
                self.pi.coeffs = coeffs
            self._coeffs = coeffs

            
class IndependentLogLikelihood(Function):
    r""" Handling likelihoods in the form :math:`\pi({\bf y}\vert{\bf x}) = \prod_{i=1}^{n}\pi_i({\bf y}_i\vert{\bf x}_i)`

    Args:
      factors (:class:`list` of :class:`tuple`): each tuple contains a
        log-likelihood (:class:`LogLikelihood`) and the sub-set of variables
        of :math:`{\bf x}` on which it acts.

    Example
    -------
    Let :math:`\pi(y_0,y_2\vert x_0,x_1,x_2)= \pi_0(y_0\vert x_0) \pi_2(y_2,x_2)`.

    >>> factors = [(ll0, [0]),
    >>>            (ll2, [2])]
    >>> ll = IndependentLogLikelihood(factors)
    
    """
    def __init__(self, factors):
        self.factors = []
        self.input_dim = set()
        for i, (ll, xidxs) in enumerate(factors):
            # Check right number of inputs
            if ll is not None and len(set(list(xidxs))) != ll.dim:
                raise TypeError("The dimension of the %d " % i + \
                                "log-likelihood is not consistent with " + \
                                "the number of variables.")
            self.factors.append( (ll, xidxs) )
            self.input_dim |= set(xidxs)
        dim = 0 if len(self.input_dim) == 0 else max(self.input_dim)+1
        super(IndependentLogLikelihood, self).__init__(dim)

    def get_ncalls_tree(self, indent=""):
        out = super(IndependentLogLikelihood, self).get_ncalls_tree(indent)
        for ll,_ in self.factors:
            out += ll.get_ncalls_tree(indent + '  ')
        return out

    def get_nevals_tree(self, indent=""):
        out = super(IndependentLogLikelihood, self).get_nevals_tree(indent)
        for ll,_ in self.factors:
            out += ll.get_nevals_tree(indent + '  ')
        return out

    def get_teval_tree(self, indent=""):
        out = super(IndependentLogLikelihood, self).get_teval_tree(indent)
        for ll,_ in self.factors:
            out += ll.get_teval_tree(indent + '  ')
        return out

    def update_ncalls_tree(self, obj):
        super(IndependentLogLikelihood, self).update_ncalls_tree(obj)
        for (ll,_),(obj_ll,_) in zip(self.factors,obj.factors):
            ll.update_ncalls_tree(obj_ll)

    def update_nevals_tree(self, obj):
        super(IndependentLogLikelihood, self).update_nevals_tree(obj)
        for (ll,_),(obj_ll,_) in zip(self.factors,obj.factors):
            ll.update_nevals_tree(obj_ll)

    def update_teval_tree(self, obj):
        super(IndependentLogLikelihood, self).update_teval_tree(obj)
        for (ll,_),(obj_ll,_) in zip(self.factors,obj.factors):
            ll.update_teval_tree(obj_ll)

    def reset_counters(self):
        super(IndependentLogLikelihood, self).reset_counters()
        for ll,_ in self.factors:
            ll.reset_counters()
            
    @property
    def y(self):
        return [ ll.y for ll,_ in self.factors ]

    @property
    def n_factors(self):
        return len(self.factors)

    def append(self, factor):
        r""" Add a new factor to the likelihood

        Args:
          factors (:class:`tuple`): tuple containing a
            log-likelihood (:class:`LogLikelihood`) and the sub-set of variables
            of :math:`{\bf x}` on which it acts.

        Example
        -------
        Let :math:`\pi(y_0,y_2\vert x_0,x_1,x_2)= \pi_0(y_0\vert x_0) \pi_2(y_2,x_2)` and
        let's add the factor :math:`\pi_1(y_1\vert x_1)`, obtaining:

        .. math::

           \pi(y_0,y_1,y_2\vert x_0,x_1,x_2)= \pi_0(y_0\vert x_0) \pi_1(y_1\vert x_1) \pi_2(y_2,x_2)

        >>> factor = (ll1, [1])
        >>> ll.append(factor)
        
        """
        ll, xidxs = factor
        if ll is not None and len(set(xidxs)) != ll.dim:
            raise TypeError("The dimension of the " + \
                            "log-likelihood is not consistent with " + \
                            "the number of variables.")
        self.factors.append( (ll, xidxs) )
        self.input_dim |= set(xidxs)
        self.dim = max(self.input_dim)+1

    @cached([("ll_list","n_factors")])
    @counted
    def evaluate(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- function evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        ll_list_cache = get_sub_cache(cache, ("ll_list",self.n_factors))
        out = np.zeros(x.shape[0])
        for (ll, xidxs), ll_cache in zip(self.factors, ll_list_cache):
            if ll is not None:
                out += ll.evaluate(
                    x[:,xidxs], idxs_slice=idxs_slice, cache=ll_cache, **kwargs)
        return out

    @cached([("ll_list","n_factors")])
    @counted
    def grad_x(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- gradient evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        ll_list_cache = get_sub_cache(cache, ("ll_list",self.n_factors))
        out = np.zeros(x.shape)
        for (ll, xidxs), ll_cache in zip(self.factors, ll_list_cache):
            if ll is not None:
                out[:,xidxs] += ll.grad_x(
                    x[:,xidxs], idxs_slice=idxs_slice, cache=ll_cache, **kwargs)
        return out

    @cached_tuple(['evaluate', 'grad_x'],[("ll_list","n_factors")])
    @counted
    def tuple_grad_x(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\log\pi({\bf y} \vert {\bf x}), \nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`tuple`) -- function and gradient evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        ll_list_cache = get_sub_cache(cache, ("ll_list",self.n_factors))
        fx_out = np.zeros(x.shape[0])
        gx_out = np.zeros(x.shape)
        for (ll, xidxs), ll_cache in zip(self.factors, ll_list_cache):
            if ll is not None:
                fx, gfx = ll.tuple_grad_x(
                    x[:,xidxs], idxs_slice=idxs_slice, cache=ll_cache, **kwargs)
                fx_out += fx
                gx_out[:,xidxs] += gfx
        return fx_out, gx_out
        
    @cached([("ll_list","n_factors")],False)
    @counted
    def hess_x(self, x, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d,d`]) -- Hessian evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        ll_list_cache = get_sub_cache(cache, ("ll_list",self.n_factors))
        m = x.shape[0]
        out = np.zeros( (m, self.dim, self.dim) )
        for (ll, xidxs), ll_cache in zip(self.factors, ll_list_cache):
            if ll is not None:
                out[np.ix_(range(m),xidxs,xidxs)] += \
                    ll.hess_x(
                        x[:,xidxs], idxs_slice=idxs_slice, cache=ll_cache, **kwargs)
        return out

    @cached([("ll_list","n_factors")],False)
    @counted
    def action_hess_x(self, x, dx, idxs_slice=slice(None,None,None), cache=None, **kwargs):
        r""" Evaluate :math:`\langle\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x}),\delta{\bf x}\rangle`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points
          dx (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): direction
            on which to evaluate the Hessian
          cache (dict): cache

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- Hessian evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        ll_list_cache = get_sub_cache(cache, ("ll_list",self.n_factors))
        m = x.shape[0]
        out = np.zeros( (m, self.dim) )
        for (ll, xidxs), ll_cache in zip(self.factors, ll_list_cache):
            if ll is not None:
                out[np.ix_(range(m),xidxs)] += \
                    ll.action_hess_x(
                        x[:,xidxs], dx[:,xidxs],
                        idxs_slice=idxs_slice, cache=ll_cache, **kwargs)
        return out