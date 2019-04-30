# Coinstac Group ICA/ddFNC Pipeline

This repository compiles submodules utilized for Group ICA and ddFNC.

The ddFNC pipeline consists of two distinct parts - Group or Spatially Constrained ICA first, followed by ddFNC.

## Running in the Simulator

This pipeline has been tested with the latest version of the COINSTAC simulator.


Install the simulator:

```
npm i -g coinstac-simulator
```

Download this repository

```
git clone https://github.com/MRN-Code/coinstac_ddfnc_pipeline.git
```

Initialize submodules

```
git submodule update --init --recursive
```

Copy the mask and template into the local input folders, using the bash script

```
bash copy_data.sh
```

*or* the following commands

```
cp test/remote/simulatorRun/mask.nii test/local0/simulatorRun/ ;
cp test/remote/simulatorRun/mask.nii test/local1/simulatorRun/ ;
cp test/remote/simulatorRun/NeuroMark.nii test/local0/simulatorRun/ ;
cp test/remote/simulatorRun/NeuroMark.nii test/local1/simulatorRun/ ;
```

Finally, run using the bash script (will require entry of password for **sudo**)

```
bash run.sh
```

*or*

Run using the following commands

```
sudo docker build  -t ddfnc .
sudo coinstac-simulator
```

## Spatially Constrained ICA

The stages of Spatially Constrained ICA are

 - local spatially constrained ICA (performed with GIFT)

## Group ICA

The stages of Group ICA are:

 - decentralized row means
 - decentralized PCA
 - local ICA (either with Infomax ICA, spatially-constrained ICA, or other)

## ddFNC

The stages of ddFNC are:
 - Group/ScICA ICA (as given above)
 - Local post-processing of timecourses (including windowing)
 - Decentralized Clustering
