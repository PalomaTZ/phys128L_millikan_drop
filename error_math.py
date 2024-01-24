import numpy as np
# Populate observables in an array

P = 101325
pr = 886
b = 8.2e-3
g = 9.8
tvf = 2.5e-5
tvr = 4.2e-5
tn = 1.832e-5
td = 9.1e-3
tV = 500

te_d = 5e-6
te_vr = 1e-6
te_vf = 1e-6
te_n = 0.0008e-5
te_V = 1

def sqrt_expr(vf, n):
    return ((b/(2*P))**2 + (9*n*vf/(2*pr*g)))**(1/2)

def error_propogation_d(vf, vr, n, d, V, e_d):
    q = (4*np.pi/3)*(sqrt_expr(vf,n) - (b/(2*P)))**3 *pr*g*(vf+vr)/(V*vf)*e_d
    return q

def error_propogation_vr(vf, vr, n, d, V, e_vr):
    q = (4*np.pi/3)*(sqrt_expr(vf,n) - (b/(2*P)))**3 *pr*g*d/(V*vf)*e_vr
    return q

def error_propogation_vf(vf, vr, n, d, V, e_vf):
    q1 = np.pi*d
    q2 = (2*P*sqrt_expr(vf,n)-b)**2
    q3 = 2*b*g*P*pr*vr*sqrt_expr(vf,n)+27*n*P**2*vf**2 + 9*n*P**2*vf**2 + 9*n*P**2*vr*vf-b**2*g*pr*vr
    q4 = 12*P**4*V*vf**2*sqrt_expr(vf, n)
    return q1*q2*q3/q4*e_vf

def error_propogation_n(vf, vr, n, d, V, e_n):
    q = 9*np.pi*d*(vr+vf)*(sqrt_expr(vf, n) - b/(2*P))**2 /(V*sqrt_expr(vf, n)) *e_n
    return q

def error_propogation_V(vf, vr, n, d, V, e_V):
    q = (4*np.pi/3)*(sqrt_expr(vf,n) - (b/(2*P)))**3 *pr*g*d*(vf+vr)/(V**2*vf)*e_V
    return q

print(error_propogation_V(tvf, tvr, tn, td, tV, te_V))
