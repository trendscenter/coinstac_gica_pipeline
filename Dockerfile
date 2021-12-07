# FROM ubuntu:16.04
FROM coinstacteam/coinstac-base
ENV MCRROOT=/usr/local/MATLAB/MATLAB_Runtime/v91
ENV MCR_CACHE_ROOT=/tmp

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y zip unzip

#Update this section on 11/23/2021 by AK
RUN apt-get install -yf		libjasper-runtime
RUN apt-get install -yf     libx11-dev
RUN apt-get install -yf     libxcomposite-dev
RUN apt-get install -yf   	libxcursor-dev
RUN apt-get install -yf     libxdamage-dev
RUN apt-get install -yf     libxext-dev
RUN apt-get install -yf   	libxfixes-dev
RUN apt-get install -yf     libxi-dev
RUN apt-get install -yf   	libxrandr-dev
RUN apt-get install -yf     libxt-dev
RUN apt-get install -yf     libxtst-dev
RUN apt-get install -yf   	libxxf86vm-dev
RUN apt-get install -yf     libasound2-dev
RUN apt-get install -yf   	libsndfile1-dev
RUN apt-get install -yf     libxcb1-dev
RUN apt-get install -yf     libxslt-dev
RUN apt-get install -yf   	curl

RUN mkdir /tmp/mcr_installer && \
    cd /tmp/mcr_installer && \
    wget http://ssd.mathworks.com/supportfiles/downloads/R2016b/deployment_files/R2016b/installers/glnxa64/MCR_R2016b_glnxa64_installer.zip && \
    unzip MCR_R2016b_glnxa64_installer.zip && \
    ./install -mode silent -agreeToLicense yes && \
    rm -Rf /tmp/mcr_installer

# Copy the current directory contents into the container
WORKDIR /computation
COPY requirements.txt /computation

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . /computation

COPY ./coinstac_spatially_constrained_ica/nipype-0.10.0/nipype/interfaces/gift /usr/local/lib/python3.7/site-packages/nipype/interfaces/gift

RUN mkdir /output