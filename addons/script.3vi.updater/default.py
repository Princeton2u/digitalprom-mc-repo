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
import traceback
import zipfile

Addon         = xbmcaddon.Addon(id='script.3vi.updater')
AddonLanguage = Addon.getLocalizedString
AddonIcon     = Addon.getAddonInfo('icon')
AddonFanart   = Addon.getAddonInfo('fanart')
AddonPath     = Addon.getAddonInfo('path')
AddonType     = Addon.getAddonInfo('type')
AddonId       = Addon.getAddonInfo('id')
AddonAuthor   = Addon.getAddonInfo('author')
AddonName     = Addon.getAddonInfo('name')
AddonVersion  = Addon.getAddonInfo('version')

def error_logging():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback) 
    xbmc.log(''.join('!! ' + line for line in lines))

## downloader with a progress bar
def Downloader(url,dest,description,heading):
    dp = xbmcgui.DialogProgress()
    dp.create(heading,description)
    dp.update(1)
    
    # Remove old file when present
    if os.path.isfile(dest):
        os.remove(dest)
        
    try:
        old_percent=0
        
        # Init download
        u = urllib2.urlopen(url)            
        
        # Open file for writing
        f = open(dest,'wb')
        
        # Calculate the download total length
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        file_size_dl = 0
        block_sz = 8192
        
        # Download it, update progress every block_sz bytes
        while True:
        
            buffer = u.read(block_sz)
            
            # Download finished
            if not buffer:
                break
            
            file_size_dl += len(buffer)
            f.write(buffer)
            percent = file_size_dl * 100 / file_size
            
            # Update percentage only when needed (faster, dialog update is slow)
            if int(percent) - int(old_percent) >= 1:
                dp.update(percent)
                old_percent=percent
            
            # Check if the download was cancelled
            if (dp.iscanceled()):
                dp.close()
                return -9
                break
        
        dp.update(100)
        f.close()
        return 0
    except urllib2.URLError, e:
        xbmc.log("Failed to download nightly release. Error: %s" % (e.reason))
        error_logging()
        return -1
    except urllib2.HTTPError, e:
        xbmc.log("Failed to download nightly release. Error: %s" % (e.code))
        error_logging()
        return -1
    except KeyboardInterrupt,SystemExit:
        dp.close()
        return -9

def initScreen(args):
	if xbmcgui.Dialog().yesno("Загрузка обновлений", "Загрузить новую прошивку?"):
		if os.path.isdir('/storage/.update/') != True:
			os.makedirs('/storage/.update/')
		if Downloader('http://digitalprom-mc-repo.googlecode.com/files/firmware.zip', '/storage/.update/firmware.zip', 'Не выключайте и не перезагружайте устройство,\nпока прошивка не скачается.', 'Подождите, идет загрузка. Выполнено ') == 0:
			zipdata = zipfile.ZipFile('/storage/.update/firmware.zip')
			zipinfos = zipdata.infolist()
			dp = xbmcgui.DialogProgress()
			dp.create('Подождите, идет распаковка. Выполнено ', 'Не выключайте и не перезагружайте устройство,\nпока прошивка не распакуется.')
			dp.update(1)
			i = 0;
			for zipinfo in zipinfos:
				i += 1
				zipdata.extract(zipinfo, '/storage/.update/')
				dp.update(25 * i)
			zipdata.close()
			os.remove('/storage/.update/firmware.zip')
			dp.close()
			xbmc.restart()

def main():

#	args = getArgs(sys.argv[2])
	try:
		action = args['action']
		del args['action']
	except:
		action = None
		print( '%s: Initializing addon... ' % AddonId, 1 )
#		initScreen(args)
		initScreen(None)
	if action != None:
		try: paction = globals()[action]
		except:
			paction = None
			print( '%s: Addon action "%s" is not found' % (AddonId, action), 4 )
			showToastMessage('3vi updater error', 'Addon action "%s" is not found' % action, 2000)
		if paction: paction(args)

if (__name__ == '__main__' ):
#	print( 'len(sys.argv) = %s' % len(sys.argv));
#	print( 'sys.argv = %s' % sys.argv[1]);
#	hos = int(sys.argv[1])
#	fhos = sys.argv[0]
	main()

