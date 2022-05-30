
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

import time
from api.python.context.daphne_context import DaphneContext
import sys 
import numpy as np

r=1000000 # and 1000000 # number of records (rows in X)
c=5                    # number of centroids (rows in C)
f=1000                 # number of features (columns in X and C)
i=20                   # number of iterations
daphne_context = DaphneContext()

X = daphne_context.getData("mat1_k.csv").compute()
C = daphne_context.getData("mat2_k.csv").compute()

X.shape = (r, f)
C.shape = (c, f)
t = time.time_ns()
for j in range(0,i):
    CC = np.power(C,2)
    CC = np.sum(CC,axis=1, keepdims=True)
    D = np.add(np.multiply(np.matmul(X, np.transpose(C)),-2.0),np.transpose(CC))
    minD = np.amin(D, axis=1, keepdims=True)

    P = (D <= minD).astype(int)
    P = np.divide(P, np.sum(P, axis=1, keepdims=True))

    P_denom = np.sum(P, axis=0, keepdims=True)

    pz = np.matmul(np.transpose(P),X)
    #np.seterr(invalid="ignore")
    C = np.divide((pz),np.transpose(P_denom))
print("res: 0")
print(time.time_ns()-t)
