
#!/usr/bin/python

# -------------------------------------------------------------
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# -------------------------------------------------------------

from re import M
import time
from api.python.context.daphne_context import DaphneContext
import sys 
import numpy as np

r=10000 # and 1000000 # number of records (rows in X)
c=5                    # number of centroids (rows in C)
f=1000                 # number of features (columns in X and C)
i=20                   # number of iterations
daphne_context = DaphneContext()
m1 = np.genfromtxt("mat1.csv", delimiter=",")
m2 = np.genfromtxt("mat2.csv", delimiter=",")
m1.shape = (r, f)
m2.shape = (c, f)
X = daphne_context.from_numpy_ctypes(m1)
C = daphne_context.from_numpy_ctypes(m2)
t = time.time_ns()
for j in range(0,i):
    D = (X @ C.t()) * -2.0 + (C * C).sum(0).t() 
    minD = D.aggMin(0)
    P = D <= minD
    P = P / P.sum(0)
    P_denom = P.sum(1)
    C = (P.t() @ X) / P_denom.t()

C.compute()
print(time.time_ns()-t)
