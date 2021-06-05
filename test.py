import getpass
import os

from dotenv import load_dotenv
from ldap3 import Connection, Server, ALL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List
import time
from datetime import datetime
import sys
import subprocess


def log_time() -> datetime:
    """ Returns the current time for logfiles
    :returns: Now datatime  
    """
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")


def init_driver() -> webdriver:
    """ Init WebDriver from exe file 
    :returns: Selenium WebDriver
    """
    driver = webdriver.Firefox(executable_path=r'C:\Users\username\Desktop\test\pi_test\geckodriver.exe')
    driver.wait = WebDriverWait(driver, 10)
    return driver


def check_user(driver, user, super_user, user_name, user_pass, system) -> None:
    """ Match data from AD and PWA
    :param driver: Selenium WebDriver
    :type driver: webdriver
    :param user: user from AD
    :type user: str
    :param super_user: super_user from AD
    :type super_user: str
    :param user_name: User name for login on PWA 
    :type user_name: str
    :param user_pass: User pass for login on PWA
    :type user_pass: str
    :param system: Url for login on PWA
    :type system: str
    :returns: None
    """
    print('')
    print('|CHECK|')

    try:
        driver.get(f'https://{user_name}:{user_pass}@{system}')
    except Exception as e:
        error.write('\n' + '****************')
        error.write('\n' + '|ERROR| ' + log_time() + str(' нет доступа к ' + system + '\n'))
        error.write(str(e))
        return

    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]')
        print('[+] ' + user)
    except Exception as e:
        error.write('[-] ' + user + '\n')
        error_user.write('[-] ' + user + '\n')
        print('[-] ' + user)
        return

    time.sleep(0.5)

    try:
        #driver.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]').clear()
        driver.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]')
        element.send_keys(user)
        print('[+] ввести ФИО user-а')
    except Exception as e:
        error.write('\n' + '****************')
        error.write('\n' + '|ERROR| ' + log_time() + str(' не удалось ввести ФИО user-а с первой попытки' + '\n'))
        error.write(str(e))
        error.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] ввести ФИО user-а')

    time.sleep(0.5)

    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]').click()
        print('[+] поиск ')
    except Exception as e:
        error.write('\n' + '****************')
        error.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]' + '\n'))
        error.write(str(e))
        error.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] поиск ')
        return


    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[2]/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[2]/a')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[2]/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[2]/a').click()
        print('[+] выбрать пользователя')
    except Exception as e:
        error.write('\n' + '****************')
        error.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[2]/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[2]/a. Пользователь - исключение. ' + '\n'))
        error.write(str(e))
        error.write('\n' + 'Error with ' + user + ' - ' + super_user)
        exeption_users.write('\n' + user)
        print('[+] пользователь исключение')
        print('[-] выбрать пользователя')
        return


    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[10]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/ul/li[5]/div[2]/input')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[10]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/ul/li[5]/div[2]/input')
        print('[+] AD data:  ' + user + ' - ' + super_user)
        print('[+] PWA data: ' + user + ' - ' + element.get_attribute('value'))

        if super_user != element.get_attribute('value'):
            difference_user.write(user + '\n')
            difference_super_user.write(super_user + '\n')
            print('[+] Запись в файлы несоответствий')
            change = 1
            print('[+] change = 1')
        else:
            change = 0
            print('[+] change = 0')

    except Exception as e:
        error.write('\n' + '****************')
        error.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[10]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/ul/li[5]/div[2]/input.' + '\n'))
        error.write(str(e))
        error.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] найти управляющего рассписаниями')
        print('[-] пользователь в "корзине"')
        return
    
    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input').click()
        print('[+] нажать ОК')
    except Exception as e:
        error.write('\n' + '****************')
        error.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input.' + '\n'))
        error.write(str(e))
        error.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error.write('\n' + user)
        error_user.write('[-] ' + user + '\n')
        print('[-] нажать Сохранить')
        return

    if change == 1:
        for_user(driver, user, super_user, user_name = USER_NAME, user_pass = USER_PASS, system = SYSTEM)   
    else:
        log.write('[CHECK]' + log_time() + ' Проверен: ' + user + ' - ' + super_user + '\n')


def for_user(driver, user, super_user, user_name, user_pass, system) -> None:
    """ Set correct values ​​to the system based on AD
    :param driver: Selenium WebDriver
    :type driver: webdriver
    :param user: user from AD
    :type user: str
    :param super_user: super_user from AD
    :type super_user: str
    :param user_name: User name for login on PWA 
    :type user_name: str
    :param user_pass: User pass for login on PWA
    :type user_pass: str
    :param system: Url for login on PWA
    :type system: str
    :returns: None
    """
    print('')
    print('|CHANGE|')

    # переход на страницу с параметрами 
    try:
        driver.get(f'https://{user_name}:{user_pass}@{system}')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' нет доступа к ' + system + '\n'))
        error_difference.write(str(e))
        return

    # строка ввода ФИО пользователя 
    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]')
        print('[+] ' + user)
    except Exception as e:
        error_difference.write('[-] ' + user + ' - ' + super_user + '\n')
        error_user.write('[-] ' + user + '\n')
        print('[-] ' + user)
        return

    time.sleep(0.5)

    # ввод ФИО 
    try:
        driver.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[1]')
        element.send_keys(user)
        print('[+] ФИО user-а')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не удалось ввести ФИО user-а с первой попытки' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] ФИО user-а')

    # поиск 
    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]').click()
        print('[+] OK ')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr[5]/td[2]/input[2]' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] OK ')
        return

    # клик на пользователя 
    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[2]/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[2]/a')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[2]/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[2]/a').click()
        print('[+] выбрать пользователя')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table[2]/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td[2]/a. Пользователь - исключение. ' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        exeption_users.write('\n' + user)
        print('[+] пользователь исключение')
        print('[+] запись в файл')
        return

    # обзор
    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[10]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/ul/li[5]/div[2]/button')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[10]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/ul/li[5]/div[2]/button').click()
        print('[+] выбрать пользователя')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[10]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/ul/li[5]/div[2]/button.' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        exeption_users.write('\n' + user)
        print('[+] пользователь исключение')
        print('[-] выбрать пользователя')
        return

    # захват iframe 
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/iframe")))
        print('[+] захват iframe 1')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/iframe. Пользователь в "корзине". ' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] захват iframe')
        print('[-] пользователь в "корзине"')
        return

    try:
        iframe = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/iframe")
        print('[+] захват iframe 2')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str('/html/body/div[2]/div/div[2]/iframe' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] захват iframe 2')
        return

    try:
        driver.switch_to.frame(iframe)
        print('[+] захват iframe 3')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str('/html/body/div[2]/div/div[2]/iframe' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] захват iframe 3')
        return

    # строка ввода (выбор ресурсов)
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[1]/input")))
        element = driver.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[1]/input')
        print('[+] строка ввода (выбор ресурсов)')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[1]/input' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] строка ввода (выбор ресурсов)')
        return

    time.sleep(0.5)

    # ввод ФИО управляющего рассписаниями
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[1]/input")))
        element.send_keys(super_user)
        print('[+] вставить ФИО управляющего расписаниями')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не удалось ввести ФИО user-а' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] вставить ФИО управляющего расписаниями')
        return

    # поиск 
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[3]/button")))
        element = driver.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[3]/button').click()
        print('[+] поиск')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[3]/button' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] поиск')
        return

    # выбор управляющего 
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td")))
        element = driver.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td').click()
        print('[+] выбор управляющего')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[1]/table/tbody/tr[2]/td/div/div/div/table/tbody/tr[2]/td. Суперпользователь - исключение.' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        exeption_super_users.write('\n' + super_user)
        print('[-] выбор управляющего')
        return

    # ок 
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[2]/input[1]")))
        element = driver.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[2]/input[1]').click()
        print('[+] ок')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/div[2]/input[1]' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_user.write('[-] ' + user + '\n')
        print('[-] ок')
        return

    # сохранить 
    try:
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input')))
        element.find_element_by_xpath('/html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input').click()
        print('[+] сохранить')
    except Exception as e:
        error_difference.write('\n' + '****************')
        error_difference.write('\n' + '|ERROR| ' + log_time() + str(' не найден элемент /html/body/form/div[12]/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input.' + '\n'))
        error_difference.write(str(e))
        error_difference.write('\n' + 'Error with ' + user + ' - ' + super_user)
        error_difference.write('\n' + user)
        error_user.write('[-] ' + user + '\n')
        print('[-] сохранить')
        return


    log_difference.write('[CHANGE]' + log_time() + ' Проверен: ' + user + ' - ' + super_user + '\n')


def download_all_user() -> None:
    """ Start for_users_orig.ps1 and for_super_users_orig.ps1 in cmd.
    :returns: None
    """
    try:
        subprocess.call('for_users_orig.ps1', shell=True)
    except Exception as e:
        log.write('\n' + '****************')
        log.write('\n' + '|ERROR| ' + log_time() + str(' не удалось запустить users_orig.ps1' + '\n'))
        log.write('\n' + str(e))
        sys.exit()

    try:
        subprocess.call('for_super_users_orig.ps1', shell=True)
    except Exception as e:
        log.write('\n' + '****************')
        log.write('\n' + '|ERROR| ' + log_time() + str(' не удалось запустить super_users_orig.ps1' + '\n'))
        log.write('\n' + str(e))
        sys.exit()


start_time = time.time()


# Variables
USER_NAME = ''
USER_PASS = ''
SYSTEM = 'devpwa.rt-solar.ru:8080/_layouts/15/PWA/Admin/ManageUsers.aspx'

# Log file
log = open('log.txt', 'w', encoding="utf-8", errors='ignore')
# Error file
error = open('error.txt', 'w', encoding="utf-8", errors='ignore')
# Users with error
error_user = open('error_user.txt', 'w', encoding="utf-8", errors='ignore')
# If for_user() have logs 
log_difference = open('log_difference.txt', 'w', encoding="utf-8", errors='ignore')
# If for_user() have errors
error_difference = open('error_difference.txt', 'w', encoding="utf-8", errors='ignore')
# Users with no matches
difference_user = open('difference_user.txt', 'w', encoding="utf-8", errors='ignore')
# Super users with no matches
difference_super_user = open('difference_super_user.txt', 'w', encoding="utf-8", errors='ignore')
# New exeptions users
exeption_users =  open('exeption_users.txt', 'w', encoding="utf-8", errors='ignore')
exeption_super_users = open('exeption_super_users.txt', 'w', encoding="utf-8", errors='ignore')


exeption_super_user_list = [
'name super_user'
]

exeption_user_list = [
'name user_name'
]


download_all_user()


users_orig_done = open('users_orig.txt', 'r', encoding="utf-8", errors='ignore')
super_users_orig_done = open('super_users_orig.txt', 'r', encoding="utf-8", errors='ignore')

list_users_orig_done = []
for user in users_orig_done:
    list_users_orig_done.append(user.strip())

list_super_users_orig_done = []
for super_user in super_users_orig_done:
    list_super_users_orig_done.append(super_user.strip())

for user in list_users_orig_done:
    for super_user in list_super_users_orig_done:
        if user in exeption_user_list:
            log.write('[EXEPT]' + log_time() + ' Исключение: ' + super_user + '. Исключение для : ' + user + ' - ' + super_user + '\n')
            print('')
            print('[EXEPT]')
            print('[+] Исключение для: ' + user + ' - ' + super_user + '. Исключение - ' + super_user)
            list_super_users_orig_done.pop(0)   
            break

        elif super_user in exeption_super_user_list:
            log.write('[EXEPT]' + log_time() + ' Исключение для : ' + user + ' - ' + super_user + '. Исключение: ' + super_user + '\n')
            print('')
            print('[EXEPT]')
            print('[+] Исключение для: ' + user + ' - ' + super_user + '. Исключение - ' + super_user)
            list_super_users_orig_done.pop(0)   
            break

        driver = init_driver()
        check_user(driver, user, super_user, user_name = USER_NAME, user_pass = USER_PASS, system = SYSTEM)              
        driver.quit()
        list_super_users_orig_done.pop(0)           
        break   


print('')
print(time.time() - start_time)