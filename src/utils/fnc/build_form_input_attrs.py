def build_form_input_attrs(key):
    return {
        "id": key,
        "aria-describedby": "{}_errors".format(key),
        "class": "form-control",
    }