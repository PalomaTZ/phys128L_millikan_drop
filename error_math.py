import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
# Populate observables in an array

P = 101325
pr = 886
b = 8.2e-3
g = 9.8
tvf = 3.01e-5
tvr = 15.38e-5
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

def q(vf, vr, n, d, V):
    return (4*np.pi/3)*(sqrt_expr(vf,n) - (b/(2*P)))**3 *pr*g*(vf+vr)/(V*vf)*d

file_list = os.listdir('/Users/PLo/Desktop/2024_winter/phys_128L/phys128L_millikan_drop/vid_data')

df_list = [pd.read_csv('/Users/PLo/Desktop/2024_winter/phys_128L/phys128L_millikan_drop/vid_data' + '/' + file) for file in file_list]


vr_list = df_list[0]["Velocity (m/s)"].loc[df_list[0]["Type"] == "Rise"].astype(float).to_numpy()
vf_list = df_list[0]["Velocity (m/s)"].loc[df_list[0]["Type"] == "Fall"].astype(float).to_numpy()
vr_d_list = df_list[0]["dv"].loc[df_list[0]["Type"] == "Rise"].astype(float).to_numpy()
vf_d_list = df_list[0]["dv"].loc[df_list[0]["Type"] == "Fall"].astype(float).to_numpy()

new_df = pd.DataFrame()
new_df['Vr'] = vr_list
new_df['Vf'] = vf_list
new_df['d_Vr'] = vr_d_list
new_df['d_Vf'] = vf_d_list
new_df['q'] = q(vf_list, vr_list, tn, td, tV)/1e-19
new_df.to_csv('/Users/PLo/Desktop/2024_winter/phys_128L/phys128L_millikan_drop/vid_data/new_df.csv')

x = [1]*len(new_df['q'])
plt.scatter(x, new_df['q'], color="blue", alpha=0.4)
plt.show()

"""
q_trials = []
for i, j in zip(file_list, range(len(file_list))):
    df_list[j].columns = df_list[j].iloc[0].values.tolist()
    vr_list = df_list[j]["Velocity (m/sec)"].loc[df_list[j]["Type"] == "Rise"].astype(float).to_numpy()
    vf_list = df_list[j]["Velocity (m/sec)"].loc[df_list[j]["Type"] == "Fall"].astype(float).to_numpy()

    q_list = q(vf_list, vr_list, tn, td, tV)

"""
    



#need q for each trial

q_list = q(vf_list, vr_list, tn, td, tV)/1e-19

predicted_charge = q(tvf, tvr, tn, td, tV) / 1.60e-19
print(f"q = {predicted_charge:.5f} e")
print(error_propogation_V(tvf, tvr, tn, td, tV, te_V)) # 
