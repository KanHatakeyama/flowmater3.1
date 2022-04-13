import os
import re
import itertools
import collections

import joblib

# extract lines in a graph


def clean_line(line):
    for i in ['"', 'name=']:
        line = line.replace(i, "")

    line = line.replace("&#10;", "\n")
    return line


def extract_lines(str_graph):
    """


    word_list:
        list of words in the node data
    line_pair_list:
        pair of words in the node data
    """
    # extract texts from pbmn
    raw_texts = re.findall('name=".*?"', str_graph, re.S)
    lines_list = [clean_line(i).split("\n") for i in raw_texts]

    line_pair_list = []
    word_list = []

    for lines in lines_list:
        if len(lines) < 2:
            word_list.append(lines[0])
            continue

        for num, line in enumerate(lines):
            word_list.append(line)
            if num == 0:
                continue
            line_pair_list.append((lines[num-1], lines[num]))

    return word_list, line_pair_list


# extract lines in a graph


def graph_list_to_line_counts(all_data):
    """
    output example: 
    [
        {"name":"aa","e":12},
        {"name":"vb","e":22},
        {"name":"cc","e":32},
    ]
    """

    str_graph_list = []
    title_list = []
    pk_list = []

    for d in all_data:
        str_graph_list.append(d["graph"])
        title_list.append(d["title"])
        pk_list.append(d["id"])

    # prepare load modules
    load_list = [{"name": f"load {p}_{t}", "freq": 10}
                 for (t, p) in zip(title_list, pk_list)]

    #joblib.dump(str_graph_list, "lines.bin")

    # parse lines
    all_nested_line_list, all_nested_line_pair_list = zip(* [extract_lines(
        str_graph) for str_graph in str_graph_list])
    all_line_list = list(itertools.chain.from_iterable(all_nested_line_list))
    all_line_pair_list = list(
        itertools.chain.from_iterable(all_nested_line_pair_list))

    print(all_line_pair_list)

    # process lines
    counter = collections.Counter(all_line_list)
    sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    line_frequency_list = [{"name": k, "freq": v} for (k, v) in sorted_counter]
    load_list.extend(line_frequency_list)

    # process line pairs
    pair_counter = collections.Counter(all_line_pair_list)
    sorted_pair_counter = sorted(pair_counter.items(), key=lambda x: x[1], reverse=True)
    pair_frequency_list = [{"name": k, "freq": v} for (k, v) in sorted_pair_counter]


    return load_list,pair_frequency_list


def parse_file_list(file_data):
    title_list = []
    pk_list = []

    for d in file_data:
        title_list.append(os.path.basename(d["upload"]))
        pk_list.append(d["id"])

    # prepare load modules
    load_list = [{"name": f"file {p}_{t}", "freq": 1000}
                 for (t, p) in zip(title_list, pk_list)]

    return load_list
