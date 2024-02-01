import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

d = 9.10e-3
rho = 886
g = 9.8
b = 8.2e-3
pressure = 101325
V = 500

d_error = 0.01e-3
rho_error = 0.5
g_error = 0.01
voltage_error = 1
V_error = 1

xl_file = pd.ExcelFile("video analysis.xlsx")
data_frame = pd.read_excel(xl_file, "Cleaned up data")

velocities = np.array(data_frame["Velocity (m/s)"])
velocity_errors = np.array(data_frame["Velocity Uncertainty (m/sec)"])
etas = np.array(data_frame["Eta (Nsm^-2 * 10^-5)"])[0::2]*1e-5
eta_errors = np.array(data_frame["Eta Uncertainty (Nsm^-2 * 10^-5)"])[0::2]*1e-5

fall_velocities = velocities[0::2]
rise_velocities = velocities[1::2]

fall_velocity_errors = velocity_errors[0::2]
rise_velocity_errors = velocity_errors[1::2]

a = np.sqrt((b / 2 / pressure) ** 2 + 9 * etas * fall_velocities / (2 * g * rho)) - b / (2 * pressure)

q = 4 * np.pi / 3 * (a ** 3) * rho * g * d * (fall_velocities + rise_velocities) / (V * fall_velocities)

common_a_error_term = 3/2 * (a ** 2 + 2 * a * b / 2 / pressure) / (a ** 2 + a * b / 2 / pressure)
dq_vf = fall_velocity_errors / fall_velocities * q * (1 / (1 + rise_velocities / fall_velocities) - 1 + common_a_error_term)
dq_vr = rise_velocity_errors / rise_velocities * q * (1 / (1 + fall_velocities / rise_velocities))
dq_d = d/d_error * q
dq_rho = q * rho_error / rho * (1 - common_a_error_term)
dq_eta = q * eta_errors / etas

errors = np.sqrt(dq_vf ** 2 + dq_vr ** 2)

trial_number = np.arange(len(q))
plt.errorbar(trial_number, q, yerr=errors, fmt=".")
plt.show()
