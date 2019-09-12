from . import ops

PREFIX = 'remote'


def remote_load_datasets(args):
    return ops.load_datasets(args, PREFIX)


def remote_noop(args):
    return ops.noop(args, PREFIX)


def remote_input_to_cache(args):
    return ops.input_to_cache(args, PREFIX)


def remote_output_to_cache(args):
    return ops.output_to_cache(args, PREFIX)


def remote_cache_to_input(args):
    return ops.cache_to_input(args, PREFIX)


def remote_output_to_input(args):
    return ops.output_to_input(args, PREFIX)


def remote_input_to_output(args):
    return ops.input_to_output(args, PREFIX)


def remote_dump_cache(args):
    return ops.dump_cache(args, PREFIX)


def remote_dump_cache_to_mat(args):
    return ops.dump_cache_to_mat(args, PREFIX)


def remote_dump_cache_to_npy(args):
    return ops.dump_cache_to_npy(args, PREFIX)


def remote_load_cache_from_npy(args):
    return ops.load_cache_from_npy(args, PREFIX)


def remote_clear_cache(args):
    return ops.clear_cache(args, PREFIX)


def remote_load_cache_from_file(args, **kwargs):
    return ops.load_cache_from_file(args, phase_prefix=PREFIX, **kwargs)


def remote_dump_cache_to_file(args, **kwargs):
    return ops.dump_cache_to_file(args, phase_prefix=PREFIX, **kwargs)
