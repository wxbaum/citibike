# Citibike Projects --WORK IN PROGRESS--

Welcome to my Citibike data projects repo. 

## Key Notes
* The requirements file might be considered lengthy due to the the 
requirements for the ipykernel package. To skip packages related to 
ipykernel, use: pip install -r "requirements_slim.txt". 

## Contents:
### notebooks/
This folder contains notebook analyses I've done using Citibike's data,
as well as utility notebooks. 

#### 1. Citibike Data Pull
Collects data from S3 and processes it into a much more memory-efficient
format. Running this notebook will create a /data folder in the root 
directory of the repo and write the Citibike data retrieved into it.

Much of the categorical data are replaced with integer IDs and 
stored in dimension tables to significantly reduce file sizes and file
read times. The "fact table" files are stored in Parquet format. 

#### 2. Empty Dock Analysis --WORK IN PROGRESS--




