import inspect
import json
import DeltaX2Lib

def get_class_methods(module):
    classes = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            methods = [method for method, _ in inspect.getmembers(obj, inspect.isfunction)]
            classes[name] = methods
    return classes

def generate_json_file():
    classes = get_class_methods(DeltaX2Lib)
    data = {
        "DeltaX2Lib": {
            "classes": classes
        }
    }
    with open('keywords.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    generate_json_file()
