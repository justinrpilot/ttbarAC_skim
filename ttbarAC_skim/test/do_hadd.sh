#!/bin/bash

#do hadd of the vlq files
eval `scramv1 runtime -sh`

for argument in "$@"
do
    echo ${argument};
    hadd -f root://cmseos.fnal.gov//store/user/pilot/ttbarACFiles/ttbarAC_${argument}_merged.root `xrdfs root://cmseos.fnal.gov ls -u /store/user/pilot/ttbarACFiles/ | grep ${argument} | grep "ttbarAC"`; 
done
