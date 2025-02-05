import time
import schedule
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Ambil data dari environment variables
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
URL = "https://freebitco.in/"

def get_balance(driver):
    """Fungsi untuk mengambil saldo BTC dari FreeBitco.in"""
    try:
        balance_element = driver.find_element(By.ID, "balance_small")
        balance = balance_element.text.strip()
        return balance
    except:
        return "Tidak bisa mendapatkan saldo"

def claim_faucet():
    print("\n🚀 Memulai auto claim FreeBitco.in...")

    # Setup WebDriver dengan headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Buka FreeBitco.in
        driver.get(URL)
        time.sleep(5)

        # Login
        driver.find_element(By.NAME, "login_email").send_keys(EMAIL)
        time.sleep(1)
        driver.find_element(By.NAME, "login_password").send_keys(PASSWORD)
        time.sleep(1)

        # Klik tombol "Play without Captcha" jika ada
        try:
            play_button = driver.find_element(By.XPATH, '//button[contains(text(), "Play without Captcha")]')
            play_button.click()
            print("✅ Tombol 'Play without Captcha' diklik.")
            time.sleep(3)
        except:
            print("❌ Tombol 'Play without Captcha' tidak ditemukan atau sudah diaktifkan.")

        # Klik tombol klaim faucet
        claim_button = driver.find_element(By.ID, "free_play_form_button")
        driver.execute_script("arguments[0].click();", claim_button)  # Eksekusi klik
        time.sleep(5)

        # Cek saldo setelah klaim
        balance_after = get_balance(driver)
        print(f"💰 Saldo setelah klaim: {balance_after} BTC")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

# Jalankan setiap 1 jam
schedule.every(1).hours.do(claim_faucet)

# Loop agar berjalan terus
print("🕒 Bot auto claim FreeBitco.in berjalan dengan headless mode tanpa captcha...")
while True:
    schedule.run_pending()
    time.sleep(60)

