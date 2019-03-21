import json
import decentralized_pca
import decentralized_row_means
import coinstac_globalpca
import coinstac_gica
import coinstac_backreconstruction
import coinstac_ddfnc_preproc
import coinstac_dkmeans_ms

PYTHON_CMD = "python %s %s"

PIPELINE = [
    'decentralized_row_means.py',
    #    decentralized_pca
    #    coinstac_gica,
    #    coinstac_backreconstruction,
    #    coinstac_ddfnc_preproc,
    #    coinstac_dkmeans_ms
]

INPUTS = [
    [
        {
            "data": {
                "value": [
                    [
                        "local0.sub0.data.nii",
                    ],
                    [
                        "nifti"
                    ]
                ]
            }
        },
        {
            "data": {
                "value": [
                    [
                        "local1.sub1.data.nii",
                    ],
                    [
                        "nifti"
                    ]
                ]
            }
        }
    ],
    [{
        "input": {
            "data": [
                [
                    "local0.sub0.data.nii",
                ],
                [
                    "nifti"
                ]
            ],
            "num_PC_global": 20,
            "axis": -1,
            "mean_values": [
                [
                    "row_mean_global.npz"
                ],
                [
                    "npzfile"
                ]
            ],
            "subject_level_PCA": True,
            "subject_level_num_PC": 120
        },
        "cache": {}
    },
        {
        "input": {
            "data": [
                [
                    "local1.sub1.data.nii",
                ],
                [
                    "nifti"
                ]
            ],
            "num_PC_global": 20,
            "axis": -1,
            "mean_values": [
                [
                    "row_mean_global.npz"
                ],
                [
                    "npzfile"
                ]
            ],
            "subject_level_PCA": True,
            "subject_level_num_PC": 120
        },
        "cache": {}
    }
    ]
]


for stage, inputs in zip(PIPELINE, INPUTS):
    python_cmd = PYTHON_CMD % (stage, json.dumps(inputs))
    print(python_cmd)
