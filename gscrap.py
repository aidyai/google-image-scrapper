## IMPORTING ALL THE LIBRARIES NEEDED

import os
import io
import time
import wget
import requests
from PIL import Image


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Initializing Chrome Web Driver and its Configuration
options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("window-size=1920x1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument('--disable-blink-features=AutomationControlled')



browser = webdriver.Chrome('chromedriver',options=options)



## This function is selenium automating scrolling, clicking on images finds the high resolution image and returns the url
def getimg_FROMGOOGLE(wd, delay, max_imgs):
  
  ## this function scrolls uptil the end in your browser
  def scroll_down(wd):
    wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(0)  
  
  url = "https://www.google.com/search?q=african+traditional+footwears&sxsrf=ALiCzsaHkM4jvudfOWkTgfPXnAnPvEf0jA:1656342359384&source=lnms&tbm=isch&sa=X&ved=2ahUKEwieidSP9M34AhVgRvEDHfS-B_wQ_AUoAXoECAEQAw&biw=1366&bih=663&dpr=1"
  wd.get(url)

  img_urls = set()
  skips = 0
  

  while len(img_urls) < max_imgs:
    scroll_down(wd)
    thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")  # YOU JUST NEED TO FIND THE CLASS NAME THAT MATCHES YOURS
    for imgs in thumbnails[len(img_urls): max_imgs]:
      try:
        imgs.click()
        time.sleep(1)
        #print(imgs)
      except:
        continue

      iMG = wd.find_elements(By.CLASS_NAME, "n3VNCb")    # FIND THE CLASS NAME THAT MATCHES YOURS
      for image in iMG:
        if image.get_attribute('src') in img_urls:
          max_imgs += 1
          skips += 1
          break

        if image.get_attribute('src') and 'http' in image.get_attribute('src'):
          img_urls.add(image.get_attribute('src'))
          print(f"FOUND: {len(img_urls)} ")
  return img_urls



counter = 0
path = "/content/drive/MyDrive"   # Path you want to save your image
urls = getimg_FROMGOOGLE(browser,1,8)  # calling the function



# This line gets the  images based on urls, downloads it and saves
for image in urls:
    keyword = image[-10:-6] 
    save_as = os.path.join(path, keyword + str(counter) + '.jpg')
    wget.download(image, save_as)
