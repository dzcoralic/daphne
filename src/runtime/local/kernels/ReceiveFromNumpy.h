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

#ifndef SRC_RUNTIME_LOCAL_KERNELS_RECEIVEFROMNUMPY_H
#define SRC_RUNTIME_LOCAL_KERNELS_RECEIVEFROMNUMPY_H

#include <runtime/local/context/DaphneContext.h>
#include <runtime/local/datastructures/CSRMatrix.h>
#include <runtime/local/datastructures/DataObjectFactory.h>
#include <runtime/local/datastructures/DenseMatrix.h>

#include <algorithm>
#include <random>
#include <set>
#include <type_traits>

#include <cassert>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <chrono>
#include <sys/time.h>

// ****************************************************************************
// Struct for partial template specialization
// ****************************************************************************

template<class DTRes>
struct ReceiveFromNumpy {
    static void apply(DTRes *& res,  int64_t upper, int64_t lower, int64_t rows, int64_t cols, DCTX(ctx)) = delete;
};

// ****************************************************************************
// Convenience function
// ****************************************************************************

template<class DTRes>
void receiveFromNumpy(DTRes *& res,  int64_t upper, int64_t lower, int64_t rows, int64_t cols, DCTX(ctx)) {
    ReceiveFromNumpy<DTRes>::apply(res, upper, lower, rows, cols, ctx);
}



// ****************************************************************************
// (Partial) template specializations for different data/value types
// ****************************************************************************

// ----------------------------------------------------------------------------
// DenseMatrix
// ----------------------------------------------------------------------------

struct NoOpDeleter {
    void operator()(double* p) {
        // don't delete p because the memory comes from numpy
    }
    void operator()(float* p){}
    void operator()(int32_t* p){}
    void operator()(int8_t* p){}
    void operator()(int64_t* p){}
    void operator()(uint64_t* p){}
    void operator()(uint32_t* p){}
    void operator()(uint8_t* p){}
};

template<typename VT>
struct ReceiveFromNumpy<DenseMatrix<VT>> {
    static void apply(DenseMatrix<VT> *& res, int64_t upper, int64_t lower, int64_t rows, int64_t cols, DCTX(ctx)) {
    
        struct timespec tv;
        clock_gettime(CLOCK_MONOTONIC_RAW,&tv);
        uint64_t time_before = (uint64_t)(tv.tv_sec)*1000000000+(uint64_t)(tv.tv_nsec);
        res = DataObjectFactory::create<DenseMatrix<VT>>(rows, cols, std::shared_ptr<VT[]>((VT*)((upper<<32)|lower), NoOpDeleter()));
        
        clock_gettime(CLOCK_MONOTONIC_RAW,&tv);
        uint64_t time_after =(uint64_t)(tv.tv_sec)*1000000000+(uint64_t)(tv.tv_nsec);
        printf("Time to receive data from numpy:\n%lld\n", (time_after-time_before));
    }
};


#endif //SRC_RUNTIME_LOCAL_KERNELS_RECEIVEFROMNUMPY_H
