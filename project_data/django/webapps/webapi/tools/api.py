import requests
import json
from datetime import datetime,timezone,timedelta
import pytz
from pytz import timezone
from webapi.models import TC
TZPST= timezone("America/Los_Angeles")

#--------------------
def list_alerts() :
#--------------------
  headers = {
  'X-Api-Key': 'a1f4b78c17f0699a1566c786540236312129abe51783eda',
  }
  response = requests.get('https://api.newrelic.com/v2/alerts_violations.json', headers=headers)

  return json.loads(response.text)["violations"]

#--------------------
def config_show(tcid,fname) :
#--------------------
  tc = TC.objects.get(id=int(tcid))
  return tc.raw_files(fname)
  
#--------------------
class AlertAPI() :
  #-----------------
  def __init__(self) :
  #-----------------
    self.create_list()

  #-----------------
  def create_list(self):
  #-----------------
    alerts = list_alerts()
    self.alarms = []
    for a in alerts :
      a_fix = self.fixtime(a)
      a_fix["status"] = "open"
      if "closed_utc_time" in a_fix :
        c =  datetime.utcfromtimestamp(int(a_fix["closed_at"])/1000)
        if "opened_utc_time" in a_fix :
          o =  datetime.utcfromtimestamp(int(a_fix["opened_at"])/1000)
          a_fix["delta"] = c - o
          a_fix["status"] = "closed"

      self.alarms.append(a_fix)

# for the Open and Closed We will group them together

#--------------------
  def _fixtime(self,stamp) :
#--------------------
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    event_time = datetime.utcfromtimestamp(int(stamp)/1000)
    event_time = event_time.astimezone(pytz.utc)
    local_time = event_time.astimezone(TZPST)
    return event_time.strftime(fmt),local_time.strftime(fmt)
  
#--------------------
  def fixtime(self,rec) :
#--------------------
    if "opened_at" in rec :
      rec["opened_utc_time"],rec["opened_local_time"] = self._fixtime(rec["opened_at"])
    if "closed_at" in rec  :
      rec["closed_utc_time"],rec["closed_local_time"] = self._fixtime(rec["closed_at"])
    return rec

'''
{
  "violation": {
    "id": "integer",
    "label": "string",
    "duration": "integer",
    "policy_name": "string",
    "condition_name": "string",
    "priority": "string",
    "opened_at": "integer",
    "closed_at": "integer",
    "entity": {
      "product": "string",
      "type": "string",
      "group_id": "integer",
      "id": "integer",
      "name": "string"
    },
    "links": {
      "policy_id": "integer",
      "condition_id": "integer",
      "incident_id": "integer"
    }
  }
}
'''
