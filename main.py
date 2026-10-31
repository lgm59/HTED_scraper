print('Loading...')
import pandas as pd
from io import StringIO
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print('Welcome to the High Throughput Data Expression web scraper. Please remember that your gene list should be in .csv format, and that it should have its genes in column A under the cell "GeneFarmMems" which must be in position A2. Finally, row 1 must contain text, but cell A1 must be blank.')

while True:
    go = False
    while go == False:
        try:
            filepath = input('Paste the filepath of your gene list here:')
            file = pd.read_csv(str(filepath))
            go = True
            redun = False
        except (FileNotFoundError,OSError,UnicodeDecodeError) as error:
            print('Invalid filepath, please try again.')
            redun = True
        try:
            specific_column = file["Unnamed: 0"]
            genelist = []
            for x in specific_column:
                strencode = x.encode("ascii", "ignore")
                strdecode = strencode.decode()
                genelist.append(strdecode)
            genelist.remove('GeneFamMems')
            columns = StringIO(
                'FlyAtlas2 Anatomy RNA-Seq;modENCODE Anatomy RNA-Seq;modENCODE Development RNA-Seq;modENCODE Treatments RNA-Seq')
            df = pd.read_csv(columns, sep=";")
            go = True
        except:
            if redun == True:
                pass
            else:
                print(
                    'Your gene list seems to be improperly formatted. Please reformat the gene list as needed and try again.')
                go = False

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get("http://www.flybase.org")
    n = 0
    for gene in genelist:
        n = n + 1
        elem = driver.find_element(By.NAME, "context")
        elem.clear()
        elem.send_keys(gene)
        elem.send_keys(Keys.RETURN)
        waiter=webdriver.support.wait.WebDriverWait(driver,60)
        waiter.until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#expression"]')))
        drop_1=driver.find_element(By.XPATH, '//a[@href="#expression"]')
        drop_1.click()
        a=1
        while a==1:
            try:
                time.sleep(5)
                drop_2 = driver.find_element(By.XPATH, '//div[@id="ht_data"]')
                a=47
            except (NoSuchElementException, StaleElementReferenceException):
                a=1

        driver.execute_script("arguments[0].style.display = 'block';", drop_2)
        #waiter = webdriver.support.wait.WebDriverWait(driver, 60)
        #waiter.until(EC.element_to_be_clickable((By.ID, 'FlyAtlas2_toggle')))
        try:
            drop_3a = driver.find_element(By.ID, "FlyAtlas2")
            driver.execute_script("arguments[0].style.display = 'block';", drop_3a)
            FA2Fail = False
        except NoSuchElementException:
            FA2Fail = True
            pass

        try:
            drop_3b = driver.find_element(By.ID, "modENCODE_mRNA-Seq_tissues")
            driver.execute_script("arguments[0].style.display = 'block';", drop_3b)
            TFail = False
        except NoSuchElementException:
            TFail = True
            pass

        try:
            drop_3c = driver.find_element(By.ID, "modENCODE_mRNA-Seq_development")
            driver.execute_script("arguments[0].style.display = 'block';", drop_3c)
            DFail = False
        except NoSuchElementException:
            DFail = True
            pass

        try:
            drop_3d = driver.find_element(By.ID, "modENCODE_mRNA-Seq_treatments")
            driver.execute_script("arguments[0].style.display = 'block';", drop_3d)
            TrFail = False
        except NoSuchElementException:
            TrFail = True
            pass

        if FA2Fail == True:
            FA2Final = 'No Entry'
            pass
        else:
            FlyAtlas2List = drop_3a.find_elements(By.XPATH, ".//*")
            FA2Raw = ((FlyAtlas2List[91].text).splitlines())
            for x in FA2Raw:
                try:
                    FA2Raw[FA2Raw.index(x)] = int(x)
                except ValueError:
                    FA2Raw[FA2Raw.index(x)] = x
                    pass
            FA2Dict = {FA2Raw[i]: FA2Raw[i + 1] for i in range(0, len(FA2Raw), 2)}
            FA2Dict = {k: v for k, v in sorted(FA2Dict.items(), key=lambda item: item[1], reverse=True)}
            FA2Final = ''
            for x in list(FA2Dict.keys())[0:3]:
                FA2Final = FA2Final + x + ': ' + str(FA2Dict[x]) + ', '

        if TFail == True:
            TFinal = 'No Entry'
            pass
        else:
            TissuesList = drop_3b.find_elements(By.XPATH, ".//*")
            TRaw = (TissuesList[90].text).splitlines()
            for x in TRaw:
                try:
                    TRaw[TRaw.index(x)] = int(x)
                except ValueError:
                    TRaw[TRaw.index(x)] = x
                    pass
            TDict = {TRaw[i]: TRaw[i + 1] for i in range(0, len(TRaw), 2)}
            TDict = {k: v for k, v in sorted(TDict.items(), key=lambda item: item[1], reverse=True)}
            TFinal = ''
            for x in list(TDict.keys())[0:3]:
                TFinal = TFinal + x + ': ' + str(TDict[x]) + ', '

        if DFail == True:
            DFinal = 'No Entry'
            pass
        else:
            DevelopmentList = drop_3c.find_elements(By.XPATH, ".//*")
            DRaw = (DevelopmentList[90].text).splitlines()
            for x in DRaw:
                try:
                    DRaw[DRaw.index(x)] = int(x)
                except:
                    DRaw[DRaw.index(x)] = x
                    pass
            DDict = {DRaw[i]: DRaw[i + 1] for i in range(0, len(DRaw), 2)}
            DDict = {k: v for k, v in sorted(DDict.items(), key=lambda item: item[1], reverse=True)}
            DFinal = ''
            for x in list(DDict.keys())[0:3]:
                DFinal = DFinal + x + ': ' + str(DDict[x]) + ', '

        if TrFail == True:
            TrFinal = 'No Entry'
            pass
        else:
            TreatmentsList = drop_3d.find_elements(By.XPATH, ".//*")
            TrRaw = ((TreatmentsList[90].text).splitlines())
            for x in TrRaw:
                try:
                    TrRaw[TrRaw.index(x)] = int(x)
                except:
                    TrRaw[TrRaw.index(x)] = x
                    pass
            TrDict = {TrRaw[i]: TrRaw[i + 1] for i in range(0, len(TrRaw), 2)}
            TrDict = {k: v for k, v in sorted(TrDict.items(), key=lambda item: item[1], reverse=True)}
            TrFinal = ''
            for x in list(TrDict.keys())[0:3]:
                TrFinal = TrFinal + x + ': ' + str(TrDict[x]) + ', '

        df.loc[len(df)] = [FA2Final, TFinal, DFinal, TrFinal]
        print('Gene ' + gene + ' has been logged. ' + str(len(genelist) - n) + ' genes remaining.')
    driver.close()
    print('Operation complete.')

    while True:
        copy = input('Type "c" to copy the gene dataframe to your clipboard, or type "r" to restart the program: ')
        if str(copy) == 'c':
            df.to_clipboard(index=False)
            print("Dataframe copied.")
        elif str(copy) == 'r':
            break
        else:
            print('Invalid input, please try again.')