data(zinc.1):        'zinc.col', x=1, y=2, v=3, log, d=1;
data(zinc.2):        'zinc.col', x=1, y=2, v=3, log, d=2;
data(zinc.3):        'zinc.col', x=1, y=2, v=3, log, d=3;

mask:                'floodcls.map';

predictions(zinc.1): 'zinc1.prd';
predictions(zinc.2): 'zinc2.prd';
predictions(zinc.3): 'zinc3.prd';
variances(zinc.1):   'zinc1.var';
variances(zinc.2):   'zinc2.var';
variances(zinc.3):   'zinc3.var';
