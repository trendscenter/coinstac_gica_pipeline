FROM coinstacteam/coinstac-base:python3.7-buster
ENV MCRROOT=/usr/local/MATLAB/MATLAB_Runtime/v91
ENV MCR_CACHE_ROOT=/tmp

RUN apt-get clean && apt-get update && apt-get install -y \
    zip unzip wget \
    libx11-dev libxcomposite-dev \
    libxcursor-dev libxdamage-dev libxext-dev \
    libxfixes-dev libxft-dev libxi-dev \
    libxrandr-dev libxt-dev libxtst-dev \
    libxxf86vm-dev libasound2-dev libatk1.0-dev \
    libcairo2-dev gconf2 \
    libsndfile1-dev libxcb1-dev libxslt-dev \
    curl \
    libgtk-3-dev 

RUN mkdir /tmp/mcr_installer && \
    cd /tmp/mcr_installer && \
    wget http://ssd.mathworks.com/supportfiles/downloads/R2016b/deployment_files/R2016b/installers/glnxa64/MCR_R2016b_glnxa64_installer.zip && \
    unzip MCR_R2016b_glnxa64_installer.zip && \
    ./install -mode silent -agreeToLicense yes && \
    rm -Rf /tmp/mcr_installer

# Copy the current directory contents into the container
WORKDIR /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt
COPY ./groupicatv4.0b/icatb/nipype-0.10.0/nipype/interfaces/gift /usr/local/lib/python3.7/site-packages/nipype/interfaces/gift
RUN chmod -R a+wrx /app
#RUN chmod -R a+wrx /usr/local/MATLAB/MATLAB_Runtime/v91

ENV MCRROOT=/usr/local/MATLAB/MATLAB_Runtime/v91
ENV MCR_CACHE_ROOT=/computation/mcrcache

# Copy the current directory contents into the container
WORKDIR /computation
COPY requirements.txt /computation

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install awscli s3utils
RUN pip install nipy

RUN mkdir -p /computation/mcrcache

RUN mkdir /output

# GIFT version 4.0.4.11, including sliced masks still running on MATLAB 2016b
RUN mkdir /computation/groupica_v4.0.4.11
RUN wget -P /computation/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/groupica
RUN wget -P /computation/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/run_groupica.sh
RUN wget -P /computation/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/requiredMCRProducts.txt
RUN wget -P /computation/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/readme.txt
RUN wget -P /computation/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/mccExcludedFiles.log

RUN mkdir /app/groupica_v4.0.4.11
RUN wget -P /app/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/groupica
RUN wget -P /app/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/run_groupica.sh
RUN wget -P /app/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/requiredMCRProducts.txt
RUN wget -P /app/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/readme.txt
RUN wget -P /app/groupica_v4.0.4.11 https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/stand_alone/coinstac/082223/coinstac-giftv4.0.4.11_Lnx2016b/mccExcludedFiles.log

# Remove 4 lines below if groupica v4.0.4.11 works
# GIFT version from 012423 still running on MATLAB 2016b
COPY ./groupicatv4.0b/groupica_git_012423 /computation/groupica_git_012423
COPY ./groupicatv4.0b/groupica_git_012423 /app/groupica_git_012423
# Remove 4 lines above if groupica v4.0.4.11 works

RUN (timeout 20s /app/groupicatv4.0b/GroupICATv4.0b_standalone/run_groupica.sh /usr/local/MATLAB/MATLAB_Runtime/v91/; exit 0)

COPY ./coinstac_masking /computation/coinstac_masking
COPY ./coinstac_decentralized_row_means /computation/coinstac_decentralized_row_means

COPY ./coinstac_node_ops /computation/coinstac_node_ops
COPY ./coinstac_spatially_constrained_ica /computation/coinstac_spatially_constrained_ica
COPY ./local_data /computation/local_data

COPY ./*.py /computation/


RUN chmod -R a+wrx /computation
ENV PYTHONPATH=/computation
ENV PYTHONPATH=${PATH}:/computation
COPY . /app
#RUN (timeout 300 bash /app/groupicatv4.0b/GroupICATv4.0b_standalone/run_groupica.sh /usr/local/MATLAB/MATLAB_Runtime/v91; exit 0)


