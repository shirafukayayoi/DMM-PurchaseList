from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    login_url = "https://accounts.dmm.co.jp/service/login/password/=/path=SgVTFksZDEtUDFNKUkQfGA__"
    email = ""
    password = ""
    csv_title = f"DMM_{today}_PURCHASED_LIST.csv"

    driver = webdriver.Chrome()
    
    dmm_login = DMMLogin(driver, login_url, email, password)
    dmm_login.login()
    
    dmm_library = DMMLibrary(driver)
    dmm_library.navigate_to_library()
    data = dmm_library.scroll_and_collect_data()
    
    csv_writer = CSVWriter(csv_title)
    csv_writer.write_data(data)
    
    driver.quit()

class DMMLogin:
    def __init__(self, driver, login_url, email, password):
        self.driver = driver
        self.login_url = login_url
        self.email = email
        self.password = password

    def login(self):
        self.driver.get(self.login_url)
        self.driver.set_window_size(1000, 1000)
        time.sleep(10)
        
        try:
            name_box = self.driver.find_element(By.NAME, "login_id")
            name_box.send_keys(self.email)
        except Exception as e:
            print(f"ユーザー名入力フィールドが見つかりません: {e}")
        
        try:
            pass_box = self.driver.find_element(By.NAME, "password")
            pass_box.send_keys(self.password)
        except Exception as e:
            print(f"パスワード入力フィールドが見つかりません: {e}")
        
        try:
            remember_box = self.driver.find_element(By.CLASS_NAME, "checkbox-input")
            remember_box.click()
        except Exception as e:
            print(f"チェックボックスが見つかりません: {e}")
        
        try:
            login_button = self.driver.find_element(By.XPATH, '//input[@value="ログイン"]')
            login_button.click()
        except Exception as e:
            print(f"フォームの送信に失敗しました: {e}")
        
        time.sleep(4)

class DMMLibrary:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_library(self):
        self.driver.get("https://www.dmm.co.jp/dc/-/mylibrary/")
        try:
            yes_button = self.driver.find_element(By.XPATH, "//a[contains(@href, 'declared=yes')]")
            yes_button.click()
        except Exception as e:
            print(f"「はい」が見つかりません: {e}")
        time.sleep(4)

    def scroll_and_collect_data(self):
        try:
            svg_path = self.driver.find_element(By.XPATH, "//*[@class='silex-element-content']")
            svg_path.click()
        except Exception as e:
            print(f"「×」が見つかりません")
        
        actions = self.driver.find_element(By.CLASS_NAME,"purchasedListArea1Znew")
        previous_scroll_height = 0
        
        while True:
            current_scroll_height = self.driver.execute_script("return arguments[0].scrollTop + arguments[0].clientHeight;", actions)
            self.driver.execute_script("arguments[0].scrollTop += arguments[0].clientHeight;", actions)
            time.sleep(1)
            new_scroll_height = self.driver.execute_script("return arguments[0].scrollTop + arguments[0].clientHeight;", actions)
            if new_scroll_height == current_scroll_height:
                break
        
        titles = self.driver.find_elements(By.CLASS_NAME, "productTitle3sdi8")
        circles = self.driver.find_elements(By.CLASS_NAME, "circleName209pI")
        kinds = self.driver.find_elements(By.CLASS_NAME, "default3EHgn")

        length = min(len(titles), len(circles), len(kinds))
        data = [(titles[i].text, circles[i].text, kinds[i].text) for i in range(length)]
        
        for title, circle, kind in data:
            print(title, circle, kind)

        return data

class CSVWriter:
    def __init__(self, filename):
        self.filename = filename

    def write_data(self, data):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["タイトル", "サークル", "種類"])
            writer.writerows(data)

if __name__ == "__main__":
    main()
