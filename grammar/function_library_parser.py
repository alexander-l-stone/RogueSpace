def parse_library_file(module) -> dict:
    func_dict = {}
    for name, val in module.__dict__.items():
        if callable(val):
            func_dict[name] = val
    return func_dict