FROM centos:7

WORKDIR /computation
ADD . /computation

#----------------------------
# Install common dependencies
#----------------------------
RUN yum install -y -q bzip2 ca-certificates curl unzip \
    && yum clean packages \
    && rm -rf /var/cache/yum/* /tmp/* /var/tmp/*

#-------------------------------------------------
# Install Miniconda, and set up Python environment
#-------------------------------------------------
ENV PATH=/opt/miniconda/envs/default/bin:$PATH
RUN curl -ssL -o miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash miniconda.sh -b -p /opt/miniconda \
    && rm -f miniconda.sh \
    && /opt/miniconda/bin/conda config --add channels conda-forge \
    && /opt/miniconda/bin/conda create -y -q -n default python=3.5.1 \
    	traits pandas \
    && /opt/miniconda/bin/conda clean -y --all \
    && pip install -U -q --no-cache-dir pip \
    && pip install -q --no-cache-dir \
    	nipype \
    && rm -rf /opt/miniconda/[!envs]*

#----------------------
# Install MCR and SPM12
#----------------------
# Install required libraries
RUN yum install -y -q libXext.x86_64 libXt.x86_64 gcc libxrandr\
    && yum clean packages \
    && rm -rf /var/cache/yum/* /tmp/* /var/tmp/* 

# Install MATLAB Compiler Runtime
WORKDIR /opt
RUN curl -sSL -o mcr.zip http://ssd.mathworks.com/supportfiles/downloads/R2016a/deployment_files/R2016a/installers/glnxa64/MCR_R2016a_glnxa64_installer.zip \
    && unzip -q mcr.zip -d mcrtmp \
    && mcrtmp/install -destinationFolder /opt/mcr -mode silent -agreeToLicense yes \
    && rm -rf mcrtmp mcr.zip /tmp/*

ENV MATLABCMD=/opt/mcr/v*/toolbox/matlab \
    LD_LIBRARY_PATH=/opt/mcr/v*/runtime/glnxa64:/opt/mcr/v*/bin/glnxa64:/opt/mcr/v*/sys/os/glnxa64:$LD_LIBRARY_PATH
    

#FROM ubuntu:16.04

#RUN apt-get update && apt-get install -y software-properties-common
#RUN apt-get update && apt-get install -y zip unzip libxt-dev wget libjasper-runtime libxrandr-dev
#RUN mkdir /tmp/mcr_installer && \
#    cd /tmp/mcr_installer && \
#    wget http://ssd.mathworks.com/supportfiles/downloads/R2016a/deployment_files/R2016a/installers/glnxa64/MCR_R2016a_glnxa64_installer.zip && \
#    unzip MCR_R2016a_glnxa64_installer.zip && \
#    ./install -mode silent -agreeToLicense yes && \
#    rm -Rf /tmp/mcr_installer


#FROM coinstac/coinstac-base-python-stream

# Set the working directory
WORKDIR /computation


# Copy the current directory contents into the container
COPY requirements.txt /computation

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ENV MCRROOT=/usr/local/MATLAB/MATLAB_Runtime/v901 MCR_CACHE_ROOT=/tmp

#/opt/miniconda/envs/default/lib/python3.5/site-packages/nipype
#COPY ./coinstac_spatially_constrained_ica/nipype-0.10.0/nipype/interfaces/gift /usr/local/lib/python3.6/site-packages/nipype/interfaces/gift
COPY ./coinstac_spatially_constrained_ica/nipype-0.10.0/nipype/interfaces/gift /opt/miniconda/envs/default/lib/python3.5/site-packages/nipype/interfaces/gift
#COPY --from=0 /usr/local/MATLAB /usr/local/MATLAB

# Copy the current directory contents into the container
COPY . /computation

