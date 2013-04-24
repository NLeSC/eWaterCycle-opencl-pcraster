# model for simulation of rainfall and evapotranspiration
# one timeslice represents one month

binding
 RainTimeSeries=rain12.tss;	# timeseries with rainfall (mm) per month 
				# for two rain areas	
 Precip=rain;			# reported maps with precipitation,
				# rain is suffix of filenames
 RainAreas=rainarea.map;	# map with two rain areas
 VolumePrecip=volrain.tss;	# reported timeseries with volume rain per
				# month (cubic metres per second)
 CropCoeffTable=crcoefa.tbl;	# column table with crop coefficients for
				# classes on LandUse 
 LandUse=landuse.map;		# map with nominal landuse classes 1,2,3 
 EvapRefTimeSeries=evaref12.tss;# timeseries with reference 
				# evapotranspiration (mm) per month
 K=cropcoef.map;		# reported map with crop coefficients

areamap
 clone.map;

timer
 1 12 1;

initial
 # crop coefficients (k)
 report K=lookupscalar(CropCoeffTable,LandUse);
 
dynamic
 # precipitation
 report Precip=timeinputscalar(RainTimeSeries,RainAreas);
 # total volume precipitation over study area, in cubic metres per second 
 report VolumePrecip=maptotal(Precip)*(cellarea()/2628);

 # reference evapotranspiration
 EvapRef=timeinputscalar(EvapRefTimeSeries,1);
 # evapotranspiration
 report Evap=K*EvapRef;
