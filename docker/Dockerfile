FROM ubuntu:xenial
MAINTAINER Gabe Fierro <gtfierro@eecs.berkeley.edu>

RUN apt-get update && apt-get install -y octave less wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD sdh_office_data.csv sdh_office_data.csv
ADD sdhofficesGedges.mat sdhofficesGedges.mat
ADD idea1.csv idea1.csv
ADD sdh_sub.csv sdh_sub.csv
ADD Gedges.mat Gedges.mat
ADD subGedges.mat subGedges.mat

ADD sdh_small_edges.mat sdh_small_edges.mat
ADD sdh_small_data.csv sdh_small_data.csv

ADD sdh_small_edges_30m.mat sdh_small_edges_30m.mat
ADD sdh_small_data_30m.csv sdh_small_data_30m.csv

ADD soda_amplab_edges.mat soda_amplab_edges.mat
ADD soda_amplab_data.csv soda_amplab_data.csv
ADD IPF.m IPF.m

# where the entity file goes
ENTRYPOINT [ "/bin/bash" ]
