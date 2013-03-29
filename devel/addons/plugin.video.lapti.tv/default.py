# -*- coding: utf-8 -*-
#!/usr/bin/python
# Writer (c) 2012, Silhouette, E-mail: otaranda@hotmail.com
# Rev. 0.1.1



import urllib
import urllib2
import sys
import os
import re
import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
import time
import random
import threading
from StringIO import StringIO
import gzip

pluginhandle = int(sys.argv[1])
Addon         = xbmcaddon.Addon(id='plugin.video.lapti.tv')
addon_id      = Addon.getAddonInfo('id')
addon_icon    = Addon.getAddonInfo('icon')

INC_url = 'http://lapti.tv/'

dbg = 1
def dbg_log(line):
  if dbg: xbmc.log(line)

def ShowMessage(heading, message, times = 3000, pics = addon_icon):
    try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading.encode('utf-8'), message.encode('utf-8'), times, pics.encode('utf-8')))
    except Exception, e:
        print( '[%s]: ShowMessage: Transcoding UTF-8 failed [%s]' % (addon_id, e), 2 )
        try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, times, pics))
        except Exception, e:
            print( '[%s]: ShowMessage: exec failed [%s]' % (addon_id, e), 3 )

def get_url(target, post=None):
    try:
        request = urllib2.Request(url = 'http://www.lapti.tv', data = post,  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:19.0) Gecko/20121218 Firefox/19.0'})
        request.add_header('User-Agent', 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.7.62 Version/11.00')
        request.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
        request.add_header('Accept-Language', 'ru,en;q=0.9')
        response = urllib2.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            http = f.read()
        else:
            http = response.read()
        response.close()
        return http
    except Exception, e:
        print( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
        ShowMessage('HTTP ERROR', e, 5000)
        #print('{LOG}[GET]:Error')

def INC_prls(url):
    dbg_log('INC_prls')
   
    http = get_url(url)
    oneline = re.sub('[\r\n\t]', ' ', http)
    ch_cont = re.compile('<div class="ch-wrappers ch-center"> +?<ul> +?(.+?) +?</ul> +?</div>').findall(oneline)
    if len(ch_cont):
        pr_ls = re.compile('<a class="(.+?)" +?href="(.+?)"></a>').findall(ch_cont[0])
    else:
        pr_ls = None

    if pr_ls:
        for descr, href in pr_ls:
            name = descr
            dbg_log(name)
            item = xbmcgui.ListItem(name)
            uri = sys.argv[0] + '?mode=PLAY'
            uri += '&url='+urllib.quote_plus(INC_url + href)
            item.setInfo( type='video', infoLabels={'title': name, 'plot': descr})
            item.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(pluginhandle, uri, item)
    xbmcplugin.endOfDirectory(pluginhandle)    
    
def INC_play(url, name, thumbnail, plot, mycookie):
    dbg_log('-INC_play')
    response = get_url(url)
    lnks_ls = re.compile('http://([^|^&]+?)/playlist\.m3u8').findall(response)
    if len(lnks_ls):
        item = xbmcgui.ListItem(path = 'http://' + lnks_ls[0] + '/playlist.m3u8')
        xbmcplugin.setResolvedUrl(pluginhandle, True, item)
   
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
url=None
name=''
plot=''
cook=''
mode=None
#thumbnail=fanart
thumbnail=''

dbg_log('OPEN:')

try:
    mode=params['mode']
    dbg_log('-MODE:'+ mode + '\n')
except: pass
try:
    url=urllib.unquote_plus(params['url'])
    dbg_log('-URL:'+ url + '\n')
except: pass
try:
    cook=urllib.unquote_plus(params['cook'])
    dbg_log('-COOK:'+ cook + '\n')
except: pass
try:
    name=urllib.unquote_plus(params['name'])
    dbg_log('-NAME:'+ name + '\n')
except: pass
try: 
    thumbnail=urllib.unquote_plus(params['thumbnail'])
    dbg_log('-THAMB:'+ thumbnail + '\n')
except: pass
try: 
    plot=urllib.unquote_plus(params['plot'])
    dbg_log('-PLOT:'+ plot + '\n')
except: pass



if mode == 'PLAY': INC_play(url, name, thumbnail, plot, cook)
elif mode == None: INC_prls(INC_url)

dbg_log('CLOSE:')

