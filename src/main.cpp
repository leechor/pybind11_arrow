#include <pybind11/pybind11.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
using namespace pybind11::literals;
//py::object DataFrame = py::module_::import("pandas").attr("DataFrame");
//py::object print_df = py::module_::import("pd_func").attr("print_df");

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(python_example, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

    m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");

   m.def("mul", [](int i, int j) {return i * j; }, R"pbdoc(
        Multiply two numbers
   )pbdoc", "i"_a, "j"_a);

   m.def("printDf", [](py::object df) {
//        print_df(df);
        py::print(df);
        return df;
       }, R"pbdoc(
        printDf function
    )pbdoc");


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
