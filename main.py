from acc import Account, Mail
import time
import pyautogui
import decoder

def register(account):
    account.get("https://www.bananki.pl/#register")
    ipt_em1 = account.wait_for_element('//*[@id="form-register"]/input[1]')
    ipt_em2 = account.wait_for_element('//*[@id="form-register"]/input[2]')
    ipt_em1.send_keys(account.mail.mail)
    ipt_em2.send_keys(account.mail.mail)
    account.wait_n_click('//*[@id="form-register"]/input[3]')

    # wait for adblock
    # account.wait_for_element('//*[@id="abm"]')
    # account.execute_script("$('#abm').remove()")

    account.wait_n_click('//label[@class="sex male"]')
    ipt_login = account.wait_for_element('//input[@name="user_name"]')
    ipt_login.send_keys(account.login)
    account.wait_n_click('//button[@class="btn submit"]')
    account.wait_n_click('//a[@id="accept-cookies-checkbox"]')

    account.wait_n_click('//button[text()="Ruszamy! "]')
    account.wait_n_click('//button[text()="Dalej "]')
    # account.wait_n_click('//span[text()="1x Losowy klucz Steam"]')
    account.wait_for_element('//*[@id="skip"]')
    account.js_click('//*[@id="skip"]')
    # account.execute_script("a = document.getElementById('skip'); a.click()")
    # account.wait_n_click('//*[@id="skip"]')
    account.wait_n_click('//button[text()="Super !"]')

    account.wait_n_click('//label[text()="Chcę otrzymywać informacje o nowościach i promocjach od Sedoc LLC."]')
    account.wait_n_click('//label[text()="Chcę otrzymywać powiadomienia"]')
    account.wait_n_click('//button[text()="Dalej "]')
    account.wait_n_click('//button[text()="Super !"]')

    account.execute_script('a = document.querySelector("#instruction > div > form > button"); a.click();')
    # account.wait_n_click('//button[text()="Do dzieła!"]')
    account.wait_n_click('//span[@class="play"]')
    # kill popup window
    for i in range(5):
        try:
            account.switch_to.window(account.window_handles[1])
            break
        except IndexError:
            time.sleep(1)
            continue
    account.close()
    account.switch_to.window(account.window_handles[0])

    time.sleep(4)
    account.wait_n_click('//*[@id="onesignal-bell-launcher"]')
    time.sleep(10)

def perform_offer(account):
    account.get("https://www.bananki.pl/zdobywaj-bananki/")
    account.wait_n_click('//a[@class="close transition"]')
    account.get("https://www.bananki.pl/zdobywaj-bananki/ads/")
    account.wait_n_click('//strong[text()="Potwierdź"]')

    # account.execute_script("$('body').css('overflow','auto');$('#popup').remove()")

    account.wait_n_click('//ul[@class="list ads"]/li[1]')
    # switch to adgate
    for i in range(5):
        try:
            account.switch_to.window(account.window_handles[1])
            break
        except IndexError:
            time.sleep(1)
            continue

    account.hover_mouse('//span[text()="Wypełnij ankietę"]')
    account.wait_n_click('//span[text()="Zamknij"]')
    account.wait_n_click('//span[text()="Roblox Jailbreak Ultimate Test!"]')
    # account.wait_n_click('//span[text()="Earn 9 Bananas"]')


def quiz(account):
    # switch to quiz
    for i in range(5):
        try:
            account.switch_to.window(account.window_handles[2])
            break
        except IndexError:
            time.sleep(1)
            continue
    account.wait_n_click('//a[text()="Continue"]')
    account.wait_n_click('//a[text()="Start Quiz"]')

    account.wait_n_click('//button[text()="Ray 9"]')
    account.js_click('//*[@id="nextbutton"]')
    # account.execute_script("a = document.getElementById('nextbutton'); a.click();")
    account.wait_n_click('//button[text()="600,000"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="750"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="$500"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="Glider Store"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="Mini Train Station"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="$250,000"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="Bank rooftop"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="1M Dealership"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="20"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="30"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="20"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="15"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="Posh"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="Interrogator"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="107 mph"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="80"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="52 mph"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="250 mph"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="Uranium Rod"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="4"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="$1,000"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="Volt"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="100"]')
    account.js_click('//*[@id="nextbutton"]')

    account.wait_n_click('//button[text()="$25,000"]')
    account.js_click('//*[@id="nextbutton"]')

    time.sleep(10)

    account.close()
    account.switch_to.window(account.window_handles[1])
    account.close()
    account.switch_to.window(account.window_handles[0])
    account.refresh()


if __name__ == "__main__":
    for i in range(4, 6):
        m = Mail()
        a = Account(m)
        register(a)
        perform_offer(a)
        time.sleep(5)
        decoder.decode_move("swing1.txt")
        decoder.sim_click()
        time.sleep(3)
        decoder.decode_move("swing2.txt")
        decoder.sim_click()
        decoder.decode_move("swing3.txt")
        decoder.sim_click()
        decoder.decode_move("swing4.txt")
        decoder.sim_click()
        decoder.decode_move("swing5.txt")
        decoder.sim_click()
        decoder.decode_move("swing6.txt")
        # decoder.sim_click()
        quiz(a)

        a.verify()
        a.join_roulette(i+1)
        a.save_logindata()
        input("change the ip")

        a.quit()
        m.quit()
