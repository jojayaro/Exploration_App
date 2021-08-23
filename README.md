# Python scripts to parse data from AER ST1 and ST49 Reports

## Update 22-08-2021
All the data was moved to a MongoDB Database and now the script downloads the text files daily, parses them, and inserts the data into the database.

App in the following link pulls the data directly from database to simplify the whole process.

https://github.com/jojayaro/Exploration_Data_Container

## Next Steps
- ?

<<<<<<< HEAD
## Deprecated
Python Scripts download AER daily reports in raw text, then parse them, enter data into dataframe, write data into CSV file, and a separate script merges the CSVs into one file (e.g. ST1.csv or ST49.csv)
=======
- Develop Streamlit App to include more visualizations and information
- Deploy container in Kubernetes cluster and use Okteto to continue development
- Convert notebooks into python scripts and run them automatically in the server
- Improve merging the new data into the main CSVs
- Move data from dataframes into a DB instead of using CSVs

## Update 1
- Deployed container in Kubernetes cluster
- Converted notebooks into python scripts and run them automatically in the server
- Improved merging the new data into the main CSVs

## Update 2
- Installed ArgoCD in cluster and testing Automatic refresh when Container gets rebuilt
>>>>>>> 202fcf38d0e6b379bf129c76f98dae2706b852f1
