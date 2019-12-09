import coinstac_node_ops.local as ops_local
import coinstac_node_ops.remote as ops_remote
import coinstac_masking.local as mask_local
import coinstac_masking.remote as mask_remote
import coinstac_decentralized_row_means.local as drm_local
import coinstac_decentralized_row_means.remote as drm_remote
import coinstac_spatially_constrained_ica.local as scica_local
import coinstac_spatially_constrained_ica.remote as scica_remote
import coinstac_backreconstruction.local as br_local
import coinstac_backreconstruction.remote as br_remote
import coinstac_decentralized_pca.local as dpca_local
import coinstac_decentralized_pca.remote as dpca_remote
import coinstac_gica.local as gica_local
import coinstac_gica.remote as gica_remote

# Init
"""
INIT_LOCAL = [
    dict(
        do=[
            ops_local.local_load_datasets,
            ops_local.local_output_to_cache,
            ops_local.local_input_to_cache,
            ops_local.local_dump_cache,
            ops_local.local_clear_cache
        ],
        recv=[],
        send='local_clear_cache'
    )
]
INIT_REMOTE = [
    dict(
        do=[
            ops_remote.remote_noop,
        ],
        recv=INIT_LOCAL[0].get("send"),
        send='remote_noop'
    )
]

# Masking
MASKING_LOCAL = [
    dict(
        do=[
            ops_local.local_input_to_cache,
            ops_local.local_load_cache,
            ops_local.local_cache_to_input,
            mask_local.masking_local_1
        ],
        recv='remote_noop',
        send='masking_local_1'
    )
]
MASKING_REMOTE = [
    dict(
        do=[
            mask_remote.masking_remote_1
        ],
        recv='masking_local_1',
        send='masking_remote_1'
    )
]

# Row Means
ROW_MEANS_LOCAL = [
    dict(
        do=[drm_local.drm_local_1],
        recv='masking_remote_1',
        send='drm_local_1',
    )
]
ROW_MEANS_REMOTE = [
    dict(
        do=[
            drm_remote.drm_remote_1,
            ops_remote.remote_output_to_cache,
            ops_remote.remote_dump_cache
        ],
        recv=ROW_MEANS_LOCAL[0].get('send'),
        send='remote_dump_cache',
    )
]
"""

NOOP_LOCAL = [
    dict(
        do=[
            ops_local.local_noop
        ],
        recv=[],
        send='local_noop',
        args=[
            []
        ],
        kwargs=[
            {}
        ]
    )
]

NOOP_REMOTE = [
    dict(
        do=[
            ops_remote.remote_noop
        ],
        recv="local_noop",
        send='remote_noop',
        args=[
            []
        ],
        kwargs=[
            {}
        ]
    )
]

INIT_LOCAL = [
    dict(
        do=[
            ops_local.local_load_datasets,
            ops_local.local_output_to_input,
            mask_local.masking_local_1,
            ops_local.local_output_to_cache,
            ops_local.local_cache_to_input,
            drm_local.drm_local_1,
        ],
        recv=[],
        send='local_init',
        args=[
            [],
            [],
            [],
            [],
            []
        ],
        kwargs=[
            {},
            {},
            {},
            {},
            {}
        ],
    )
]

INIT_REMOTE = [
    dict(
        do=[
            drm_remote.drm_remote_1,
            ops_remote.remote_output_to_cache,
            ops_remote.remote_dump_cache_to_mat
        ],
        recv=INIT_LOCAL[0].get("send"),
        send='remote_init',
        args=[
            [],
            [],
            []
        ],
        kwargs=[
            {},
            {},
            {}
        ],

    )
]

# Spatially Constrained ICA
SPATIALLY_CONSTRAINED_ICA_LOCAL = [
    dict(
        do=[
            scica_local.scica_local_1,
            ops_local.local_output_to_cache,
            ops_local.local_dump_cache_to_npy,
            ops_local.local_clear_cache
        ],
        recv=[],
        send='scica_local_1',
        args=[
            [],
            [],
            [],
            []
        ],
        kwargs=[
            {},
            {},
            {},
            {}
        ],
    )
]
SPATIALLY_CONSTRAINED_ICA_REMOTE = [
    dict(
        do=[
            ops_remote.remote_noop
        ],
        recv=SPATIALLY_CONSTRAINED_ICA_LOCAL[0].get('send'),
        send='scica_remote_noop',
        args=[
            []
        ],
        kwargs=[
            {}
        ],
    )
]

