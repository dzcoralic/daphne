# Copyright 2021 The DAPHNE Consortium
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# *****************************************************************************
# CallData library
# *****************************************************************************

set(SOURCES CallData.cpp)
set(LIBS Proto)

add_library(CallData ${SOURCES})
target_link_libraries(CallData PRIVATE ${LIBS})


# *****************************************************************************
# ProtoDataConverter library
# *****************************************************************************

set(SOURCES ProtoDataConverter.cpp)
set(LIBS DataStructures Proto)

add_library(ProtoDataConverter ${SOURCES})
target_link_libraries(ProtoDataConverter PRIVATE ${LIBS})

# *****************************************************************************
# WorkerImpl library
# *****************************************************************************

# FIXME: use DaphneIrExecutor target instead
set(SOURCES WorkerImpl.cpp ../../../compiler/execution/DaphneIrExecutor.cpp)

#source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})

get_property(dialect_libs GLOBAL PROPERTY MLIR_DIALECT_LIBS)
get_property(conversion_libs GLOBAL PROPERTY MLIR_CONVERSION_LIBS)
set(LIBS
        ${dialect_libs}
        ${conversion_libs}
        MLIRDaphne
        MLIRDaphneTransforms
        MLIRExecutionEngine
        #DaphneIrExecutor
        DataStructures
        IO
        ProtoDataConverter
        CallData
        Proto
        )

add_library(WorkerImpl ${SOURCES})
#llvm_update_compile_flags(WorkerImpl)
target_link_libraries(WorkerImpl PRIVATE ${LIBS})
#mlir_check_all_link_libraries(WorkerImpl)

# *****************************************************************************
# DistributedWorker executable
# *****************************************************************************

add_executable(DistributedWorker main.cpp)
target_link_libraries(DistributedWorker
        PRIVATE
        Proto
        WorkerImpl
        MLIRDaphne)