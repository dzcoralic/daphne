#include "runtime/local/io/DaphneLibResult.h"

static DaphneLibResult daphne_lib_res;

DaphneLibResult* getDaphneLibResult()
{
    return &daphne_lib_res;
}