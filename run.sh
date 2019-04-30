echo "Building docker file...";
sudo docker build  -t ddfnc .;
echo "Running Simulator...";
sudo coinstac-simulator;
