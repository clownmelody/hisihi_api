__author__ = 'bliss'


def get_url_no_param(request):
    full_path = str(request.full_path)
    q_index = full_path.find('?')
    full_path = full_path[0:q_index]
    return full_path