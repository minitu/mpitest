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
p = 6

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

data = np.array([[1.48, 1.51, 1.43, 1.56, 1.62, 1.67],
  [1.47, 1.51, 1.55, 1.56, 1.56, 1.55],
  [1.49, 1.53, 1.56, 1.55, 1.56, 1.57],
  [1.52, 1.69, 1.70, 1.82, 1.78, 1.81],
  [1.60, 1.72, 1.79, 1.79, 1.86, 1.85]])
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
print('### Eager messages (256B - 64KB)\n')

n = np.array([512, 1024, 2048, 4096, 8192, 16384, 32768, 65536])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[2.22, 2.36, 2.35, 2.41, 2.55, 2.44],
  [2.45, 2.52, 2.61, 2.77, 2.75, 2.90],
  [3.13, 3.16, 3.10, 3.14, 3.30, 3.40],
  [3.79, 3.93, 4.32, 4.69, 5.20, 5.51],
  [5.23, 5.26, 5.67, 6.15, 6.65, 7.19],
  [7.08, 7.55, 8.49, 9.21, 9.57, 10.84],
  [9.50, 10.47, 12.10, 13.48, 15.47, 18.70],
  [12.43, 15.39, 19.84, 23.41, 28.31, 32.74]])
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
print('### Rendezvous messages (128KB - 4MB)\n')

n = np.array([131072, 262144, 524288, 1048576, 2097152, 4194304])
k = np.arange(p)+1
kn_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(p):
    sigma = np.append(sigma, [np.sqrt(i)])

data = np.array([[20.44, 30.83, 40.81, 50.63, 60.47, 71.56],
    [31.56, 51.86, 72.73, 93.18, 113.95, 137.13],
    [52.85, 94.89, 137.72, 184.13, 222.62, 263.16],
    [99.09, 181.79, 264.48, 348.34, 429.74, 519.82],
    [191.07, 351.34, 516.33, 681.90, 852.71, 1025.47],
    [374.65, 690.66, 1021.88, 1354.93, 1698.60, 2042.48]])
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
