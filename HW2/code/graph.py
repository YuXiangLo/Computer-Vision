import plotly.express as px
import pandas as pd
df = pd.read_csv('histogram.csv')
fig = px.bar(df, x='Intensity', y='PixelCount', title='Histogram')
fig.show()

