# Coinstac Group ICA/ddFNC Pipeline

This repository compiles submodules utilized for Group ICA and ddFNC.

The ddFNC pipeline consists of two distinct parts - Group ICA first, followed by ddFNC.

## Group ICA

The stages of Group ICA are:

 - decentralized row means
 - decentralized PCA
 - local ICA (either with Infomax ICA, spatially-constrained ICA, or other)

## ddFNC

The stages of ddFNC are:
 - Group ICA (as given above)
 - Local post-processing of timecourses (including windowing)
 - Decentralized Clustering

