name = "MultiBinary"

import threading, queue


def binary_search_thread(item):
    while True:
        try:
            list_item, index = work.get(False)
        except queue.Empty:
            return
        if list_item == item:
            set_results(True, index, item)


def build_que(search_list):
    for i in range(len(search_list)):
        work.put([search_list[i], i])


def set_results(found, index, item):
    result = [found, index, item]
    output.append(result)


def get_results():
    return output


def binary_search(somelist, someitem, t_limit=100):
    build_que(somelist)
    for i in range(t_limit):
        thread = threading.Thread(target=binary_search_thread, args=(someitem,))
        thread.start()
        thread.join()
        return get_results()


work = queue.Queue(0)
output = []
