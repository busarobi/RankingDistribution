import numpy as np
import os
os.chdir("/Users/busafekete/work/RankingDistribution/trank/")
from trank import normalizationMallows
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools




M=10
arr = np.arange(0.0,1.01,0.01)
narr = np.arange(0.0,1.01,0.01)
for i, phi in enumerate(arr):
    narr[i] = normalizationMallows(M, phi)
    print(phi, narr[i])

# Create a trace
trace = go.Scatter(
    x = arr,
    y = narr
)

data = [trace]

py.plot(data, filename='normalization')