import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import socket
import xbmcaddon
import cookielib
import urllib2

settings = xbmcaddon.Addon(id='script.module.torrent.ts')
language = settings.getLocalizedString
version = "0.0.1"
plugin = "torrent.ts-" + version

try:
	import StorageServer
	cache = StorageServer.StorageServer("TSEngine")
except:
	import storageserverdummy as StorageServer
	cache = StorageServer.StorageServer("TSEngine")
			
if cache.lock("TSLock"):
	cache.set("Mode",'init')
	cache.unlock("TSLock")		