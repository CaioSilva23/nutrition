def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()
