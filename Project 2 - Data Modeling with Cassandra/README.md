# Project: Data Modeling with Cassandra

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
The analytics team is particularly interested in understanding what songs users are listening to.

In this project, we'll help them by creating a database on Apache Cassandra and ETL pipeline for this analysis.

## Dataset Description
The data used in this work are located in the **event_data folder** and are partitioned by day and are in CSV format. 
For instance, here is the file path to one file in this dataset.

```
event_data/2018-11-01-events.csv
```

And below is an example of what the data in an $event_data$ file, 2018-11-01-events.csv, looks like.

