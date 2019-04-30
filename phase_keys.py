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
import coinstac_ddfnc_preproc.local as dfncpp_local
import coinstac_ddfnc_preproc.remote as dfncpp_remote
import coinstac_dkmeans_ms.local as dkm_local
import coinstac_dkmeans_ms.remote as dkm_remote

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

# DDFNC
DFNC_PREPROC_LOCAL_EXEMPLARS = [
    dict(
        do=[
            ops_local.local_load_cache_from_npy,
            ops_local.local_cache_to_input,
            dfncpp_local.br_local_compute_windows,
            ops_local.local_output_to_cache,
            ops_local.local_dump_cache_to_file
        ],
        recv=SPATIALLY_CONSTRAINED_ICA_REMOTE[0].get('send'),
        send='dfncpp_local_exemplars_1',
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
            {'exemplar': True},
            {},
            {'filename': "exemplar_window_filenames.json"}
        ],
    )
]

DFNC_PREPROC_REMOTE_EXEMPLARS = [
    dict(
        do=[dfncpp_remote.dfncpp_remote_noop],
        recv=DFNC_PREPROC_LOCAL_EXEMPLARS[0].get('send'),
        send='dfncpp_remote_exemplars_noop',
        args=[],
        kwargs=[],
    )
]

DFNC_PREPROC_LOCAL = [
    dict(
        do=[
            ops_local.local_load_cache_from_npy,
            ops_local.local_cache_to_input,
            dfncpp_local.br_local_compute_windows,
            ops_local.local_output_to_cache,
            ops_local.local_dump_cache_to_file
        ],
        recv=DFNC_PREPROC_REMOTE_EXEMPLARS[0].get('send'),
        send='dfncpp_local_1',
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
            {"exemplar": False},
            {},
            {'filename': "window_filenames.json"}
        ],
    )
]
DFNC_PREPROC_REMOTE = [
    dict(
        do=[ops_remote.remote_noop],
        recv=DFNC_PREPROC_LOCAL[0].get('send'),
        send='dfncpp_remote_noop',
        args=[],
        kwargs=[],
    )
]


# DKMEANS
DKMEANS_LOCAL = [  # Local 0
    dict(
        do=[
            ops_local.local_noop
        ],
        recv=DFNC_PREPROC_REMOTE[0].get('send'),
        send='dkm_local_noop',
        args=[
            []
        ],
        kwargs=[
            {}
        ],
    ),
]
DKMEANS_REMOTE = [  # Remote 0
    dict(
        do=[
            dkm_remote.dkm_remote_init_env,
            ops_remote.remote_output_to_cache,
            ops_remote.remote_dump_cache_to_file
        ],
        recv=DKMEANS_LOCAL[0].get('send'),
        send='dkm_remote_init',
        args=[
            [],
            [],
            []
        ],
        kwargs=[
            {},
            {},
            {"filename": "dkm_inputs.npy"}
        ],
    )
]

DKMEANS_LOCAL.append(
    dict(  # Local 1
        do=[
            ops_local.local_load_cache_from_file,
            dkm_local.dkm_local_init_env,
            ops_local.local_output_to_input,
            dkm_local.dkm_local_init_centroids
        ],
        recv=DKMEANS_REMOTE[0].get('send'),
        send='dkm_local_init_centroids',
        args=[
            [],
            [],
            [],
            []
        ],
        kwargs=[
            {'filename': 'exemplar_window_filenames.json', 'keys': ['all_windows']},
            {},
            {},
            {}
        ],

    )
)
DKMEANS_REMOTE.append(
    dict(  # Remote 1
        do=[
            dkm_remote.dkm_remote_init_centroids,
        ],
        recv=DKMEANS_LOCAL[1].get('send'),
        send='dkm_remote_init_centroids',
        args=[
            [],
        ],
        kwargs=[
            {},
        ],
    )
)

DKMEANS_LOCAL.append(
    dict(  # Local 2
        do=[
            dkm_local.dkm_local_compute_clustering,
            ops_local.local_output_to_input,
            dkm_local.dkm_local_compute_optimizer
        ],
        recv=DKMEANS_REMOTE[1].get('send'),
        send='dkm_local_compute_optimizer',
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
)
DKMEANS_REMOTE.append(
    dict(  # Remote 2
        do=[
            dkm_remote.dkm_remote_aggregate_optimizer,
            ops_remote.remote_output_to_input,
            dkm_remote.dkm_remote_optimization_step
        ],
        recv=DKMEANS_LOCAL[2].get('send'),
        send='dkm_remote_otpimization_step',
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
)
DKMEANS_LOCAL.append(
    dict(  # Local 3
        do=[
            dkm_local.dkm_local_compute_clustering
        ],
        recv=DKMEANS_REMOTE[2].get('send'),
        send='dkm_local_compute_clustering_2',
        args=[
            []
        ],
        kwargs=[
            {}
        ],
    )
)
DKMEANS_REMOTE.append(
    dict(  # Remote 3
        do=[
            dkm_remote.dkm_remote_check_convergence
        ],
        recv=DKMEANS_LOCAL[3].get('send'),
        send=None,
        args=[
            [],
            []
        ],
        kwargs=[
            {},
            {}
        ],
    )
)
DKMEANS_LOCAL.append(
    dict(  # Local 4
        do=[
            dkm_local.dkm_local_compute_optimizer
        ],
        recv='dkm_remote_converged_false',
        send='dkm_local_compute_optimizer',
        args=[
            [],
        ],
        kwargs=[
            {},
        ],
    )
)
DKMEANS_LOCAL.append(
    dict(  # Local 5
        do=[
            dkm_local.dkm_local_compute_clustering,
            ops_local.local_output_to_cache,
            ops_local.local_dump_cache_to_file
        ],
        recv='dkm_remote_converged_true',
        send='dkm_local_final_clustering',
        args=[
            [],
            [],
            []
        ],
        kwargs=[
            {},
            {},
            {'filename': "final_exemplar_clustering.npy"}
        ],
    )
)
DKMEANS_REMOTE.append(
    dict(  # Remote 5
        do=[
            dkm_remote.dkm_remote_stop,
            ops_local.local_dump_cache_to_file
        ],
        recv=DKMEANS_LOCAL[5].get('send'),
        send='dkm_remote_stop',
        args=[
            [],
            []
        ],
        kwargs=[
            {},
            {'filename': "final_exemplar_clustering.npy"}
        ],
    )
)
# END DKMEANS


# DKM_NOEX
DKM_NOEX_LOCAL = [  # Local 0
    dict(
        do=[
            ops_local.local_noop
        ],
        recv=DKMEANS_REMOTE[-1].get('send'),
        send='dkmnx_local_noop',
        args=[
            []
        ],
        kwargs=[
            {}
        ],
    ),
]
DKM_NOEX_REMOTE = [  # Remote 0
    dict(
        do=[
            dkm_remote.dkm_remote_init_env,
            ops_remote.remote_output_to_cache,
            ops_remote.remote_dump_cache_to_file
        ],
        recv=DKM_NOEX_LOCAL[0].get('send'),
        send='dkmnx_remote_init',
        args=[
            [],
            [],
            []
        ],
        kwargs=[
            {},
            {},
            {"filename": "dkmnx_inputs.npy"}
        ],
    )
]

DKM_NOEX_LOCAL.append(
    dict(  # Local 1
        do=[
            ops_local.local_load_cache_from_file,
            dkm_local.dkm_local_init_env,
            ops_local.local_output_to_input,
            dkm_local.dkm_local_init_centroids
        ],
        recv=DKM_NOEX_REMOTE[0].get('send'),
        send='dkmnx_local_init_centroids',
        args=[
            [],
            [],
            [],
            []
        ],
        kwargs=[
            {'filename': 'window_filenames.json', 'keys': ['all_windows']},
            {},
            {},
            {}
        ],

    )
)
DKM_NOEX_REMOTE.append(
    dict(  # Remote 1
        do=[
            dkm_remote.dkm_remote_init_centroids,
        ],
        recv=DKM_NOEX_LOCAL[1].get('send'),
        send='dkmnx_remote_init_centroids',
        args=[
            [],
        ],
        kwargs=[
            {},
        ],
    )
)

DKM_NOEX_LOCAL.append(
    dict(  # Local 2
        do=[
            dkm_local.dkm_local_compute_clustering,
            ops_local.local_output_to_input,
            dkm_local.dkm_local_compute_optimizer
        ],
        recv=DKM_NOEX_REMOTE[1].get('send'),
        send='dkmnx_local_compute_optimizer',
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
)
DKM_NOEX_REMOTE.append(
    dict(  # Remote 2
        do=[
            dkm_remote.dkm_remote_aggregate_optimizer,
            ops_remote.remote_output_to_input,
            dkm_remote.dkm_remote_optimization_step
        ],
        recv=DKM_NOEX_LOCAL[2].get('send'),
        send='dkmnx_remote_otpimization_step',
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
)
DKM_NOEX_LOCAL.append(
    dict(  # Local 3
        do=[
            dkm_local.dkm_local_compute_clustering
        ],
        recv=DKM_NOEX_REMOTE[2].get('send'),
        send='dkmnx_local_compute_clustering_2',
        args=[
            []
        ],
        kwargs=[
            {}
        ],
    )
)
DKM_NOEX_REMOTE.append(
    dict(  # Remote 3
        do=[
            dkm_remote.dkmnx_remote_check_convergence
        ],
        recv=DKM_NOEX_LOCAL[3].get('send'),
        send=None,
        args=[
            [],
            []
        ],
        kwargs=[
            {},
            {}
        ],
    )
)
DKM_NOEX_LOCAL.append(
    dict(  # Local 4
        do=[
            dkm_local.dkm_local_compute_optimizer
        ],
        recv='dkmnx_remote_converged_false',
        send='dkmnx_local_compute_optimizer',
        args=[
            [],
        ],
        kwargs=[
            {},
        ],
    )
)
DKM_NOEX_LOCAL.append(
    dict(  # Local 5
        do=[
            dkm_local.dkm_local_compute_clustering,
            ops_local.local_output_to_cache,
            ops_local.local_dump_cache_to_file
        ],
        recv='dkmnx_remote_converged_true',
        send='dkmnx_local_final_clustering',
        args=[
            [],
            [],
            []
        ],
        kwargs=[
            {},
            {},
            {'filename': "final_full_clustering.npy"}
        ],
    )
)
DKM_NOEX_REMOTE.append(
    dict(  # Remote 5
        do=[
            dkm_remote.dkm_remote_stop,
            ops_local.local_dump_cache_to_file
        ],
        recv=DKM_NOEX_LOCAL[5].get('send'),
        send='dkmnx_remote_stop',
        args=[
            [],
            []
        ],
        kwargs=[
            {},
            {'filename': "final_full_clustering.npy"}
        ],
    )
)
# END DKM_NOEX

DFNC_STATS_LOCAL = [
    dict(
        do=[],
        recv=DKMEANS_REMOTE[4].get('send'),
        send='dkm_local_stats',
        args=[],
        kwargs=[],
    )
]
DFNC_STATS_REMOTE = [
    dict(
        do=[],
        recv=DFNC_STATS_LOCAL[0].get('send'),
        send='dkm_remote_stats',
        args=[],
        kwargs=[],
    )
]
