from selenium import webdriver

from ssologin import SSOLogin
from downloadVideo import downloadVideo
from downloadpdf import downloadpdf
from parsePage import parsePage, printElements
from setAndCreateFirefoxProfile import setAndCreateFirefoxProfile
from UI import UI

path_to_mozilladriver = "/home/fusy/geckodriver-v0.27.0-linux32/geckodriver"
fp = setAndCreateFirefoxProfile()

driver = webdriver.Firefox(executable_path = path_to_mozilladriver, firefox_profile = fp)
#driver = None
#courseURL = "https://elearning.dei.unipd.it/course/view.php?id=4476"
courseURL = "https://elearning.unipd.it/chimica/course/view.php?id=603"

SSOLogin(driver, courseURL)
	
elements = parsePage(driver, courseURL)

ui = UI(elements)
selection = ui.performSelection()

#download(driver, selection)

printElements(selection)

#downloadVideo(driver, elements.video)
#downloadpdf(driver, elements.resource)

driver.quit()