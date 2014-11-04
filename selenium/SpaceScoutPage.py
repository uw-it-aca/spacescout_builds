# Selenium
from selenium import webdriver

from selenium.common.exceptions import NoSuchFrameException, StaleElementReferenceException, ElementNotVisibleException, WebDriverException, NoSuchElementException
from selenium.common.exceptions import TimeoutException as TE

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Python
import time

class SpaceScoutPage():

    def __init__(self, driver, username, password, url, clearFavorites=False, loginType='django'):
        self.driver = driver
        self.username = username
        self.password = password
        self.url = url
        self.loginType = loginType

        if clearFavorites:
            self.loginAsUser()
            if self.getFavoriteCount() > 0:
                for room in self.getFavoriteRoomList():
                    self.unfavoriteRoom(room)

            self.logout()

    # - General Use Functions -

    def getElement(self, selector, xpath=False, name=False, errorText=False, click=False):
        if xpath:
            byMethod = By.XPATH
        else:
            byMethod = By.CSS_SELECTOR

        element = None

        try:
            if click:
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((byMethod, selector))).click()
            else:
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((byMethod, selector)))
        except TE:
            raise self.customAE(selector, name, errorText)
        except (ElementNotVisibleException, WebDriverException):
            if xpath:
                self.driver.execute_script("$x(\"" + selector + "\").click()")
            else:
                self.driver.execute_script("$(\"" + selector + "\").click()")

        return element

    def getElements(self, selector, xpath=False, name=False, errorText=False):
        if xpath:
            byMethod = By.XPATH
        else:
            byMethod = By.CSS_SELECTOR

        try:
            return WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((byMethod, selector)))
        except TE:
            raise self.customAE(selector, name, errorText)

    def customAE(self, selector, name=False, errorText=False):
        if errorText:
            return AssertionError(errorText)
        elif name:
            return AssertionError("Could not find element " + name + ".")
        else:
            return AssertionError("Could not find element at " + selector)

    def clickElementGroup(self, selPrefix, itemList, listName):
        for item in itemList:
            self.getElement(selPrefix + item, errorText="Could not find " + item + " in " + listName + ".", click=True)

    def newTab(self):
        mainWindow = self.driver.window_handles[0]
        newWindow = None
        self.driver.execute_script("window.open()")

        for handle in self.driver.window_handles:
            if handle != mainWindow:
                newWindow = handle

        self.driver.switch_to_window(newWindow)
        return newWindow

    def closeTab(self, newWindow):
        self.driver.switch_to_window(newWindow)
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    # - Page Interaction -

    # Filter Options

    def toggle_filter(self):
        self.getElement("button#filter_button", name="filter toggle", click=True)

    def check_spaces(self, itemList):
#       roomTypes = ['study_room', 'study_area', 'computer_lab', 'studio', 'classroom', 'open', 'lounge', 'cafe', 'outdoor']
        self.clickElementGroup("fieldset#filter_space_types input#", itemList, "room types")

    def check_reservable_only(self):
        self.getElement("fieldset#filter_reservability input#reservable", name="reservable spaces checkbox", click=True)

    def set_capacity(self, capacity):
        select = Select(self.getElement("fieldset#filter_capacity select#capacity"))
        select.select_by_visible_text(str(capacity))

    def specify_day_and_time(self):
        self.getElement("fieldset#filter_hours input#hours_list_input", name="specify day and time radio button", click=True)

    def specify_open_now(self):
        self.getElement("fieldset#filter_hours input#open_now", name="specify open now radio button", click=True)

    def set_day_and_time(self, froms, untils):
        fromDay  = Select(self.getElement("div#hours_list_container select#day-from", name="from-day"))
        fromTime = Select(self.getElement("div#hours_list_container select#hour-from", name ="from-time"))
        fromAmPm = Select(self.getElement("div#hours_list_container select#ampm-from", name="from-ampm"))

        untilDay   = Select(self.getElement("div#hours_list_container select#day-until", name="until-day"))
        untilTime  = Select(self.getElement("div#hours_list_container select#hour-until", name="until-time"))
        untilAmPm  = Select(self.getElement("div#hours_list_container select#ampm-until", name="until-ampm"))

        fromDay.select_by_visible_text(froms['day'])
        fromTime.select_by_visible_text(froms['time'])
        fromAmPm.select_by_visible_text(froms['ampm'])

        untilDay.select_by_visible_text(untils['day'])
        untilTime.select_by_visible_text(untils['time'])
        untilAmPm.select_by_visible_text(untils['ampm'])

    def specify_buildings(self):
        self.getElement("fieldset#filter_location input#building_list_input", name="specific buildings radio button", click=True)

    def specify_campus(self):
        self.getElement("fieldset#filter_location input#entire_campus", name="entire campus radio button", click=True)

    def set_buildings(self, buildings):
        buildingBox = self.getElement("div#building_list_container li.search-field input", name="building box")
        for building in buildings:
            for char in building:
                if char is '(':
                    buildingBox.click()
                    buildingBox.send_keys(Keys.SHIFT, "9")
                else:
                    buildingBox.click()
                    buildingBox.send_keys(char)

            buildingBox.send_keys(Keys.RETURN)


    def check_resources(self, itemList):
#       resList = ['whiteboards', 'outlets', 'computers', 'scanner', 'displays', 'projector', 'printing']
        self.clickElementGroup("fieldset#filter_equipment_types input#has_", itemList, "resources list")

    def check_noise_levels(self, itemList):
#       levels = ['silent', 'quiet', 'moderate']
        self.clickElementGroup("fieldset#filter_noise_level input#", itemList, "noise levels list")

    def check_natural_light(self):
        self.getElement("fieldset#filter_lighting input#lighting", name="lighting checkbox", click=True)

    def check_food_coffee(self, itemList):
#       locations = ['space', 'building', 'neighboring']
        self.clickElementGroup("fieldset#filter_food_coffee input#", itemList, "food/coffee locations list")

    def button_reset(self):
        self.getElement("button#cancel_results_button", name="cancel results button", click=True)

    def button_apply(self):
        self.getElement("button#view_results_button", name="view results button", click=True)
        time.sleep(4)

    # Results Interaction

    def getBuildingList(self):
        buildingList = []
        buildingElements = self.getElements("div#info_list h3.building_header", name="building names")
        for building in buildingElements:
            buildingList.append(building.text)

        return buildingList

    def getRoomList(self):
        roomList = []
        roomElements = self.getElements("div#info_list div.space-detail-name", name="room names")
        try:
            for room in roomElements:
                roomList.append(room.text)
        except StaleElementReferenceException:
            return self.getRoomList()

        return roomList

    def getRoomListFromBuilding(self, building):
        roomList = []
        roomElements = self.getElements("//div[@id='info_list']//h3[. = '" + building + "']/..//div[@class = 'space-detail-name']", xpath=True, name=("room names for building " + building))
        for room in roomElements:
            roomList.append(room.text)

        return roomList

    # Room Interaction

    def openRoomDetails(self, room):
        self.getElement("div#info_list button.space-detail-list-item[aria-label='Get space details for " + room + "']", name="detail opener", click=True)
        # try:
        #     self.driver.find_element_by_css_selector("div.space-detail-container")
        # except NoSuchElementException:
        #     self.openRoomDetails(room)

    def closeRoomDetails(self):
        self.getElement("div.space-detail a.close", name="detail closer", click=True)

    def openRoomMap(self, room):
        self.openRoomDetails(room)
        self.getElement("div.space-detail button#mapControl", name="map control button", click=True)
        time.sleep(1)
        self.getElement("div.space-detail button#carouselControl", name="carousel control button", click=True)
        time.sleep(1)
        self.getElement("div.space-detail button#mapControl", name="map control button", click=True)
        return "display: block" in self.getElement("div.space-detail div#spaceMap").get_attribute('style') 

    def getRoomType(self, room):
        self.openRoomDetails(room)
        roomType = self.getElement("div.space-detail div.space-detail-type", name="room type").text
        return roomType

    def getRoomCapacity(self, room):
        self.openRoomDetails(room)
        roomCap = self.getElement("div.space-detail span.space-detail-capacity", name="room capacity").text
        return int(roomCap[-3:-1].strip())

    def getRoomDetail(self, room, detailType):
        self.openRoomDetails(room)
        try:
            detailText =  self.getElement("//div[@class = 'space-detail']//li[@class = 'clearfix']//h3[. = '" + detailType + "']/../div[@class = 'space-info-detail pull-left']", xpath=True, name=("room detail " + detailType)).text
        except StaleElementReferenceException:
            return self.getRoomDetail(room, detailType)

        return detailText


    # Time Stuffs

    def convertTo24(self, time):
        if time == "12:00PM" or time == "Noon":
            return 1200

        if time == "Midnight":
            return 0

        hourMin = time[:-2]
        hourMin = hourMin.split(':')
        hour = int(hourMin[0])
        minutes = 0
        if len(hourMin) > 1:
            minutes = int(hourMin[1])

        if time.endswith("PM"):
            hour = hour + 12
        elif hour is 12:
            hour = 0

        return hour * 100 + minutes   

    class HourInterval():
        def __init__(self, openTime, closeTime):
            self.openTime = openTime
            self.closeTime = closeTime

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return "[" + str(self.openTime) + " - " + str(self.closeTime) + "]"

    def getNextDay(self, day):
        days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su', 'M']
        return days[days.index(day) + 1]

    def getOpenHours(self, room):
        self.openRoomDetails(room)

        hours = { 'M' : [], 'T' : [], 'W' : [], 'Th': [], 'F' : [], 'Sa': [], 'Su': [] }

        hoursText =  self.getElement("//div[@class = 'space-detail']//li[@class = 'clearfix']//h3[. = 'Hours']/../div[@class = 'space-info-detail pull-left']", xpath=True, name="room hours").text        
        if hoursText == "":
            return self.getOpenHours(room)
        hoursLines = hoursText.split('\n')

        for day in hours.keys():
            for line in hoursLines:
                line = line.split(':', 1)
                if day in line[0]:
                    openHours = line[1].split('-')

                    if line[1].endswith("24 Hours"):
                        openTime = 0
                        closeTime = 2359
                    elif line[1].endswith("Midnight"):
                        openTime  = self.convertTo24(openHours[0].strip())
                        closeTime = 2359
                    else:
                        openTime  = self.convertTo24(openHours[0].strip())
                        closeTime = self.convertTo24(openHours[1].strip())

                    if closeTime < openTime:
                        # Morning After mode
                        hours[self.getNextDay(day)].append(self.HourInterval(0, closeTime))
                        closeTime = 2359

                    hours[day].append(self.HourInterval(openTime, closeTime))

        return hours

    def roomIsOpen(self, room, time):
        day  = time['day']
        hour = self.convertTo24(time['hour'].strip())   
        hours = self.getOpenHours(room)

        for interval in hours[day]:
            if hour >= interval.openTime and hour <= interval.closeTime:
                return True

        return False

    def favoriteRoom(self, room):
        self.openRoomDetails(room)
        self.getElement("button#favorite_space", name="favorite button", click=True)
        time.sleep(3)

    def shareRoom(self, room, recipient, message):
        self.openRoomDetails(room)
        self.getElement("button#share_space", name="share button", click=True)

        toField = self.getElement("input#id_recipient-tokenfield", name="recipient field")
        toField.send_keys(recipient)

        messageField = self.getElement("textarea#id_message", name="message field")
        messageField.send_keys(message)

        self.getElement("input#formSubmit_button", name="submit button", click=True)

        checkRes = self.getElement("h2", name="thank-you").text == 'Thank You'
        self.getElement("div#main_content a", click=True)
        return checkRes       

    def roomFavorited(self, room):
        if self.getFavoriteCount() == 0:
            raise AssertionError("No favorite rooms")

        windowHandle = self.newTab()
        self.driver.get(self.url + '/favorites')

        favoritedRooms = self.getElements("div.space-detail-container h4#space-name", name="favorited rooms")
        favoriteTitles = []
        for favorite in favoritedRooms:
            favoriteTitles.append(favorite.text.split('\n')[1])

        self.closeTab(windowHandle)

        return room in favoriteTitles

    def getFavoriteRoomList(self):
        windowHandle = self.newTab()
        self.driver.get(self.url + '/favorites')
        roomNames = []
        for element in self.getElements("div.space-detail-header h4#space-name", name="space detail header"):
            roomNames.append(element.text)

        return roomNames

    def unfavoriteRoom(self, room):
        windowHandle = self.newTab()
        self.driver.get(self.url + '/favorites')

        for element in self.getElements("div.space-detail-header", name="space detail header"):
            try:
                if element.find_element_by_css_selector("h4#space-name").text.endswith(room):
                    try:
                        element.find_element_by_css_selector("a.space-detail-fav").click()
                        break
                    except TE:
                        raise AssertionError("Could not find unfavorite button for room " + room + ".")
            except TE:
                raise AssertionError("Could not find room title.")

        self.getElement("div#space-detail-blank a", name="favorites return link", click=True)
        self.closeTab(windowHandle)

    def getFavoriteCount(self):
        windowHandle = self.newTab()
        self.driver.get(self.url + '/favorites')

        time.sleep(5)
        favText = self.getElement("span.favorites_total_container", name="favorite count").text

        self.closeTab(windowHandle)
        return int(favText[0:2].strip())

    def writeReview(self, room, stars, reviewText):
        self.openRoomDetails(room)
        self.getElement("button#Write_Review_btn", name="write review button", click=True)
        time.sleep(1)
        self.getElement("fieldset.space-review-rating input[value='" + str(stars) + "']", name="stars", click=True)
        try:
            self.getElement("textarea#Review_comment", name="review textarea").send_keys(reviewText)
        except ElementNotVisibleException:
            self.writeReview(room, stars, reviewText)
        self.getElement("button#space-review-submit", name="submit button", click=True)


    # User Management

    def loginAsUser(self):
        self.getElement("a#login_button", name="login button", click=True)
        time.sleep(2)

        if self.loginType == 'netid':
            try:
                self.getElement("input#weblogin_netid", name="username field").send_keys(self.username)
            except AssertionError as err:
                if self.getElement("li.login-static-name span", name="username label").text == self.username:
                    pass
                else:
                    raise err
            self.getElement("input#weblogin_password", name="password field").send_keys(self.password)
            self.getElement("ul.submit input", name="submit button", click=True)
            time.sleep(2)

        elif self.loginType == 'django':
            self.getElement("input#id_username", name="username field").send_keys(self.username)
            self.getElement("input#id_password", name="password field").send_keys(self.password)
            self.getElement("//input[@type='submit']", name="submit button", xpath=True, click=True)

        else:
            raise AssertionError("No login type specified")

        time.sleep(2)

    def logout(self):
        self.driver.delete_all_cookies()
        self.getElement("a#logout_button", name="logout button", click=True)
        self.driver.get(self.url)

    # Link Tests
    def check_link(self, linkElement, url):
        mainWindow = self.driver.window_handles[0]
        newWindow = None
        linkElement.click()
        time.sleep(2)

        for handle in self.driver.window_handles:
            if handle != mainWindow:
                newWindow = handle

        self.driver.switch_to_window(newWindow)
        result = self.driver.current_url.startswith(url)
        self.driver.close()
        self.driver.switch_to_window(mainWindow)

        return result

    def check_suggestIt(self):
        self.getElement("a#suggest", name="suggest it link", click=True) 
        time.sleep(2)
        result = self.driver.current_url.startswith(self.url + "suggest") or self.driver.current_url.startswith(self.url + "/suggest")
        self.driver.back()
        return result

    def check_privacy_link(self):
        return self.check_link(self.getElements("div#footer a", name="footer links")[0], ("http://www.washington.edu/online/privacy"))

    def check_terms_link(self):
        return self.check_link(self.getElements("div#footer a", name="footer links")[1], ("http://www.washington.edu/online/terms/"))

    def check_about_link(self):
        return self.check_link(self.getElements("div#footer a", name="footer links")[2], ("http://www.washington.edu/itconnect/learn/tools/spacescout"))

    def check_faq_link(self):
        return self.check_link(self.getElements("div#footer a", name="footer links")[3], ("http://www.washington.edu/itconnect/learn/tools/spacescout"))

    # Location Management
    def changeLocation(self, location):
        # Location Values: Seattle, Tacoma
        locationSelect = Select(self.getElement("select#location_select", name="location select"))
        locationSelect.select_by_visible_text("UW " + location)

    # Time Stuffs

    def convertTo24(self, time):
        if time == "12:00PM" or time == "Noon":
            return 1200

        if time == "Midnight":
            return 0

        hourMin = time[:-2]
        hourMin = hourMin.split(':')
        hour = int(hourMin[0])
        minutes = 0
        if len(hourMin) > 1:
            minutes = int(hourMin[1])

        if time.endswith("PM"):
            hour = hour + 12
        elif hour is 12:
            hour = 0

        return hour * 100 + minutes   

    def getNextDay(self, day):
        days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su', 'M']
        return days[days.index(day) + 1]

class HourInterval():
    def __init__(self, openTime, closeTime):
        self.openTime = openTime
        self.closeTime = closeTime

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        if self.openTime == other.openTime and self.closeTime == other.closeTime:
            return 0
        elif self.openTime > other.openTime:
            return 1
        elif self.openTime < other.openTime:
            return -1
        else:
            if self.closeTime < other.closeTime:
                return -1
            else:
                return 1

    def __str__(self):
        return "[" + str(self.openTime) + " - " + str(self.closeTime) + "]"



    """ Currently not working/serving any purpose
    def getOpenStats(self):
        times = ["1AM", "2AM", "3AM", "4AM", "5AM", "6AM", "7AM", "8AM", "9AM", "10AM", "11AM", "Noon",
                 "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM", "10PM", "11PM", "12AM"]
        days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su']

        opens = {}
        for day in days:
            opens[day] = {}
            for time in times:
                opens[day][time] = 0
            
        rooms = self.getRoomList()
        for room in rooms:
            print(room)
            hours = self.getOpenHours(room)
            for day in days:
                print(day)
                for time in times:
                    print(time)
                    if self.roomIsOpen(room, {'day':day,'hour':time}):
                        opens[day][time] = opens[day][time] + 1

        return opens
"""
