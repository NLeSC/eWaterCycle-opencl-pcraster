# This example script demonstrates the use of the
# PCRasterModflow extension. It recreates the example
# problem given in the user guide of MODFLOW-2000
# (Open file report 00-92)
#
# To run the script use
# python2.5 example.py

from PCRaster import *


setclone("clone.map")
mf = initialise(clone())

# grid specification
mf.createBottomLayer("bottom.map", "l1_top.map")
mf.addConfinedLayer("l2_top.map")
mf.addLayer("l3_top.map")
mf.addConfinedLayer("l4_top.map")
mf.addLayer("elev.map")

# simulation parameter
mf.setDISParameter(1, 0, 86400, 1, 1, 1)

# adding the boundary conditions to the MODFLOW model
mf.setBoundary("l1_bound.map", 1)
mf.setBoundary("l3_bound.map", 3)
mf.setBoundary("l5_bound.map", 5)

# adding the initial values to the MODFLOW model
mf.setInitialHead("head.map", 1)
mf.setInitialHead("head.map", 3)
mf.setInitialHead("head.map", 5)

# adding the conductivities to the MODFLOW model
mf.setConductivity(0, "hcond_l1.map", "vcond_l1.map", 1)
mf.setConductivity(0, "hcond_l1.map", "vcond_l2.map", 2)
mf.setConductivity(0, "hcond_l3.map", "vcond_l3.map", 3)
mf.setConductivity(0, "hcond_l3.map", "vcond_l4.map", 4)
mf.setConductivity(1, "hcond_l5.map", "vcond_l5.map", 5)

# solver package
mf.setSIP(50, 5, 1.0, 0.001, 0, 0.001)

mf.setDryHead(1E30)

# adding the drain
mf.setDrain("drain_elev.map", "drain_cond.map", 5)

# specifying the recharge
mf.setRecharge("rch.map", 1)

# adding well 
mf.setWell("well_l1.map", 1)
mf.setWell("well_l3.map", 3)
mf.setWell("well_l5.map", 5)


# execute MODFLOW modelling engine
mf.run();

# retrieve head values
hFive = mf.getHeads(5)
report(hFive, "hFive.map")
hThree = mf.getHeads(3)
report(hThree, "hThree.map")
hOne = mf.getHeads(1)
report(hOne, "hOne.map")

# retrieve drain leakage
dFive = mf.getDrain(5);
report(dFive, "dFive.map")
