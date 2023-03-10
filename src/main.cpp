#include <pybind11/pybind11.h>
#include <arrow/python/pyarrow.h>
#include "arrow_conversions.h"
#include <arrow/table.h>
#include <pybind11/functional.h>
#include <iostream>
#include <pybind11/stl.h>

#include <arrow/csv/api.h>
#include <arrow/filesystem/localfs.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;
const char* pd_func_module = "src.app.tm.pd_func";

int add(int i, int j) {
    return i + j;
}

py::object invoke_by_json(std::string arg) {
    py::object pf =  py::module_::import(pd_func_module);
    py::object ibj = pf.attr("invoke_by_json");
    return ibj(arg);
}

py::object read_csv(std::string filePath) {
    arrow::io::IOContext io_context = arrow::io::default_io_context();
    arrow::fs::LocalFileSystem local_fs(
            arrow::fs::LocalFileSystemOptions::Defaults());
    auto result_ifstream = local_fs.OpenInputStream(filePath);
    if (!result_ifstream.ok()) {
        std::cout << "Failed to open file: " << filePath << std::endl;
    }
    std::shared_ptr<arrow::io::InputStream> input = result_ifstream.ValueOrDie();

    auto read_options = arrow::csv::ReadOptions::Defaults();
    auto parse_options = arrow::csv::ParseOptions::Defaults();
    auto convert_options = arrow::csv::ConvertOptions::Defaults();

    // Instantiate TableReader from input stream and options
    auto maybe_reader =
            arrow::csv::TableReader::Make(io_context,
                                          input,
                                          read_options,
                                          parse_options,
                                          convert_options);
    if (!maybe_reader.ok()) {
        // Handle TableReader instantiation error...
    }
    std::shared_ptr<arrow::csv::TableReader> reader = *maybe_reader;

    // Read table from CSV file
    auto maybe_table = reader->Read();
    if (!maybe_table.ok()) {
        // Handle CSV read error
        // (for example a CSV syntax error or failed type conversion)
    }
    std::shared_ptr<arrow::Table> table = *maybe_table;

    py::object arrow_to_dataframe = py::module_::import(pd_func_module).attr("arrow_to_dataframe");
    return arrow_to_dataframe(table);
}

std::string valid_regular_expression(std::string expression){
    py::object pyo = py::module_::import("src.app.tm.indicator");
    py::object func = pyo.attr("valid_expression");
    py::str result = func(expression);
    return result;
}

py::object invoke_m(py::object target, py::str name, py::args args, py::kwargs kwargs) {
    py::object iim = py::module_::import("app.tools.invoke_inject");
    py::object ii = iim.attr("invoke_m")(target, name, *args, **kwargs);
    return ii;
}

void load_module() {
    py::object module_loading = py::module_::import("app.tools.module_loading");
    py::object load_func = module_loading.attr("load_module");
    py::object mu = load_func("D:/project/simul/hello.py");
    mu.attr("hello")();
}

std::shared_ptr<arrow::Table> castToArrow(py::object df) {
    py::object dataframe_to_arrow = py::module_::import(pd_func_module).attr("dataframe_to_arrow");
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
        auto pd_func = py::module_::import(pd_func_module).attr("print_df");

       pd_func(df);
       return df;
       }, R"pbdoc(
        printDf function
    )pbdoc");

   m.def("testDataFrameC", []() {
      auto testDataFrame = py::module_::import("tests").attr("testDataFrame");
      auto np = py::module_::import("numpy");
      auto pd = py::module_::import("pandas");

      auto a = np.attr("random").attr("standard_normal")(py::make_tuple(2, 4));
      auto index = pd.attr("date_range")("2000-01-01", "periods"_a=2, "freq"_a="W-WED");
      auto frame = pd.attr("DataFrame")(a, "index"_a=index, "columns"_a=std::vector<std::string> {"Colorado", "Texas", "New York", "Ohio"});
      py::print(frame);
   });

    m.def("load_module", &load_module);
    m.def("castToArrow", &castToArrow);
    m.def("castToDataFrame", &castToDataFrame);
    m.def("print_table", &print_table);
    m.def("invoke_m", &invoke_m);
    m.def("valid_regular_expression", &valid_regular_expression);
    m.def("read_csv", &read_csv);



#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}

int main(){
    load_module();
}