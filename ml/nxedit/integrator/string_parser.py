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
        unit = re.sub("[0-9, \-\.]* ", "", vals)
        prop = re.sub(" *[^0-9, \-\.]*", "", vals)

        # no unit vals
        if unit == prop:
            unit = ""
    else:
        # str vals
        unit = ""
        prop = vals

    # special cases
    if title in ["Date", "date"]:
        unit = ""
        prop = vals

    return title, prop, unit


def clean_line(content):
    # remove extra spaces at start and end
    rep_content = re.sub("^ *", "", content)
    rep_content = re.sub(" *$", "", rep_content)
    return rep_content
