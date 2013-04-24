straopk.std=sqrt(straopk.var);
straopk.low=straopk.prd-(2*straopk.std);
straopk.upp=straopk.prd+(2*straopk.std);
cri_stra.map=straopk.low gt ln(500); 
sav_stra.map=straopk.upp lt ln(500);
ndi_stra.map=(straopk.low le ln(500)) and (straopk.upp ge ln(500));
