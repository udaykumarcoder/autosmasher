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
        """Setup Chrome browser for Render.com headless operation"""
        chrome_options = Options()
        
        # Render.com headless setup
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
        
        print("🌐 Starting headless browser on Render...")
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.status = "browser_ready"
            print("✅ Headless browser started on Render!")
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"❌ Error starting browser: {e}")
            return False
    
    def navigate_to_game(self, url="https://smashkarts.io/"):
        """Navigate to the game automatically"""
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
            
            self.status = "game_loaded"
            print("✅ Game loaded!")
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
        """Main bot movement cycle"""
        print("🤖 Bot started on Render! Running movement pattern...")
        self.status = "running"
        self.start_time = time.time()
        
        try:
            # Get the body element to send keys to
            body = self.driver.find_element(By.TAG_NAME, "body")
            actions = ActionChains(self.driver)
            
            while self.bot_running:
                try:
                    self.cycle_count += 1
                    print(f"🔄 Render Cycle {self.cycle_count}")
                    
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
        print("🛑 Bot stopped on Render")
    
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