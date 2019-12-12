echo "Building docker file...";
sudo docker build  -t dgica .;
echo "Running Simulator...";
sudo coinstac-simulator;
