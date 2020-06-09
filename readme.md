## What Is This?

A Super Simple Monitoring Webapp Thingi

## Deployment

Deploying BasicMonitor is super simple. Install using pip:
```pip
pip install https://github.com/TorbenFricke/basicmonitor/archive/master.zip
```

#### Where is my data

Your data is stored in a sqlite database in your home directory (i.e. `/home/tim/basicmonitor/basicmonitor.db`)



## General Concept

### Sensors

Gather data, such as:
* Time utill DOM/HTML content
* HTML content from a URL
* Host system CPU usage

### Triggers

Connect Sensors to Alerts. If for instance the HTML contains 
a substing, trigger an alert.

### Action

Alert a user that something happend or cause somthing to happen automatically. Alerts available:
* [Pushover](https://pushover.net/)
* (in development) Webhook (allow interaction with [IFTTT](https://ifttt.com/maker_webhooks))