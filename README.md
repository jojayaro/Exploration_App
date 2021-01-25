# Streamlit App and Python Script to process and visualize AER ST1 and ST49 Data (WIP)

Python Scripts are currently jupyter notebooks that download AER daily reports in raw text, then parse them, enter data into dataframe, write data into CSV file, and a separate script merges the CSVs into one file (e.g. ST1.csv or ST49.csv)

Streamlit App then uses the merged CSV files to visualize the data

All this is being developed in a container for later deployment on a Kubernetes cluster (k3s)

## Next Steps

- Develop Streamlit App to include more visualizations and information
- Deploy container in Kubernetes cluster and use Okteto to continue development
- Convert notebooks into python scripts and run them automatically in the server
- Improve merging the new data into the main CSVs
- Move data from dataframes into a DB instead of using CSVs

## Update 1
- Deployed container in Kubernetes cluster and using Argo CD (slow)
- Converted notebooks into python scripts and run them automatically in the server
- Improved merging the new data into the main CSVs
