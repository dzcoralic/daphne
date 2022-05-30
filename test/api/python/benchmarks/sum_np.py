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

ftime = time.time_ns()
dim = int(sys.argv[1])
t_gen = time.time_ns()
m1 = np.array(np.random.randint(100, size=dim*dim)+1.01, dtype=np.double)
m1.shape = (dim, dim)
t_gen = time.time_ns()-t_gen
t = time.time_ns()
m1 = m1+m1
print("Time to add:")
print(time.time_ns()-t)
t = time.time_ns()

sum = np.sum(m1)
print("Time to sum: ")
print((time.time_ns()-t))
print("res: 0")
print(time.time_ns()-t)
print("npgen time:")
print(t_gen)
print("ftime:")
print(time.time_ns()-ftime)
