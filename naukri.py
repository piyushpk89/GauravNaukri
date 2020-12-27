import glob
import os
import time
import traceback
from datetime import datetime, timedelta
from pprint import pprint
import threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

def setup_driver():
    chromedriver = 'chromedriver.exe'
    # anchorClient = Redis_Sadd()
    options = webdriver.ChromeOptions()
    EXTENSION_PATH = "ofmpippaeehejklbooedhpaopdoijibh.crx"
    options.add_extension(EXTENSION_PATH)
    # options.add_argument('--headless')
    options.set_capability("acceptInsecureCerts", True)
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--disable-gpu')
    # options.add_argument("--no-sandbox")
    # options.add_argument("download.default_directory=")
    path = os.getcwd() + os.path.sep + "cv_downloads"
    prefs = {'download.default_directory': path}
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


def getLatestFilename(timeNow, path, timeout):
    # path with ending seperator ex: D:/Mega
    time.sleep(2)
    while timeout:
        time.sleep(1)
        list_of_files = glob.glob(path+"*")
        latest_file = max(list_of_files, key=os.path.getctime)
        if os.path.getctime(latest_file)>timeNow:
            return latest_file
        timeout= timeout-1

    return "NOT FOUND"



def get_ClientInfo(driver):

    try:
        clientName= driver.find_element_by_css_selector("span.userName").text
        clientResumeID= driver.find_element_by_css_selector("span.resume-id").text
        clientPhone= driver.find_element_by_css_selector("div.bkt4.phoneNo").text
        clientEmail= driver.find_element_by_css_selector("div.bkt4.email").text
        time.sleep(5)
        urlLink = str(driver.current_url)


        clientResumeID = clientResumeID.split(":")[1].strip()
        clientEmail = clientEmail.split(":")[1].strip()
        clientPhone = clientPhone.split(":")[1].strip()

        with open("clientData.csv" ,'a',encoding='utf-8') as fp:
            fp.write(f"{clientName},{clientResumeID},{clientPhone},{clientEmail}")
            fp.write("\n")

        try:
            timeNow  = datetime.timestamp(datetime.now())

            clientCV= driver.find_element_by_css_selector("a.downloadCv").click()
            path = os.getcwd() + os.path.sep + "cv_downloads" + os.path.sep
            # time.sleep(2)
            clientFileName = getLatestFilename(timeNow, path, timeout=15)
            # if clientFileName==0:
            with open("clientWithLink.csv", 'a', encoding='utf-8') as fp:
                fp.write(f'"{clientName}",{clientResumeID},{clientPhone},{clientEmail},"{clientFileName}","{urlLink}"')
                fp.write("\n")

            print(f'"{clientName}",{clientResumeID},{clientPhone},{clientEmail},"{clientFileName}","{urlLink}"')

        except Exception as e:
            print(str(e))

    except Exception as e:
        print(str(e))
        traceback.print_exc()

def thread_run(timeout,driver):
    # timeout refresh = 10
    # driver = driver
    global stop_threads
    driver.switch_to.window(driver.window_handles[-1])
    current = datetime.now()
    now_plus_10 = now_plus_10m = current + timedelta(minutes = timeout)
    # time.sleep(timeout-1)
    while True:
        # print(datetime.now(), 'thread running')
        current = datetime.now()
        if current>now_plus_10:
            driver.refresh()
            print("REFRESHING PAGE")
            now_plus_10 = current + timedelta(minutes = timeout)

        if stop_threads:
            print(datetime.now())
            print("Thread_Killed")
            break
        time.sleep(1)


if __name__ == '__main__':
    driver = setup_driver()
    # driver.implicitly_wait(10)
    stop_threads = False
    driver.get("http://www.keydew.tk/g/index.php?username=sol1220n")

# '//*[@id="basicDet"]/div[2]/div[1]/div[1]/span'
    driver.find_element_by_xpath("//*[@id='password']").send_keys('sol#d77')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="gobutton"]').click()
    """----------------------------------------------------------------------"""
    # Give Refresh Timeout
    timeout = 1 # In Minutes
    myArgs = {'timeout': timeout, 'driver': driver}
    t1 = threading.Thread(target=thread_run, kwargs=myArgs)
    """----------------------------------------------------------------------"""
    okay = input("Search Page is Reached ?? _")


    while (okay.lower()=='y'):
            print("Starting find div again")
            source_list = []
            stop_threads = True
            while t1.is_alive():
                t1.join()

            driver.switch_to.window(driver.window_handles[1])

            allDiv= driver.find_elements_by_css_selector("div.tuple")

            print(len(allDiv))

            for div in allDiv:
                try:

                    myinput = div.find_element_by_class_name("userChk")
                    try:
                        if(myinput.is_selected()):
                            anchorElment = div.find_element_by_class_name("clFx").find_element_by_tag_name("a")
                            hover = ActionChains(driver).move_to_element(anchorElment)
                            hover.perform()
                            # time.sleep(1)
                            # driver.execute_script(mouseOverScript, anchorElment)
                            temp = anchorElment.get_attribute("href")
                            source_list.append(str(temp))
                            print(str(temp))
                            # print("Found in 1.1")

                    except Exception as e:
                        print(str(e))

                except Exception as e:
                    print(str(e))

            print("Starting profile Scanning")

            driver.implicitly_wait(5)
            for url in source_list:
                try:
                    driver.get(url)
                except Exception:
                    pass
                time.sleep(2)
                get_ClientInfo(driver)

            driver.close()
            stop_threads=False
            t1 = threading.Thread(target=thread_run, kwargs=myArgs)
            t1.start()
            print("Profile Scanning Completed .......")
            okay = input("Want to Search More ???")

    stop_threads = True
    if t1.is_alive():
        t1.join()

    print("Process Completed")
