import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

EMAIL = "weixuan0204@126.com"
USERNAME = "Russell333_"
PASSWORD = "Oubrejr.3"
MAX_COMMENTS = 20000
KEYWORD = "Tiktok ban"
CSV_FILE = "tiktok_ban_comments.csv"

# Define time interval
months = [
    ("2024-12-01", "2024-12-31"),
    ("2025-01-01", "2025-01-31"),
    ("2025-02-01", "2025-02-28"),
    ("2025-03-01", "2025-03-31"),
    ("2025-04-01", "2025-04-30")
]

def login(driver):
    driver.get("https://twitter.com/login")
    time.sleep(3)
    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(EMAIL)
    username_input.send_keys(Keys.RETURN)
    time.sleep(2)

    try:
        handle_input = driver.find_element(By.NAME, "text")
        if handle_input:
            print("需要输入用户名...")
            handle_input.send_keys(USERNAME)
            handle_input.send_keys(Keys.RETURN)
            time.sleep(2)
    except:
        print("跳过用户名输入（未要求）")

    try:
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
    except:
        print("找不到密码输入框，可能需要手动验证")
    time.sleep(5)

def search_keyword(driver, keyword, since, until):
    query = f"{keyword} since:{since} until:{until}"
    query_encoded = query.replace(" ", "%20").replace(":", "%3A")
    search_url = f"https://twitter.com/search?q={query_encoded}&src=typed_query"

    driver.get(search_url)
    time.sleep(5)

    tweet_links = set()
    for _ in range(10):
        articles = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        for article in articles:
            try:
                link = article.find_element(By.XPATH, ".//a[@role='link' and contains(@href, '/status/')]").get_attribute("href")
                tweet_links.add(link.replace("x.com", "twitter.com"))
            except:
                continue
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    return list(tweet_links)

def extract_comment_data(article):
    try:
        user = article.find_element(By.XPATH, './/div[@dir="ltr"]/span').text
        time_element = article.find_element(By.XPATH, './/time')
        timestamp = time_element.get_attribute("datetime")
        comment_element = article.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
        comment = comment_element.text.strip()
        return (user, timestamp, comment)
    except:
        return None

def scroll_and_extract_replies(driver, url, collected, limit):
    driver.get(url)
    time.sleep(5)
    if not driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]'):
        print("⚠️ 页面中未发现评论，跳过该推文。")
        return collected

    seen = set()
    no_new_count = 0
    while len(collected) < limit and no_new_count < 1:
        articles = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        before_count = len(collected)

        for article in articles:
            data = extract_comment_data(article)
            if data and data not in seen:
                seen.add(data)
                collected.append(data)
                if len(collected) >= limit:
                    break

        if len(collected) == before_count:
            no_new_count += 1
        else:
            no_new_count = 0

        print(f"⏬ 正在滚动，当前收集 {len(collected)} 条评论，未增长次数 {no_new_count}")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    return collected

def save_to_csv(data, filename, append=False):
    mode = "a" if append else "w"
    header = not append or not os.path.exists(filename)
    with open(filename, mode=mode, encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(["UserID", "Date", "Comment"])
        writer.writerows(data)

def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        login(driver)
        collected_comments = []
        last_saved_count = 0

        for since, until in months:
            print(f"\n📅 正在搜索时间区间：{since} ~ {until}")
            tweet_links = search_keyword(driver, KEYWORD, since, until)
            print(f"  ➤ 找到 {len(tweet_links)} 条推文")

            for url in tweet_links:
                if len(collected_comments) >= MAX_COMMENTS:
                    break
                print(f"\n正在抓取推文：{url}")
                collected_comments = scroll_and_extract_replies(driver, url, collected_comments, MAX_COMMENTS)
                print(f"当前已收集：{len(collected_comments)} 条评论")

                if len(collected_comments) - last_saved_count >= 100:
                    save_to_csv(collected_comments[last_saved_count:], CSV_FILE, append=True)
                    last_saved_count = len(collected_comments)
                    print(f"📁 已自动保存 {last_saved_count} 条评论到 {CSV_FILE}")

            if len(collected_comments) >= MAX_COMMENTS:
                break

        # 保存剩余的最后一批（<500）
        if len(collected_comments) > last_saved_count:
            save_to_csv(collected_comments[last_saved_count:], CSV_FILE, append=True)
            print(f"📁 已自动保存最终 {len(collected_comments)} 条评论到 {CSV_FILE}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
