obks.std=sqrt(obks.var);
obks.low=obks.prd-(2*obks.std);
obks.upp=obks.prd+(2*obks.std);
cri_obks.map=obks.low gt ln(500); 
sav_obks.map=obks.upp lt ln(500);
ndi_obks.map=(obks.low le ln(500)) and (obks.upp ge ln(500));
