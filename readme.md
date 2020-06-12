## What Is This?

A Super Simple Monitoring Webapp Thingi written in Python 3 on top of flask.

#### Deployment

Deploying BasicMonitor is super simple. 
Part of my motivation for writing basicmonitor came from the frustations in deploying the otherwise 
amazing monitoring software [Zabbix](https://www.zabbix.com/) 
Install using pip:
```pip
pip install https://github.com/TorbenFricke/basicmonitor/archive/master.zip
```

And run using:
```bash
python -m basicmonitor
```

You can specify some baisc settings using command line arguments. Check them out using: 
```bash
python -m basicmonitor --help
```
Most importantly, you can run basicmonitor from a prefix. 
This prefix will apply to all routes allowing you reverse proxy from another Webapp without interfereing with its routes.

#### Security

Basicmonitor does not provide a sufficient amount of security on its own for any environment.
Having access to the basicmonitor API allows for trivial denial of service attacks and surely, there is some remote code 
execution in there. 

**So, what should you do?** Run basicmonitor with a prefix `python -m basicmonitor -prefix monitor` 
and reverse proxy to it from another Webapp that provides 
authentication or from a Webserver like nginx with 
[baisc auth](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/).

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

