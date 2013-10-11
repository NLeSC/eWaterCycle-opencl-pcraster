# model for simulation of flower seed dispersal
# ProbReach=(0.1)^(Distance/Range)

binding
 InitialPlants=iniscen.map;	# map with distribution of 
				# plants at start of modelrun
 Distance=distance;		# reported maps with distance to nearest
				# plants 
 Range=350;			# Distance for which probability is 0.1
 Probability=probab;		# reported maps with probability that
				# seed reaches cell and comes out
 NewPlants=newplant;		# reported maps with locations where
				# new plants will grow next year as a
				# result of seed dispersal
 Plants=plants;			# reported maps with the distribution of
				# plants in summertime
 Woodland=wpresent.map;		# map with forested area

areamap
 placlone.map;

timer
 1 15 1;

initial
 # distribution of plants at start of model run
 Plants=InitialPlants;
 # distribution of new plants at start of model run
 NewPlants=boolean(0);

dynamic
 # distribution of plants
 report Plants=Plants or NewPlants and Woodland;

 # distance to nearest cell with plants (m)
 report Distance=spread(Plants,0,1);
 # probability that seed reaches cell and comes out next year
 report Probability=0.1**(Distance/Range);

 # cells where plants will grow next year as a result of seed dispersal
 report NewPlants=Probability gt uniform(1);
