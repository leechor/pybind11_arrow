import importlib
import os
import sys
from importlib import import_module
from importlib.util import find_spec as importlib_find


def cached_import(module_path, class_name):
    # Check whether module is loaded and fully initialized.
    module = module_import(module_path)
    return getattr(module, class_name)


def module_import(module_path):
    if not (
            (module := sys.modules.get(module_path))
            and (spec := getattr(module, "__spec__", None))
            and getattr(spec, "_initializing", False) is False
    ):
        module = import_module(module_path)
    return module


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err


def module_has_submodule(package, module_name):
    """See if 'module' is in 'package'."""
    try:
        package_name = package.__name__
        package_path = package.__path__
    except AttributeError:
        # package isn't a package.
        return False

    full_module_name = package_name + "." + module_name
    try:
        return importlib_find(full_module_name, package_path) is not None
    except ModuleNotFoundError:
        # When module_name is an invalid dotted path, Python raises
        # ModuleNotFoundError.
        return False


def module_dir(module):
    """
    Find the name of the directory that contains a module, if possible.

    Raise ValueError otherwise, e.g. for namespace packages that are split
    over several directories.
    """
    # Convert to list because __path__ may not support indexing.
    paths = list(getattr(module, "__path__", []))
    if len(paths) == 1:
        return paths[0]
    else:
        filename = getattr(module, "__file__", None)
        if filename is not None:
            return os.path.dirname(filename)
    raise ValueError("Cannot determine directory containing %s" % module)


class ModuleInfo:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.module_name = os.path.basename(file_path)
        self.spec = importlib.util.spec_from_file_location(self.module_name, file_path)
        self.module = importlib.util.module_from_spec(self.spec)

    def load(self):
        sys.modules[self.module_name] = self.module
        self.spec.loader.exec_module(self.module)

    def reload(self):
        self.load()

    def remove(self):
        module = self.module
        del sys.modules[self.module_name]
        del module


if __name__ == '__main__':
    mu = ModuleInfo(r'D:\project\simul\hello.py')
    mu.load()
    mu.module.hello()
    mu.remove()
    mu.reload()
    mu.module.hello()
