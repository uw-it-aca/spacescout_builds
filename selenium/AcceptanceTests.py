# Selenium
from selenium import webdriver

# PyVirtualDisplay
from pyvirtualdisplay import Display

# Page class
from SpaceScoutPage import SpaceScoutPage
from SpaceScoutPage import HourInterval
import unittest

import time
import TestParameters as TP

username  = TP.username
password  = TP.password
pageUrl   = TP.pageUrl
loginType = TP.loginType

# Set up display, remove these lines if not running tests headless
display = Display(visible=0, size=(800, 600))
display.start()

# Set up webdriver
webDriver = webdriver.Firefox()
webDriver.get(pageUrl)

# Set up page controller
pageController = SpaceScoutPage(webDriver, username, password, pageUrl, clearFavorites=True, loginType=loginType)

class AcceptanceTests(unittest.TestCase):

    def test00_access_main_page(self):
        assert webDriver.current_url.startswith(pageUrl)

    def test01_aa_balcony_set_filters(self):
        # Enter Search Criteria 
        pageController.toggle_filter()
        pageController.specify_buildings()
        pageController.set_buildings(['Art Atrium', 'Library'])
        pageController.check_spaces(['outdoor', 'study_room'])
        pageController.specify_day_and_time()
        pageController.set_day_and_time({'day':'MON','time':'12:00', 'ampm':'AM'}, {'day':'THU', 'time':'11:30', 'ampm':'PM'})
        pageController.button_apply()
        
    def test02_aa_balcony_found_and_open_hours(self):
        # Open room and check hours
        assert 'AA Balcony' in pageController.getRoomList()
        openHours = pageController.getOpenHours('AA Balcony')
        expectedHours = {'W': [HourInterval(0, 2359)], 'F': [HourInterval(0, 2359)], 'M': [HourInterval(0, 2359)], 'Su': [HourInterval(0, 2359)], 'T': [HourInterval(0, 2359)], 'Th': [HourInterval(0, 2359)], 'Sa': [HourInterval(0, 2359)]}
        assert expectedHours == openHours , ("\nExpected: " + str(expectedHours) + "\nActual  : " + str(openHours))
        
    def test03_aa_balcony_close_room_and_edit_filters(self):
        # Close room and edit filter
        pageController.toggle_filter()
        pageController.check_natural_light()
        pageController.button_apply()

        assert 'AA Balcony' in pageController.getRoomList()

        pageController.toggle_filter()
        pageController.check_food_coffee(['neighboring'])
        pageController.button_apply()
        
        assert 'AA Balcony' in pageController.getRoomList()
        
    def test04_aa_balcony_favorite_room(self):
        # Favorite room
        pageController.loginAsUser()
        pageController.favoriteRoom('AA Balcony')

        assert pageController.roomFavorited('AA Balcony')
        
    def test05_aa_balcony_reset_filters(self):
        # Reset filters
        pageController.toggle_filter()
        pageController.check_natural_light()
        pageController.check_food_coffee(['neighboring'])
        pageController.check_resources(['whiteboards'])
        pageController.check_reservable_only()
        pageController.set_capacity(5)
        pageController.button_apply()
        
    def test06_study_room_233_check_room_details(self):
        # Verify Study Room 233
        assert 'Study Room 233' in pageController.getRoomList()
        assert 8 == pageController.getRoomCapacity('Study Room 233')

#       pageController.closeRoomDetails()

        expectedHours = {'W': [HourInterval(0, 2359)], 'F': [HourInterval(0, 2000)], 'M': [HourInterval(0, 2359)], 'Su': [HourInterval(1200, 2359)], 'T': [HourInterval(0, 2359)], 'Th': [HourInterval(0, 2359)], 'Sa': [HourInterval(1200, 2000)]}
        assert expectedHours == pageController.getOpenHours('Study Room 233')
        assert 'Whiteboards' in pageController.getRoomDetail('Study Room 233', 'Resources')

    def test07_study_room_233_write_review(self):
        pageController.writeReview('Study Room 233', 3, "I love it")
        assert pageController.shareRoom('Study Room 233', 'lisatest@uw.edu', 'Message is this.'), "Failed to share study room 233"
        
    def test08_change_campus_to_tacoma(self):
        # Change to Tacoma campus
        pageController.changeLocation("Tacoma")

    def test09_room_301_check_for_room(self):
        pageController.toggle_filter()
        pageController.button_reset()
        pageController.specify_day_and_time()
        pageController.set_day_and_time({'day':'MON','time':'8:00', 'ampm':'AM'}, {'day':'MON', 'time':'4:00', 'ampm':'PM'})
        pageController.button_apply()

        assert 'Sad' in pageController.getBuildingList()
        assert 'Room 301' in pageController.getRoomList()

    def test10_room_301_open_room_map(self):
        assert pageController.openRoomMap('Room 301')

    def test11_room_301_favorite_room(self):
        # Favorite and logout
        pageController.favoriteRoom('Room 301')
        pageController.logout()
  
    def test12_check_favorites(self):
        # Log back in
        pageController.loginAsUser()
      
        webDriver.get(pageUrl + "/favorites")
        assert pageController.roomFavorited('AA Balcony')
        assert pageController.roomFavorited('Room 301')

    def test13_unfavorite_rooms(self):
        pageController.unfavoriteRoom('Room 301')
        pageController.changeLocation("Seattle")
        pageController.unfavoriteRoom('AA Balcony')
        
        assert pageController.getFavoriteCount() == 0

    def test14_check_links(self):
        for linkCheck in [pageController.check_suggestIt, pageController.check_privacy_link, pageController.check_terms_link, pageController.check_about_link, pageController.check_faq_link]:
            assert linkCheck(), ("Link check " + str(linkCheck) + " failed.")


if __name__ == "__main__":
    unittest.main()
