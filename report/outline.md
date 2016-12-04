Need a title:
- Empirically estimating thermal coupling in microzones using markov random fields

High level outline:
- why buildings?
- problem description
- prior work
- architecture of system
- problem setup
- results
- discussion
- conclusion

Why Buildings?
- buildings use 40% of energy:
    - have lots of sensors, automated control systems
    - these are often incomplete or out of date
    - much manual effort to repair this, or to build up metadata
    - metadata can help buildings be more efficient and comfortable:
        - simultaneous heating/cooling
        - misplaced thermostats (like behind 410 soda screen)
    - want to reason about how buildings behave:
      - building models one approach, but expensive and hard to do and become out of date
      - need another method, one that can be somewhat automated and not require
        immense amounts of domain expertise

Problem Description:
- buildings assume temperature is uniform across an HVAC zone: how true is this really?
    - two complementary questions:
      1. Can we determine the nature of thermal coupling between sub-hvac-zones?
      2. Could we reconstruct the assignment of rooms to hvac zones from this information?
    - We don't address the second, but we explore the first


Prior work:
- building modeling
    https://dl.acm.org/citation.cfm?id=2993583
    https://people.eecs.berkeley.edu/~arka/papers/buildsys2015_functional.pdf
- graphical models? IPF? for this sort of thing ("temporal sensor modeling")
http://web.b.ebscohost.com/abstract?direct=true&profile=ehost&scope=site&authtype=crawler&jrnl=00012505&AN=67217602&h=OcAMYs51a7hgAhqnfmr82%2boegV5HSzfWhTJUuor8sFNmpgV08dDMJCpk0sO6MSsr3Z0xCuZz4qTiz2ftmlljvw%3d%3d&crl=c&resultNs=AdminWebAuth&resultLocal=ErrCrlNotAuth&crlhashurl=login.aspx%3fdirect%3dtrue%26profile%3dehost%26scope%3dsite%26authtype%3dcrawler%26jrnl%3d00012505%26AN%3d67217602
https://s3.amazonaws.com/academia.edu.documents/30821626/sdarticle.pdf7.pdf?AWSAccessKeyId=AKIAJ56TQJRTWSMTNPEA&Expires=1480809933&Signature=rwhmZYoJG2yNxz%2Bt7cCK8EYmX%2BI%3D&response-content-disposition=inline%3B%20filename%3DAn_experimental_system_for_advanced_heat.pdf

do we need this?
Approach: "quick" overview section
- explicitly what we're going to do
- how we're going to do it
- "now we go into more detail" etc

Architecture of System:
- sensors, database:
    - KETI and the Soda deployment
- data processing pipeline:
    - need for data cleaning; complications w/ sensors ('real world')
    - how to do data cleaning, the transformations we did
- Octave script to run IPF, generate edge parameters:
    - what would the results look like and what would we expect?

Problem Setup:
- how do decompose the space, the buildings, etc we used into graph
- go over options in how we could have represented:
    - bucketing temperature
    - more nodes; more accurate? more sensors

Results:
- write it up! visualize
- we plot min/max/mean bucket at diff bucket intervals (30s, 1min 5min 10min 30min):
    - log likelihoods!
- then we interpret the highest log likelihood models:
    - fully connected
    - physically connected

Discussion:
- is this helpful?:
    - probably will pull out a couple interesting relations, but because buildings
      are conditioned spaces, temperature doesn't tell us a whole lot, ESPECIALLY
      in the open office setting

Experiments to run still:
- bucket MUCH more roughly:
    - 30min?
    - bucket by min/max/mean
- get SODA data and start traininggg


Problem: models of buildings  are hard to make. Takes domain expertise and
time, and buildings are mutable anyway so models end up being out of date.

Buildings have BMS and we can add new sensors: presents opportunity to have
empirically driven models (even at high level) of how building behaves or is
out together

Uses of models:
- generate or validate metadata
- model predictive control
- energy audits
- fault detection

So what exactly are we doing? Determining nature of thermal coupling between
microzones. Building measures at given point, assumes temperature is uniform.
So with this method we can measure how correlated these microzones actually
are. We do this in 2 buildings.

We could also use this data to discover the graph: which rooms HAVE thermal
coupling? Which AHU/VAV connected to which zones? This is an important
question: can answer it with actuation, but this is hard to do and not always
possible and takes a long time anyway.

Outline:
- why buildings?
- problem description (specific) and prior work (if any)
- architecture and problem setup; also describe problems we would like to solve but aren't doing here (graph selection for vav-assignment)
- results: interpret the thetas, visualize everything
- discussion: was this helpful? Discuss dimensionality, Ising simplification
- conclusion
