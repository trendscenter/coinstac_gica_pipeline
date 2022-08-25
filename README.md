# Coinstac Group ICA Pipeline

This repository compiles submodules utilized for Group ICA, WITHOUT ddFNC as an option.

This repository allows for decentralized group ICA, decentralized joint ICA, and decentralized auto-ICA (spatially constrained ICA). To cite the papers for each of these methods, please use the following reference:
```
```

## Running in the Simulator

This pipeline has been tested with the latest version of the COINSTAC simulator.


Install the simulator:

```
npm i -g coinstac-simulator
```

Download this repository

```
git clone git@github.com:trendscenter/coinstac_gica_pipeline.git
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
```

Finally, run using the bash script (will require entry of password for **sudo**)

```
bash run.sh
```

*or*

Run using the following commands

```
sudo docker build  -t gica .
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

## Joint ICA

The stages of Joint ICA are:

---

## Linked Repositories/Submodules

Briefly, there are a number of linked repositories attached to this pipeline.