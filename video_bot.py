import os
import time
import subprocess
import urllib.parse
import traceback
import requests
import random 
import numpy as np
from PIL import Image, ImageFilter
# ==========================================
# 🦸‍♂️ THE SUPERMAN PATCH (For Pillow 10+)
# ==========================================
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from datetime import datetime, timezone, timedelta
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# MoviePy for Video Editing
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import moviepy.audio.fx.all as afx

# ==========================================
# ⚙️ SETTINGS & TOKENS
# ==========================================
TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

MATCH_TITLE = os.environ.get('MATCH_TITLE', 'Live Match').strip()
MATCH_DESC = os.environ.get('MATCH_DESC', 'Watch Live Now').strip()
HASHTAGS = os.environ.get('HASHTAGS', '#Live').strip()

# Proxy Settings
PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

PKT = timezone(timedelta(hours=5))
WAIT_TIME_SECONDS = 300  # Har 5 minute baad nayi 10-sec video banayega (Taa ke Facebook block na kare)

# Relay Race Timers (5.5 Hours limit)
START_TIME = time.time()
RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) # 5h 30m baad naya bot
END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) # 5h 50m par khud mar jayega

# ==========================================
# 🧠 ANTI-SPAM (SPINTAX) GENERATOR
# ==========================================
def generate_unique_metadata(clip_number):
    tags_list = HASHTAGS.split()
    random.shuffle(tags_list)
    shuffled_tags = " ".join(tags_list)
    
    emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
    emo = random.sample(emojis, 3) 
    current_time = datetime.now(PKT).strftime("%I:%M %p")
    
    titles = [
        f"🔴 LIVE: {MATCH_TITLE} {emo[0]}",
        f"{emo[1]} EXCLUSIVE HIGHLIGHT: {MATCH_TITLE}",
        f"⚡ {MATCH_TITLE} - Best Moment {emo[2]}"
    ]
    
    descriptions = [
        f"{MATCH_DESC}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{shuffled_tags}",
        f"Current match situation! {emo[1]}\n\n{shuffled_tags}\n\n{MATCH_DESC}\n\n🎥 Frame: {clip_number} (Time: {current_time})\nCheck comments for 0 buffering stream link! 👇"
    ]
    
    return random.choice(titles), random.choice(descriptions)

# ==========================================
# 🔄 RELAY RACE (AUTO RESTART)
# ==========================================
def trigger_next_run():
    print("\n" + "="*50)
    print(" ⏰ RELAY RACE: STARTING NEXT GITHUB BOT ⏰")
    token = os.environ.get('GH_PAT')
    repo = os.environ.get('GITHUB_REPOSITORY') 
    branch = os.environ.get('GITHUB_REF_NAME', 'main')
    
    url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
    data = {
        "ref": branch,
        "inputs": {
            "target_url": TARGET_WEBSITE, "match_title": MATCH_TITLE,
            "match_desc": MATCH_DESC, "hashtags": HASHTAGS,
            "proxy_ip": PROXY_IP, "proxy_port": PROXY_PORT,
            "proxy_user": PROXY_USER, "proxy_pass": PROXY_PASS
        }
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 204: print("[✅] Naya Bot Background Mein Start Ho Gaya!")
    except Exception as e:
        print(f"[💥] Relay Race Failed: {e}")

# ==========================================
# STEP 1: LINK CHURANA
# ==========================================
def get_link_with_headers():
    print(f"\n[🔍] Proxy lag kar Target URL check ho raha hai...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--mute-audio')
    seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

    driver = None; data = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        driver.get(TARGET_WEBSITE)
        time.sleep(5)
        for request in driver.requests:
            if request.response and ".m3u8" in request.url:
                data = {"url": request.url, "ua": request.headers.get('User-Agent', ''), "cookie": request.headers.get('Cookie', ''), "referer": request.headers.get('Referer', TARGET_WEBSITE)}
                print(f"🎉 [BINGO] M3U8 Link Bypassed & Captured!")
                break
    except: pass
    finally:
        if driver: driver.quit()
    return data

def calculate_expiry_time(url):
    try:
        params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        exp = int(params.get('expires', params.get('e', [0]))[0])
        if exp: return datetime.fromtimestamp(exp, PKT)
    except: pass
    return datetime.now(PKT) + timedelta(hours=2)

def get_page_id():
    try:
        res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id"}).json()
        return res.get('id')
    except: return None

# ==========================================
# WORKER 1: 10 SECONDS VIDEO CAPTURE
# ==========================================
def worker_1_capture_video(data, filename, duration=10):
    print(f"[🎥 Worker 1] Stream se {duration} sec ki video record ho rahi hai...")
    headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
    cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.exists(filename)

# ==========================================
# WORKER 2: VIDEO EDITING (Blur + Merge + Audio)
# ==========================================
def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
    print(f"[🎬 Worker 2] Video Edit ho rahi hai (Blur + Custom Audio)...")
    try:
        dyn_clip = VideoFileClip(dynamic_vid)
        stat_clip = VideoFileClip(static_vid)
        dyn_clip = dyn_clip.resize(stat_clip.size)

        def blur(frame):
            return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(30)))

        dyn_clip = dyn_clip.fl_image(blur)
        merged = concatenate_videoclips([dyn_clip, stat_clip])
        
        audio = AudioFileClip(custom_audio)
        final_audio = afx.audio_loop(audio, duration=merged.duration)
        final_video = merged.set_audio(final_audio)

        # Ultra-fast rendering taake GitHub server par load na pare
        final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)

        dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
        return True
    except Exception as e:
        print(f"[❌ Worker 2] Edit Error: {e}")
        return False

# ==========================================
# WORKER 3: FACEBOOK UPLOAD & COMMENT
# ==========================================

# ==========================================
# WORKER 3: FACEBOOK UPLOAD & COMMENT WITH IMAGE
# ==========================================
def worker_3_upload(video_path, page_id, clip_number):
    print(f"[📤 Worker 3] Facebook par Video post ki ja rahi hai...")
    url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
    title, desc = generate_unique_metadata(clip_number)
    
    payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
    try:
        with open(video_path, "rb") as f:
            res = requests.post(url, data=payload, files={"source": f}).json()
        if "id" in res:
            print(f"[✅ Worker 3] Video Upload SUCCESS! (ID: {res['id']})")
            
            # --- COMMENT WITH IMAGE LOGIC ---
            time.sleep(15) # Video processing ke liye thora aur wait (15 sec)
            print("[💬 Worker 3] Comment mein Photo aur Link upload ho raha hai...")
            
            comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
            comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
            comment_img_path = "comment_image.jpeg" # Repo mein mojood static image
            
            # Check karega agar repo mein picture hai, toh picture ke sath comment karega
            if os.path.exists(comment_img_path):
                with open(comment_img_path, "rb") as img:
                    requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
                print("[✅ Worker 3] Photo wala Comment SUCCESS!")
            else:
                # Agar ghalti se picture upload nahi ki, toh error nahi dega, sirf text post kar dega
                print("[⚠️] comment_image.jpeg nahi mili! Sirf text comment kar raha hoon...")
                requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
            
            return True
    except Exception as e:
        print(f"[💥 Worker 3] Upload Error: {e}")
    return False





# ========================================

# def worker_3_upload(video_path, page_id, clip_number):
#     print(f"[📤 Worker 3] Facebook par Video post ki ja rahi hai...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     title, desc = generate_unique_metadata(clip_number)
    
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     try:
#         with open(video_path, "rb") as f:
#             res = requests.post(url, data=payload, files={"source": f}).json()
#         if "id" in res:
#             print(f"[✅ Worker 3] Video Upload SUCCESS! (ID: {res['id']})")
            
#             # Commenting
#             time.sleep(10) # Video process hone ka chota sa wait
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             requests.post(comment_url, data={"message": f"📺 Watch Full Match Here: https://bulbul4u-live.xyz", "access_token": FB_ACCESS_TOKEN})
#             print("[💬 Worker 3] Comment Placed!")
#             return True
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Error: {e}")
#     return False

# ==========================================
# MAIN LOOP (THE BRAIN)
# ==========================================
def main():
    print("========================================")
    print("   🚀 ULTIMATE CLOUD VIDEO BOT STARTED")
    print("========================================")
    
    page_id = get_page_id()
    if not page_id: return print("[❌] Token invalid!")

    data = get_link_with_headers()
    if not data: return print("[❌] Link nahi mila.")
        
    expiry_dt = calculate_expiry_time(data['url'])
    clip_counter = 1
    next_run_triggered = False
    
    static_video = "main_video.mp4"
    audio_file = "marya_live.mp3"
    
    while True:
        elapsed_time = time.time() - START_TIME
        current_time = datetime.now(PKT)
        time_left_seconds = (expiry_dt - current_time).total_seconds()
        
        # 1. Relay Race Check (5h 30m)
        if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
            trigger_next_run()
            next_run_triggered = True 
            
        # 2. Suicide Check (5h 50m - Stop before GitHub forcefully kills it)
        if elapsed_time > END_TIME_LIMIT:
            print("[🛑] Time khatam! Naya bot pichay start ho chuka hai. Main band ho raha hoon.")
            break
        
        # 3. Link Expiry Check (2 Min pehle)
        if time_left_seconds <= 120:
            print("[🚨 ALERT] Link expire hone wala hai. Naya link fetch ho raha hai...")
            new_data = get_link_with_headers()
            if new_data:
                data = new_data
                expiry_dt = calculate_expiry_time(data['url'])
            else:
                time.sleep(60); continue 
        
        print(f"\n--- Video Cycle #{clip_counter} ---")
        raw_vid = f"raw_{clip_counter}.mp4"
        final_vid = f"final_{clip_counter}.mp4"
        
        # Action Flow
        if worker_1_capture_video(data, raw_vid, duration=10):
            if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
                worker_3_upload(final_vid, page_id, clip_counter)
        
        # 🧹 GARBAGE COLLECTOR (RAM Hack)
        if os.path.exists(raw_vid): os.remove(raw_vid)
        if os.path.exists(final_vid): os.remove(final_vid)
        print("[🧹 Cleanup] Temporary videos hard-drive se ura di gayi hain.")
            
        clip_counter += 1
        print(f"[⏳] Agli video ke liye {WAIT_TIME_SECONDS} seconds wait kar raha hoon...")
        time.sleep(WAIT_TIME_SECONDS)

if __name__ == "__main__":
    main()
