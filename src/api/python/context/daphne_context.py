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
# Modifications Copyright 2022 The DAPHNE Consortium
#
# -------------------------------------------------------------

__all__ = ["DaphneContext"]

import ctypes
from api.python.operator.nodes.frame import Frame
import pandas as pd
from api.python.script_building.dag import OutputType
from api.python.utils.consts import F32, F64, SI32, SI64, SI8, UI32, UI64, UI8, VALID_INPUT_TYPES, TMP_PATH
import numpy as np
from api.python.operator.nodes.matrix import Matrix
from api.python.operator.operation_node import OperationNode
from typing import Sequence, Dict, Union

class DaphneContext(object):
    #TODO: load data from numpy array
    def from_numpy(self, mat: np.array,
            *args: Sequence[VALID_INPUT_TYPES],
            **kwargs: Dict[str, VALID_INPUT_TYPES]) -> Matrix:
        """Generate DAGNode representing matrix with data given by a numpy array.
        :param mat: the numpy array
        :param args: unnamed parameters
        :param kwargs: named parameters
        :return: A Matrix
        """

        unnamed_params = ['"src/api/python/tmp/{file_name}.csv\"']

        unnamed_params.extend(args)
        named_params = []
        return Matrix(self, 'readMatrix', unnamed_params, named_params, local_data=mat)
    
    def getData(self, file) -> Matrix:
   
        
        unnamed_params = ['\"test/api/python/benchmarks/'+file+'\"']

        return Matrix(self, 'readMatrix', unnamed_params)
    
    def readMatrix(self, file) -> Matrix:
        """Read Matrix from a provided csv file.
        :param file: path to the csv file containing data
        :return: A Matrix
        """
        unnamed_params = ['\"'+file+'\"']
        return Matrix(self, 'readMatrix', unnamed_params)
        

    def readFrame(self, file) -> Matrix:
        """Read Frame from a provided csv file.
        :param file: path to the csv file containing data
        :return: A Frame
        """
        unnamed_params = ['\"'+file+'\"']
        return Frame(self, 'readMatrix', unnamed_params)
    
    def while_loop(self, condition, body):
        named_input_nodes = {'condition':condition}
        return OperationNode(self, 'while', named_input_nodes = named_input_nodes, unnamed_input_nodes = [body], output_type=OutputType.NONE)

    def from_numpy_ctypes(self, mat: np.array) -> Matrix:
        """Generate DAGNode representing matrix with data given by a numpy array.
        :param mat: the numpy array
        :param args: unnamed parameters
        :param kwargs: named parameters
        :return: A Matrix
        """
        address = mat.ctypes.data_as(np.ctypeslib.ndpointer(dtype=mat.dtype, ndim=1, flags='C_CONTIGUOUS')).value
        upper = (address & 0xFFFFFFFF00000000)>>32;
        lower = (address & 0xFFFFFFFF)
        d_type = mat.dtype
        if d_type == np.double or d_type == np.float64:          
            vtc = F64
        elif d_type == np.float32:
            vtc = F32
        elif d_type == np.int8:
            vtc = SI8
        elif d_type == np.int32:
            vtc = SI32
        elif d_type == np.int64:
            vtc = SI64
        elif d_type == np.uint8:
            vtc = UI8
        elif d_type == np.uint32:
            vtc = UI32
        elif d_type == np.uint64:
            vtc = UI64
        else:
            print("Error")
        
        return Matrix(self, 'receiveFromNumpy', [upper, lower, mat.shape[0],mat.shape[1], vtc], local_data=mat)

    def from_pandas(self, df: pd.DataFrame,
            *args: Sequence[VALID_INPUT_TYPES],
            **kwargs: Dict[str, VALID_INPUT_TYPES]) -> Frame:
        """Generate DAGNode representing Frame with data given by a numpy array.
        :param mat: the numpy array
        :param args: unnamed parameters
        :param kwargs: named parameters
        :return: A Frame
        """

        unnamed_params = ['"src/api/python/tmp/{file_name}.csv\"']

        unnamed_params.extend(args)
        named_params = []
        return Frame(self, 'readFrame', unnamed_params, named_params, local_data=df)
    
    def fill(self, arg, rows:int, cols:int) -> 'Matrix':
        named_input_nodes = {'arg':arg, 'rows':rows, 'cols':cols}
        return Matrix(self, 'fill', [], named_input_nodes=named_input_nodes)
    def seq(self, start, end, inc) -> 'Matrix':
        named_input_nodes = {'start':start, 'end':end, 'inc':inc}
        return Matrix(self, 'seq', [], named_input_nodes=named_input_nodes)

    def cbind(self, x, y) -> 'Matrix':
        return Matrix(self, 'cbind', [x,y])

    def rand(self, rows: int, cols: int,
            min: Union[float, int] = None, max: Union[float, int] = None,sparsity: Union[float, int] = 0, seed: Union[float, int] = 0
            ) -> 'Matrix':
        """Generates a matrix filled with random values
        :param rows: number of rows
        :param cols: number of cols
        :param min: min value for cells
        :param max: max value for cells
        :param sparsity: fraction of non-zero cells
        :param seed: random seed
        :return: A Matrix
        """
        if rows < 0:
            raise ValueError("In rand statement, can only assign rows a long (integer) value >= 0 "
                            "-- attempted to assign value: {r}".format(r=rows))
        if cols < 0:
            raise ValueError("In rand statement, can only assign cols a long (integer) value >= 0 "
                            "-- attempted to assign value: {c}".format(c=cols))
        #num of rows, cols, min, max, sparsity, seed
        named_input_nodes = {
            'rows': rows, 'cols': cols, 'min': min, 'max':max, 'sparsity':sparsity, 'seed':seed}
        if min is not None:
            named_input_nodes['min'] = min
        if max is not None:
            named_input_nodes['max'] = max
        if sparsity is not None:
            named_input_nodes['sparsity'] = sparsity
        if seed is not None:
            named_input_nodes['seed'] = seed

        return Matrix(self,'rand', [], named_input_nodes=named_input_nodes)