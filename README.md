# ======

# Data and ML Monitoring with Grafana and Prometheus for Churn Prediction


## Data:

Data: Expresso Churn Prediction Challenge
https://www.kaggle.com/datasets/hamzaghanmi/expresso-churn-prediction-challenge?select=Train.csv
The objective is to develop a predictive model that determines the likelihood for a customer to churn - to stop purchasing airtime and data from Expresso telecom provider.
Data contains information of about 2 million customers.
Part of the data will be used for training and part will be used for simulating 
inference requests to perform ML monitoring.


## Prometheus:
- Pull vs Push Model:

By default, Prometheus uses the Pull Model. It scrapes (pulls) metrics from configured targets at regular intervals.
Each target exposes metrics on an HTTP endpoint (usually /metrics). This model is used for long-running services like web-servers.

Push Model: Is used when he application pushes metrics to a central metrics service or gateway. This model is used for short-lived/batch
jobs (ex Model Training) that don't live enough to be scraped. Prometheus then scrapes the metrics from the Push Gateway
as it were a normal scraping target and stores them in its time-series database.

In this project, upon ML model training completion, the class distribution metric (Churn/No Churn) is pushed to the Push Gateway 
so that we have the metrics on how well the data was ballanced during training.


TODO:


uvicorn monitoring-with-prometheus.app:app --host 0.0.0.0 --reload


UPD Dependencies (using pip-tools):
pip-compile
pip install -r requirements.py



Build image
1. docker build -t monitoring-with-prometheus:latest .
Build containers
2. docker-compose build
3. docker-compose up

Run with docker-compose

Docker:
<our>:<docker>

docker volume:

#mount our local folder to a docker folder not to have to rebuild the container
each time a file changes in or local dir

volumes:
 -<localdir>:<dockerdir>

 Note: prometheus and prometheus-data folders are created so that we can see what prometheus writes 
 to out local folder so we can access it.



Note : We need to run docker-compose build when we add new dependencies



TODO watch PromQL For Mere Mortals
Grafana - 3000
Prmoetheus - 9090
app - 8000



rate(traffic_count_total[1m])

histogram_quantile(0.5, sum(rate(seasonal_gauge[5m])) by (le))

histogram_quantile(0.5, sum(rate(seasonal_gauge[10m])))

count_over_time((seasonal_gauge - stddev_over_time(seasonal_gauge[1m])) > 1)[1h]



Delete all data in prometheus:
> Delete contents of prometheus-data/data


docker build -f Dockerfile.Api -t monitoring-with-prometheus:latest .
docker build -f Dockerfile.PushGateway -t push-gateway:latest .

Weel 1 :
Theory.
Golden signals, Software monitoring,
Prometheus and Graphana intro.


Week 2 :
Anomaly Detection.


Week 3 :
Implement Data Drift metric (Wasserstein distance)
Using the push model


Week 4 :
Implement the feedback loop:
-> Given that the actuals comee with a certain delay, create model performance monitoring metrics
based on what the model predicted and what the actulas were...