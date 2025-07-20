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
        
        # Render.com specific options
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Additional options for Render
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        print("🌐 Starting browser on Render...")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.status = "browser_ready"
            print("✅ Browser started on Render!")
            return True
            
        except Exception as e:
            self.last_error = str(e)
            self.status = "error"
            print(f"❌ Error starting browser: {e}")
            return False
    
    def navigate_to_game(self, url="https://smashkarts.io/"):
        """Navigate to the game"""
        if not self.driver:
            self.last_error = "No browser driver available"
            self.status = "error"
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
            self.last_error = str(e)
            self.status = "error"
            print(f"❌ Error loading game: {e}")
            return False
    
    def bot_cycle(self):
        """Main bot movement cycle - SIMPLIFIED FOR WORKING"""
        print("🤖 Bot started! Cart is moving...")
        self.status = "running"
        self.start_time = time.time()
        
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

# Global bot instance
bot = SmashKartsRenderBot()

def start_bot_automatically():
    """Start the bot automatically when triggered"""
    try:
        print("🚀 Starting bot automatically...")
        bot.status = "starting"
        
        # Setup browser
        print("📱 Setting up browser...")
        if not bot.setup_browser():
            bot.status = "error"
            bot.last_error = "Failed to setup browser"
            print("❌ Browser setup failed")
            return False
        
        # Navigate to game
        print("🎮 Navigating to game...")
        if not bot.navigate_to_game():
            bot.status = "error"
            bot.last_error = "Failed to navigate to game"
            print("❌ Game navigation failed")
            return False
        
        # Start bot immediately (no waiting for user)
        print("🤖 Starting bot automation...")
        if not bot.start_bot():
            bot.status = "error"
            bot.last_error = "Failed to start bot automation"
            print("❌ Bot automation failed")
            return False
        
        print("✅ Bot started successfully!")
        return True
        
    except Exception as e:
        bot.status = "error"
        bot.last_error = str(e)
        print(f"❌ Error starting bot: {e}")
        return False

@app.route('/')
def index():
    """Main page - shows Smash Karts embedded"""
    return render_template('game_embedded.html')

@app.route('/control')
def control_panel():
    """Control panel page - can be embedded in iframe"""
    return render_template('control_panel.html')

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
    """API endpoint to signal user is ready - SIMPLIFIED"""
    try:
        # Just return success - no complex waiting logic
        return jsonify({
            'success': True, 
            'message': 'User ready signal received!',
            'status': 'ready'
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

@app.route('/api/debug')
def debug_info():
    """Debug endpoint to see detailed bot information"""
    return jsonify({
        'status': bot.status,
        'bot_running': bot.bot_running,
        'driver_exists': bot.driver is not None,
        'last_error': bot.last_error,
        'cycle_count': bot.cycle_count,
        'start_time': bot.start_time,
        'thread_alive': bot.bot_thread.is_alive() if bot.bot_thread else False
    })

@app.route('/api/test_chrome')
def test_chrome():
    """Test if Chrome is working"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        print("🧪 Testing Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        return jsonify({
            'success': True,
            'message': f'Chrome test successful! Page title: {title}',
            'chrome_working': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Chrome test failed: {str(e)}',
            'chrome_working': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 