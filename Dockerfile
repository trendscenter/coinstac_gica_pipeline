FROM ubuntu:16.04
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y zip unzip libxt-dev wget libjasper-runtime
RUN mkdir /tmp/mcr_installer && \
    cd /tmp/mcr_installer && \
    wget http://ssd.mathworks.com/supportfiles/downloads/R2016a/deployment_files/R2016a/installers/glnxa64/MCR_R2016a_glnxa64_installer.zip && \
    unzip MCR_R2016a_glnxa64_installer.zip && \
    ./install -mode silent -agreeToLicense yes && \
    rm -Rf /tmp/mcr_installer


FROM coinstac/coinstac-base-python-stream

# Set the working directory
WORKDIR /computation


# Copy the current directory contents into the container
COPY requirements.txt /computation

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ENV MCRROOT=/usr/local/MATLAB/MATLAB_Runtime/v901 MCR_CACHE_ROOT=/tmp


COPY ./coinstac_spatially_constrained_ica/nipype-0.10.0/nipype/interfaces/gift /usr/local/lib/python3.6/site-packages/nipype/interfaces/gift
COPY --from=0 /usr/local/MATLAB /usr/local/MATLAB

# Copy the current directory contents into the container
COPY . /computation

