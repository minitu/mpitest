import numpy as np
from scipy.optimize import curve_fit

# Fitting functions
def time_func_old1(nk_mesh, a, rcb, rci):
  (n, k)  = nk_mesh

  func = a + (k*n / (rcb + (k-1)*rci))

  return np.ravel(func)

def time_func_old2(nk_mesh, a, b):
  (n, k) = nk_mesh

  func = a + k*n*b

  return np.ravel(func)

def time_func_old3(nk_mesh, a, rc):
  (n, k) = nk_mesh

  func = a + (k*n / min(12350, k*rc))

def time_func_new(nk_mesh, a, b1, b2, c1, c2):
  (n, k) = nk_mesh

  func = a + (n / ((b1*n + b2) + (k-1)*(c1*n + c2)))

  return np.ravel(func)

# For weighted error
'''
sigma = np.array([])
for i in n:
  for j in range(1,11):
    sigma = np.append(sigma, [np.sqrt(i)])
print(sigma)
'''

### Short
print('### Short messages (8B - 128B)\n')

# Independent variables, watch out for meshgrid parameter order
n = np.array([8, 16, 32, 64, 128])
k = np.arange(10)+1
nk_mesh = np.meshgrid(k,n)

data = np.array([[1.48, 1.51, 1.43, 1.56, 1.62, 1.67, 1.63, 1.58, 1.59, 1.60],
  [1.47, 1.51, 1.55, 1.56, 1.56, 1.55, 1.59, 1.57, 1.60, 1.58],
  [1.49, 1.53, 1.56, 1.55, 1.56, 1.57, 1.68, 1.57, 1.60, 1.57],
  [1.52, 1.69, 1.70, 1.82, 1.78, 1.81, 2.08, 2.26, 2.20, 2.12],
  [1.60, 1.72, 1.79, 1.79, 1.86, 1.85, 2.13, 2.27, 2.19, 2.23]])
print('Measured data:')
print(data, '\n')

# Old function 1
guess_vals_old1 = [1.5, 10, 1]

fit_params, cov_mat = curve_fit(time_func_old1, nk_mesh, np.ravel(data), p0=guess_vals_old1, method='lm')
fit_errors = np.sqrt(np.diag(cov_mat))
fit_data = time_func_old1(nk_mesh, *fit_params).reshape(data.shape)
print('Fitted data with old function 1:')
print(fit_data, '\n')

fit_residual = data - fit_data
fit_rsq = 1 - np.var(fit_residual) / np.var(data)
print('Fit R-squared:', fit_rsq)
print('Fit a:', fit_params[0], '\u00b1', fit_errors[0])
print('Fit Rcb:', fit_params[1], '\u00b1', fit_errors[1])
print('Fit Rci:', fit_params[2], '\u00b1', fit_errors[2])
print('\n')

'''
# Old function 2
guess_vals_old2 = [1.5, 0.1]

#fit_params, cov_mat = curve_fit(time_func_old2, nk_mesh, np.ravel(data), p0=guess_vals_old2, method='lm', sigma=sigma, absolute_sigma=True)
fit_params, cov_mat = curve_fit(time_func_old2, nk_mesh, np.ravel(data), p0=guess_vals_old2, method='lm')
fit_errors = np.sqrt(np.diag(cov_mat))
fit_data = time_func_old2(nk_mesh, *fit_params).reshape(data.shape)
print('Fitted data with old function 2:')
print(fit_data, '\n')

fit_residual = data - fit_data
fit_rsq = 1 - np.var(fit_residual) / np.var(data)
print('Fit R-squared:', fit_rsq)
print('Fit a:', fit_params[0], '\u00b1', fit_errors[0])
print('Fit b:', fit_params[1], '\u00b1', fit_errors[1])
print('\n')
'''

### Eager
print('### Eager messages (256B - 64KB)\n')

n = np.array([512, 1024, 2048, 4096, 8192, 16384, 32768, 65536])
k = np.arange(10)+1
nk_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(10):
    sigma = np.append(sigma, [np.sqrt(i)])
    #sigma = np.append(sigma, [i])
    #sigma = np.append(sigma, [1])

data = np.array([[2.22, 2.36, 2.35, 2.41, 2.55, 2.44, 2.62, 2.95, 2.81, 2.84],
  [2.45, 2.52, 2.61, 2.77, 2.75, 2.90, 2.85, 3.10, 3.08, 3.17],
  [3.13, 3.16, 3.10, 3.14, 3.30, 3.40, 3.54, 3.66, 3.75, 3.91],
  [3.79, 3.93, 4.32, 4.69, 5.20, 5.51, 6.16, 6.43, 6.94, 7.05],
  [5.23, 5.26, 5.67, 6.15, 6.65, 7.19, 7.51, 8.21, 8.57, 9.36],
  [7.08, 7.55, 8.49, 9.21, 9.57, 10.84, 11.35, 12.71, 13.04, 14.45],
  [9.50, 10.47, 12.10, 13.48, 15.47, 18.70, 17.08, 21.42, 21.26, 25.26],
  [12.43, 15.39, 19.84, 23.41, 28.31, 32.74, 34.33, 41.01, 41.41, 48.75]])
print('Measured data:')
print(data, '\n')

# Old function 1
guess_vals_old1 = [2, 1000, 10]

#fit_params, cov_mat = curve_fit(time_func_old1, nk_mesh, np.ravel(data), p0=guess_vals_old1, method='lm')
fit_params, cov_mat = curve_fit(time_func_old1, nk_mesh, np.ravel(data), p0=guess_vals_old1, method='lm', sigma=sigma, absolute_sigma=True)
fit_errors = np.sqrt(np.diag(cov_mat))
fit_data = time_func_old1(nk_mesh, *fit_params).reshape(data.shape)
print('Fitted data with old function 1:')
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
k = np.arange(10)+1
nk_mesh = np.meshgrid(k,n)

sigma = np.array([])
for i in n:
  for j in range(10):
    sigma = np.append(sigma, [np.sqrt(i)])
    #sigma = np.append(sigma, [i])
    #sigma = np.append(sigma, [1])

data = np.array([[20.44, 30.83, 40.81, 50.63, 60.47, 71.56, 81.44, 92.47, 101.48, 113.62],
    [31.56, 51.86, 72.73, 93.18, 113.95, 137.13, 160.77, 180.20, 197.12, 224.18],
    [52.85, 94.89, 137.72, 184.13, 222.62, 263.16, 309.28, 347.58, 396.45, 435.62],
    [99.09, 181.79, 264.48, 348.34, 429.74, 519.82, 603.56, 685.46, 772.83, 857.42],
    [191.07, 351.34, 516.33, 681.90, 852.71, 1025.47, 1195.35, 1362.23, 1535.92, 1706.70],
    [374.65, 690.66, 1021.88, 1354.93, 1698.60, 2042.48, 2378.50, 2722.02, 3061.10, 3399.56]])
print('Measured data:')
print(data, '\n')

# Old function 3
guess_vals_old3 = [20, 10000]

#fit_params, cov_mat = curve_fit(time_func_old1, nk_mesh, np.ravel(data), p0=guess_vals_old1, method='lm')
fit_params, cov_mat = curve_fit(time_func_old3, nk_mesh, np.ravel(data), p0=guess_vals_old3, method='lm', sigma=sigma, absolute_sigma=True)
fit_errors = np.sqrt(np.diag(cov_mat))
fit_data = time_func_old3(nk_mesh, *fit_params).reshape(data.shape)
print('Fitted data with old function 3:')
print(fit_data, '\n')

fit_residual = data - fit_data
fit_rsq = 1 - np.var(fit_residual) / np.var(data)
print('Fit R-squared:', fit_rsq)
print('Fit a:', fit_params[0], '\u00b1', fit_errors[0])
print('Fit Rcb:', fit_params[1], '\u00b1', fit_errors[1])
print('\n')

