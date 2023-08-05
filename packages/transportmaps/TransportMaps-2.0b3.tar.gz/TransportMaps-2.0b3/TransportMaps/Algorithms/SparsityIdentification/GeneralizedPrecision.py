'''This file computes the gradient with respect to map coefficients of the
hessian of the log target pdf. It also computes the variance of the generalized
precision matrix omega.'''
import numpy as np

__all__ = ['gen_precision','grad_a_omega','var_omega']

nax = np.newaxis
def gen_precision(pb_dist, data):
    # Compute omega (expectation over samples)
    hess_samps = pb_dist.hess_x_log_pdf(data)
    gen_prec = np.mean(np.abs(hess_samps), axis=0)
    return gen_prec

def grad_a_omega(pb_dist, data):

    grad_omega = pb_dist.grad_a_hess_x_log_pdf(data)
    # note: case where gradient of abs val not defined is not accounted for here
    omega_jac = np.mean(np.multiply(grad_omega, np.sign(grad_omega)), axis=0)

    return omega_jac

def var_omega(pb_dist, data):
    n = data.shape[0]
    dim = pb_dist.transport_map.dim
    omega_CI_jac = grad_a_omega(pb_dist, data)
    fisher_info_samps = pb_dist.hess_a_log_pdf(data)
    fisher_info = - np.mean(fisher_info_samps,axis=0)
    var_a = 1/n * np.linalg.inv(fisher_info)
    var_omega = np.zeros([dim, dim])
    for i in range(dim):
        for j in range(dim):
            temp = np.dot(var_a,omega_CI_jac[:,i,j])
            var_omega[i,j] = np.dot(omega_CI_jac[:,i,j].T,temp)

    return var_omega
