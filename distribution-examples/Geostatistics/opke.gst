data(lzinc):        'zinc.col', x=1, y=2, v=3, log, max=25;
variogram(lzinc):   1.0 Exp(100); # replace it with your model!
mask:               'clone.map';
predictions(lzinc): 'opke.prd';
variances(lzinc):   'opke.var';
