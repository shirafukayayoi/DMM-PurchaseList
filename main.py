import asyncio
import csv
import json
import os

from playwright.async_api import async_playwright


class DMMLibrary:
    def __init__(self, page):
        self.page = page

    async def navigate_to_library(self):
        await self.page.goto("https://www.dmm.co.jp/dc/-/mylibrary/")
        try:
            await asyncio.sleep(3)
            await self.page.click('a[href*="declared=yes"]')
            print("「はい」をクリックしました")
        except Exception as e:
            print(f"「はい」が見つかりません: {e}")
        await asyncio.sleep(4)

    async def scroll_and_collect_data(self):
        try:
            # 「×」ボタンをクリック
            await self.page.click(".silex-element-content")
            print("「×」をクリックしました")
        except Exception as e:
            print(f"「×」が見つかりません: {e}")

        # スクロール対象の要素を取得
        actions = self.page.locator(".purchasedListArea1Znew")
        if await actions.count() == 0:
            print("スクロール対象の要素が見つかりません")
            return []

        previous_scroll_height = 0

        while True:
            # 現在のスクロール位置と要素の高さを取得
            current_scroll_height = await self.page.evaluate(
                "(element) => element.scrollTop + element.clientHeight",
                await actions.element_handle(),
            )

            # スクロールを実行
            await self.page.evaluate(
                "(element) => { element.scrollTop += element.clientHeight; }",
                await actions.element_handle(),
            )
            await asyncio.sleep(1)

            # 新しいスクロール位置を取得
            new_scroll_height = await self.page.evaluate(
                "(element) => element.scrollTop + element.clientHeight",
                await actions.element_handle(),
            )

            # スクロールが終了したか確認
            if new_scroll_height == current_scroll_height:
                print("スクロールが終了しました")
                break

        # タイトル、サークル、種類を取得
        titles = await self.page.query_selector_all(".productTitle3sdi8")
        circles = await self.page.query_selector_all(".circleName209pI")
        kinds = await self.page.query_selector_all(".default3EHgn")

        titles_text = [await title.inner_text() for title in titles]
        circles_text = [await circle.inner_text() for circle in circles]
        kinds_text = [await kind.inner_text() for kind in kinds]

        length = min(len(titles_text), len(circles_text), len(kinds_text))
        data = [(titles_text[i], circles_text[i], kinds_text[i]) for i in range(length)]

        return data


async def main():
    email = input("DMMのメールアドレスを入力してください: ")
    password = input("DMMのパスワードを入力してください: ")

    login_url = "https://accounts.dmm.co.jp/service/login/password/=/path=SgVTFksZDEtUDFNKUkQfGA__"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        if os.path.exists("dmm_cookies.json"):
            with open("dmm_cookies.json", "r") as f:
                cookies = json.load(f)
            await page.context.add_cookies(cookies)
            print("クッキーを読み込みました")
        else:
            # DMMにログイン
            await page.goto(login_url)
            await page.fill('input[name="login_id"]', email)
            await page.fill('input[name="password"]', password)
            await page.click('button:text("ログイン")')
            print("ログイン完了")
            cookies = await page.context.cookies()
            with open("dmm_cookies.json", "w") as f:
                json.dump(cookies, f)
                print("クッキーを保存しました")

            await asyncio.sleep(3)

        dmm_library = DMMLibrary(page)
        await dmm_library.navigate_to_library()
        data = await dmm_library.scroll_and_collect_data()
        await browser.close()

        if data and isinstance(data[0], dict):
            with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)


if __name__ == "__main__":
    asyncio.run(main())
