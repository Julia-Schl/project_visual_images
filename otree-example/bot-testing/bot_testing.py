from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import random
import string
import time


def build_driver():
    return webdriver.Chrome()


def welcome(driver):
    time.sleep(0.3)
    driver.find_element(By.XPATH, '/html/body/div/form/div/div/button').click()

def Page1(driver):
    time.sleep(0.3)
    radio = driver.find_elements(By.NAME,"popout_question_competence")
    random_input = random.randint(0, len(radio) - 1)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio[random_input])
    time.sleep(0.3)
    radio[random_input].click()
    time.sleep(0.3)
    driver.find_element(By.XPATH, '/html/body/div/form/div/div[3]/div/div/button').click()


def Transition(driver):
    time.sleep(0.3)
    driver.find_element(By.XPATH, '/html/body/div/form/div/div/button').click()


def Page2(driver):
    time.sleep(0.3)
    radio_fem = driver.find_elements(By.NAME,"popout_question_femininity")
    random_input_fem = random.randint(0, len(radio_fem) - 1)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_fem[random_input_fem])
    time.sleep(0.3)
    radio_fem[random_input_fem].click()
    time.sleep(0.3)
    driver.find_element(By.XPATH, "/html/body/div/form/div/div[4]/div/div/button").click()



def run_bots(runs,link):
    driver = build_driver()

    #pass through the survey n times
    for i in range(runs):
        print(f"\nStarting Bot: {i}")
        driver.get(link)

        #pass welcome 
        welcome(driver)

        #pass through Page1 10 times
        for x in range(10):
            Page1(driver)
            print(f"Bot {i} passed round {x+1}") 

        #pass transition
        Transition(driver)

        #pass trough Page2 10 times
        for z in range(10):
            Page2(driver)
            print(f"Bot {i} passed round {z+11}") 

        print(f"Bot {i} passed successfully!")

    print("All Bots passed through the survey!")   

#set link for bots and number of times they should run trough it 
link = "http://localhost:8000/join/jumakuro"
#run 5 bots
run_bots(5,link)