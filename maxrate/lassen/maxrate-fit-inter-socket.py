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
print('### Short messages (8B - 128B)\n')

# Independent variables, watch out for meshgrid parameter order
n = np.array([8, 16, 32, 64, 128])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([
  [0.97, 1.26],
  [0.98, 1.25],
  [0.99, 1.23],
  [1.13, 1.34],
  [1.12, 1.33]])
print('Measured data:')
print(data, '\n')

guess_vals = [1, 10, 1]

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
print('### Eager messages (256B - 64KB)\n')

n = np.array([128, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([
  [1.28, 1.43],
  [1.45, 1.57],
  [1.50, 1.66],
  [1.70, 1.84],
  [2.21, 2.56],
  [2.96, 3.17],
  [6.99, 7.58],
  [8.73, 9.15],
  [13.15, 13.80]])
print('Measured data:')
print(data, '\n')

guess_vals = [1, 1000, 10]

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
print('### Rendezvous messages (128KB - 4MB)\n')

n = np.array([131072, 262144, 524288, 1048576, 2097152, 4194304])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([
  [19.47, 20.57],
  [33.27, 35.68],
  [62.92, 70.98],
  [129.45, 142.53],
  [267.01, 285.44],
  [490.02, 530.91]])
print('Measured data:')
print(data, '\n')

guess_vals = [20, 10000, 1000]

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
