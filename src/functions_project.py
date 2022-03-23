#here we are going to input the functions for the project to be used. 
from re import S
import requests
import pandas as pd
from time import sleep
import numpy as np
from datetime import datetime
import sidetable #bonus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

opciones= Options()
opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
#hide as a robot
opciones.add_experimental_option('useAutomationExtension', False)
opciones.add_argument('--start-maximized') #start maximized
opciones.add_argument('user.data-dir=selenium') #save cookies
opciones.add_argument('--incognito')#incognito window

df_companies = pd.read_csv('../data/companiesclean.csv')
df_other = pd.read_csv('../data/other_ticker.csv')



def scrapping_file():
    y = str(input('Would you like to analyze a Company or Other(Index/Commodity/Crypto)?: ')).title()
    y2 = y.title()
    
    if y2 == 'Company':
        t1 = str(input("Which company would you like to analyze?(i.e. Apple): ")).title()
          
    else:
        print(df_other)
        print('-------------------------------------------------------------------')
        o1 = str(input("Which of the following other?(copy/paste desired ticker): "))
        

    try:
        other = list(df_other.loc[df_other['ticker'] == o1]['ticker'])
        print('----------------------------------')
        print(f'Let the scrapping begin for {other[0]}')
        print('----------------------------------')
            
    except:
        ticker = list(df_companies.loc[df_companies['company'] == t1]['ticker'])
        print('----------------------------------')
        print(f'Let the scrapping begin for {ticker[0]}')
        print('----------------------------------')

    try:
        other = list(df_other.loc[df_other['ticker'] == o1]['ticker'])
    except:
        ticker = list(df_companies.loc[df_companies['company'] == t1]['ticker'])
    
    url_inicial = "https://finance.yahoo.com/"

    driver = webdriver.Chrome(ChromeDriverManager().install())
    tabla = []
    driver.get(url_inicial)

    driver.find_element_by_xpath("//button[@value='agree']").click()
    sleep(5)

    if y2 == 'Company':
        driver.find_element_by_xpath("//input[@placeholder = 'Search for news, symbols or companies']").send_keys(f"{ticker[0]}")
        sleep(12)

        driver.find_element_by_xpath("//button[@id= 'header-desktop-search-button']").click()
        sleep(5)

        driver.find_element_by_xpath("//span[text() = 'Historical Data']").click()
        sleep(5)

        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span').click()
        sleep(15)

        driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button').click()
        sleep(2)

        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button').click()
        sleep(2)
        #NUEVO TEST
        scrolls = 18
        while True:
            scrolls -= 1
            action = ActionChains(driver)
            action.send_keys(Keys.END).perform()
            sleep(3)
            if scrolls < 0:
                break

        tabla.append(driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section').text)
    else:
        driver.find_element_by_xpath("//input[@placeholder = 'Search for news, symbols or companies']").send_keys(f"{other[0]}")
        sleep(12)

        driver.find_element_by_xpath("//button[@id= 'header-desktop-search-button']").click()
        sleep(5)

        driver.find_element_by_xpath("//span[text() = 'Historical Data']").click()
        sleep(5)

        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span').click()
        sleep(15)

        driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button').click()
        sleep(2)

        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button').click()
        sleep(2)
        #NUEVO TEST
        scrolls = 18
        while True:
            scrolls -= 1
            action = ActionChains(driver)
            action.send_keys(Keys.END).perform()
            sleep(3)
            if scrolls < 0:
                break
        
        tabla.append(driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section').text)
        da_tabla = pd.DataFrame(tabla)

    return da_tabla.to_csv('tabla_scrapping.csv', index = False)
    
def clean_scrapping():

#import the table scrapped and create a copy to work with 
    da_tabla = pd.read_csv('tabla_scrapping.csv.csv')
    da_tabla2 = da_tabla.copy()

#additional edits to the file leading to declaration of df_stocks. see cleaning file for more details. 
    df = pd.DataFrame(da_tabla2.loc[0,0].split("\n")[6:-2])
    df_st = df[0].str.split(" ", expand = True)
    df_st[9] = df_st[0] + ' ' + df_st[1] + ' ' + df_st[2]
    df_st.columns = ['d1', 'd2', 'd3', 'Open','High','Low','Close','Adj Close','Volume','date']
    df_st.drop(['d1','d2','d3'], axis = 1, inplace = True)
    df_st = df_st.apply(lambda x: x.str.replace(',',''))
    df_st['date'] = pd.to_datetime(df_st['date'], format='%b %d %Y')
    df_stocks = df_st.loc[(~df_st['Close'].isnull())]

#additional df_stocks cleaning. see cleaning file for more details 

    df_stocks['Open'] = df_stocks['Open'].astype(float)
    df_stocks['High'] = df_stocks['High'].astype(float)
    df_stocks['Low'] = df_stocks['Low'].astype(float)
    df_stocks['Close'] = df_stocks['Close'].astype(float)
    df_stocks['Adj Close'] = df_stocks['Adj Close'].astype(float)
    df_stocks['Volume'] = df_stocks['Volume'].astype(float)

#import the tweets clean file from the join merge cleaning. see cleaning file for more details. 
#clean file briefly by changing type of date
    df_twt = pd.read_csv('tweetsclean.csv')
    df_twt['date'] = pd.to_datetime(df_twt['fecha'])
    df_twt.drop(['fecha'], axis = 1, inplace = True)

#preration of file for analysis
    df_atwt = pd.merge(df_twt,df_stocks, how = 'outer', on = 'date')
    df_atwt['market_op_cl'] = np.where(df_atwt['Open'] > 0, 'market_open', 'market_closed')

    return df_atwt.to_csv('../data/analysis1.csv', index = False) #guardado y listo para análisis

def clean_json_companies():
#bring the json file 

    df = pd.read_json('../data/company_tickers.json').T
 #declare x as variable to test
    x = 'Apple Inc.'
    x.split(' ')[0]
#now create function to clean up the title
    def limpiar_comp(x): 
        comp = (x.split(" ")[0]).title()
        return comp

#some names like "Tesla, Inc" will give me the "," after the split, so I am replacing them
    df.replace(',','', regex=True, inplace=True)

#change column names to be easier to understand and eliminate the others that I dont need. 
    df["company"] = df["title"].apply(limpiar_comp)

    df.drop(['cik_str','title'], axis = 1, inplace = True)

    print(df.head(5)) #to check if it works in the data set

    return df.to_csv('../data/companiesclean.csv', index = False) #save new file


#graphs

def tw_count():
        # line 1 points
    x1 = df_elect_ym1['year_month']
    y1 = df_elect_ym1['tw_count_tr']
    # plotting the line 1 points 
    plt.plot(x1, y1, label = "Trump")
    # line 2 points
    x2 = df_elect_ym1['year_month']
    y2 = df_elect_ym1['tw_count_cl']
    # plotting the line 2 points 
    plt.plot(x2, y2, label = "Clinton")
    plt.xlabel('Year_Month')
    # Set the y axis label of the current axis.
    plt.ylabel('Tweet_Count')
    # Set a title of the current axes.
    plt.title('Twitter Count per candidate per month ')
    # show a legend on the plot
    plt.legend()
    # Display a figure.
    return plt.show()

def ret_count():
        # line 3 points
    x3 = df_elec_ym2['year_month']
    y3 = df_elec_ym2['retweets_clinton']
    # plotting the line 1 points 
    plt.plot(x3, y3, label = "Ret_Clinton")
    # line 4 points
    x3 = df_elec_ym2['year_month']
    y3 = df_elec_ym2['retweets_trump']
    # plotting the line 1 points 
    plt.plot(x3, y3, label = "Ret_Trump")
    plt.xlabel('Year_Month')
    # Set the y axis label of the current axis.
    plt.ylabel('Tweet_Count')
    # Set a title of the current axes.
    plt.title('Twitter Count per candidate per month ')
    # show a legend on the plot
    plt.legend()
    # Display a figure.
    return plt.show()
