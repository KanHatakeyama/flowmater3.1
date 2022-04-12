# parse lines in nodes of graphs

from .models import Graph, MediaFile
import itertools
import collections
from django.http import JsonResponse
import os
import re


# extract lines in a graph

def clean_line(line):
    for i in ['"', 'name=']:
        line = line.replace(i, "")

    line = line.replace("&#10;", "\n")
    return line


def extract_lines(str_graph):
    # extract texts
    raw_lines = re.findall('name=".*?"', str_graph, re.S)
    return [clean_line(i) for i in raw_lines]

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
    load_list = [{"name": f"load {p}_{t}", "freq": 1000}
                 for (t, p) in zip(title_list, pk_list)]

    # parse lines
    all_nested_line_list = [extract_lines(
        str_graph) for str_graph in str_graph_list]
    all_line_list = list(itertools.chain.from_iterable(all_nested_line_list))
    counter = collections.Counter(all_line_list)

    sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    line_frequency_list = [{"name": k, "freq": v} for (k, v) in sorted_counter]
    load_list.extend(line_frequency_list)

    return load_list


def parse_file_list(file_data):
    title_list = []
    pk_list = []

    for d in file_data:
        title_list.append(os.path.basename(d["upload"]))
        pk_list.append(d["id"])
        #time_list.append(d["created_at"].strftime('%Y-%m-%d %H:%M:%S'))

    # prepare load modules
    #load_list=[{"name": f"file {p}_{t}_{time}", "freq": 1000} for (t,p,time) in zip(title_list,pk_list,time_list)]
    load_list = [{"name": f"file {p}_{t}", "freq": 1000}
                 for (t, p) in zip(title_list, pk_list)]

    return load_list


# parse all lines in all graphs and return their line counts

# TODO: this would take a long time with large databases.
# cached data should be used instead in some cases (and avoid too much json data transfer)
def collect_all_graphs(request):

    current_line = request.GET['cl']
    upper_line = request.GET['ul']
    print(current_line, upper_line)

    graph_list = Graph.objects.all()
    graph_list = list(graph_list.values())
    frequency_list = graph_list_to_line_counts(graph_list)

    file_list = parse_file_list(list(MediaFile.objects.all().values()))
    # joblib.dump(file_list,"graph/debug/media.bin")

    frequency_list.extend(file_list)

    return JsonResponse(
        data=frequency_list,
        safe=False
    )
