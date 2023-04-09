driver.get(f"https://{s}")
            time.sleep(3)
            driver.execute_script('document.querySelector("#usercentrics-root").shadowRoot.querySelector("#uc-center-container > div.sc-bYoBSM.jvautU > div > div > div > button.sc-gsDKAQ.fWOgSr").click()')
            time.sleep(0.5)
            city_input = driver.find_element("xpath", "//*[@id=\"oss-location\"]").send_keys(self.props["stadt"])
            time.sleep(0.7)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
            if self.props["mieten"] == 1:
                
                driver.find_element("xpath", "//*[@id=\"oss-form\"]/article/div/div[1]/div/div[3]/div/div/select/option[1]")
            else:
                driver.find_element("xpath", "//*[@id=\"oss-form\"]/article/div/div[1]/div/div[3]/div/div/select/option[2]")
            if self.props["preis"][1] > 0:
                driver.find_element("xpath", "//*[@id=\"oss-price\"]").send_keys(self.props["preis"][1])
            
            if self.props["zimmer"][0] == 1:
                driver.find_element("xpath", "//*[@id=\"oss-rooms\"]/option[2]")
            if self.props["zimmer"][0] == 2:
                driver.find_element("xpath", "//*[@id=\"oss-rooms\"]/option[4]")
            if self.props["zimmer"][0] == 3:
                driver.find_element("xpath", "//*[@id=\"oss-rooms\"]/option[6]")
            if self.props["zimmer"][0] == 4:
                driver.find_element("xpath", "//*[@id=\"oss-rooms\"]/option[6]")
            if self.props["zimmer"][0] > 4:
                driver.find_element("xpath", "//*[@id=\"oss-rooms\"]/option[6]")
                if self.props["zimmer"][0] > 5:
                    print("Max Zimmer erreicht. Forgot to implement minimum number of rooms bigger than website startpage max val")
            if self.props["qm"][0] != 0:
                driver.find_element("xpath", "//*[@id=\"oss-area\"]").send_keys(self.props["qm"][0])
            time.sleep(1)
            driver.execute_script('document.querySelector("#oss-form > article > div > div.grid-item.oss-layer-one-whole.oss-no-layer-one-sixth.search-section.oss-no-layer-form-content-offset > button").click()')
            time.sleep(5)
            driver.find_element(By.XPATH, "//*[@id=\"captcha-box\"]/div/div[2]/div[1]/div[3]").click()
            driver.find_element(By.XPATH, "//*[@id=\"captcha-box\"]/div/div[2]/div[2]/div").click()
            if (self.props["preis"][0]==0 and self.props["zimmer"][1]==0 and self.props["qm"][1]==0): #common search
                pass
            else:
                if self.props["preis"][0]!=0:
                    driver.find_element(By.XPATH, "//*[@id=\"reactCockpitForm\"]/div/div[1]/div/div/div[2]/div/div/div/div").click()
                    driver.find_element(By.XPATH, "//*[@id=\"priceRangeMin\"]").send_keys(self.props["zimmer"][1])
                    driver.find_element(By.XPATH, "//*[@id=\"reactCockpitForm\"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/button").click()
                if self.props["qm"][1]!=0:
                    driver.find_element(By.XPATH, "//*[@id=\"reactCockpitForm\"]/div/div[1]/div/div/div[3]/div/div/div/div").click()
                    driver.find_element(By.XPATH, "//*[@id=\"netAreaRangeMax\"]").send_keys(self.props["qm"][1])
                    driver.find_element(By.XPATH, "//*[@id=\"reactCockpitForm\"]/div/div[1]/div/div/div[3]/div/div/div[2]/div[2]/button").click()
                if self.props["zimmer"][0]!=0:
                    driver.find_element(By.XPATH, "//*[@id=\"reactCockpitForm\"]/div/div[1]/div/div/div[4]/div/div/div/div").click()
                    driver.find_element(By.XPATH, "//*[@id=\"numberOfRoomsRangeMax\"]").send_keys(self.props["zimmer"][0])
                    driver.find_element(By.XPATH, "//*[@id=\"reactCockpitForm\"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/button").click()
                
            def get_pages():
                try:
                    driver.find_element(By.ID, "listings").find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")[-2].get_attribute("innerHTML")
                except BaseException:
                    return 1
            def decode_urls(driver):
                items = driver.find_element(By.ID, "resultListItems").find_elements(By.TAG_NAME, "li")
                res = []
                for i in items:
                    try:
                        id = i.get_attribute("data-id")
                    except BaseException:
                        pass
                    else:
                        res.append(f"https://www.immobilienscout24.de/expose/{id}#/")
            self.page_current = 1
            while (self.page_current <= get_pages()):
                self.links_arr.append(decode_urls(driver))
                try:
                    driver.find_element(By.ID, "listings").find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")[-1].click()
                except BaseException:
                    return
