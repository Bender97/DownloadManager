# DownloadManager
<ul>
  <li>For Linux, just download the folder (if zipped then unzip)
    <ul>
      <li>sudo pip install selenium</li>
      <li>sudo pip install requests</li>
      <li>sudo apt-get install python3-tk</li>
      <li>download the webdriver ( suggestion: gecko driver for linux) and update the path in createDriver.py</li>
    </ul>
    
    and type on a terminal
       python3 dm.py
  </li>

  <li>
    For Windows:
    <ul>
      <li>Install Python3
        <ul>
          <li>download it from here https://www.python.org/downloads/windows/</li>
          <li>follow the launcher. Remember to allor PATH edit!!! </li>
        </ul>
      </li>
      <li>download chrome webdriver from here https://chromedriver.chromium.org/downloads
        <ul>
           <li>extract the webdriver</li>
           <li>modify the file <i>createDriver.py</i> pasting the path to the just extracted webdriver on the 44th row (inside quotes!!)</li>
        </ul>
      </li>
      <li> in a command prompt terminal opened on the folder you downloaded from here (the extracted one!) type <i>python setup.py install</i>
      </li>
      <li>
        Use the program! :) on a command prompt terminal opened on the folder you downloaded from here (the extracted one!) type<br>
        <i>python dm.py</i>
      </li>
    </ul>
  </li>
</ul>
