#include <pybind11/pybind11.h>
#include <arrow/python/pyarrow.h>
#include "arrow_conversions.h"
#include <arrow/table.h>
#include <iostream>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
const std::string modelName = "pd_func";

int add(int i, int j) {
    return i + j;
}


std::shared_ptr<arrow::Table> castToArrow(py::object df) {
    py::object dataframe_to_arrow = py::module_::import(modelName).attr("dataframe_to_arrow");
    py::object src = dataframe_to_arrow(df);
    PyObject *source = src.ptr();

    if (!arrow::py::is_table(source))
        return nullptr;

    arrow::Result<std::shared_ptr<arrow::Table>> result = arrow::py::unwrap_table(source);
    if (!result.ok())
        return nullptr;
    auto value = std::static_pointer_cast<arrow::Table>(result.ValueOrDie());
    return value;
}

py::object castToDataFrame(std::shared_ptr<arrow::Table> src) {
    return py::reinterpret_steal<py::object>(arrow::py::wrap_table(src));
}

// Convert pyarrow table to native C++ object and print its contents
void print_table(std::shared_ptr<arrow::Table> table)
{
//    std::shared_ptr<arrow::Table> table = castToArrow(df);
    if (table == nullptr) {
        std::cout<< "Table pointer is nullptr";
        return;
    }

    std::cout << "Table schema: " << std::endl;
    std::cout << table->schema()->ToString() << std::endl;
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
        auto pd_func = py::module_::import(modelName).attr("print_df");

       pd_func(df);
       return df;
       }, R"pbdoc(
        printDf function
    )pbdoc");

    m.def("castToArrow", &castToArrow);
    m.def("castToDataFrame", &castToDataFrame);
    m.def("print_table", &print_table);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
