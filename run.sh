echo "Stopping old dockers...";
docker stop $(docker ps -a -q);
echo "Building docker file...";
sudo docker build  -t ddfnc .;
echo "Running Simulator...";
sudo coinstac-simulator;
