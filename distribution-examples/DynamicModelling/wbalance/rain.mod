# model for simulation of rainfall
# one timeslice represents one month

binding
 RainTimeSeries=rain12.tss;	# timeseries with rainfall (mm) per month 
				# for two rain areas	
 Precip=rain;			# reported maps with precipitation,
				# rain is suffix of filenames
 RainAreas=rainarea.map;	# map with two rain areas

areamap
 clone.map;

timer
 1 12 1;

initial
 # this section is empty

dynamic
 # precipitation
 report Precip=timeinputscalar(RainTimeSeries,RainAreas);
