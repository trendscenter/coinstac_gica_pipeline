#!/bin/bash
fileid="1d33OXJVjpWzHiphkOnzCI3OeeqCyDEp_"
filename="GICA.zip"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}
#wget --no-check-certificate 'https://docs.google.com/uc?export=download&id='${fileid} -O ${filename}
unzip GICA.zip -d .
cp GroupICATv4.0b_standalone_aug_8_2019/MCRInstaller.zip . -v
rm -r GroupICATv4.0b_standalone_aug_8_2019 -v
rm GICA.zip -v
