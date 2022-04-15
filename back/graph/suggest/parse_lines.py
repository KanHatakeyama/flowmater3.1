# parse lines in nodes of graphs

from ..models import Graph, MediaFile
from .data_parser import graph_list_to_line_counts, parse_file_list
from django.http import JsonResponse
import time

# to cache DB info
last_call_time = time.time()
COOL_TIME = 30
frequency_list = []
pair_frequency_list = []
MAX_SUGGESTIONS = 10


# parse all lines in all graphs and return their line counts
# CAUTION: no authorization needed!
def calc_suggest_data(request):
    global frequency_list, pair_frequency_list, last_call_time, COOL_TIME

    current_line = request.GET['cl']
    upper_line = request.GET['ul']
    current_time = time.time()

    # reload whole DB after cool time
    if len(frequency_list) == 0 or (current_time-last_call_time) > COOL_TIME:

        # load graph data
        graph_list = Graph.objects.all().order_by("-updated_at")
        graph_list = list(graph_list.values())

        # calc frequency info
        frequency_list, pair_frequency_list = graph_list_to_line_counts(
            graph_list)

        # extend file data
        file_list = parse_file_list(
            list(MediaFile.objects.all().order_by("-updated_at").values()))
        frequency_list.extend(file_list)

        last_call_time = current_time

    filt_list = []
    name_list = []

    # normal search
    if current_line != "":
        for i in frequency_list:
            if i["name"].startswith(current_line):
                name = i["name"]
                if name not in name_list:
                    filt_list.append(({"name": name, "freq": i["freq"]}))
                    name_list.append(name)

    # if the current field is blank
    else:
        for i in pair_frequency_list:
            if i["name"][0].startswith(upper_line):
                name = i["name"][1]
                if name not in name_list:
                    filt_list.append(({"name": name, "freq": i["freq"]}))
                    name_list.append(name)

    return JsonResponse(
        # data=frequency_list,
        data=filt_list[:MAX_SUGGESTIONS],
        safe=False
    )
