FROM ghcr.io/allennliu/node-base:16.0.0-slim

ENV NODE_SOURCE /usr/src

COPY . $NODE_SOURCE

WORKDIR $NODE_SOURCE

RUN apt-get update && \
    apt-get install -y gcc g++ make \
                       libncurses5-dev \
                       libncursesw5-dev \
                       ncurses-dev && \
    cd tools && \
    tar zxvf vim74.tar.gz && \
    cd vim74 && \
    ./configure --prefix=/usr \
                --with-features=huge \
                --disable-selinux \
                --enable-pythoninterp \
                --enable-cscope \
                --enable-multibyte && \
    make && make install && \
    ln -s /usr/local/bin/vim /usr/local/bin/vi


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                       curl dnsutils git libhiredis-dev node-gyp \
                       ssh sshpass plink telnet unzip \
                       python3 \
                       python3-dev \
                       build-essential \
                       python3-setuptools \
                       python3-pip \
                       default-libmysqlclient-dev \
                       libmariadbclient-dev \
                       unixodbc unixodbc-dev

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements_external.txt || true

RUN echo 'alias vi="vim"' >> ~/.bashrc

EXPOSE 8000 22

USER root

ENV PYTHONIOENCODING utf-8

CMD ["bash", "service.sh", "--prod"]
