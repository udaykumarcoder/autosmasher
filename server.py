import os
import time
import threading
import json
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

class SmashKartsRenderBot:
    def __init__(self):
        self.driver = None
        self.bot_running = False
        self.bot_thread = None
        self.status = "idle"
        self.cycle_count = 0
        self.last_error = None
        self.start_time = None
        
    def setup_browser(self):
        """Setup Chrome browser for Render.com operation"""
        chrome_options = Options()
        
        # Create a separate profile for the bot to avoid conflicts
        temp_profile = os.path.join(os.getcwd(), "bot_profile")
        chrome_options.add_argument(f"--user-data-dir={temp_profile}")
        
        # Anti-detection measures
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Performance and stealth options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        
        # Use a different port to avoid conflicts
        chrome_options.add_argument("--remote-debugging-port=9223")
        
        # For Render.com, we need headless but with better compatibility
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        
        print("🌐 Starting browser on Render...")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.status = "browser_ready"
            print("✅ Browser started on Render!")
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error starting browser: {e}")
            return False
    
    def navigate_to_game(self, url="https://smashkarts.io/"):
        """Navigate to game and prepare for bot"""
        if not self.driver:
            return False
            
        try:
            print(f"🎮 Opening {url}...")
            self.driver.get(url)
            time.sleep(5)
            
            # Focus on game - try different selectors like your working code
            try:
                for selector in ["canvas", "#game", ".game", "iframe", "body"]:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        element.click()
                        print(f"✅ Focused on {selector}")
                        break
                    except:
                        continue
            except:
                print("⚠️ Could not focus game, but continuing...")
            
            self.status = "game_loaded"
            print("✅ Game loaded and focused!")
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error loading game: {e}")
            return False
    
    def wait_for_user_ready(self):
        """Wait for user to be ready in the game"""
        try:
            print("⏳ Waiting for user to be ready in game...")
            self.status = "waiting_for_user"
            
            # Wait for user to signal they're ready
            # This will be triggered by the web interface
            while self.status == "waiting_for_user":
                time.sleep(1)
            
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error waiting for user: {e}")
            return False
    
    def bot_cycle(self):
        """Main bot movement cycle using your proven approach"""
        print("🤖 Bot started! Running movement pattern...")
        self.status = "running"
        self.start_time = time.time()
        
        # Switch to iframe context first and focus
        try:
            iframe = self.driver.find_element(By.TAG_NAME, "iframe")
            self.driver.switch_to.frame(iframe)
            print("✅ Switched to iframe context")
            
            # Focus on the iframe content
            self._focus_iframe()
            time.sleep(1)
            
            # Get the body element inside iframe
            body = self.driver.find_element(By.TAG_NAME, "body")
            actions = ActionChains(self.driver)
            print("✅ Got iframe body element and ActionChains ready")
        except Exception as e:
            print(f"❌ Error switching to iframe: {e}")
            # Fallback to main page
            try:
                self.driver.switch_to.default_content()
                body = self.driver.find_element(By.TAG_NAME, "body")
                actions = ActionChains(self.driver)
                print("✅ Got main page body element and ActionChains ready")
            except Exception as e2:
                print(f"❌ Error getting body element: {e2}")
                return
        
        try:
            while self.bot_running:
                try:
                    self.cycle_count += 1
                    print(f"🔄 Cycle {self.cycle_count}")
                    
                    # 1. Hold Up for 5 seconds
                    try:
                        actions.key_down(Keys.ARROW_UP).perform()
                    except:
                        self._send_key_to_iframe('ArrowUp', 'keydown')
                    if not self._sleep_check(5, "Up"):
                        break
                    
                    # 2. Up+Left for 5 seconds
                    try:
                        actions.key_down(Keys.ARROW_LEFT).perform()
                    except:
                        self._send_key_to_iframe('ArrowLeft', 'keydown')
                    if not self._sleep_check(5, "Up+Left"):
                        break
                    try:
                        actions.key_up(Keys.ARROW_LEFT).perform()
                    except:
                        self._send_key_to_iframe('ArrowLeft', 'keyup')
                    
                    # 3. Up+Right for 5 seconds
                    try:
                        actions.key_down(Keys.ARROW_RIGHT).perform()
                    except:
                        self._send_key_to_iframe('ArrowRight', 'keydown')
                    if not self._sleep_check(5, "Up+Right"):
                        break
                    try:
                        actions.key_up(Keys.ARROW_RIGHT).perform()
                    except:
                        self._send_key_to_iframe('ArrowRight', 'keyup')
                    
                    # 4. Space
                    try:
                        actions.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                    except:
                        self._send_key_to_iframe('Space', 'keydown')
                        self._send_key_to_iframe('Space', 'keyup')
                    if not self._sleep_check(0.5, "Space"):
                        break
                    
                    # 5. Down for 5 seconds
                    try:
                        actions.key_up(Keys.ARROW_UP).perform()
                        actions.key_down(Keys.ARROW_DOWN).perform()
                    except:
                        self._send_key_to_iframe('ArrowUp', 'keyup')
                        self._send_key_to_iframe('ArrowDown', 'keydown')
                    if not self._sleep_check(5, "Down"):
                        break
                    
                    # 6. Down+Left for 5 seconds
                    try:
                        actions.key_down(Keys.ARROW_LEFT).perform()
                    except:
                        self._send_key_to_iframe('ArrowLeft', 'keydown')
                    if not self._sleep_check(5, "Down+Left"):
                        break
                    try:
                        actions.key_up(Keys.ARROW_LEFT).perform()
                    except:
                        self._send_key_to_iframe('ArrowLeft', 'keyup')
                    
                    # 7. Down+Right for 5 seconds
                    try:
                        actions.key_down(Keys.ARROW_RIGHT).perform()
                    except:
                        self._send_key_to_iframe('ArrowRight', 'keydown')
                    if not self._sleep_check(5, "Down+Right"):
                        break
                    try:
                        actions.key_up(Keys.ARROW_RIGHT).perform()
                    except:
                        self._send_key_to_iframe('ArrowRight', 'keyup')
                    
                    # 8. Space
                    try:
                        actions.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                    except:
                        self._send_key_to_iframe('Space', 'keydown')
                        self._send_key_to_iframe('Space', 'keyup')
                    
                    # Reset for next cycle
                    try:
                        actions.key_up(Keys.ARROW_DOWN).perform()
                    except:
                        self._send_key_to_iframe('ArrowDown', 'keyup')
                    
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
    
    def _focus_iframe(self):
        """Focus on the iframe content"""
        try:
            # Switch to iframe
            iframe = self.driver.find_element(By.TAG_NAME, "iframe")
            self.driver.switch_to.frame(iframe)
            
            # Focus on the iframe content
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.click()
            print("✅ Focused on iframe content")
            
        except Exception as e:
            print(f"⚠️ Error focusing iframe: {e}")
            # Switch back to main content
            try:
                self.driver.switch_to.default_content()
            except:
                pass
    
    def _send_key_to_iframe(self, key, action_type="keydown"):
        """Send keyboard event directly to iframe using JavaScript"""
        try:
            js_code = f"""
            var event = new KeyboardEvent('{action_type}', {{
                key: '{key}',
                code: '{key}',
                keyCode: {self._get_key_code(key)},
                which: {self._get_key_code(key)},
                bubbles: true,
                cancelable: true
            }});
            document.dispatchEvent(event);
            """
            self.driver.execute_script(js_code)
            print(f"✅ Sent {action_type} event for {key} via JavaScript")
        except Exception as e:
            print(f"❌ Error sending JavaScript key event: {e}")
    
    def _get_key_code(self, key):
        """Get key code for JavaScript events"""
        key_codes = {
            'ArrowUp': 38,
            'ArrowDown': 40,
            'ArrowLeft': 37,
            'ArrowRight': 39,
            'Space': 32
        }
        return key_codes.get(key, 0)
    
    def _sleep_check(self, duration, action):
        """Sleep while checking if bot should stop"""
        end_time = time.time() + duration
        while time.time() < end_time:
            if not self.bot_running:
                return False
            time.sleep(0.1)
        return True
    
    def _release_all_keys(self):
        """Release all keys using ActionChains (like your working code)"""
        try:
            actions = ActionChains(self.driver)
            for key in [Keys.ARROW_UP, Keys.ARROW_DOWN, Keys.ARROW_LEFT, Keys.ARROW_RIGHT, Keys.SPACE]:
                actions.key_up(key)
            actions.perform()
            print("✅ Released all keys")
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

# Global bot instance
bot = SmashKartsRenderBot()

def start_bot_automatically():
    """Start the bot automatically when triggered"""
    try:
        print("🚀 Starting bot automatically...")
        
        # Setup browser
        if not bot.setup_browser():
            return False
        
        # Navigate to game
        if not bot.navigate_to_game():
            return False
        
        # Wait for user to be ready
        if not bot.wait_for_user_ready():
            return False
        
        # Start bot
        if not bot.start_bot():
            return False
        
        print("✅ Bot started successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return False

@app.route('/')
def index():
    """Main page - shows Smash Karts embedded"""
    return render_template('game_embedded.html')

@app.route('/api/start_bot', methods=['POST'])
def start_bot():
    """API endpoint to start the bot"""
    try:
        if bot.status == "idle":
            # Start bot in background thread
            threading.Thread(target=start_bot_automatically, daemon=True).start()
            return jsonify({
                'success': True, 
                'message': 'Bot starting in background...',
                'status': 'starting'
            })
        else:
            return jsonify({
                'success': False, 
                'message': f'Bot is already {bot.status}',
                'status': bot.status
            })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': str(e),
            'status': 'error'
        })

@app.route('/api/user_ready', methods=['POST'])
def user_ready():
    """API endpoint to signal user is ready"""
    try:
        if bot.status == "waiting_for_user":
            bot.status = "user_ready"
            return jsonify({
                'success': True, 
                'message': 'User ready! Starting bot...',
                'status': 'user_ready'
            })
        else:
            return jsonify({
                'success': False, 
                'message': f'Bot is not waiting for user (status: {bot.status})',
                'status': bot.status
            })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': str(e),
            'status': 'error'
        })

@app.route('/api/status')
def get_status():
    """Get bot status"""
    uptime = 0
    if bot.start_time:
        uptime = int(time.time() - bot.start_time)
    
    return jsonify({
        'status': bot.status,
        'cycle_count': bot.cycle_count,
        'uptime': uptime,
        'error': bot.last_error,
        'bot_running': bot.bot_running
    })

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    try:
        if bot.stop_bot():
            return jsonify({'success': True, 'message': 'Bot stopped!'})
        else:
            return jsonify({'success': False, 'message': 'Bot was not running'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/cleanup', methods=['POST'])
def cleanup_bot():
    """Cleanup the bot"""
    try:
        bot.cleanup()
        return jsonify({'success': True, 'message': 'Bot cleaned up!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 