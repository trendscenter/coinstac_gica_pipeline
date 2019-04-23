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

# Row Means
ROW_MEANS_LOCAL = [
    dict(
        do=[drm_local.drm_local_1],
        recv=[],
        send='drm_local_1',
    )
]
ROW_MEANS_REMOTE = [
    dict(
        do=[drm_remote.drm_remote_1],
        recv=ROW_MEANS_LOCAL[0].get('send'),
        send='drm_remote_1',
    )
]

# Spatially Constrained ICA
SPATIALLY_CONSTRAINED_ICA_LOCAL = [
    dict(
        do=[scica_local.scica_local_1],
        recv=ROW_MEANS_REMOTE[0].get('send'),
        send='scica_local_1',
    )
]
SPATIALLY_CONSTRAINED_ICA_REMOTE = [
    dict(do=[scica_remote.scica_remote_noop],
         recv=SPATIALLY_CONSTRAINED_ICA_LOCAL[0].get('send'),
         send='scica_remote_noop')
]

# dPCA
DECENTRALIZED_PCA_LOCAL = [
    dict(do=[dpca_local.dpca_local_1],
         recv=SPATIALLY_CONSTRAINED_ICA_REMOTE[0].get('send'),
         send='dpca_local_1')
]
DECENTRALIZED_PCA_REMOTE = [
    dict(
        do=[dpca_remote.dpca_remote_1],
        recv=DECENTRALIZED_PCA_LOCAL[0].get('send'),
        send='dpca_remote_1',
    )
]

# Group ICA
GROUP_ICA_LOCAL = [
    dict(do=[gica_local.gica_local_noop],
         recv=DECENTRALIZED_PCA_REMOTE[0].get('send'),
         send='gica_local_noop')
]
GROUP_ICA_REMOTE = [
    dict(do=[gica_remote.gica_remote_init_env, gica_remote.gica_remote_ica],
         recv=GROUP_ICA_LOCAL[0].get('send'),
         send='gica_remote_ica')
]

# Backreconstruction
BACKRECONSTRUCTION_LOCAL = [
    dict(
        do=[br_local.br_local_1],
        recv=GROUP_ICA_REMOTE[0].get('send'),
        send='br_local_1',
    )
]
BACKRECONSTRUCTION_REMOTE = [
    dict(do=[br_remote.br_remote_noop],
         recv=BACKRECONSTRUCTION_LOCAL[0].get('send'),
         send='br_remote_noop')
]

# DDFNC
DFNC_PREPROC_LOCAL = [
    dict(
        do=[dfncpp_local.br_local_compute_windows],
        recv=BACKRECONSTRUCTION_REMOTE[0].get('send'),
        send='dfncpp_local_1',
    )
]
DFNC_PREPROC_REMOTE = [
    dict(do=[dfncpp_remote.dfncpp_remote_noop],
         recv=DFNC_PREPROC_LOCAL[0].get('send'),
         send='dfncpp_remote_noop')
]

# DKMEANS
DKMEANS_LOCAL = [  # Local 0
    dict(
        do=[dkm_local.dkm_local_noop],
        recv=DFNC_PREPROC_REMOTE[0].get('send'),
        send='dkm_local_noop',
    ),
]
DKMEANS_REMOTE = [  # Remote 0
    dict(do=[dkm_remote.dkm_remote_init_env],
         recv=DKMEANS_LOCAL[0].get('send'),
         send='dkm_remote_init')
]

DKMEANS_LOCAL.append(
    dict(  # Local 1
        do=[dkm_local.dkm_local_init_env, dkm_local.dkm_local_init_centroids],
        recv=DKMEANS_REMOTE[0].get('send'),
        send='dkm_local_init_centroids'))
DKMEANS_REMOTE.append(
    dict(  # Remote 1
        do=[dkm_remote.dkm_remote_init_centroids],
        recv=DKMEANS_LOCAL[1].get('send'),
        send='dkm_remote_init_centroids'))
DKMEANS_LOCAL.append(
    dict(  # Local 2
        do=[
            dkm_local.dkm_local_compute_clustering,
            dkm_local.dkm_local_compute_optimizer
        ],
        recv=DKMEANS_REMOTE[1].get('send'),
        send='dkm_local_compute_optimizer'))
DKMEANS_REMOTE.append(
    dict(  # Remote 2
        do=[
            dkm_remote.dkm_remote_aggregate_optimizer,
            dkm_remote.dkm_remote_optimization_step
        ],
        recv=DKMEANS_LOCAL[2].get('send'),
        send='dkm_remote_otpimization_step'), )
DKMEANS_LOCAL.append(
    dict(  # Local 3
        do=[dkm_local.dkm_local_compute_clustering],
        recv=DKMEANS_REMOTE[2].get('send'),
        send='dkm_local_compute_clustering_2'))
DKMEANS_REMOTE.append(
    dict(  # Remote 3
        do=[
            dkm_remote.dkm_remote_check_convergence,
            dkm_remote.dkm_remote_aggregate_output
        ],
        recv=DKMEANS_LOCAL[3].get('send'),
        send='dkm_remote_aggregate_output'), )
DKMEANS_LOCAL.append(
    dict(  # Local 4
        do=[dkm_local.dkm_local_compute_optimizer],
        recv=DKMEANS_REMOTE[3].get('send') + '_false',
        send='dkm_local_compute_optimizer'))
DKMEANS_LOCAL.append(
    dict(  # Local 5
        do=[dkm_local.dkm_local_compute_clustering],
        recv=DKMEANS_REMOTE[3].get('send') + '_true',
        send='dkm_local_compute_clustering'))
DKMEANS_REMOTE.append(
    dict(  # Remote 5
        do=[dkm_remote.dkm_remote_stop],
        recv=DKMEANS_LOCAL[5].get('send'),
        send='dkm_remote_stop'), )
# END DKMEANS

DFNC_STATS_LOCAL = [
    dict(
        do=[],
        recv=DKMEANS_REMOTE[4].get('send'),
        send='dkm_local_stats',
    )
]
DFNC_STATS_REMOTE = [
    dict(do=[], recv=DFNC_STATS_LOCAL[0].get('send'), send='dkm_remote_stats')
]
