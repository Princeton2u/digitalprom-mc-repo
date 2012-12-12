# -*- coding: utf-8 -*-
#!/usr/bin/python
# Writer (c) 2012, Digitalprom, E-mail: info@digitalprom.ru
# Rev. 0.1.1



import urllib,urllib2,re,sys,os,time
import xbmcplugin,xbmcgui,xbmcaddon

pluginhandle = int(sys.argv[1])
__addon__       = xbmcaddon.Addon(id='plugin.video.lapti.tv') 
addon_icon    = __addon__.getAddonInfo('icon')
addon_icon    = __addon__.getAddonInfo('icon')
addon_fanart  = __addon__.getAddonInfo('fanart')
addon_path    = __addon__.getAddonInfo('path')
addon_type    = __addon__.getAddonInfo('type')
addon_id      = __addon__.getAddonInfo('id')
addon_author  = __addon__.getAddonInfo('author')
addon_name    = __addon__.getAddonInfo('name')
addon_version = __addon__.getAddonInfo('version')

#fanart    = xbmc.translatePath( __addon__.getAddonInfo('path') + 'fanart.jpg')
#xbmcplugin.setPluginFanart(pluginhandle, fanart)

INC_url = 'http://www.lapti.tv'
INC_ch = '/'


try:
	import platform
	xbmcver=xbmc.getInfoLabel( "System.BuildVersion" ).replace(' ','_').replace(':','_')
	UA = 'XBMC/%s (%s; U; %s %s %s %s) %s/%s XBMC/%s'% (xbmcver,platform.system(),platform.system(),platform.release(), platform.version(), platform.machine(),addon_id,addon_version,xbmcver)
except:
	UA = 'XBMC/Unknown %s/%s/%s' % (urllib.quote_plus(addon_author), addon_version, urllib.quote_plus(addon_name))

dbg = 1
def dbg_log(line):
  if dbg: xbmc.log(line)

def get_url(url, data = None, cookie = None, save_cookie = False, referrer = None):
	try:
		req = urllib2.Request(url, data, headers = {'User-Agent':UA})
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		dbg_log(e);
        
def INC_prls(url):
    dbg_log('INC_prls')
    
    http = get_url(url)
    oneline = re.sub('[\r\n\t]', ' ', http)
    ch_cont = re.compile('<div class="channels-block"> +?<ul> +?(.+?) +?</ul> +?</div>').findall(oneline)
    pr_ls = re.compile('<a class="(.+?)" +?href="(.+?)"></a>').findall(ch_cont[0])

    if len(pr_ls):
        for descr, href in pr_ls:
            name = descr
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
elif mode == None: INC_prls(INC_url + INC_ch)

dbg_log('CLOSE:')

