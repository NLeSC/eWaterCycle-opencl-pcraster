# model for simulation of flower seed dispersal
# ProbReach=(0.1)^(Distance/Range)

binding
 InitialPlants=inipla.map;	# map with distribution of 
				# plants at start of modelrun
 Distance=distance;		# reported maps with distance to nearest
				# plants 
 Range=350;			# Distance for which probability is 0.1
 Probability=probab;		# reported maps with probability that
				# seed reaches cell and comes out

areamap
 placlone.map;


timer
 1 1 1;


initial
 # distribution of plants at start of model run
 Plants=InitialPlants;

dynamic
 # distance to nearest cell with plants (m)
 report Distance=spread(Plants,0,1);
 # probability that seed reaches cell and comes out next year
 report Probability=0.1**(Distance/Range);
