from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

from boexplorer.download.utils import get_random_user_agent

def create_stealth_driver(user_agent):
    # create a new Service instance and specify path to Chromedriver executable
    service = ChromeService(executable_path=ChromeDriverManager().install())

    # create a ChromeOptions object
    options = webdriver.ChromeOptions()

    #run in headless mode
    options.add_argument("--headless")

    # disable the AutomationControlled feature of Blink rendering engine
    options.add_argument('--disable-blink-features=AutomationControlled')

    # disable pop-up blocking
    options.add_argument('--disable-popup-blocking')

    # start the browser window in maximized mode
    options.add_argument('--start-maximized')

    # disable extensions
    options.add_argument('--disable-extensions')

    # disable sandbox mode
    options.add_argument('--no-sandbox')

    # disable shared memory usage
    options.add_argument('--disable-dev-shm-usage')

    # set user agent
    options.add_argument(f'user-agent={user_agent}')

    #create a new driver instance
    driver = webdriver.Chrome(service=service, options=options)

    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    return driver

def fetch_cookies(driver, url):
    #navigate to url
    driver.get(url)
    # Wait for page to load
    while driver.execute_script("return document.readyState") != "complete":
        pass
    return driver.get_cookies()

def extract_cookie(cookies, name):
    for cookie in cookies:
        if cookie['name'] == name:
            return f"{cookie['name']}={cookie['value']}"
    return None

def session_cookie(url, cookie_name):
    user_agent = get_random_user_agent()
    driver = create_stealth_driver(user_agent)
    cookies = fetch_cookies(driver, url)
    cookie = extract_cookie(cookies, cookie_name)
    driver.quit()
    return user_agent, cookie
