
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

r = int(sys.argv[1]) 
c = int(sys.argv[2])   
daphne_context = DaphneContext()
XY = np.array(np.random.uniform(0.0,1.0, size=[r,c]), dtype=np.double)
t = time.time_ns()
XY =  daphne_context.from_numpy_ctypes(XY)
X = XY['',daphne_context.seq(0,c-2,1)]
y = XY['',daphne_context.fill(c-1,1,1)]
X = (X-X.mean(1))/X.stddev(1)
X = daphne_context.cbind(X, daphne_context.fill(1.0, X.nrow(),1))
lmbda = daphne_context.fill(0.001, X.ncol(),1)
A = (X.t() @ X) + lmbda.diagMatrix()
b = X.t() @ y
beta = A.solve(b)
beta.compute()
print(time.time_ns()-t)
