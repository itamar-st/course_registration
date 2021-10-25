import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import gui


# contains the user info for logging in
class LoginInfo:

    def __init__(self):
        with open("/home/itamar/PycharmProjects/registration_auto/login info") as f:
            self.email_address = f.readline()
            self.email_password = f.readline()
            self.id = f.readline()
            self.website_password = f.readline()


def registration_bot(logging_info, usr_choice, usr_action):
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

    # navigate the page and try to register to the course.
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
        # finds the usres course

        desired_course = soup.find(string=usr_choice)
        relevant_section = desired_course.findParent("tr")
        # checks if the image of "open to register" exists
        image_of_change = relevant_section.find("td")

        def register():
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME,
                                                "ctl00$ContentPlaceHolder1$gvLinkToLessons$GridRow2$btnLinkStudentToLesson"))
            )
            registration_button = driver.find_element(By.NAME,
                                                      "ctl00$ContentPlaceHolder1$gvLinkToLessons$GridRow2$btnLinkStudentToLesson")
            registration_button.click()
            ## beta - for register to a course with exercise
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID,
            #                                     "rbSelectLesson"))
            # )
            # registration_circle = driver.find_element(By.ID,
            #                                           "rbSelectLesson")
            # registration_circle.click()
            #
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID,
            #                                     "ContentPlaceHolder1_ucMandatoryAdditionalLessonsSelection_btnAssign"))
            # )
            # approve_button = driver.find_element(By.ID,
            #                                      "ContentPlaceHolder1_ucMandatoryAdditionalLessonsSelection_btnAssign")
            # approve_button.click()
            time.sleep(5)
            actions = ActionChains(driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(10)
        # if the course is available, act as the user chooses
        while True:
            # a length of the section with the registration image is 3
            if len(image_of_change) == 3: # TODO: complete

                if usr_action == "                              auto registration                ":
                    register()
                elif usr_action == "                   send me a mail when available                ":
                    # send_mail(logging_info, usr_choice, "only notify")
                    pass
                elif usr_action == "                   auto registration + send a mail                ":
                    register()
                    # send_mail(usr_choice, "send + sign up")
                    pass
                else:
                    pass
            else:
                # wait and refresh
                time.sleep(60)
                driver.refresh()

    except:
        pass
        # send_mail(logging_info, usr_choice, usr_action)

    finally:
        time.sleep(5)
        driver.quit()


# sending email, option for adding attachments
# for this function to work, you need to remove two step authentication in your gmail account
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
    registration_bot(logging_info, usr_choice, usr_action)



