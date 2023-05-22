# download dataset
download yellow taxi data 2022/01 and 2022/02
```
cd data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet
```

# mlops maturity
0. No mlops
   - no automation
   - all code in jupyter

1. Devops, no mlops
   - releases are automated
   - unit & integration tests
   - ci/cd
   - ops metrics
   - no experiment tracking
   - no reproducibility
   - ds seperated from engineers

2. Automated training
   - training pipeline
   - experiment tracking
   - model registry
   - low friction deployment
   - ds work with engineers

3. Automated deployment
   - easy to deploy model
   - a/b test
   - model monitoring

4. Full mlops automation

ref: https://learn.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model