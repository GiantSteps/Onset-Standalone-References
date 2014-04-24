#!/bin/bash
SCRIPTROOT=/Users/carthach/Dev/mtg/my_projects/onset_detection/Onset-Standalone-References/onset_detectors;

SCRIPTNAMES[0]=SuperFlux;
SCRIPTNAMES[1]=essentia_example;
SCRIPTNAMES[2]=essentia_global;
SCRIPTNAMES[3]=modal;

SCRIPTS[0]=$SCRIPTROOT/${SCRIPTNAMES[0]}.py;
SCRIPTS[1]=$SCRIPTROOT/${SCRIPTNAMES[1]}.py;
SCRIPTS[2]=$SCRIPTROOT/${SCRIPTNAMES[2]}.py;
SCRIPTS[3]=$SCRIPTROOT/${SCRIPTNAMES[3]}.py;

DATASETROOT=/Users/carthach;

DATASETS[0]=$DATASETROOT/GiantSteps-Share/datasets/ENST/drummer_1/audio;
DATASETS[1]=$DATASETROOT/GiantSteps-Share/datasets/ENST/drummer_2/audio;
DATASETS[3]=$DATASETROOT/GiantSteps-Share/datasets/ENST/drummer_3/audio;
DATASETS[4]=$DATASETROOT/GiantSteps-Share/datasets/jku/onsets/audio;
DATASETS[5]=$DATASETROOT/GiantSteps-Share/datasets/Leveau/audio;

length=${#SCRIPTS[@]};

for ((i = 0;i < $length; i++)); do
    echo ${SCRIPTNAMES[$i]};
    echo ${SCRIPTS[$i]};
    for j in "${DATASETS[@]}"; do
	echo $j;
    done
done

