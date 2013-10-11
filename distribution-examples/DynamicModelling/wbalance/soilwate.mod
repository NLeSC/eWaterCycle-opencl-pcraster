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
 PrecipSurplus=rainsur;		# reported maps with precipitation surplus (mm/month)
 InitSoilwater=initsw.map;	# map with initial soilwater content
 Soilwater=soilwate;		# reported maps with soilwater content (mm)
 
areamap
 clone.map;

timer
 1 12 1;

initial
 # crop coefficients (k)
 K=lookupscalar(CropCoeffTable,LandUse);

 # initial soilwater content (mm)
 Soilwater=InitSoilwater; 
 # maximum soilwater content (mm)
 MaxSoilwater=scalar(400);

dynamic
 # precipitation
 report Precip=timeinputscalar(RainTimeSeries,RainAreas);
 # total volume precipitation over study area, in cubic metres per second 
 report VolumePrecip=maptotal(Precip)*(cellarea()/2628);

 # reference evapotranspiration
 EvapRef=timeinputscalar(EvapRefTimeSeries,1);
 # evapotranspiration
 report Evap=K*EvapRef;

 # precipitation surplus
 report PrecipSurplus=Precip-Evap;

 # intermediate soilwater content: soilwater plus precipitation surplus
 Soilwater=Soilwater+PrecipSurplus;
 # soilwater content, no saturation
 report Soilwater=min(Soilwater,MaxSoilwater);
