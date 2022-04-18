from ..basic_utils import search_target_word


def search_tips(content_array):

    # raise error if there are multiple starts or no start
    start_ids = search_target_word(content_array, "start")
    if start_ids.shape[0] != 1:
        raise ValueError("'start' should be only one")

    start_id = start_ids[0]

    # raise error if there are more than two ends
    end_ids = search_target_word(content_array, "end")
    if end_ids.shape[0] >= 2:
        raise ValueError("'end' should be only one")

    # in a graph, "end" node can be abbreviated. if so, the end_id will be -1
    if end_ids.shape[0] == 0:
        end_id = -1
    else:
        end_id = end_ids[0]

    return start_id, end_id
