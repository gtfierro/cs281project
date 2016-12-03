cp ../*.csv .
cp ../*.mat .
cp ../IPF.m .
docker build -t gtfierro/octave .
docker push gtfierro/octave
