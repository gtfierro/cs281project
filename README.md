# CS281A Project

Determining the nature of thermal coupling between 'microzones'; essentially fitting a graphical model from empirical data

The components:
- quantize AMP lab into "microzones": 1 per small room, and divide up the main shared office space into known-size chunks:
    - some of these will have sensors
    - some will have thermostats
    - some will have dampers (air output)
    - some will have windows
    - idea: make thermostats, dampers, windows, etc another kind of node?
    - SIMPLIFY the interactions between 

We can create a graph of the nodes and their edges at a given point in time (say we divide up time into 5 or 10 minute intervals); an edge
means there is some amount of thermal coupling between those two nodes.


### Idea 1

Model the connections between microzones as a pairwise Markov Random field; the edges are +1,-1 if they are connected/unconnected (maybe use 1,0?).
The data vectors are "between" readings: for each node `X_s`, value is +1 if temperature went up, -1 if temperature went down.

This can be nice because we can 'stream' it; insert a new data point and re-train to see the new model?

Steps (for SDH):
- Data collection:
  - [ ] Download the KETI-mote temperature data (raw)
  - [ ] Transform to bucket into N-minute chunks (probably 5-min)
- Graph structure:
  - [ ] Need image of the floor
  - [ ] Need positions of the KETI motes
  - [ ] Divide floor into microzones and place KETImotes, dampers, thermostats, etc inside them


### Implementations:

Libs to look at:
https://github.com/jmschrei/pomegranate
http://pgmpy.org/estimators.html
