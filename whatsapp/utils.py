def replace_shortcodes(template, data):
    result = template
    for key, value in data.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result
