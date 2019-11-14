import numpy as np

y = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 12, 10]]

m = np.shape(y)[1]

y = np.mat(y)

z = y * y.T

#m = np.shape(y)

a = np.argmax(y, axis=1)

print(np.insert(z, -1, [0], axis = 1))
print(np.append(z, [[0], [0]], axis = 1))
print(np.argmax(y, axis = 1))
print(np.max(y, axis = 1))
print(str(a[1]))