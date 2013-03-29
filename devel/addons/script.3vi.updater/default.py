# -*- coding: utf-8 -*-
#!/usr/bin/python
# Writer (c) 2013, Golovastikov Denis, Digitalprom, E-mail: dgolovastikov@digitalprom.ru
# Rev. 0.0.1

import urllib
import urllib2
import sys
import os
import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
import time
import random
import threading

Addon         = xbmcaddon.Addon(id='script.3vi.updater')
AddonLanguage      = Addon.getLocalizedString
AddonIcon    = Addon.getAddonInfo('icon')
AddonFanart  = Addon.getAddonInfo('fanart')
AddonPath    = Addon.getAddonInfo('path')
AddonType    = Addon.getAddonInfo('type')
AddonId      = Addon.getAddonInfo('id')
AddonAuthor  = Addon.getAddonInfo('author')
AddonName    = Addon.getAddonInfo('name')
AddonVersion = Addon.getAddonInfo('version')

def getArgs(paramstring):
	param=[]
	if len(paramstring)>=2:
		params=paramstring
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
	if len(param) > 0:
		for cur in param:
			param[cur] = urllib.unquote_plus(param[cur])
	return param

def showToastMessage(heading, message, timeout = 3000, icon = AddonIcon):
	try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading.encode('utf-8'), message.encode('utf-8'), timeout, icon.encode('utf-8')))
	except Exception, e:
		print( '[%s]: showToastMessage: Transcoding UTF-8 failed [%s]' % (addon_id, e), 2 )
		try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, timeout, icon))
		except Exception, e:
			print( '[%s]: showToastMessage: exec failed [%s]' % (addon_id, e), 3 )

def uriFactory(args):
	return '%s?%s' % (fhos, urllib.urlencode(args))

def initScreen(args):
	li = xbmcgui.ListItem(language(30014), iconImage = AddonIcon, thumbnailImage = AddonIcon)
	uri = construct_request({
		'action': 'update',
		'url': 'http://code.google.com/p/digitalprom-mc-repo/downloads/detail?name=DPMC-ION.i386-2012-1212-r0001.zip&can=2&q='
	})
	li.setProperty('fanart_image', AddonFanart)
	xbmcplugin.addDirectoryItem(hos, uri, li, True)

	xbmcplugin.endOfDirectory(hos)
	

def main():

	args = getArgs(sys.argv[2])
	try:
		action = args['action']
		del args['action']
	except:
		action = None
		print( '%s: Initializing addon... ' % AddonId, 1 )
		initScreen(args)
	if action != None:
		try: paction = globals()[action]
		except:
			paction = None
			print( '%s: Addon action "%s" is not found' % (AddonId, action), 4 )
			showToastMessage('3vi updater error', 'Addon action "%s" is not found' % action, 2000)
		if paction: paction(args)

if (__name__ == '__main__' ):
	print( 'sys.argv = %s' % sys.argv[1]);
#	hos = int(sys.argv[1])
	fhos = sys.argv[0]
	main()

