#include <climits>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#define XTENSOR_USE_XSIMD
#include "xtensor/xmath.hpp"              // xtensor import for the C++ universal functions
#define FORCE_IMPORT_ARRAY                // numpy C api loading
#include "xtensor-python/pyarray.hpp"     // Numpy bindings

// #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
// #include <numpy/arrayobject.h>
#include <Python.h>
#include <algorithm>
#include <xsimd/xsimd.hpp>
#include <xsimd/math/xsimd_scalar.hpp>

// py::array_t<int64_t> bin()
double sum_of_sines(xt::pyarray<double>& m)
{
    auto sines = xt::sin(m);  // sines does not actually hold values.
    return std::accumulate(sines.cbegin(), sines.cend(), 0.0);
}

using namespace std;


namespace xsimd {
    template <class T>
    inline T select(bool cond, const T& tru, const T& fal)
    {
        return cond ? tru : fal;
    }
    // template <class T>
    // inline T isnan(bool cond, const T& tru, const T& fal)
    // {
    //     std::isnan()
    // }
}

auto bin(xt::pyarray<double, xt::layout_type::row_major>& x, double xmin, double xmax, int width)//, xt::pyarray<int64_t>& counts) 
{
    auto indices = xt::pyarray<double, xt::layout_type::row_major>::from_shape(x.shape());
    double scale = 1./(xmax - xmin);
    xsimd::transform(x.begin(), x.end(), indices.begin(), 
        [&](auto x) {
            auto normalized = (x-xmin) * scale;
            auto indices = normalized * width + 2;
            using batch_type = std::decay_t<decltype(x)>;
            indices = xsimd::select(normalized > batch_type(1.), batch_type(width+3-1), batch_type(indices));
            indices = xsimd::select(normalized < batch_type(0.), batch_type(1.), batch_type(indices));
            indices = xsimd::select(isnan(x), batch_type(0.), batch_type(indices));
            return indices;
        });
    return indices;
}

auto bin_scalar(xt::pyarray<double, xt::layout_type::row_major>& x, double xmin, double xmax, int width)//, xt::pyarray<int64_t>& counts) 
{
    auto indices = xt::pyarray<double, xt::layout_type::row_major>::from_shape(x.shape());
    double scale = 1./(xmax - xmin);
    std::transform(x.begin(), x.end(), indices.begin(), 
        [&](auto x) {
            auto normalized = (x-xmin) * scale;
            auto indices = normalized * width + 2;
            using batch_type = std::decay_t<decltype(x)>;
            indices = xsimd::select(normalized > batch_type(1.), batch_type(width+3-1), batch_type(indices));
            indices = xsimd::select(normalized < batch_type(0.), batch_type(1.), batch_type(indices));
            indices = xsimd::select(isnan(x), batch_type(0.), batch_type(indices));
            return indices;
        });
    return indices;
}

PYBIND11_MODULE(xstats, m) {
    _import_array();
    m.doc() = "fast operations on string sequences";
    m.def("bin", &bin);
    m.def("bin_scalar", &bin_scalar);
    m.def("sum_of_sines", sum_of_sines, "Sum the sines of the input values");
}