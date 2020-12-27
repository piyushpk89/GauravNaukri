import glob
import os
import time
import traceback
import pathlib
from datetime import datetime, timedelta
from pprint import pprint
import threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

FolderDownload = "CV_" + datetime.now().strftime("%H_%M")
folderpath = os.getcwd() + os.path.sep + FolderDownload

def setup_driver():
    chromedriver = 'chromedriver.exe'
    # anchorClient = Redis_Sadd()
    options = webdriver.ChromeOptions()
    EXTENSION_PATH = "extensions/mdatabaseservice.crx"
    EXTENSION_PATH2 = "extensions/recuirtment_extension.crx"
    options.add_extension(EXTENSION_PATH)
    options.add_extension(EXTENSION_PATH2)
    # options.add_argument('--headless')
    options.set_capability("acceptInsecureCerts", True)
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--disable-gpu')
    # options.add_argument("--no-sandbox")
    # options.add_argument("download.default_directory=")
    prefs = {'download.default_directory': folderpath}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--start-maximized")
    # options.
    # options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    # optional
    # driver = []
    driver= webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    # driver.maximize_window()

    return driver

#
# def getLatestFilename(timeNow, path, timeout):
#     # path with ending seperator ex: D:/Mega
#     time.sleep(1)
#     while timeout:
#         time.sleep(1)
#         list_of_files = glob.glob(path+"*")
#         latest_file = max(list_of_files, key=os.path.getctime)
#         if os.path.getctime(latest_file)>timeNow:
#             return latest_file
#         timeout= timeout-1
#
#     return "NOT FOUND"
#
#
#

def getCandidateInfo(driver):

    try:
        driver.switch_to.window(driver.window_handles[1])
    except Exception:
        print("Drive not Able to Switch Window ")

    try:

        clientName= driver.find_element_by_css_selector("div.candidate-name").text
        clientResumeID= driver.find_element_by_css_selector("div.header-profile-id").text
        clientPhone= driver.find_element_by_xpath('//*[@id="contact_details_num_2"]').text
        clientEmail= driver.find_element_by_xpath('//*[@id="contact_details_num_3"]').text
        time.sleep(1)
        urlLink = str(driver.current_url)


        clientResumeID = clientResumeID.split(":")[1].strip()
        # clientEmail = clientEmail.split(":")[1].strip()
        # clientPhone = clientPhone.split(":")[1].strip()
        waContact = clientName + ";91" + clientPhone
        # clientResumeID = "http://www.keydew.tk/g/getResumeDoc.php?resId=" + clientResumeID;


        with open(os.path.join(folderpath, 'CandidateList.csv') ,'a',encoding='utf-8') as fp:
            #fp.write(f"{clientName},{clientResumeID},{clientPhone},{clientEmail}")
            fp.write(f"{clientName},{clientPhone},{clientEmail},{clientResumeID},{waContact}")
            fp.write("\n")

        try:
            #timeNow  = datetime.timestamp(datetime.now())

            clientCV= driver.find_element_by_css_selector("a.downloadCv").click()
            #path = os.getcwd() + os.path.sep + "cv_downloads" + os.path.sep
            # time.sleep(2)
            #clientFileName = getLatestFilename(timeNow, path, timeout=15)
            # if clientFileName==0:
            #with open("clientWithLink.csv", 'a', encoding='utf-8') as fp:
             #   fp.write(f'"{clientName}",{clientResumeID},{clientPhone},{clientEmail},"{clientFileName}","{urlLink}"')
              #  fp.write("\n")

            #print(f'"{clientName}",{clientResumeID},{clientPhone},{clientEmail},"{clientFileName}","{urlLink}"')

        except Exception as e:
            print(str(e))


    except Exception as e:
        print("Error in Tag Element of HTML for client Info")
        print(str(e))

        traceback.print_exc()
    finally:
        if len(driver.window_handles)>2:
            driver.close()
            driver.switch_to(driver.window_handles[-1])

# def thread_run(timeout,driver):
#     # timeout refresh = 10
#     # driver = driver
#     global stop_threads
#     driver.switch_to.window(driver.window_handles[-1])
#     current = datetime.now()
#     now_plus_10 = now_plus_10m = current + timedelta(minutes = timeout)
#     # time.sleep(timeout-1)
#     while True:
#         # print(datetime.now(), 'thread running')
#         current = datetime.now()
#         if current>now_plus_10:
#             driver.refresh()
#             print("REFRESHING PAGE")
#             now_plus_10 = current + timedelta(minutes = timeout)
#
#         if stop_threads:
#             print(datetime.now())
#             print("Thread_Killed")
#             break
#         time.sleep(1)


if __name__ == '__main__':
    driver = setup_driver()
    # driver.implicitly_wait(10)

    """
    https://rb.gy/78ge6k
    sol1220m
    sol@ap2
    """
    stop_threads = False
    driver.get("https://rb.gy/78ge6k")

    okay = input("Search Page is Reached ?? _")
    driver.switch_to.window(driver.window_handles[1])

    while (okay.lower() == 'y'):
        print("Start Find Div Again")
        rows  = driver.find_elements_by_css_selector("div.single_profile_card")

        for row in rows[:2]:
            if row.find_element_by_css_selector("input.select_single_profile").is_selected():
                anchorElment = row.find_element_by_css_selector("div.d-flex.align-items-center").find_element_by_tag_name("a")
                hover = ActionChains(driver).move_to_element(anchorElment)
                hover.perform()
                # time.sleep(1)
                # driver.execute_script(mouseOverScript, anchorElment)

                temp = anchorElment.get_attribute("href")
                # source_list.append(str(temp))
                print(str(temp))
                anchorElment.click()
                getCandidateInfo(driver)

        print("Profile Scanning Completed .......")
        okay = input("Want to Search More ???")

# '//*[@id="basicDet"]/div[2]/div[1]/div[1]/span'

