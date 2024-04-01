# Anomaly Visualizer

Anomaly Visualizer is a Python tool that can help you visualize your data. Find anomalies, understand the baseline for your data and also designed to visualize hierarchical data with NetworkX and Matplotlib. It generates a river flow metaphor visualization for a given dataset, facilitating the analysis of hierarchical relationships between data attributes.

## Features

- Supports visualization of hierarchical data with varying levels of depth.
- Generates dynamic node sizes and colors based on data attributes.
- Provides flexibility in adjusting distinct value limits and default colors.

## Requirements
Please run in a virtual environment
```
pip install -r req.txt --upgrade
```

## Sample Usage 

#### From Code

```python
# Sample DataFrame
data = {'A': [1, 1, 2, 2], 'B': [1, 2, 3, 4], 'C': [5, 6, 7, 8]} #use your complex data here
df = pd.DataFrame(data)

# Instantiate AnomalyVisualizer and visualize the DataFrame
anomaly_visualizer = AnomalyVisualizer()
anomaly_visualizer.anomaly_visualizer(df)
```

#### From Commandline