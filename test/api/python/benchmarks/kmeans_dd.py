
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
#mat1 = sys.argv[1]
#mat2 = sys.argv[2]

t = time.time_ns()
r = int(sys.argv[1]) # and 1000000 # number of records (rows in X)
f = int(sys.argv[2])                 # number of features (columns in X and C)
c = int(sys.argv[3])                    # number of centroids (rows in C)
i = int(sys.argv[4])         # number of iterations

daphne_context = DaphneContext()
X = daphne_context.rand(r,f,0.0,1.0,1,1)
C = daphne_context.rand(c,f,0.0,1.0,1,1)

#C = daphne_context.getData(mat2)

for j in range(0,i):
    D = (X @ C.t()) * -2.0 + (C * C).sum(0).t() 
    minD = D.aggMin(0)
    P = D <= minD
    P = P / P.sum(0)
    P_denom = P.sum(1)
    C = (P.t() @ X) / P_denom.t()

C.compute()
print(time.time_ns()-t)
