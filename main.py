import string
import unittest

from playwright.sync_api import sync_playwright
from string import ascii_letters
from random import choices
from time import sleep


class TestCaseAuth(unittest.TestCase):
    def test_correct_user_login(self):
        email = 'vidra8888@yandex.ru'
        password = '0QBY1q0Ps/60'
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/sign-in')
            page.type("input[name=login]", email)
            page.type("input[name=password]", password)
            page.click('//html/body/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div/div/div[2]/button[2]')
            sleep(0.5)
            res = page.query_selector('//html/body/div[2]/div')
            self.assertTrue(res is None)

    def test_incorrect_users_login(self):
        test_data = (
            ('+792111', 'password'),
            ('+77777777777', 'password'),
            ('vidra', 'password'),
            ('vidra@yaru', 'password'),
            ('vidra@ya.ru', 'password'),
            ('vidra@ya.ru UNION SELECT * FROM users', 'password')
        )
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/sign-in')
            for login, password in test_data:
                page.type("input[name=login]", login)
                page.type("input[name=password]", password)
                page.click(
                    '//html/body/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div/div/div[2]/button[2]')
                sleep(0.5)
                res = page.query_selector('//html/body/div[2]/div')
                self.assertFalse(res is None)

    def test_correct_user_login_sms(self):
        phone = '+79214228036'
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/sign-in')
            page.type("input[name=login]", phone)
            page.click('//html/body/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div/div/div[2]/button[1]')
            sleep(0.5)
            page.screenshot(path='ex.png')
            res = page.query_selector('//html/body/div[2]/div')
            self.assertTrue(res.inner_text() == 'Сообщение отправлено' or
                            'превышен лимит' in res.inner_text().lower())

    def test_incorrect_user_login_sms(self):
        test_data = (
            '+782',
            '82s23er',
            'fsdfsgfdhd',
            'vidra8888@yandex.ru',
            '+99999999999999999'
        )
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/restore-password')
            for login in test_data:
                page.type("input[name=login]", login)
                page.click(
                    '//html/body/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div/div/div[2]/button[1]')
                sleep(0.5)
                res = page.query_selector('//html/body/div[2]/div')
                self.assertTrue(res is not None and res.inner_text() != 'Сообщение отправлено')


class TestCasePasswordReset(unittest.TestCase):
    def test_correct_email(self):
        email = 'vidra8888@yandex.ru'
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/restore-password')
            page.type("input[name=forget_email]", email)
            page.click('text=Сбросить пароль')
            sleep(0.5)
            res = page.query_selector('//html/body/div[2]')
            self.assertTrue(res is not None)

    def test_incorrect_email(self):
        test_data = (
            'user',
            'admin',
            'vidra@rrrr',
            'v@t.r',
            '+79214228036'
        )
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/restore-password')
            for email in test_data:
                page.type("input[name=forget_email]", email)
                page.click('text=Сбросить пароль')
                sleep(0.5)
                res = page.query_selector('//html/body/div[2]/div')
                self.assertTrue(res.inner_text() ==
                                'Пользователя с такими данными не существует.')


class TestCaseRegister(unittest.TestCase):
    def test_correct_user_register(self):
        email = ''.join(choices(ascii_letters, k=10)) + '@mail.ru'
        phone = '+7' + ''.join([str(i) for i in choices(string.digits, k=10)])
        name = 'Vasia'
        surname = 'Pupkin'
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/sign-up')
            page.type("input[name=e-mail]", email)
            page.type("input[name=phone]", phone)
            page.click('text=Далее')
            sleep(0.5)
            page.type("input[name=lname]", name)
            page.type("input[name=fname]", surname)
            page.click('text=Зарегистрироваться')
            sleep(0.5)
            res = page.query_selector('//html/body/div[2]')
            self.assertTrue(res is not None)

    def test_incorrect_user_reg(self):
        test_data = (
            ('vidra8888@yandex.ru', '+88888888888'),
            ('fffs@mail.ru', '+79214228036')
        )
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('https://dev.lk.tr-line.ru/sign-up')
            for email, phone in test_data:
                page.type("input[name=e-mail]", email)
                page.type("input[name=phone]", phone)
                page.click('text=Далее')
                sleep(0.5)
                res = page.query_selector('input[name=e-mail]')
                self.assertTrue(res is not None)


if __name__ == '__main__':
    unittest.main()
