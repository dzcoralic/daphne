// Linear regression model training.


import time
from api.python.context.daphne_context import DaphneContext
import sys 
r = 10**3
f = 10**5
daphne_context = DaphneContext()

# Data generation.
XY = daphne_context.rand(r, f, 0.0, 1.0, 1, -1)

# Extraction of X and y.
#X = XY[, seq(0, as.si64($c) - 2, 1)]
#y = XY[, fill(as.si64($c) - 1, 1, 1)]
# Linear regression model training (decisive part).
#X = (X - mean(X, 1)) / stddev(X, 1)
#X = cbind(X, fill(1.0, nrow(X), 1))
#lambda = fill(0.001, ncol(X), 1)
#A = t(X) @ X + diagMatrix(lambda)
#b = t(X) @ y;
#beta = solve(A, b);

# Result output.
#print(beta)