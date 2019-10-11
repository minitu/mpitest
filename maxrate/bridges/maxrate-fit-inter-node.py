import numpy as np
from scipy.optimize import curve_fit

# Fitting functions
def time_func_1(kn_mesh, a, rcb, rci):
  (k, n)  = kn_mesh

  func = a + (k*n / (rcb + (k-1)*rci))

  return np.ravel(func)

def time_func_2(kn_mesh, a, rc):
  (k, n) = kn_mesh

  func = a + (k*n / min(12350, k*rc))

  return np.ravel(func)

def time_func_3(kn_mesh, a, b):
  (k, n) = kn_mesh

  func = a + k*n*b

  return np.ravel(func)

# Max number of process pairs
p = 2

### Short
print('### Short messages (8B - 512B)\n')

# Independent variables, watch out for meshgrid parameter order
n = np.array([8, 16, 32, 64, 128, 256, 512])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[1.34, 1.40],
  [1.60, 1.88],
  [1.52, 1.86],
  [1.56, 1.86],
  [2.13, 2.28],
  [2.18, 2.37],
  [2.31, 2.52]])
print('Measured data:')
print(data, '\n')

guess_vals = [1.5, 10, 1]

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

guess_vals = [1.5, 10000]

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
print('### Eager messages (1024B - 128KB)\n')

n = np.array([1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[2.57, 2.84],
  [3.30, 3.41],
  [4.01, 4.66],
  [6.18, 7.18],
  [13.34, 14.41],
  [17.74, 18.64],
  [32.93, 33.55],
  [56.26, 79.73]])
print('Measured data:')
print(data, '\n')

guess_vals = [2, 1000, 10]

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
print('### Rendezvous messages (256KB - 4MB)\n')

n = np.array([262144, 524288, 1048576, 2097152, 4194304])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[88.26, 110.90],
  [109.83, 178.35],
  [196.68, 343.17],
  [337.16, 674.26],
  [710.97, 1334.90]])
print('Measured data:')
print(data, '\n')

guess_vals = [80, 10000, 1000]

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
