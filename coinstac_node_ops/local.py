from . import ops

PREFIX = 'local'


def local_load_datasets(args):
    return ops.load_datasets(args, PREFIX)


def local_noop(args):
    return ops.noop(args, PREFIX)


def local_input_to_cache(args):
    return ops.input_to_cache(args, PREFIX)


def local_output_to_cache(args):
    return ops.output_to_cache(args, PREFIX)


def local_cache_to_input(args):
    return ops.cache_to_input(args, PREFIX)


def local_dump_cache(args):
    return ops.dump_cache(args, PREFIX)


def local_clear_cache(args):
    return ops.clear_cache(args, PREFIX)
