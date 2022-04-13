# parse lines in nodes of graphs

from ..models import Graph, MediaFile
from .data_parser import graph_list_to_line_counts, parse_file_list
from django.http import JsonResponse
import time

# to cache DB info
last_call_time = time.time()
COOL_TIME = 30
frequency_list = []


# parse all lines in all graphs and return their line counts

def calc_suggest_data(request):
    global frequency_list, last_call_time, COOL_TIME

    current_line = request.GET['cl']
    upper_line = request.GET['ul']
    current_time = time.time()

    # reload whole DB after cool time
    if len(frequency_list) == 0 or (current_time-last_call_time) > COOL_TIME:
        print(current_line, upper_line)
        graph_list = Graph.objects.all()
        graph_list = list(graph_list.values())
        frequency_list = graph_list_to_line_counts(graph_list)
        file_list = parse_file_list(list(MediaFile.objects.all().values()))
        frequency_list.extend(file_list)

        last_call_time = current_time

    filt_list = []
    for i in frequency_list:
        if i["name"].startswith(current_line):
            filt_list.append(({"name": i["name"], "freq": i["freq"]}))

    return JsonResponse(
        # data=frequency_list,
        data=filt_list,
        safe=False
    )
