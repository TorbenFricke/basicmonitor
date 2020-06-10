## What Is This?

A Super Simple Monitoring Webapp Thingi

#### Deployment

Deploying BasicMonitor is super simple. Install using pip:
```pip
pip install https://github.com/TorbenFricke/basicmonitor/archive/master.zip
```

And run using:
```bash
python -m basicmonitor
```

## General Concept

#### Sensors

Gather data, such as:
* Time utill DOM/HTML content
* HTML content from a URL
* Host system CPU usage

#### Triggers

Connect Sensors to Alerts. If for instance the HTML contains 
a substing, trigger an alert.

#### Actions

Alert a user that something happend or cause somthing to happen automatically. Alerts available:
* [Pushover](https://pushover.net/)
* (in development) Webhook (allow interaction with [IFTTT](https://ifttt.com/maker_webhooks))


---

#### Where is my data

All your data is stored in a sqlite database in your home directory. 
On unix this will look something like this: 
`/home/tim/basicmonitor/basicmonitor.db` 

On Windows you'll end up with this 
`c:\\user\tim\basicmonitor\basicmonitor.db`

