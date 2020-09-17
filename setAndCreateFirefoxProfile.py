from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def setAndCreateFirefoxProfile():
	fp = webdriver.FirefoxProfile()

	mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
	fp.set_preference("browser.download.manager.showWhenStarting", False)
	fp.set_preference("plugin.scan.plid.all", False)
	#fp.set_preference("plugin.scan.Acrobat", 99.0)
	fp.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
	fp.set_preference("pdfjs.disabled", True)
	return fp