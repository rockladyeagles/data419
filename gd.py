
# Let's create a super simple linear-ish data set, and fit a linear regression
# model to it 4 different ways:
#
# 1. By using the "Normal Equation" (with Moore-Penrose Pseudoinverse, as in
#   lrByHand.py)
# 2. By using sklearn's LinearRegression (duh).
# 3. By converging on the best coefficients/weights using Gradient Descent.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(123)

N = 1000    # number of training points. (Eschewing Géron's syntax)

np.set_printoptions(precision=4)
np.set_printoptions(floatmode='fixed')

true_int = 17
true_x0_slope = 2.43

print(f"True weights:    {np.array([true_int, true_x0_slope])}")

X = 2*np.random.rand(N,1)
y = true_int + true_x0_slope * X + np.random.normal(0,1,size=(N,1))


# 1. Use Normal Equation.
X = np.c_[np.ones((N,1)),X]    # Add column of ones

moore_penrose_pseudo_inv = np.linalg.inv(X.T @ X) @ X.T
weights_best = moore_penrose_pseudo_inv @ y
print(f"Normal equation: {weights_best.ravel()}")



# 2. Use sklearn's LinearRegression.
from sklearn.linear_model import LinearRegression
lr = LinearRegression(fit_intercept=False)
lr.fit(X,y)
print(f"sklearn LR:      {lr.coef_[0]}")



# 3. Use Gradient Descent.
# Start off with random (wacky) weights.
wacky_initial_intercept_guess = -94
wacky_initial_x0_slope_guess = 18.2
weights = np.array([[wacky_initial_intercept_guess],
    [wacky_initial_x0_slope_guess]])
eta = .15       # Our learning rate.
n_iter = 100   # We'll make this many adjustments to the weights.

# (Keep track of the weights as they're adjusted over time, for plotting.)
intercepts = np.empty(n_iter)
slopes = np.empty(n_iter)
intercepts[0] = weights[0]
slopes[0] = weights[1]

for i in range(1,n_iter):

    # Why is the gradient the following equation? Because if you symbolically
    #   differentiate the MSE (mean-squared error) surface generated by some
    #   value of the weights, these are your partial derivatives.
    gradient = 2/N * X.T @ (X @ weights - y)

    # Nudge our weights in the right direction, using eta as a learning rate.
    weights -= eta * gradient

    # (Record the new intercept and slope, for later plotting.)
    intercepts[i] = weights[0]
    slopes[i] = weights[1]

print(f"Gradient Desc:   {np.array([intercepts[-1],slopes[-1]])}")


fig, axs = plt.subplots(2,1)
axs[0].plot(intercepts)
axs[0].axhline(y=true_int, color="red")
axs[0].set_ylim(min(true_int, intercepts.min()) - 5,
    max(true_int,intercepts.max()) + 5)
axs[0].set_ylabel("Estimated intercept")
axs[1].plot(slopes)
axs[1].axhline(y=true_x0_slope, color="red")
axs[1].set_ylim(slopes.min() - 5, slopes.max() + 5)
axs[1].set_ylim(min(true_x0_slope, slopes.min()) - 5,
    max(true_x0_slope,slopes.max()) + 5)
axs[1].set_xlabel("Number of iterations")
axs[1].set_ylabel("Estimated x0 slope")
fig.suptitle("Gradient Descent -- weight convergence")
plt.show()
