import pathlib
import random
import string

import m3u8_To_MP4
from playwright.sync_api import sync_playwright
from pynput import keyboard

wldbr_url = ("https://www.wildberries.ru/catalog/192186031"
             "/feedbacks?imtId=183532775&size=313642019")
m3u8_lst = []

download_path = pathlib.Path("./mp4")
download_path.mkdir(parents=True, exist_ok=True)


def download_m3u8():
    last_m3u8 = m3u8_lst[-1]
    mp4_file_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    m3u8_To_MP4.multithread_download(
        last_m3u8, mp4_file_dir="./mp4", mp4_file_name=mp4_file_name
    )


def on_press(key):
    if key == keyboard.Key.shift_r:
        print("Press shift_r Key")
        download_m3u8()


def intercept_response(response):
    if "index.m3u8" in response.url:
        print(response.url)
        m3u8_lst.append(response.url)
        return response


listener = keyboard.Listener(on_press=on_press)
listener.start()


with sync_playwright() as p:

    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.on("response", intercept_response)
    page.goto(wldbr_url)
    page.pause()

    # browser.close()
