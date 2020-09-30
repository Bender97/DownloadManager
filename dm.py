from selenium import webdriver

from ssologin import SSOLogin
from Download import Download
from parsePage import parsePage, printElements
from setAndCreateFirefoxProfile import setAndCreateFirefoxProfile
from UI import UI


path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"
fp = setAndCreateFirefoxProfile()

driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)
#driver = None
#courseURL = "https://elearning.dei.unipd.it/course/view.php?id=4476"
courseURL = "https://elearning.unipd.it/chimica/course/view.php?id=603"

ssologin = SSOLogin(driver)
ssologin.login(courseURL)
	
elements = parsePage(driver, courseURL)

ui = UI(elements)
selection = ui.UI_CategorySorted()

download = Download()
download.download(driver, selection)

driver.quit()