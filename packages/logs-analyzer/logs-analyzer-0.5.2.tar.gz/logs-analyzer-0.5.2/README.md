# Logs-analyzer

Logs-analyzer is a Python based library containing functions that can help you extract usable data from logs.

## Status

**Master:** ![Codeship Status for ddalu5/logs-analyzer](https://codeship.com/projects/b12161a0-f65e-0133-0e7a-7e18ff1a37b8/status?branch=master)
 [![Build Status](https://travis-ci.org/ddalu5/logs-analyzer.svg?branch=master)](https://travis-ci.org/ddalu5/logs-analyzer)
 
**Develop:** ![Codeship Status for ddalu5/logs-analyzer](https://codeship.com/projects/b12161a0-f65e-0133-0e7a-7e18ff1a37b8/status?branch=develop)
 [![Build Status](https://travis-ci.org/ddalu5/logs-analyzer.svg?branch=develop)](https://travis-ci.org/ddalu5/logs-analyzer)

## Quickstart

### Support
**Python 2:** 2.7
**Python 3:** 3.6, 3.7

### Install
using pip : `pip install logs-analyzer`

### Code sample
```python
from logs_analyzer.lib import LogsAnalyzer

nginx_logsanalyzer = LogsAnalyzer('nginx')
nginx_logsanalyzer.add_date_filter(minute='*', hour=22, day=4, month=5)
nginx_logsanalyzer.add_filter('192.10.1.1')
requests = nginx_logsanalyzer.get_requests()

```

## Non-object functions

### Function get_service_settings
Get default settings for the said service from the settings file, three type
of logs are supported right now: `nginx`, `apache2` and `auth`.
#### Parameters
**service_name:** service name  (e.g. nginx, apache2...).
#### Return
Returns a dictionary containing the chosen service settings or `None` if the
service doesn't exists.
#### Sample
`nginx_settings = get_service_settings('nginx')`

### Function get_date_filter
Get the date's pattern that can be used to filter data from
logs based on the parameters.
#### Parameters
**settings:** the target logs settings.

**minute:** default now, minutes or * to ignore.

**hour:** default now, hours or * to ignore.

**day:** default now, day of month.

**month:** default now, month number.

**year:** default now, year.

#### Sample
```python
nginx_settings = get_service_settings('nginx')
date_pattern = get_date_filter(nginx_settings, 13, 13, 16, 1, 1989)
print(date_pattern)
```
Prints `[16/Jan/1989:13:13`

### Function filter_data
Filter received data/file content and return the results.
#### Parameters
**log_filter:** string that will be used to filter data

**data:** data to be filtered (String) or None if the data will
be loaded from a file.

**filepath:** filepath from where data will be loaded or None if
the data has been passed as a parameter.

**is_casesensitive:** if the filter has to be case sensitive
(default True).

**is_regex:** if the filter string is a regular expression
(default False).

**is_reverse:** (boolean) invert selection.
#### Return
Returns filtered data (String).
#### Sample
```python
nginx_settings = get_service_settings('nginx')
date_filter = get_date_filter(nginx_settings, '*', '*', 27, 4, 2016)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(base_dir, 'logs-samples/nginx1.sample')
data = filter_data('192.168.5', filepath=file_name)
data = filter_data(date_filter, data=data)
```

### Function get_web_requests
Analyze the web logs (Nginx & Apache2 for now) data and return list of requests
formatted as the model (pattern) defined.
#### Parameters
**data:** (String) data to analyzed.

**pattern:** (Regular expression) used to extract requests.

**date_pattern:** (Regular expression or None) used to extract date elements
to have ISO formatted dates.

**date_keys:** (List or None) list of extracted date elements placements.
#### Sample
```python
apache2_settings = get_service_settings('apache2')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(base_dir, 'logs-samples/apache1.sample')
data = filter_data('127.0.1.1', filepath=file_name)
requests = get_web_requests(data, apache2_settings['request_model'],
                            nginx_settings['date_pattern'], nginx_settings['date_keys'])
```

### Function get_auth_requests
Analyze the Auth logs data and return list of requests
formatted as the model (pattern) defined.
#### Parameters
**data:** (String) data to analyzed.

**pattern:** (Regular expression) used to extract requests.

**date_pattern:** (Regular expression or None) used to extract date elements
to have ISO formatted dates.

**date_keys:** (List or None) list of extracted date elements placements.
#### Sample
```python
auth_settings = get_service_settings('auth')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
date_filter = get_date_filter(auth_settings, '*', 22, 4, 5)
file_name = os.path.join(base_dir, 'logs-samples/auth.sample')
data = filter_data('120.25.229.167', filepath=file_name)
data = filter_data(date_filter, data=data)
requests = get_auth_requests(data, auth_settings['request_model'],
                                     auth_settings['date_pattern'], auth_settings['date_keys'])
```