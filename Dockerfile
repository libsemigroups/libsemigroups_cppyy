FROM libsemigroups/libsemigroups

MAINTAINER Murray Whyte <mw231@st-andrews.ac.uk>

RUN sudo apt-get install -y python3-pip vim

RUN pip3 install cppyy tox

RUN git clone https://github.com/libsemigroups/libsemigroups_cppyy

ENV PATH="/home/libsemigroups/.local/bin/:${PATH}"

ENV LD_LIBRARY_PATH="/usr/local/lib/:${LD_LIBRARY_PATH}"

WORKDIR /home/libsemigroups/libsemigroups_cppyy
