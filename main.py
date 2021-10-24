import smtplib
import webbrowser
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import selenium.common.exceptions
from bs4 import BeautifulSoup
import requests
import urllib.request

import schedule
import time
import tk



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import gui


class LoginInfo:

    def __init__(self):
        with open("/home/itamar/PycharmProjects/registration_auto/login info") as f:
            self.email_address = f.readline()
            self.email_password = f.readline()
            self.id = f.readline()
            self.website_password = f.readline()


def scraper(logging_info, usr_choice, usr_action):
    url = "https://inbar.biu.ac.il/live/CreateStudentWeeklySchedule.aspx"
    # create the web driver
    path_to_webdriver = "/usr/bin/chromedriver"
    ser = Service(path_to_webdriver)
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    driver = webdriver.Chrome(service=ser) # need to add the option param and pass it op

    # check if there is an internet connection
    while True:
        try:
            driver.get(url)
            break
        # wait 60 sec and try again
        except selenium.common.exceptions.WebDriverException:
            time.sleep(60)

    # fill in the logging info
    usr_id = logging_info.id.strip()
    usr_pass = logging_info.website_password.strip()
    enter_id = driver.find_element(By.ID, "edtUsername")
    enter_id.send_keys(usr_id)
    enter_pw = driver.find_element(By.ID, "edtPassword")
    enter_pw.send_keys(usr_pass)
    enter_pw.send_keys(Keys.ENTER)
    try:
        time.sleep(3)
        # ID of the relevant elements for clicking
        commands = ["tvMainn10", "ContentPlaceHolder1_btnCloseThresholdRemark", "tbActions_ctl04_btnAddLessons",
                    "ContentPlaceHolder1_btnCloseThresholdRemark", "ContentPlaceHolder1_gvBalance_lblBalanceName_9"]
        # clicking scheme: when the element occurrs (wait for max of 10 sec), find it and click
        for element_id in commands:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            reg_button = driver.find_element(By.ID, element_id)
            reg_button.click()
        # parse the HTML code and check if the specific course name is available for registration
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, 'html.parser')
        # s = soup.findAll("tr", {"id":'ContentPlaceHolder1_gvLinkToLessons'})
        # finds the usres course
        desired_course = soup.find(string=usr_choice)
        relevant_section = desired_course.findParent("tr")
        # checks if the image of "open to register" exists
        image_of_change = relevant_section.find("td")
        print(len(image_of_change))
        print("++++++++++++++++=")
        print(relevant_section)
        # if the course is available, act as the user chooses
        while True:
            # a length of the section with the registration image is 3
            if len(image_of_change) == 3: # TODO: complete
                if usr_action == "                              auto registration                ":
                    pass
                elif usr_action == "                   send me a mail when available                ":
                    send_mail(logging_info, usr_choice, "only notify")
                elif usr_action == "                   auto registration + send a mail                ":
                    pass
                else:
                    pass
                break
            else:
                # wait and refresh
                time.sleep(60)
                driver.execute_script("window.scrollTo(0,50") # TODO: check if works
                driver.refresh()

    except:
        pass
        send_mail(logging_info, usr_choice, usr_action)

    finally:
        time.sleep(5)
        driver.quit()


# sending email, option for adding attachments
def send_mail(course_name, type_of_message):
    log_info = LoginInfo()
    contact = [log_info.email_address]
    msg = MIMEMultipart()
    msg['Subject'] = "The course you wanted is now available!!!"
    msg['From'] = log_info.email_address
    msg['To'] = ', '.join(contact)
    if type_of_message == "only notify":
        msg.attach(MIMEText(
            f'your course {course_name} is now available!! hurry up to sign up!!!!'))
    elif type_of_message == "send + sign up":
        msg.attach(MIMEText(
            f'your course {course_name} is now available!! we have already signed you up to the course'))
    elif type_of_message == "error":
        msg.attach(MIMEText(
            'something went wrong -  we cant access to the website...\n'
            ' please check you internet connection or the website'))
    else:
        pass  # TODO: change to better handling, maybe exception

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(log_info.email_address.strip(), log_info.email_password.strip())
        smtp.sendmail(log_info.email_address, contact, msg.as_string())


# schedule.every().day.at('16:04').do(scaper)# scechuling the function
# while True:
#     schedule.run_pending()
# schedule.clear()


if __name__ == '__main__':
    ui = gui.UI()
    usr_choice = ui.get_usr_choice()
    usr_action = ui.get_usr_action()
    logging_info = LoginInfo()
    send_mail(usr_choice, "only notify")
    # scraper(logging_info, usr_choice, usr_action)



