# model for simulating overland flow with manning formula
# no infiltration
# one timeslice represents 10 seconds 

binding
 Dem=demman.map;		# digital elevation model
 Ldd=lddman.map;		# local drain direction map
 RainTSS=rainman.tss;		# timeseries with rainintensity (mm/hour)
 S=slopeman.map;		# reported map with slope
 B=50;				# width of flow (metres)
 N=0.05;			# mannings roughness coefficient
 OutFlowPoint=outman.map;	# boolean map with outflow point
 DischargeTSS=discharg.tss;	# reported timeseries with discharge at
				# outflowpoint

areamap
 cloneman.map; 

timer
 1 360 1;
 
initial
 # slope in percent
 report S=slope(Dem); 
 # initial state of water
 WaterHeight=0;

dynamic
 # amount of rain per timestep (metre waterslice)
 Rain=
 # amount of water in cell (metre waterslice)
 WaterHeight=max(WaterHeight+Rain,0);
 # hydrolic radius, WaterHeight=H!!
 R=
 # flow velocity (m/s)
 V=
 # discharge (m3/s)
 report Q=
 # discharge (metre waterslice in cell) over a timestep (10 seconds)
 QHeightTimeStep=
 # inflow from neighbouring upstream cells to each cell (metre waterslice)
 InflowHeightTimeStep=upstream(Ldd,QHeightTimeStep);
 # new waterheight (metre waterslice) is old waterheight minus flow 
 # from the cell plus flow to the cell
 WaterHeight=
 # report timeseries with Q
 report DischargeTSS=timeoutput(OutFlowPoint,Q);
