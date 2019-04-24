echo "Buildingg docker file...";
docker build -t ddfnc .;
echo "Running Simulator...";
sudo coinstac-simulator;
