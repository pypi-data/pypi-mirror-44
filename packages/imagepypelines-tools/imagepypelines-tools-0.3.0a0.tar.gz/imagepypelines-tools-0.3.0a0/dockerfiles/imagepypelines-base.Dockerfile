# inherit from an NVIDIA ubuntu build
# this will setup an image with CUDA and OPENGL preinstalled
FROM nvidia/cudagl:10.0-devel
MAINTAINER Jeff Maggio, Ryan Hartzell, Nathan Dileas

# ENVIRONMENTAL VARIABLES
################################################################################
# disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV OPENCV_VERSION="4.0.1"
ENV IP_GPU_ENABLED=OFF
ENV IP_ABORT_NESTED_SHELLS=ON


# BASE DEPENDENCIES
# The following was originally modified from buildpack-deps
# https://github.com/docker-library/buildpack-deps/blob/3fd6bc9602ab42ec1f11dd5680e528d2266f3325/bionic/Dockerfile
################################################################################
RUN apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
		curl \
		netbase \
		wget \
	&& rm -rf /var/lib/apt/lists/*

RUN set -ex; \
	if ! command -v gpg > /dev/null; then \
		apt-get update; \
		apt-get install -y --no-install-recommends \
			gnupg \
			dirmngr \
		; \
		rm -rf /var/lib/apt/lists/*; \
	fi

# procps is very common in build systems, and is a reasonably small package
RUN apt-get update && apt-get install -y --no-install-recommends \
		bzr \
		git \
		mercurial \
		openssh-client \
		subversion \
		\
		procps \
	&& rm -rf /var/lib/apt/lists/*

RUN set -ex; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		autoconf \
		automake \
		bzip2 \
		dpkg-dev \
		file \
		g++ \
		gcc \
		imagemagick \
		libbz2-dev \
		libc6-dev \
		libcurl4-openssl-dev \
		libdb-dev \
		libevent-dev \
		libffi-dev \
		libgdbm-dev \
		libgeoip-dev \
		libglib2.0-dev \
		libjpeg-dev \
		libkrb5-dev \
		liblzma-dev \
		libmagickcore-dev \
		libmagickwand-dev \
		libncurses5-dev \
		libncursesw5-dev \
		libpng-dev \
		libpq-dev \
		libreadline-dev \
		libsqlite3-dev \
		libssl-dev \
		libtool \
		libwebp-dev \
		libxml2-dev \
		libxslt-dev \
		libyaml-dev \
		make \
		patch \
		unzip \
		xz-utils \
		zlib1g-dev \
		\
# https://lists.debian.org/debian-devel-announce/2016/09/msg00000.html
		$( \
# if we use just "apt-cache show" here, it returns zero because "Can't select versions from package 'libmysqlclient-dev' as it is purely virtual", hence the pipe to grep
			if apt-cache show 'default-libmysqlclient-dev' 2>/dev/null | grep -q '^Version:'; then \
				echo 'default-libmysqlclient-dev'; \
			else \
				echo 'libmysqlclient-dev'; \
			fi \
		) \
	; \
	rm -rf /var/lib/apt/lists/*

# PYTHON
################################################################################
# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# extra dependencies (over what buildpack-deps already includes)
RUN apt-get update && apt-get install -y --no-install-recommends \
		tk-dev \
	&& rm -rf /var/lib/apt/lists/*

ENV GPG_KEY 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D
ENV PYTHON_VERSION 3.6.8

RUN set -ex \
	\
	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
	&& gpg --batch --verify python.tar.xz.asc python.tar.xz \
	&& { command -v gpgconf > /dev/null && gpgconf --kill all || :; } \
	&& rm -rf "$GNUPGHOME" python.tar.xz.asc \
	&& mkdir -p /usr/src/python \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz \
	\
	&& cd /usr/src/python \
	&& gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
	&& ./configure \
		--build="$gnuArch" \
		--enable-loadable-sqlite-extensions \
		--enable-shared \
		--with-system-expat \
		--with-system-ffi \
		--without-ensurepip \
	&& make -j "$(nproc)" \
	&& make install \
	&& ldconfig \
	\
	&& find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' + \
	&& rm -rf /usr/src/python \
	\
	&& python3 --version

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
	&& ln -s idle3 idle \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python3-config python-config

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 19.0.3

RUN set -ex; \
	\
	wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION" \
	; \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py

# OPENCV INSTALLATION
################################################################################
# gstreamer
RUN  apt-get update -y && apt-get install -y \
            libgstreamer1.0-0 \
            gstreamer1.0-plugins-base \
            gstreamer1.0-plugins-good \
            gstreamer1.0-plugins-bad \
            gstreamer1.0-plugins-ugly \
            gstreamer1.0-libav \
            gstreamer1.0-doc \
            gstreamer1.0-tools \
            libgstreamer1.0-dev \
			libgstreamer-plugins-base1.0-dev \
			&& rm -rf /var/lib/apt/lists/*

# GTK (for graphics)
# TODO: add VTK support
RUN apt-get update && apt-get install -y \
						libgtkglext1 \
						libgtkglext1-dev \
						&& rm -rf /var/lib/apt/lists/*

# other opencv dependencies
RUN apt-get update && \
  apt-get install -y \
  build-essential \
  cmake \
  git \
  wget \
  unzip \
  yasm \
  pkg-config \
  libswscale-dev \
  libtbb2 \
  libtbb-dev \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libavformat-dev \
  libpq-dev \
	libgtk2.0-dev \
	libavcodec-dev \
	libdc1394-22-dev \
	autotools-dev \
	&& rm -rf /var/lib/apt/lists/*

# Eigen, Lapack
# TODO add CUSTOM HAL support
RUN apt-get update && apt-get install -y \
	libeigen3-dev \
	libxvidcore-dev \
	libx264-dev \
	libatlas-base-dev \
	gfortran \
	libopenblas-dev \
	liblapack-dev \
	liblapacke-dev \
	&& rm -rf /var/lib/apt/lists/*

# numpy for opencv-python
RUN pip install numpy

WORKDIR /
RUN wget https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.zip \
&& unzip ${OPENCV_VERSION}.zip \
&& rm ${OPENCV_VERSION}.zip
RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
&& unzip ${OPENCV_VERSION}.zip \
&& mkdir /opencv-${OPENCV_VERSION}/cmake_binary \
&& cd /opencv-${OPENCV_VERSION}/cmake_binary \
&& cmake \
  -DBUILD_TIFF=ON \
  -DBUILD_opencv_java=OFF \
  -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-${OPENCV_VERSION}/modules \
  -DOPENCV_ENABLE_NONFREE=ON \
  -DWITH_CUDA=$IP_GPU_ENABLED \
  -DWITH_OPENGL=ON \
  -DWITH_GSTREAMER=ON \
  -DWITH_GSTREAMER_0_10=OFF \
  -DENABLE_FAST_MATH=ON \
  -DCUDA_FAST_MATH=$IP_GPU_ENABLED \
  -DWITH_CUBLAS=$IP_GPU_ENABLED \
  -DWITH_OPENCL=OFF \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DPYTHON_EXECUTABLE=/usr/bin/python3 \
  -DPYTHON_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
  .. \
&& make -j4 \
&& make install \
&& ldconfig \
&& rm /${OPENCV_VERSION}.zip \
&& rm -rf /opencv-${OPENCV_VERSION} \
&& rm -rf /opencv_contrib-${OPENCV_VERSION}

ENV PYTHONPATH="/usr/lib/python3.6/site-packages/:$PYTHONPATH" 

# IMAGEPYPEPLINES DEPENDENCIES --- CPU BOUND ON WINDOWS!!! THIS IS DEFAULT!
################################################################################
RUN if [ "$IP_GPU_ENABLED" = "ON" ]; then pip install tensorflow-gpu==1.13.1; else pip install tensorflow==1.13.1; fi
RUN pip install imagepypelines
# dev dependencies
RUN pip install Sphinx \
	  sphinx_bootstrap_theme \
	  m2r \
	  pytest \
	  pytest-cov \
	  hypothesis \
	  coverage \
	  codecov


# FINISH UP
################################################################################
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y vim
# Install X11 dependencies for future graphics support (March 2nd, 2019)
RUN apt-get update && apt-get install -y libxtst-dev


# Copy the startup script into the docker image
COPY ./startup.sh /root/startup.sh
RUN echo '/root/startup.sh' >> /root/.bashrc
# RUN if [ "$IP_GPU_ENABLED" = "ON" ]; then echo 'export PS1="\033[38;5;208m"\(imagepypelines-gpu\)"\e[39m\e[49m$PS1"' >> /root/.bashrc; else echo 'export PS1="\033[38;5;208m"\(imagepypelines\)"\e[39m\e[49m$PS1"' >> /root/.bashrc; fi
