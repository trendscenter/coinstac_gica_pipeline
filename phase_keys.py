import decentralized_row_means as drm
import coinstac_spatially_constrained_ica as scica
import coinstac_backreconstruction as br
import decentralized_pca as dpca
import coinstac_gica as gica
import coinstac_ddfnc_preproc as dfncpp
import coinstac_dkmeans_ms as dkm


# Row Means
ROW_MEANS_LOCAL = [
    dict(
        do=[drm.local.drm_local_1],
        recv=None,
        send='drm_local_1',
    )
]
ROW_MEANS_REMOTE = [
    dict(
        do=[drm.remote.drm_remote_1],
        recv=ROW_MEANS_LOCAL[0].get('send'),
        send='drm_remote_1',
    )
]

# Spatially Constrained ICA
SPATIALLY_CONSTRAINED_ICA_LOCAL = [
    dict(
        do=[scica.local.scica_local_1],
        recv=ROW_MEANS_REMOTE[0].get('send'),
        send='scica_local_1',
    )
]
SPATIALLY_CONSTRAINED_ICA_REMOTE = [
    dict(
        do=[scica.remote.scica_remote_noop],
        recv=SPATIALLY_CONSTRAINED_ICA_LOCAL[0].get('send'),
        send='scica_remote_noop'
    )
]

# dPCA
DECENTRALIZED_PCA_LOCAL = [
    dict(
        do=[dpca.local.dpca_local_1],
        recv=SPATIALLY_CONSTRAINED_ICA_REMOTE[0].get('send'),
        send='dpca_local_1'
    )
]
DECENTRALIZED_PCA_REMOTE = [
    dict(
        do=[dpca.remote.dpca_remote_1],
        recv=DECENTRALIZED_PCA_LOCAL[0].get('send'),
        send='dpca_remote_1',
    )
]

# Group ICA
GROUP_ICA_LOCAL = [
    dict(
        do=[gica.local.gica_local_noop],
        recv=DECENTRALIZED_PCA_REMOTE[0].get('send'),
        send='gica_local_noop'
    )
]
GROUP_ICA_REMOTE = [
    dict(
        do=[
            gica.remote.gica_remote_init_env,
            gica.remote.gica_remote_ica
        ],
        recv=GROUP_ICA_LOCAL[0].get('send'),
        send='gica_remote_ica'
    )
]

# Backreconstruction
BACKRECONSTRUCTION_LOCAL = [
    dict(
        do=[br.local.br_local_1],
        recv=GROUP_ICA_REMOTE[0].get('send'),
        send='br_local_1',
    )
]
BACKRECONSTRUCTION_REMOTE = [
    dict(
        do=[br.remote.br_remote_noop],
        recv=BACKRECONSTRUCTION_LOCAL[0].get('send'),
        send='br_remote_noop'
    )
]

# DDFNC
DFNC_PREPROC_LOCAL = [
    dict(
        do=[dfncpp.local.br_local_compute_windows],
        recv=BACKRECONSTRUCTION_REMOTE[0].get('send'),
        send='dfncpp_local_1',
    )
]
DFNC_PREPROC_REMOTE = [
    dict(
        do=[dfncpp.remote.br_remote_noop],
        recv=DFNC_PREPROC_LOCAL[0].get('send'),
        send='dfncpp_remote_noop'
    )
]

# DKMEANS
DKMEANS_LOCAL = [  # Local 0
    dict(
        do=[dkm.local.dkm_local_noop],
        recv=DFNC_PREPROC_REMOTE[0].get('send'),
        send='dkm_local_noop',
    ),

]
DKMEANS_REMOTE = [  # Remote 0
    dict(
        do=[dkm.remote.dkm_remote_init_env],
        recv=DKMEANS_LOCAL[0].get('send'),
        send='dkm_remote_init'
    )
]

DKMEANS_LOCAL.append(
    dict(  # Local 1
        do=[
            dkm.local.dkm_local_init_env,
            dkm.local.dkm_local_init_centroids
        ],
        recv=DKMEANS_REMOTE[0].get('send'),
        send='dkm_local_init_centroids'
    ))
DKMEANS_REMOTE.append(
    dict(  # Remote 1
        do=[dkm.remote.dkm_remote_init_centroids],
        recv=DKMEANS_LOCAL[1].get('send'),
        send='dkm_remote_init_centroids'
    )
)
DKMEANS_LOCAL.append(
    dict(  # Local 2
        do=[
            dkm.local.dkm_local_compute_clustering,
            dkm.local.dkm_local_compute_optimizer
        ],
        recv=DKMEANS_REMOTE[1].get('send'),
        send='dkm_local_compute_optimizer'
    ))
DKMEANS_REMOTE.append(
    dict(  # Remote 2
        do=[
            dkm.remote.dkm_remote_aggregate_optimizer,
            dkm.remote.dkm_remote_optimization_step
        ],
        recv=DKMEANS_LOCAL[2].get('send'),
        send='dkm_remote_otpimization_step'
    ),
)
DKMEANS_LOCAL.append(
    dict(  # Local 3
        do=[
            dkm.local.dkm_local_compute_clustering
        ],
        recv=DKMEANS_REMOTE[2].get('send'),
        send='dkm_local_compute_clustering_2'
    )
)
DKMEANS_REMOTE.append(
    dict(  # Remote 3
        do=[
            dkm.remote.dkm_remote_check_convergence,
            dkm.remote.dkm_remote_aggregate_output
        ],
        recv=DKMEANS_LOCAL[3].get('send'),
        send='dkm_remote_aggregate_output'
    ),
)
DKMEANS_LOCAL.append(
    dict(  # Local 4
        do=[
            dkm.local.dkm_local_compute_optimizer
        ],
        recv=DKMEANS_REMOTE[3].get('send') + '_false',
        send='dkm_local_compute_optimizer'
    )
)
DKMEANS_LOCAL.append(
    dict(  # Local 5
        do=[
            dkm.local.dkm_local_compute_clustering
        ],
        recv=DKMEANS_REMOTE[3].get('send') + '_true',
        send='dkm_local_compute_clustering'
    )
)
DKMEANS_REMOTE.append(
    dict(  # Remote 5
        do=[
            dkm.remote.dkm_remote_stop
        ],
        recv=DKMEANS_LOCAL[5].get('send'),
        send='dkm_remote_stop'
    ),
)
# END DKMEANS

DFNC_STATS_LOCAL = [
    dict(
        do=[],
        recv=DKMEANS_REMOTE[5].get('send'),
        send='dkm_local_stats',
    )
]
DFNC_STATS_REMOTE = [
    dict(
        do=[],
        recv=DFNC_STATS_LOCAL[0].get('send'),
        send='dkm_remote_stats'
    )
]
