# -*- coding: utf-8 -*-

import requests
import ast
from datetime import datetime
import ConfigParser

cfgPars  = ConfigParser.RawConfigParser()
cfgPars.read('hitron.cfg')

username = cfgPars.get('Login', 'username')
password = cfgPars.get('Login', 'password')

downFile = cfgPars.get('Stat files', 'downFile')
upFile = cfgPars.get('Stat files', 'upFile')

homeURL = 'http://hitronhub.home/'
loginURL = homeURL + 'goform/login'
downStatsURL = homeURL + 'data/dsinfo.asp'
upStatsURL = homeURL + 'data/usinfo.asp'

s = requests.Session()

payload = {'usernamehaha': username, 'passwordhaha': password}
rLogin = s.post(loginURL, data=payload)

rDown = s.get(downStatsURL)
rUp = s.get(upStatsURL)
timestamp = datetime.now()

statsDown = ast.literal_eval(rDown.text.encode(rDown.encoding))
statsUp = ast.literal_eval(rUp.text.encode(rUp.encoding))

fDown = open(downFile, 'a')
fUp = open(upFile, 'a')

for e in statsDown:
  line = timestamp.strftime('%Y-%m-%dT%H:%M:%S') + '\t' + \
         e['portId'] + '\t' + \
         e['channelId'] + '\t' + \
         e['frequency'] + '\t' + \
         e['symbolRate'] + '\t' + \
         e['modulation'] + '\t' + \
         e['signalStrength'] + '\t' + \
         e['snr'] + '\n'
  fDown.write(line)

for e in statsUp:
  line = timestamp.strftime('%Y-%m-%dT%H:%M:%S') + '\t' + \
         e['portId'] + '\t' + \
         e['channelId'] + '\t' + \
         e['frequency'] + '\t' + \
         e['bandwidth'] + '\t' + \
         e['scdmaMode'] + '\t' + \
         e['signalStrength'] + '\n'
  fUp.write(line)

fDown.close()
fUp.close()
