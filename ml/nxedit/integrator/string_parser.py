import re


def parse_command(content: str):
    """
    e.g., content="temperature = 100 oC"

    title: temperature
    prop: 100
    unit oC
    """
    # parse line
    title = re.sub(" *=.*", "", content)

    vals = re.sub(".*= *", "", content)
    vals = vals.replace("%", " %")
    vals = vals.replace("r.t.", "25 oC")

    # normal numbers
    if re.match("[0-9\-]", vals):
        """
        unit = re.sub("[0-9, \-\.]* ", "", vals)
        prop = re.sub(" *[^0-9, \-\.]*", "", vals)

        # no unit vals
        if unit == prop:
            unit = ""
        """
        unit = re.sub(
            "[+-]?(?:\d+\.?\d*|\.\d+)(?:(?:[eE][+-]?\d+)|(?:\*10\^[+-]?\d+))?", "", vals)
        prop = vals.replace(unit, "").replace(" ", "")
        unit = re.sub("^\ ?", "", unit)

    else:
        # str vals
        unit = ""
        prop = vals
    # special cases
    if title in ["Date", "date"]:
        unit = ""
        prop = vals

    # if split with semicolons
    """
    e.g., unit,prop
    FROM: ('S/cm; S/cm', '7.93e-5S/cm;1.68e-4S/cm')
    TO: ('S/cm;S/cm', '7.93e-5;1.68e-4')

    """
    if prop.find(";"):
        unit = unit.replace(" ", "")
        prop = prop.replace(" ", "")

        actual_unit = unit.split(";")[0]
        prop = prop.replace(actual_unit, "")

    return title, prop, unit


def clean_line(content):
    # remove extra spaces at start and end
    rep_content = re.sub("^ *", "", content)
    rep_content = re.sub(" *$", "", rep_content)
    return rep_content
