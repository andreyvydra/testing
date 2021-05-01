from playwright.sync_api import sync_playwright
from time import sleep

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto('https://dev.lk.tr-line.ru/sign-in')
        page.type("input[name=login]", "12345")
        page.type("input[name=password]", "12345")
        page.click('//html/body/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div/div/div[2]/button[2]')
        sleep(0.5)
        res = page.query_selector('//html/body/div[2]/div')
        print(res)
        if res is None:
            print(1)
        else:
            print(2)
        page.screenshot(path=f'example-{browser_type.name}.png')
        browser.close()
