import numpy as np
from scipy.optimize import curve_fit

# Fitting functions
def time_func_1(kn_mesh, a, rcb, rci):
  (k, n)  = kn_mesh

  func = a + (k*n / (rcb + (k-1)*rci))

  return np.ravel(func)

def time_func_2(kn_mesh, a, rc):
  (k, n) = kn_mesh

  if k * rc >= 12350:
    func = a + k*n / 12350
  else:
    func = a + n / rc

  return np.ravel(func)

def time_func_3(kn_mesh, a, b):
  (k, n) = kn_mesh

  func = a + k*n*b

  return np.ravel(func)

# Max number of process pairs
p = 3

### Short
print('### Short messages (8B - 128B)\n')

# Independent variables, watch out for meshgrid parameter order
n = np.array([8, 16, 32, 64, 128])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[0.92, 1.10, 1.14],
  [0.92, 1.13, 1.17],
  [0.92, 1.15, 1.16],
  [1.09, 1.39, 1.29],
  [1.16, 1.42, 1.35]])
print('Measured data:')
print(data, '\n')

guess_vals = [0.9, 0.001]

fit_params, cov_mat = curve_fit(time_func_3, kn_mesh, np.ravel(data), p0=guess_vals, method='lm', sigma=sigma, absolute_sigma=True)
fit_errors = np.sqrt(np.diag(cov_mat))
fit_data = time_func_3(kn_mesh, *fit_params).reshape(data.shape)
print('Fitted data with function 3:')
print(fit_data, '\n')

fit_residual = data - fit_data
fit_rsq = 1 - np.var(fit_residual) / np.var(data)
print('Fit R-squared:', fit_rsq)
print('Fit a:', fit_params[0], '\u00b1', fit_errors[0])
print('Fit b:', fit_params[1], '\u00b1', fit_errors[1])
print('\n')

### Eager
print('### Eager messages (256B - 8KB)\n')

n = np.array([256, 512, 1024, 2048, 4096, 8192])
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[1.24, 1.38, 1.44],
  [1.35, 1.57, 1.64],
  [1.43, 1.67, 1.68],
  [1.64, 1.90, 1.88],
  [2.28, 2.53, 2.57],
  [3.00, 3.18, 3.18]])
print('Measured data:')
print(data, '\n')

guess_vals = [1.2, 50, 5]

fit_params, cov_mat = curve_fit(time_func_1, kn_mesh, np.ravel(data), p0=guess_vals, method='lm', sigma=sigma, absolute_sigma=True)
fit_errors = np.sqrt(np.diag(cov_mat))
fit_data = time_func_1(kn_mesh, *fit_params).reshape(data.shape)
print('Fitted data with function 1:')
print(fit_data, '\n')

fit_residual = data - fit_data
fit_rsq = 1 - np.var(fit_residual) / np.var(data)
print('Fit R-squared:', fit_rsq)
print('Fit a:', fit_params[0], '\u00b1', fit_errors[0])
print('Fit Rcb:', fit_params[1], '\u00b1', fit_errors[1])
print('Fit Rci:', fit_params[2], '\u00b1', fit_errors[2])
print('\n')

### Rendezvous
print('### Rendezvous messages (16KB - 4MB)\n')

n = np.array([16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304])
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[6.07, 6.42, 6.60],
  [8.10, 8.44, 8.48],
  [12.50, 12.76, 13.01],
  [18.94, 19.52, 19.93],
  [32.98, 34.32, 37.32],
  [63.25, 69.95, 76.35],
  [130.44, 141.50, 143.86],
  [267.83, 283.12, 291.97],
  [510.49, 541.64, 564.41]])
print('Measured data:')
print(data, '\n')

guess_vals = [4, 1000, 100]

fit_params, cov_mat = curve_fit(time_func_1, kn_mesh, np.ravel(data), p0=guess_vals, method='lm', sigma=sigma, absolute_sigma=True)
fit_errors = np.sqrt(np.diag(cov_mat))
fit_data = time_func_1(kn_mesh, *fit_params).reshape(data.shape)
print('Fitted data with function 1:')
print(fit_data, '\n')

fit_residual = data - fit_data
fit_rsq = 1 - np.var(fit_residual) / np.var(data)
print('Fit R-squared:', fit_rsq)
print('Fit a:', fit_params[0], '\u00b1', fit_errors[0])
print('Fit Rcb:', fit_params[1], '\u00b1', fit_errors[1])
print('Fit Rci:', fit_params[2], '\u00b1', fit_errors[2])
print('\n')
