import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SimpleSmashKartsBot:
    def __init__(self):
        self.driver = None
        self.bot_running = False
        self.bot_thread = None
        self.status = "idle"
        self.cycle_count = 0
        
    def setup_browser(self):
        """Setup Chrome browser"""
        chrome_options = Options()
        
        # For local testing - remove headless to see what's happening
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        print("🌐 Starting browser...")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.status = "browser_ready"
            print("✅ Browser started!")
            return True
            
        except Exception as e:
            print(f"❌ Error starting browser: {e}")
            return False
    
    def navigate_to_game(self, url="https://smashkarts.io/"):
        """Navigate to the game"""
        if not self.driver:
            return False
            
        try:
            print(f"🎮 Navigating to {url}...")
            self.driver.get(url)
            time.sleep(5)
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Focus on the game
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.click()
            
            self.status = "game_loaded"
            print("✅ Game loaded and focused!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading game: {e}")
            return False
    
    def bot_cycle(self):
        """Main bot movement cycle - SIMPLIFIED FOR WORKING"""
        print("🤖 Bot started! Cart is moving...")
        self.status = "running"
        
        try:
            # Get the body element to send keys to
            body = self.driver.find_element(By.TAG_NAME, "body")
            actions = ActionChains(self.driver)
            
            while self.bot_running:
                try:
                    self.cycle_count += 1
                    print(f"🔄 Cycle {self.cycle_count} - Cart moving!")
                    
                    # SIMPLE MOVEMENT PATTERN - JUST MAKE THE CART MOVE
                    
                    # 1. Forward movement
                    actions.key_down(Keys.ARROW_UP).perform()
                    if not self._sleep_check(3, "Forward"):
                        break
                    
                    # 2. Turn left
                    actions.key_down(Keys.ARROW_LEFT).perform()
                    if not self._sleep_check(2, "Left"):
                        break
                    actions.key_up(Keys.ARROW_LEFT).perform()
                    
                    # 3. Turn right
                    actions.key_down(Keys.ARROW_RIGHT).perform()
                    if not self._sleep_check(2, "Right"):
                        break
                    actions.key_up(Keys.ARROW_RIGHT).perform()
                    
                    # 4. Jump
                    actions.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                    if not self._sleep_check(1, "Jump"):
                        break
                    
                    # 5. Backward
                    actions.key_up(Keys.ARROW_UP).perform()
                    actions.key_down(Keys.ARROW_DOWN).perform()
                    if not self._sleep_check(3, "Backward"):
                        break
                    
                    # 6. Stop and repeat
                    actions.key_up(Keys.ARROW_DOWN).perform()
                    if not self._sleep_check(1, "Pause"):
                        break
                    
                except Exception as e:
                    print(f"❌ Error in cycle: {e}")
                    break
            
        except Exception as e:
            print(f"❌ Error in bot cycle: {e}")
        
        # Clean up keys
        self._release_all_keys()
        self.status = "stopped"
        print("🛑 Bot stopped")
    
    def _sleep_check(self, duration, action):
        """Sleep while checking if bot should stop"""
        end_time = time.time() + duration
        while time.time() < end_time:
            if not self.bot_running:
                return False
            time.sleep(0.1)
        return True
    
    def _release_all_keys(self):
        """Release all keys"""
        try:
            actions = ActionChains(self.driver)
            for key in [Keys.ARROW_UP, Keys.ARROW_DOWN, Keys.ARROW_LEFT, Keys.ARROW_RIGHT, Keys.SPACE]:
                actions.key_up(key)
            actions.perform()
        except:
            pass
    
    def start_bot(self):
        """Start the bot"""
        if not self.bot_running and self.driver:
            self.bot_running = True
            self.bot_thread = threading.Thread(target=self.bot_cycle, daemon=True)
            self.bot_thread.start()
            return True
        return False
    
    def stop_bot(self):
        """Stop the bot"""
        if self.bot_running:
            self.bot_running = False
            if self.bot_thread:
                self.bot_thread.join(timeout=2)
            return True
        return False
    
    def cleanup(self):
        """Clean up everything"""
        self.stop_bot()
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.status = "idle"

def test_bot():
    """Test the bot locally"""
    bot = SimpleSmashKartsBot()
    
    print("🧪 Testing Smash Karts Bot...")
    
    # Setup browser
    if not bot.setup_browser():
        print("❌ Failed to setup browser")
        return
    
    # Navigate to game
    if not bot.navigate_to_game():
        print("❌ Failed to load game")
        bot.cleanup()
        return
    
    print("✅ Ready! Starting bot in 3 seconds...")
    time.sleep(3)
    
    # Start bot
    if bot.start_bot():
        print("🚗 Bot is running! Press Ctrl+C to stop...")
        
        try:
            while bot.bot_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping bot...")
            bot.stop_bot()
    
    bot.cleanup()
    print("✅ Test completed!")

if __name__ == "__main__":
    test_bot() 