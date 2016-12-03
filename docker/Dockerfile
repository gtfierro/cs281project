FROM ubuntu:xenial
MAINTAINER Gabe Fierro <gtfierro@eecs.berkeley.edu>

RUN apt-get update && apt-get install -y octave less wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD idea1.csv idea1.csv
ADD sdh_sub.csv sdh_sub.csv
ADD Gedges.mat Gedges.mat
ADD subGedges.mat subGedges.mat
ADD IPF.m IPF.m

# where the entity file goes
ENTRYPOINT [ "/usr/bin/octave-cli" ]
