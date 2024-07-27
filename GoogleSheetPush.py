from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    login_url = "https://accounts.dmm.co.jp/service/login/password/=/path=SgVTFksZDEtUDFNKUkQfGA__"
    email = ""
    password = ""
    csv_title = f"DMM_{today}_PURCHASED_LIST.csv"
    sheet_url = ""

    driver = webdriver.Chrome()
    
    dmm_login = DMMLogin(driver, login_url, email, password)
    dmm_login.login()
    
    dmm_library = DMMLibrary(driver)
    dmm_library.navigate_to_library()
    data = dmm_library.scroll_and_collect_data()
    
    google_spreadsheet = GoogleSpreadsheet()    # initを実行するために必要
    google_spreadsheet.write_data(data)
    google_spreadsheet.get_last_column_and_convert_to_alpha()

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
            time.sleep(3)
            login_button = self.driver.find_element(By.XPATH, '//input[@value="ログイン"]')
            login_button.click()
            print("フォームを送信しました")
        except Exception as e:
            print(f"フォームの送信に失敗しました: {e}")

class DMMLibrary:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_library(self):
        time.sleep(3)
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

class GoogleSpreadsheet:
    def __init__(self,sheet_url):
        self.scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
        self.creds = Credentials.from_service_account_file('credentials.json', scopes=self.scope)
        self.client = gspread.authorize(self.creds)
        self.spreadsheet = self.client.open_by_url(sheet_url)
        self.sheet = self.spreadsheet.sheet1  # 最初のシートにアクセス
        print("Google Spreadsheetに接続しました")

    # Googleスプレッドシートにデータを書き込む
    def write_data(self, data):
        self.sheet.clear()
        self.sheet.insert_row(["タイトル", "サークル", "種類"], 1)
        for row in data:
            time.sleep(3)
            count += 1
            return count
            self.sheet.append_row(row)
            print(row)
        print(f"{count}回データを書き込みました。")
    
    # フィルターを設定
    def get_last_column_and_convert_to_alpha(self):
        # 最終列の数値を取得
        last_column_num = len(self.sheet.row_values(1))
        print(f"最終列は{last_column_num}です")
        
        # 数値からアルファベットを求める内部関数
        def num2alpha(num):
            if num <= 26:
                return chr(64 + num)
            elif num % 26 == 0:
                return num2alpha(num // 26 - 1) + chr(90)
            else:
                return num2alpha(num // 26) + chr(64 + num % 26)
        
        # 最終列を数値→アルファベットへ変換
        last_column_alp = num2alpha(last_column_num)
        print(f'最終列のアルファベットは{last_column_alp}です')
        self.sheet.set_basic_filter(name=(f'A:{last_column_alp}'))
        print("フィルターを設定しました")        


if __name__ == "__main__":
    main()