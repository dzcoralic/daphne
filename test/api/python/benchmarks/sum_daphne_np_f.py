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


import sys
import numpy as np
import time
from api.python.context.daphne_context import DaphneContext
ftime = time.time_ns()
dim = int(sys.argv[1])
daphne_context = DaphneContext()
m1 = daphne_context.rand(rows=dim,cols=dim,min=1,max=5,sparsity=0.5,seed=123).compute(type="files")
m1.shape = (dim, dim)
t = time.time_ns()
m1 = m1+m1
print("Time to add:")
print(time.time_ns()-t)
t = time.time_ns()
print("Time to sum:")
np.sum(m1)
print(time.time_ns()-t)

print("ftime:")
print(time.time_ns()-ftime)
