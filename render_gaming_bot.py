import os
import sys
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class RenderGamingBot:
    def __init__(self):
        self.driver = None
        self.bot_running = False
        self.bot_thread = None
        self.status = "idle"
        self.cycle_count = 0
        self.last_error = None
        
    def setup_browser(self):
        """Setup Chrome browser for local operation"""
        chrome_options = Options()
        
        # Local browser setup (not headless so you can see what's happening)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Keep browser visible so you can see what's happening
        # chrome_options.add_argument("--headless")  # Commented out for visibility
        
        print("🌐 Starting browser for Render gaming...")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.status = "browser_ready"
            print("✅ Browser started successfully!")
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error starting browser: {e}")
            return False
    
    def open_render_website(self):
        """Open Render.com website"""
        if not self.driver:
            return False
            
        try:
            print("🌐 Opening Render.com website...")
            self.driver.get("https://render.com")
            time.sleep(3)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Render.com website loaded!")
            self.status = "render_loaded"
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error loading Render.com: {e}")
            return False
    
    def find_and_click_signin(self):
        """Find and click the sign in button"""
        try:
            print("🔍 Looking for sign in button...")
            
            # Common selectors for sign in buttons
            signin_selectors = [
                "a[href*='signin']",
                "a[href*='login']",
                "button[data-testid*='signin']",
                "button[data-testid*='login']",
                ".signin",
                ".login",
                "[data-testid='signin-button']",
                "[data-testid='login-button']",
                "a:contains('Sign In')",
                "a:contains('Log In')",
                "button:contains('Sign In')",
                "button:contains('Log In')"
            ]
            
            for selector in signin_selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Found sign in button with selector: {selector}")
                    element.click()
                    time.sleep(2)
                    return True
                except:
                    continue
            
            # Try finding by text content
            try:
                signin_links = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Sign In') or contains(text(), 'Log In')]")
                for link in signin_links:
                    if link.is_displayed() and link.is_enabled():
                        print("✅ Found sign in link by text")
                        link.click()
                        time.sleep(2)
                        return True
            except:
                pass
            
            print("⚠️ Could not find sign in button automatically")
            print("🔧 Please manually click the 'Sign In' button in the browser window")
            input("Press Enter after you've clicked Sign In...")
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error finding sign in button: {e}")
            return False
    
    def wait_for_google_signin(self):
        """Wait for Google sign in option and guide user"""
        try:
            print("🔍 Looking for Google sign in option...")
            
            # Wait for Google sign in to appear
            google_selectors = [
                "[data-provider='google']",
                ".google-signin",
                ".google-login",
                "button[data-testid*='google']",
                "div[data-testid*='google']",
                "button:contains('Google')",
                "div:contains('Google')"
            ]
            
            google_found = False
            for selector in google_selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Found Google sign in option with selector: {selector}")
                    google_found = True
                    break
                except:
                    continue
            
            if not google_found:
                print("⚠️ Could not find Google sign in automatically")
                print("🔧 Please manually click the 'Sign in with Google' button")
            
            print("\n🎯 MANUAL SIGN IN REQUIRED:")
            print("1. In the browser window, click 'Sign in with Google'")
            print("2. Complete the Google sign in process")
            print("3. Wait until you're logged into Render.com dashboard")
            print("4. Then come back here and press Enter")
            
            input("Press Enter after you've signed in with Google...")
            
            # Wait a bit for the dashboard to load
            time.sleep(3)
            print("✅ Assuming Google sign in completed!")
            self.status = "signed_in"
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error during Google sign in: {e}")
            return False
    
    def navigate_to_games_section(self):
        """Navigate to games or web services section"""
        try:
            print("🎮 Looking for games or web services section...")
            
            # Try to find dashboard or services section
            dashboard_selectors = [
                "a[href*='dashboard']",
                "a[href*='services']",
                "a[href*='web-services']",
                ".dashboard",
                ".services",
                "[data-testid='dashboard']",
                "[data-testid='services']"
            ]
            
            for selector in dashboard_selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Found dashboard/services link: {selector}")
                    element.click()
                    time.sleep(3)
                    break
                except:
                    continue
            
            print("✅ Navigated to dashboard/services section")
            self.status = "dashboard_loaded"
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error navigating to dashboard: {e}")
            return False
    
    def find_and_run_games(self):
        """Find and run games using Render resources"""
        try:
            print("🎮 Looking for games or applications to run...")
            
            # Look for common game-related elements
            game_selectors = [
                "a[href*='game']",
                "a[href*='play']",
                ".game",
                ".play",
                "[data-testid*='game']",
                "[data-testid*='play']"
            ]
            
            games_found = []
            for selector in game_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            text = element.text.strip()
                            if text and len(text) > 0:
                                games_found.append((element, text))
                except:
                    continue
            
            if games_found:
                print(f"🎮 Found {len(games_found)} potential games/applications:")
                for i, (element, text) in enumerate(games_found[:5]):  # Show first 5
                    print(f"   {i+1}. {text}")
                
                # Try to click the first game
                try:
                    first_game = games_found[0][0]
                    print(f"🎮 Attempting to run: {games_found[0][1]}")
                    first_game.click()
                    time.sleep(3)
                    print("✅ Game/application launched!")
                    self.status = "game_running"
                    return True
                except Exception as e:
                    print(f"❌ Error launching game: {e}")
            
            print("⚠️ No games found automatically")
            print("🔧 Please manually navigate to a game or application in Render")
            input("Press Enter after you've opened a game...")
            
            self.status = "game_running"
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error finding games: {e}")
            return False
    
    def bot_cycle(self):
        """Main bot movement cycle for the game"""
        print("🤖 Bot started! Running movement pattern...")
        self.status = "running"
        
        try:
            # Get the body element to send keys to
            body = self.driver.find_element(By.TAG_NAME, "body")
            actions = ActionChains(self.driver)
            
            while self.bot_running:
                try:
                    self.cycle_count += 1
                    print(f"🔄 Cycle {self.cycle_count}")
                    
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
                    self.last_error = str(e)
                    print(f"❌ Error in cycle: {e}")
                    break
            
        except Exception as e:
            self.last_error = str(e)
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

def main():
    print("🎮 Render Gaming Bot")
    print("=" * 40)
    print("This bot will:")
    print("1. Open Render.com website")
    print("2. Help you sign in with Google")
    print("3. Navigate to games/applications")
    print("4. Run games using Render's web resources")
    print("5. Print everything happening to console")
    print("=" * 40)
    
    bot = RenderGamingBot()
    
    try:
        # Setup browser
        if not bot.setup_browser():
            return
        
        # Open Render website
        if not bot.open_render_website():
            return
        
        # Find and click sign in
        if not bot.find_and_click_signin():
            return
        
        # Wait for Google sign in
        if not bot.wait_for_google_signin():
            return
        
        # Navigate to games section
        if not bot.navigate_to_games_section():
            return
        
        # Find and run games
        if not bot.find_and_run_games():
            return
        
        print("\n🎯 GAME SETUP COMPLETE!")
        print("The game should now be running in the browser")
        print("You can now start the bot to play automatically")
        
        input("Press Enter to start the bot...")
        
        # Start bot
        if bot.start_bot():
            print("\n🚀 Bot is now running!")
            print("📝 You can now:")
            print("   - Watch the game in the browser")
            print("   - See all actions in this console")
            print("   - The bot runs using Render's web resources")
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