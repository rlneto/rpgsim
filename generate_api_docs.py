import os
import sys
import inspect
import importlib

sys.path.insert(0, os.path.abspath('.'))

def get_module_docstring(module):
    """Gets the docstring of a module."""
    return inspect.getdoc(module)

def get_class_docstrings(module):
    """Gets the docstrings of classes in a module."""
    docstrings = ""
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__ == module.__name__:
            docstrings += f"### class `{name}`\n\n"
            docstrings += f"{inspect.getdoc(obj) or ''}\n\n"
            for func_name, func_obj in inspect.getmembers(obj):
                if inspect.isfunction(func_obj) and not func_name.startswith("_"):
                    docstrings += f"#### `{func_name}`\n\n"
                    docstrings += f"{inspect.getdoc(func_obj) or ''}\n\n"
                    try:
                        sig = inspect.signature(func_obj)
                        docstrings += f"**Signature:** `{func_name}{sig}`\n\n"
                    except ValueError:
                        docstrings += f"**Signature:** Could not determine signature for `{func_name}`\n\n"
    return docstrings

def get_function_docstrings(module):
    """Gets the docstrings of functions in a module."""
    docstrings = ""
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__module__ == module.__name__ and not name.startswith("_"):
            docstrings += f"### `{name}`\n\n"
            docstrings += f"{inspect.getdoc(obj) or ''}\n\n"
            try:
                sig = inspect.signature(obj)
                docstrings += f"**Signature:** `{name}{sig}`\n\n"
            except ValueError:
                docstrings += f"**Signature:** Could not determine signature for `{name}`\n\n"

    return docstrings

def generate_doc(system_name):
    """Generates the documentation for a system."""
    system_path = os.path.join("core", "systems", system_name)
    doc_content = f"# {system_name.capitalize()} System\n\n"

    for root, _, files in os.walk(system_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(module_path.replace(os.sep, '.'))[0]

                try:
                    module = importlib.import_module(module_name)
                    doc_content += f"## `{file}`\n\n"
                    doc_content += (get_module_docstring(module) or '') + "\n\n"
                    doc_content += "### Classes\n\n"
                    doc_content += get_class_docstrings(module)
                    doc_content += "### Functions\n\n"
                    doc_content += get_function_docstrings(module)
                except Exception as e:
                    doc_content += f"## `{file}`\n\n"
                    doc_content += f"Error loading module `{module_name}`: {e}\n\n"

    with open(os.path.join("docs", "api", f"{system_name}.md"), "w") as f:
        f.write(doc_content)

if __name__ == "__main__":
    systems = [d for d in os.listdir(os.path.join("core", "systems")) if os.path.isdir(os.path.join("core", "systems", d)) and not d.startswith("__") and d != "city_management"]
    for system in systems:
        generate_doc(system)
