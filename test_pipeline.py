import json
import decentralized-pca
import coinstac_globalpca
import coinstac_gica
import coinstac_backreconstruction
import coinstac_ddfnc_preproc
import coinstac_dkmeans_ms

PYTHON_CMD = "python %s %s"

PIPELINE = [
    decentralized-pca
    #    coinstac_gica,
    #    coinstac_backreconstruction,
    #    coinstac_ddfnc_preproc,
    #    coinstac_dkmeans_ms
]


for stage in PIPELINE:
