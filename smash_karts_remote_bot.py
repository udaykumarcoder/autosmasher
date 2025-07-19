import os
import sys
import time
import threading
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SmashKartsRemoteBot:
    def __init__(self):
        self.driver = None
        self.bot_running = False
        self.bot_thread = None
        self.remote_url = None
        self.session_id = None
        
    def setup_remote_browser(self, remote_url="http://localhost:4444/wd/hub"):
        """Setup remote Chrome browser using Selenium Grid or cloud service"""
        chrome_options = Options()
        
        # Headless mode for remote execution
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        print("🌐 Connecting to remote browser...")
        try:
            self.driver = webdriver.Remote(
                command_executor=remote_url,
                options=chrome_options
            )
            
            # Hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.remote_url = remote_url
            print("✅ Connected to remote browser!")
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to remote browser: {e}")
            return False
    
    def setup_cloud_browser(self, service="browserstack"):
        """Setup browser on cloud service (BrowserStack, Sauce Labs, etc.)"""
        if service == "browserstack":
            return self._setup_browserstack()
        elif service == "saucelabs":
            return self._setup_saucelabs()
        else:
            print("❌ Unsupported cloud service")
            return False
    
    def _setup_browserstack(self):
        """Setup BrowserStack remote browser"""
        # You'll need to set these environment variables
        username = os.getenv('BROWSERSTACK_USERNAME')
        access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
        
        if not username or not access_key:
            print("❌ Please set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables")
            return False
        
        chrome_options = Options()
        chrome_options.set_capability('bstack:options', {
            'os': 'Windows',
            'osVersion': '10',
            'browserVersion': 'latest',
            'projectName': 'SmashKartsBot',
            'sessionName': 'Bot Session',
            'seleniumVersion': '4.0.0'
        })
        
        remote_url = f"https://{username}:{access_key}@hub-cloud.browserstack.com/wd/hub"
        
        print("☁️ Connecting to BrowserStack...")
        try:
            self.driver = webdriver.Remote(
                command_executor=remote_url,
                options=chrome_options
            )
            self.remote_url = remote_url
            print("✅ Connected to BrowserStack!")
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to BrowserStack: {e}")
            return False
    
    def _setup_saucelabs(self):
        """Setup Sauce Labs remote browser"""
        username = os.getenv('SAUCE_USERNAME')
        access_key = os.getenv('SAUCE_ACCESS_KEY')
        
        if not username or not access_key:
            print("❌ Please set SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables")
            return False
        
        chrome_options = Options()
        chrome_options.set_capability('platformName', 'Windows 10')
        chrome_options.set_capability('browserVersion', 'latest')
        
        remote_url = f"https://{username}:{access_key}@ondemand.us-west-1.saucelabs.com:443/wd/hub"
        
        print("☁️ Connecting to Sauce Labs...")
        try:
            self.driver = webdriver.Remote(
                command_executor=remote_url,
                options=chrome_options
            )
            self.remote_url = remote_url
            print("✅ Connected to Sauce Labs!")
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to Sauce Labs: {e}")
            return False
    
    def navigate_and_setup(self, url="https://smashkarts.io/"):
        """Navigate to game and prepare for bot"""
        print(f"🎮 Opening {url}...")
        self.driver.get(url)
        time.sleep(5)
        
        # Wait for page to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print("⚠ Page load timeout, but continuing...")
        
        print("\n🎯 REMOTE BOT SETUP:")
        print("1. The game is now running on the remote server")
        print("2. You can monitor the session through the cloud service dashboard")
        print("3. The bot will run automatically in the background")
        print("4. No local resources will be used")
        
    def bot_cycle(self):
        """Main bot movement cycle"""
        print("🤖 Remote bot started! Running movement pattern...")
        
        # Get the body element to send keys to
        body = self.driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(self.driver)
        
        cycle_count = 0
        while self.bot_running:
            try:
                cycle_count += 1
                print(f"🔄 Remote Cycle {cycle_count}")
                
                # 1. Hold Up for 5 seconds
                actions.key_down(Keys.ARROW_UP).perform()
                if not self._sleep_check(5, "Up"):
                    break
                
                # 2. Up+Left for 5 seconds
                actions.key_down(Keys.ARROW_LEFT).perform()
                if not self._sleep_check(5, "Up+Left"):
                    break
                actions.key_up(Keys.ARROW_LEFT).perform()
                
                # 3. Up+Right for 5 seconds
                actions.key_down(Keys.ARROW_RIGHT).perform()
                if not self._sleep_check(5, "Up+Right"):
                    break
                actions.key_up(Keys.ARROW_RIGHT).perform()
                
                # 4. Space
                actions.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                if not self._sleep_check(0.5, "Space"):
                    break
                
                # 5. Down for 5 seconds
                actions.key_up(Keys.ARROW_UP).perform()
                actions.key_down(Keys.ARROW_DOWN).perform()
                if not self._sleep_check(5, "Down"):
                    break
                
                # 6. Down+Left for 5 seconds
                actions.key_down(Keys.ARROW_LEFT).perform()
                if not self._sleep_check(5, "Down+Left"):
                    break
                actions.key_up(Keys.ARROW_LEFT).perform()
                
                # 7. Down+Right for 5 seconds
                actions.key_down(Keys.ARROW_RIGHT).perform()
                if not self._sleep_check(5, "Down+Right"):
                    break
                actions.key_up(Keys.ARROW_RIGHT).perform()
                
                # 8. Space
                actions.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                
                # Reset for next cycle
                actions.key_up(Keys.ARROW_DOWN).perform()
                
            except Exception as e:
                print(f"❌ Error in remote cycle: {e}")
                break
        
        # Clean up keys
        self._release_all_keys()
        print("🛑 Remote bot stopped")
    
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
        """Start the bot in background thread"""
        if not self.bot_running:
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

def main():
    print("🎮 Smash Karts Remote Bot (No Local Heat!)")
    print("=" * 50)
    print("Choose your remote option:")
    print("1. Selenium Grid (self-hosted)")
    print("2. BrowserStack (cloud)")
    print("3. Sauce Labs (cloud)")
    print("4. Local headless (minimal heat)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    bot = SmashKartsRemoteBot()
    
    try:
        if choice == "1":
            # Selenium Grid
            grid_url = input("Enter Selenium Grid URL (default: http://localhost:4444/wd/hub): ").strip()
            if not grid_url:
                grid_url = "http://localhost:4444/wd/hub"
            
            if not bot.setup_remote_browser(grid_url):
                return
                
        elif choice == "2":
            # BrowserStack
            if not bot.setup_cloud_browser("browserstack"):
                return
                
        elif choice == "3":
            # Sauce Labs
            if not bot.setup_cloud_browser("saucelabs"):
                return
                
        elif choice == "4":
            # Local headless (minimal heat)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            print("🌐 Starting local headless browser...")
            try:
                bot.driver = webdriver.Chrome(options=chrome_options)
                bot.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                print("✅ Local headless browser started!")
            except Exception as e:
                print(f"❌ Error starting browser: {e}")
                return
        else:
            print("❌ Invalid choice")
            return
        
        # Navigate and start bot
        bot.navigate_and_setup()
        
        if choice in ["2", "3"]:
            print("\n☁️ Cloud bot is ready!")
            print("📊 You can monitor the session in your cloud service dashboard")
        else:
            print("\n🎯 Bot is ready!")
        
        input("Press Enter to start the bot...")
        
        # Start bot
        if bot.start_bot():
            print("\n🚀 Remote bot is now running!")
            print("❄️ Your PC will stay cool!")
            print("📝 You can now:")
            print("   - Work on other tasks")
            print("   - Use your PC normally")
            print("   - Monitor the bot remotely")
            print("\n⏹ Press Enter anytime to STOP the bot...")
            
            # Wait for user to stop
            input()
            
        else:
            print("❌ Failed to start bot")
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🧹 Cleaning up...")
        bot.cleanup()
        print("✅ Done!")

if __name__ == "__main__":
    main() 