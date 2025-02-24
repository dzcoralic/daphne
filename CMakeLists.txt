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

cmake_minimum_required(VERSION 3.17)

# use gcc 8 because CUDA broke on my Ubuntu 21.10
if (UNIX)
#    set(CMAKE_CUDA_HOST_COMPILER g++-8 CACHE INTERNAL "" FORCE)
    #    set(CMAKE_CUDA_HOST_COMPILER clang++ CACHE INTERNAL "" FORCE)
    set(CMAKE_CUDA_COMPILER /usr/local/cuda/bin/nvcc CACHE INTERNAL "" FORCE)
    #    set(CMAKE_CXX_COMPILER g++ CACHE INTERNAL "" FORCE)
endif()

# Build release version by default (override with -DCMAKE_BUILD_TYPE=Debug in your initial cmake invocation)
# This needs to be set *before* the project() command
set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build.")

project(daphne-prototype LANGUAGES CXX C)

set(CMAKE_BUILD_WITH_INSTALL_NAME_DIR ON)

set(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ standard to conform to")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS_DEBUG="${CMAKE_CXX_FLAGS_DEBUG} -O0")
# silence a warning about DEPFILE path transformations (used in LLVM)
cmake_policy(SET CMP0116 OLD)

# *****************************************************************************
# Related to MLIR/LLVM
# *****************************************************************************

find_package(MLIR REQUIRED CONFIG)

message(STATUS "Using MLIRConfig.cmake in: ${MLIR_DIR}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

set(LLVM_RUNTIME_OUTPUT_INTDIR ${CMAKE_BINARY_DIR}/bin)
set(LLVM_LIBRARY_OUTPUT_INTDIR ${CMAKE_BINARY_DIR}/lib)
set(MLIR_BINARY_DIR ${CMAKE_BINARY_DIR})

list(APPEND CMAKE_MODULE_PATH "${MLIR_CMAKE_DIR}")
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(TableGen)
include(AddLLVM)
include(AddMLIR)

# the next command needs to be guarded because it messes with compiler flags
if (CMAKE_BUILD_TYPE STREQUAL "Release")
    set(LLVM_ENABLE_ASSERTIONS OFF)
endif()

include(HandleLLVMOptions)

include_directories(${LLVM_INCLUDE_DIRS})
include_directories(${MLIR_INCLUDE_DIRS})

link_directories(${LLVM_BUILD_LIBRARY_DIR})
add_definitions(${LLVM_DEFINITIONS})

# Enable exception handling and run-time type information.
set(LLVM_ENABLE_EH ON)
set(LLVM_ENABLE_RTTI ON)

# *****************************************************************************
# Related to external libraries (OpenBLAS, CUDA, etc)
# *****************************************************************************

SET(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

include_directories(${OPENBLAS_INST_DIR}/include)
SET(OPENBLAS_LIBRARIES ${OPENBLAS_INST_DIR}/lib/libopenblas.a ${CMAKE_THREAD_LIBS_INIT})

# check <package>_ROOT env var
cmake_policy(SET CMP0074 NEW)

option(USE_CUDA "Whether to activate compilation of CUDA features" OFF)
include(CheckLanguage)
check_language(CUDA)
if(USE_CUDA AND CMAKE_CUDA_COMPILER)
    enable_language(CUDA)
    find_package(CUDAToolkit REQUIRED)
    set(CMAKE_CUDA_ARCHITECTURES  OFF)
    cmake_policy(SET CMP0104 NEW)
    add_definitions(-DUSE_CUDA)
    set(CMAKE_CUDA_STANDARD 17)
    set(CMAKE_CUDA_STANDARD_REQUIRED ON)
    message(STATUS "CUDA enabled (version ${CMAKE_CUDA_COMPILER_VERSION})")
endif()

option(USE_ARROW "Whether to activate compilation of Arrow/Parquet features" OFF)
if(USE_ARROW)
    find_package(Arrow CONFIG REQUIRED)
    find_package(Parquet CONFIG REQUIRED
        PATHS /usr/local/lib/cmake/arrow
        NO_DEFAULT_PATH
    )
    link_libraries(arrow_shared parquet_shared)
    add_definitions(-DUSE_ARROW)
    message(STATUS "Arrow/Parquet enabled")
endif()

# *****************************************************************************
# Project-specific include directories
# *****************************************************************************

include_directories(${PROJECT_SOURCE_DIR}/src)
include_directories(${PROJECT_BINARY_DIR}/src)

# *****************************************************************************
# Descend to subdirectories
# *****************************************************************************

add_subdirectory(src/api/cli)
add_subdirectory(src/compiler/execution)
add_subdirectory(src/compiler/explanation)
add_subdirectory(src/compiler/inference)
add_subdirectory(src/compiler/lowering)
add_subdirectory(src/ir/daphneir)
add_subdirectory(src/parser)
add_subdirectory(src/parser/config)
add_subdirectory(src/runtime/distributed/proto)
add_subdirectory(src/runtime/distributed/worker)
add_subdirectory(src/runtime/local/datastructures)
add_subdirectory(src/runtime/local/io)
add_subdirectory(src/runtime/local/kernels)
add_subdirectory(src/util)

add_subdirectory(test)
