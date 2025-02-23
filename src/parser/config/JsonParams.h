/*
 * Copyright 2021 The DAPHNE Consortium
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef SRC_PARSER_CONFIG_JSONPARAMS_H
#define SRC_PARSER_CONFIG_JSONPARAMS_H

#include <string>
#include <unordered_map>

/**
 * @brief A Container that contains names of JSON parameters for user
 * configuration.
 */
struct DaphneConfigJsonParams {
    inline static const std::string USE_CUDA = "use_cuda";
    inline static const std::string USE_VECTORIZED_EXEC = "use_vectorized_exec";
    inline static const std::string USE_OBJ_REF_MGNT = "use_obj_ref_mgnt";
    inline static const std::string CUDA_FUSE_ANY = "cuda_fuse_any";
    inline static const std::string VECTORIZED_SINGLE_QUEUE = "vectorized_single_queue";

    inline static const std::string DEBUG_LLVM = "debug_llvm";
    inline static const std::string EXPLAIN_KERNELS = "explain_kernels";
    inline static const std::string EXPLAIN_LLVM = "explain_llvm";
    inline static const std::string EXPLAIN_PARSING = "explain_parsing";
    inline static const std::string EXPLAIN_PROPERTY_INFERENCE = "explain_property_inference";
    inline static const std::string EXPLAIN_SQL = "explain_sql";
    inline static const std::string EXPLAIN_VECTORIZED = "explain_vectorized";
    inline static const std::string EXPLAIN_OBJ_REF_MGNT = "explain_obj_ref_mgnt";
    inline static const std::string TASK_PARTITIONING_SCHEME = "taskPartitioningScheme";
    inline static const std::string NUMBER_OF_THREADS = "numberOfThreads";
    inline static const std::string MINIMUM_TASK_SIZE = "minimumTaskSize";

    inline static const std::string CUDA_DEVICES = "cuda_devices";

    inline static const std::string LIB_DIR = "libdir";
    inline static const std::string LIBRARY_PATHS = "library_paths";

    inline static const std::string JSON_PARAMS[] = {
            USE_CUDA,
            USE_VECTORIZED_EXEC,
            USE_OBJ_REF_MGNT,
            CUDA_FUSE_ANY,
            VECTORIZED_SINGLE_QUEUE,
            DEBUG_LLVM,
            EXPLAIN_KERNELS,
            EXPLAIN_LLVM,
            EXPLAIN_PARSING,
            EXPLAIN_PROPERTY_INFERENCE,
            EXPLAIN_SQL,
            EXPLAIN_VECTORIZED,
            EXPLAIN_OBJ_REF_MGNT,
            TASK_PARTITIONING_SCHEME,
            NUMBER_OF_THREADS,
            MINIMUM_TASK_SIZE,
            CUDA_DEVICES,
            LIB_DIR,
            LIBRARY_PATHS
    };
};

#endif
