Simple Helpers
--------------

This is a collection of helper functions that I frequently use and hope that others
will also find useful.

Currently there is only one fuction inside that is to track the progress of a
parallelized function given an iterable of arguments.

To use:

    >>> import simple_helpers
    >>> def my_func(args):
    ... 	""" an arbitrary function """
    ... 	arg1_int, arg2_int = args
    ... 	return arg1_int + arg2_int
    >>> arguments = [[i, i ** 2] for i in range(10)] # an arbitrary list of arguments
    >>> print(results = simple_helpers.parallel_progress(my_func, arguments))
