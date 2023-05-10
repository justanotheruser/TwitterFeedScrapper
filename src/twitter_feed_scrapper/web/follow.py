def follow(driver, user: str):
    driver.get(f'https://twitter.com/{user}')
    input()
