import io

from memory_profiler import profile

memory_usage_stream = io.StringIO('')


def record_memory_usage(activate=False, stream=None):
    def wrap(org_func):
        if activate:

            @profile(stream=stream)
            def wrapped_func(*args, **kwargs):
                return org_func(*args, **kwargs)
            return wrapped_func
        else:
            def wrapped_func(*args, **kwargs):
                return org_func(*args, **kwargs)
            return wrapped_func

    return wrap
