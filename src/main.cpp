#include <pybind11/pybind11.h>
#include <arrow/python/pyarrow.h>
#include "arrow_conversions.h"
#include <arrow/table.h>
#include <iostream>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

int add(int i, int j) {
    return i + j;
}

// Convert pyarrow table to native C++ object and print its contents
void print_table(std::shared_ptr<arrow::Table> &table)
{
    // print table
    std::cout << "Table schema: " << std::endl;
    std::cout << table->schema()->ToString() << std::endl;
    std::cout << "Table columns: " << std::endl;
    for (int i = 0; i < table->num_columns(); i++)
    {
        std::cout << "Column " << i << ": " << std::endl;
        std::cout << table->column(i)->ToString() << std::endl;
    }
}

PYBIND11_MODULE(python_example, m) {

using namespace pybind11::literals;


    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    if (arrow::py::import_pyarrow())
        throw std::runtime_error("Failed to initialize PyArrow");

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
        py::object DataFrame = py::module_::import("pandas").attr("DataFrame");
        auto pd_func = py::module_::import("pd_func").attr("print_df");

       py::print(pd_func(df));
       return df;
       }, R"pbdoc(
        printDf function
    )pbdoc");

    m.def("print_table", &print_table, pybind11::call_guard<pybind11::gil_scoped_release>());


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
