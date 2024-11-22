FROM python:3.8

# Initiation of system
RUN export MCR_CACHE_VERBOSE=true
RUN apt-get update -y \
 && apt-get install -y wget unzip libxext-dev libxt-dev libxmu-dev libglu1-mesa-dev libxrandr-dev build-essential \
 && mkdir -p /tmp_mcr \
 && cd /tmp_mcr \
 && wget https://ssd.mathworks.com/supportfiles/downloads/R2022b/Release/9/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2022b_Update_9_glnxa64.zip \
 && unzip MATLAB_Runtime_R2022b_Update_9_glnxa64.zip \
 && ./install -destinationFolder /usr/local/MATLAB/MATLAB_Runtime/ -mode silent -agreeToLicense yes \
 && mkdir -p /computation \
 && mkdir /computation/groupica_v4.0.4.11 \
 && rm -rf /tmp_mcr \
 && wget -P /computation/groupica_v4.0.4.11/ https://trends-public-website-fileshare.s3.amazonaws.com/public_website_files/software/gift/software/bids/v4.0.5.2M2022b/groupica
# groupica is compiled using MATLAB version R2022b.

# Environment variables
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu/:/usr/local/MATLAB/MATLAB_Runtime/R2022b/:/usr/local/MATLAB/MATLAB_Runtime/R2022b/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/R2022b/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/R2022b/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/R2022b/sys/java/jre/glnxa64/jre/lib/amd64/native_threads:/usr/local/MATLAB/MATLAB_Runtime/R2022b/sys/java/jre/glnxa64/jre/lib/amd64/server:/usr/local/MATLAB/MATLAB_Runtime/R2022b/sys/java/jre/glnxa64/jre/lib/amd64
ENV XAPPLRESDIR=/usr/local/MATLAB/MATLAB_Runtime/R2022b/X11/app-defaults
ENV MCR_CACHE_VERBOSE=true
ENV MCR_CACHE_ROOT=/tmp
ENV PATH=$PATH:/computation/groupica_v4.0.4.11:
ENV MATLAB_VER=R2022b
ENV GICA_VER=v4.0.5.2
ENV GICA_INSTALL_DIR=/computation/groupica_v4.0.4.11

# Building entrypoint
WORKDIR /computation
RUN chmod +x /computation/groupica_v4.0.4.11/groupica

# Install any needed packages specified in requirements.txt
COPY ./groupicatv4.0b/icatb/nipype-0.10.0/nipype/interfaces/gift /usr/local/lib/python3.8/site-packages/nipype/interfaces/gift

# Copy the current directory contents into the container
COPY requirements.txt /computation

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install nipy

COPY ./run_groupica.sh /computation/groupica_v4.0.4.11/
COPY ./coinstac_masking /computation/coinstac_masking
COPY ./coinstac_decentralized_row_means /computation/coinstac_decentralized_row_means

COPY ./coinstac_node_ops /computation/coinstac_node_ops
COPY ./coinstac_spatially_constrained_ica /computation/coinstac_spatially_constrained_ica
COPY ./local_data /computation/local_data

COPY ./*.py /computation/


RUN chmod -R a+wrx /computation
ENV PYTHONPATH=/computation
ENV PYTHONPATH=${PATH}:/computation

CMD ["python", "/computation/entry.py"]
