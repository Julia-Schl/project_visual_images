from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

'''
Both Page handlers have a short sleept timer to allow time for scrolling. Decreasing this timer will result in more exceptions occuring
'''
#initialize driver
def build_driver():
    return webdriver.Chrome()

#handle welcome page
def welcome(driver):
    driver.find_element(By.XPATH, '/html/body/div/form/div/div/button').click()

#handle Page1
def Page1(driver):

    #access radio question 
    radio = driver.find_elements(By.NAME, "comp_trust")
    #first layer of error handling
    if not radio:
        raise NoSuchElementException("No radio buttons found on Page1")
    
    #randomly select input 
    random_input = random.randint(0, len(radio) - 1)
    
    #this scrolls the page to the question. Needed so the script can access the radio button proberly 
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio[random_input])
    time.sleep(0.3)
    #input for radio buttons 
    radio[random_input].click()

    #click next button
    driver.find_element(By.XPATH, '/html/body/div/form/div/div[3]/div/div/button').click()

#handle transition page
def Transition(driver):
    driver.find_element(By.XPATH, '/html/body/div/form/div/div/button').click()

def Page2(driver):
    #same logic and similar code as for Page1
    radio_fem = driver.find_elements(By.NAME, "popout_question_femininity")
    if not radio_fem:
        raise NoSuchElementException("No radio buttons found on Page2")
    random_input_fem = random.randint(0, len(radio_fem) - 1)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_fem[random_input_fem])
    time.sleep(0.3)
    radio_fem[random_input_fem].click()
    driver.find_element(By.XPATH, "/html/body/div/form/div/div[4]/div/div/button").click()

#method that runs a specifieed number of bots over the pages 
def run_bots(runs, link):
    driver = build_driver()

    #counter for bots that skipped because they encountered an error
    skipped_bots = 0
    #pass through the survey n times
    for i in range(runs):
        print(f"\nStarting Bot: {i}")
        try:
            #initialize driver and pass welcome page
            driver.get(link)
            welcome(driver)
            
            #pass Page1 10 times
            for _ in range(10):
                Page1(driver)

            #pass Transiton page 
            Transition(driver)
            
            #pass Page2 10 times
            for _ in range(10):
                Page2(driver)
            print(f"Bot {i} passed successfully!")

        #handle ecxceptions: if one of these exceptions occur the cirrent bot is skipped 
        # the "Not interactable" exception occurs randomly, most likely when the page takes longer than normal to load 
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"Bot {i} encountered an error and will be skipped: {e}")
            #iterate counter if an exception is encountered
            skipped_bots += 1
            #skip to next bot 
            continue
    #print  number of bots and the percentage of bots that where skipped
    print(f"{runs} Bots passed through the survey! Total skipped bots: {skipped_bots} ({(skipped_bots/runs) * 100:.2f}% of Bots)")

link = "http://localhost:8000/join/hokafura"
run_bots(10, link)
