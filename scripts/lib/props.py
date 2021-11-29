import importlib.util
import os
import sys


def load_props(filename):
    props = {}

    if os.path.exists(filename):
        spec = importlib.util.spec_from_file_location("props", filename)
        module = importlib.util.module_from_spec(spec)
        sys.modules["props"] = module
        spec.loader.exec_module(module)

        for name, value in vars(module).items():
            if not name.startswith('_'):
                props[name] = value

    return props
