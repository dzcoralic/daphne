
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
import numpy as np
import sys 


r=10000
c=10000
f=20
i=1
X = np.array(np.random.uniform(0.0,1.0, size=[r,f]), dtype=np.double)
C = np.array(np.random.uniform(0.0,1.0, size=[c,f]), dtype=np.double)
X.shape = (r, f)
C.shape = (c, f)
t = time.time_ns()
for j in range(0,i):
    CC = C**2
    CC = np.sum(CC,axis=0)
    D = np.add(np.dot(np.matmul(X, np.transpose(C)),-2.0),np.transpose(np.sum(CC)))
    print(np.matmul(X, np.transpose(C)))
    minD = np.fmin(D,0)
    print((minD))
    P = (D <= minD).astype(int)
    if(np.sum(P)!=0):
        P = np.divide(P, np.sum(P))

    P_denom = np.sum(P, axis=1)
    C = np.divide((np.matmul(np.transpose(P),X)),np.transpose(P_denom))
print("res: 0") 
print(time.time_ns()-t)