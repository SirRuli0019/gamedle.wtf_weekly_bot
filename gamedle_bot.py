from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
#COOMENTA TUS CODIGOS CIRIO
def main():
    print("=== Gamedle Bot ===")

    print("Select browser:")
    print("1. Chrome")
    print("2. Brave")
    browser_choice = input("Enter choice (1 or 2): ").strip()

    browser_path = None

    if browser_choice == "1":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                browser_path = path
                break

        if not browser_path:
            print("Chrome browser not found. Make sure it's installed.")
            return

        print("Using Chrome browser")

    elif browser_choice == "2":
        brave_paths = [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")
        ]

        for path in brave_paths:
            if os.path.exists(path):
                browser_path = path
                break

        if not browser_path:
            print("Brave browser not found. Make sure it's installed.")
            return

        print("Using Brave browser")

    else:
        print("Invalid choice. Please select 1 or 2.")
        return

    numero = input("Enter week number: ")

    chrome_options = Options()
    chrome_options.binary_location = browser_path
    chrome_options.add_argument("--start-maximized")
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    def obtener_label_de_network(driver, endpoint_name):
        logs = driver.get_log('performance')
        for log in logs:
            try:
                message = json.loads(log['message'])
                method = message['message']['method']

                if method == 'Network.responseReceived':
                    response = message['message']['params']['response']
                    if endpoint_name in response['url']:
                        request_id = message['message']['params']['requestId']

                        try:
                            response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                            body_data = json.loads(response_body['body'])

                            if 'gameLegendAC' in body_data and 'label' in body_data['gameLegendAC']:
                                return body_data['gameLegendAC']['label']
                        except:
                            pass
            except:
                pass
        return None

    while True:
        driver = None
        try:
            driver = webdriver.Chrome(options=chrome_options)

            print("\nLoading weekly selection page...")
            driver.get("https://www.gamedle.wtf/weeklyselect")
            time.sleep(1.5)

            try:
                consent_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-cta-consent"))
                )
                consent_button.click()
                print("Consent dialog accepted")
                time.sleep(0.5)
            except:
                pass

            print("Selection page loaded")

            url = f"https://www.gamedle.wtf/weekly/{numero}"
            print(f"Navigating to week {numero}...")
            driver.get(url)
            time.sleep(1.5)
            print("Week page loaded successfully")

            print("\nSearching for first game...")
            time.sleep(0.5)
            label = obtener_label_de_network(driver, 'legendBoardLoadWeekly')

            if not label:
                print("Could not get first game")
                if driver:
                    driver.quit()
                break

            print(f"✓ Game found: {label}")

            intento = 1
            while True:
                print(f"\n--- Attempt {intento} ---")
                print(f"Typing in input: {label}")

                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "searchBox"))
                )
                search_box.clear()
                search_box.send_keys(label)
                time.sleep(0.8)

                print("Selecting from dropdown...")
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".tt-suggestion.tt-selectable"))
                    )
                    time.sleep(0.3)

                    suggestions = driver.find_elements(By.CSS_SELECTOR, ".tt-suggestion.tt-selectable")

                    clicked = False
                    for suggestion in suggestions:
                        if suggestion.text.strip() == label:
                            suggestion.click()
                            clicked = True
                            print(f"Selected: {label}")
                            break

                    if not clicked and len(suggestions) > 0:
                        suggestions[0].click()
                        print(f"Selected first option: {suggestions[0].text.strip()}")

                    time.sleep(0.5)
                except:
                    print("No suggestion found, continuing...")

                print("Clicking GUESS button...")
                time.sleep(0.3)
                guess_button = driver.find_element(By.ID, "guess")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", guess_button)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", guess_button)
                time.sleep(0.8)

                time.sleep(0.5)
                next_buttons = driver.find_elements(By.ID, "next")

                if len(next_buttons) == 0:
                    print("\nWeek completed! No more games.")
                    break

                print("Clicking NEXT button...")
                next_button = next_buttons[0]
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", next_button)
                print("Waiting for next game to load...")
                time.sleep(1.5)

                print("Searching for next game in network...")
                label = obtener_label_de_network(driver, 'nextWeeklyLegend')

                if not label:
                    print("\nWeek completed! No more games.")
                    break

                print(f"✓ Next game: {label}")
                intento += 1

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if driver:
                print("\nClosing browser...")
                driver.quit()

        print("\n" + "="*50)
        continuar = input("Do you want to play another week? (yes/no): ").lower().strip()

        if continuar != "yes":
            print("\nBot finished!")
            break

        numero = input("Enter the new week number: ")

if __name__ == "__main__":
    main()
