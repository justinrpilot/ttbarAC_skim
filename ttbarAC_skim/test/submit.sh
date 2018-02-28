#!/bin/bash

filelist=$1

#cd ${_CONDOR_SCRATCH_DIR}
cp submit_template.cmd submit_this.cmd;
for file in $(cat $filelist);
        do `echo ${file} > thisfile.txt`;
        echo ${file};
        newfile=thisfile.txt;
        #python vlq_fwlite.py --files thisfile.txt;
        #sed -i "s/FNAME/${newfile}/g" submit_this.cmd;
        #sed -i "s/SAMPLE_NAME/$2/g" submit_this.cmd;
        echo "Arguments = ${file} $2 \$(Process)" >> submit_this.cmd;
        echo "Queue 1" >> submit_this.cmd;
done

condor_submit submit_this.cmd;
