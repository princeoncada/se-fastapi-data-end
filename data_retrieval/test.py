from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def main():
    service = Service('./chromedriver.exe')
    # Initialize the WebDriver (you may need to specify the path to your WebDriver executable)
    driver = webdriver.Chrome(service=service)

    # Open a website
    driver.get("https://www.google.com/")

    # Find an input element by its name and interact with it

    # Wait for a few seconds (you can use WebDriverWait for more precise waits)
    import time
    time.sleep(5)

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    main()
