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

Addon         = xbmcaddon.Addon(id='script.3vi.updater')
addon_id      = Addon.getAddonInfo('id')
addon_icon    = Addon.getAddonInfo('icon')
