ARG TARGET_IMAGE
FROM $TARGET_IMAGE

ARG LC_ALL=C
ARG DEBIAN_FRONTEND=noninteractive

ENV CONAN_REVISIONS_ENABLED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    nodejs \
    ninja-build \
    unzip \
    wget \
    python3 \
    python-is-python3 \
    python3-pip \
    sudo \
    apt-transport-https

RUN pip install conan

WORKDIR /home/SomeBuildingRepo

ENTRYPOINT ["/bin/bash"]