


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
print("[*] Checking Pillow version and applying Superman Patch if needed...")
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS
    print("[✅] Superman Patch Applied: ANTIALIAS redirected to LANCZOS.")

from datetime import datetime, timezone, timedelta
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# MoviePy for Video Editing
print("[*] Loading MoviePy modules...")
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import moviepy.audio.fx.all as afx

# ==========================================
# ⚙️ SETTINGS & TOKENS
# ==========================================
print("\n[*] Initializing Settings and Environment Variables...")
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
WAIT_TIME_SECONDS = 300  
print(f"[*] System Timezone set to PKT (+5).")
print(f"[*] Loop Wait Time set to {WAIT_TIME_SECONDS} seconds.")

# Relay Race Timers
START_TIME = time.time()
RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 

# ==========================================
# 🧠 ANTI-SPAM (SPINTAX) GENERATOR
# ==========================================


# ==========================================
# 🧠 ANTI-SPAM (SPINTAX) GENERATOR
# ==========================================
def generate_unique_metadata(clip_number):
    print(f"\n[🧠] Generating Unique Metadata (Spintax) for Clip #{clip_number}...")
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
    
    chosen_title = random.choice(titles)
    chosen_desc = random.choice(descriptions)
    
    # ✂️ THE SMART TRIMMER (Facebook API 255 Char Limit Fix)
    if len(chosen_title) > 250:
        print(f"[⚠️] Title lamba ho gaya tha ({len(chosen_title)} chars). Facebook ke liye trim kar raha hoon...")
        # 247 characters tak rakho aur aagay 3 dots lagao taake total 250 rahay
        chosen_title = chosen_title[:247] + "..."
        
    print(f"  --> Selected Title: {chosen_title}")
    print(f"  --> Emojis Used: {emo}")
    return chosen_title, chosen_desc








# ===============================================

# def generate_unique_metadata(clip_number):
#     print(f"\n[🧠] Generating Unique Metadata (Spintax) for Clip #{clip_number}...")
#     tags_list = HASHTAGS.split()
#     random.shuffle(tags_list)
#     shuffled_tags = " ".join(tags_list)
    
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")
    
#     titles = [
#         f"🔴 LIVE: {MATCH_TITLE} {emo[0]}",
#         f"{emo[1]} EXCLUSIVE HIGHLIGHT: {MATCH_TITLE}",
#         f"⚡ {MATCH_TITLE} - Best Moment {emo[2]}"
#     ]
    
#     descriptions = [
#         f"{MATCH_DESC}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{shuffled_tags}",
#         f"Current match situation! {emo[1]}\n\n{shuffled_tags}\n\n{MATCH_DESC}\n\n🎥 Frame: {clip_number} (Time: {current_time})\nCheck comments for 0 buffering stream link! 👇"
#     ]
    
#     chosen_title = random.choice(titles)
#     chosen_desc = random.choice(descriptions)
    
#     print(f"  --> Selected Title: {chosen_title}")
#     print(f"  --> Emojis Used: {emo}")
#     return chosen_title, chosen_desc

# ==========================================
# 🔄 RELAY RACE (AUTO RESTART)
# ==========================================
def trigger_next_run():
    print("\n" + "="*50)
    print(" ⏰ RELAY RACE: STARTING NEXT GITHUB BOT ⏰")
    print("="*50)
    token = os.environ.get('GH_PAT')
    repo = os.environ.get('GITHUB_REPOSITORY') 
    branch = os.environ.get('GITHUB_REF_NAME', 'main')
    
    print(f"[*] Preparing API Request for Repo: {repo}, Branch: {branch}...")
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
        print("[*] Sending dispatch trigger to GitHub API...")
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 204: 
            print("[✅] SUCCESS! Naya Bot Background Mein Start Ho Gaya Hai!")
        else:
            print(f"[⚠️] Unexpected Status Code: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[💥] Relay Race Failed: {e}")

# ==========================================
# STEP 1: LINK CHURANA
# ==========================================
def get_link_with_headers():
    print(f"\n[🔍] Starting Selenium Webdriver with Proxy...")
    print(f"[*] Target URL: {TARGET_WEBSITE}")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--mute-audio')
    seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

    driver = None; data = None
    try:
        print("[*] Initializing ChromeDriverManager...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
        print("[*] Loading Website...")
        driver.get(TARGET_WEBSITE)
        
        print("[⏳] Waiting 5 seconds for page load and Cloudflare bypass...")
        time.sleep(5)
        
        print("[*] Scanning Network Requests for .m3u8 token...")
        for request in driver.requests:
            if request.response and ".m3u8" in request.url:
                data = {"url": request.url, "ua": request.headers.get('User-Agent', ''), "cookie": request.headers.get('Cookie', ''), "referer": request.headers.get('Referer', TARGET_WEBSITE)}
                print(f"🎉 [BINGO] M3U8 Link Bypassed & Captured!")
                print(f"  --> Found URL: {request.url[:80]}...") # Print half link for safety
                break
                
        if not data:
            print("[⚠️] M3U8 link NOT found in network requests.")
            
    except Exception as e: 
        print(f"[💥] Selenium Error: {e}")
    finally:
        if driver: 
            print("[*] Closing Chrome browser and releasing proxy...")
            driver.quit()
    return data

def calculate_expiry_time(url):
    print("[*] Calculating Link Expiry Time...")
    try:
        params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        exp = int(params.get('expires', params.get('e', [0]))[0])
        if exp: 
            exp_time = datetime.fromtimestamp(exp, PKT)
            print(f"[⏰] Link will expire at: {exp_time.strftime('%I:%M:%S %p PKT')}")
            return exp_time
    except Exception as e: 
        print(f"[-] Could not parse expiry: {e}")
        pass
    
    fallback_time = datetime.now(PKT) + timedelta(hours=2)
    print(f"[⚠️] Setting Fallback Expiry Time: {fallback_time.strftime('%I:%M:%S %p PKT')}")
    return fallback_time

def get_page_id():
    print("[*] Verifying Facebook Access Token...")
    try:
        res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
        if 'id' in res:
            print(f"[+] Connected successfully to Page: {res.get('name', 'Unknown')} (ID: {res['id']})")
            return res.get('id')
        else:
            print(f"[-] API Response error: {res}")
    except Exception as e: 
        print(f"[💥] Token Check Error: {e}")
    return None

# ==========================================
# WORKER 1: 10 SECONDS VIDEO CAPTURE
# ==========================================
def worker_1_capture_video(data, filename, duration=10):
    print(f"\n[🎥 Worker 1] Initiating Stream Capture...")
    print(f"[*] Target File: {filename} | Duration: {duration} seconds")
    headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
    cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
    print("[*] Executing FFmpeg command...")
    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(filename):
        print(f"[✅ Worker 1] Capture successful! File saved.")
        return True
    else:
        print(f"[❌ Worker 1] Capture failed! File not created.")
        return False

# ==========================================
# WORKER 2: VIDEO EDITING (Blur + Merge + Audio)
# ==========================================
def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
    print(f"\n[🎬 Worker 2] Starting Video Editing Engine (MoviePy)...")
    try:
        print(f"[*] Loading Dynamic Clip: {dynamic_vid}")
        dyn_clip = VideoFileClip(dynamic_vid)
        
        print(f"[*] Loading Static Clip: {static_vid}")
        stat_clip = VideoFileClip(static_vid)
        
        print(f"[*] Resizing dynamic clip to match static clip size: {stat_clip.size}")
        dyn_clip = dyn_clip.resize(stat_clip.size)

        def blur(frame):
            return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(30)))

        print("[*] Applying Gaussian Blur (Radius: 20) to dynamic clip...")
        dyn_clip = dyn_clip.fl_image(blur)
        
        print("[*] Concatenating (Merging) dynamic and static clips...")
        merged = concatenate_videoclips([dyn_clip, stat_clip])
        
        print(f"[*] Loading Custom Audio: {custom_audio} and looping to match video duration...")
        audio = AudioFileClip(custom_audio)
        final_audio = afx.audio_loop(audio, duration=merged.duration)
        
        print("[*] Setting final audio track...")
        final_video = merged.set_audio(final_audio)

        print(f"[*] Rendering Final Video to: {output_vid}")
        print("[*] Settings: codec=libx264, audio=aac, preset=ultrafast")
        # Ultra-fast rendering taake GitHub server par load na pare
        final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)

        print("[*] Closing resources and freeing up RAM...")
        dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
        
        print("[✅ Worker 2] Editing Completed Successfully!")
        return True
    except Exception as e:
        print(f"[❌ Worker 2] Edit Error: {e}")
        return False

# ==========================================
# WORKER 3: FACEBOOK UPLOAD & COMMENT WITH IMAGE
# ==========================================
def worker_3_upload(video_path, page_id, clip_number):
    print(f"\n[📤 Worker 3] Preparing Facebook Upload...")
    url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
    title, desc = generate_unique_metadata(clip_number)
    
    payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
    try:
        print(f"[*] Pushing video file '{video_path}' to Graph API...")
        with open(video_path, "rb") as f:
            res = requests.post(url, data=payload, files={"source": f}).json()
            
        if "id" in res:
            print(f"[✅ Worker 3] Video Upload SUCCESS! (Post ID: {res['id']})")
            
            # --- COMMENT WITH IMAGE LOGIC ---
            print("[⏳] Waiting 15 seconds for Facebook to process the video before commenting...")
            time.sleep(15) 
            
            print("[💬 Worker 3] Preparing Comment with Promotional Image and Link...")
            comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
            comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
            comment_img_path = "comment_image.jpeg" 
            
            print(f"[*] Checking for '{comment_img_path}' in directory...")
            if os.path.exists(comment_img_path):
                print(f"[+] Image found! Uploading comment with image...")
                with open(comment_img_path, "rb") as img:
                    comment_res = requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
                if 'id' in comment_res.json():
                    print("[✅ Worker 3] Photo Comment SUCCESS!")
                else:
                    print(f"[⚠️ Worker 3] Comment failed: {comment_res.json()}")
            else:
                print(f"[⚠️] '{comment_img_path}' NOT FOUND! Proceeding with Text-Only comment...")
                requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
                print("[✅ Worker 3] Text Comment Placed.")
            
            return True
        else:
             print(f"[❌ Worker 3] Facebook API Error: {res}")
    except Exception as e:
        print(f"[💥 Worker 3] Upload Crash: {e}")
    return False


# ==========================================
# MAIN LOOP (THE BRAIN)
# ==========================================
def main():
    print("\n" + "="*50)
    print("   🚀 ULTIMATE CLOUD VIDEO BOT STARTED")
    print("="*50)
    
    page_id = get_page_id()
    if not page_id: 
        print("[❌] FATAL: Token invalid! Halting script.")
        return 

    print("[*] Initiating First Link Fetch Cycle...")
    data = get_link_with_headers()
    if not data: 
        print("[❌] FATAL: M3U8 Link nahi mila. Halting script.")
        return 
        
    expiry_dt = calculate_expiry_time(data['url'])
    clip_counter = 1
    next_run_triggered = False
    
    static_video = "main_video.mp4"
    audio_file = "marya_live.mp3"
    
    print("[*] Checking required local assets...")
    if not os.path.exists(static_video) or not os.path.exists(audio_file):
         print(f"[⚠️] WARNING: Missing '{static_video}' or '{audio_file}'. Worker 2 WILL fail!")
    else:
         print(f"[+] Local assets found.")
    
    while True:
        elapsed_time = time.time() - START_TIME
        current_time = datetime.now(PKT)
        time_left_seconds = (expiry_dt - current_time).total_seconds()
        
        print(f"\n" + "-"*40)
        print(f"--- 🔄 Starting Video Cycle #{clip_counter} ---")
        print(f"[-] Bot Uptime: {int(elapsed_time/60)} minutes")
        print(f"[-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
        print("-" * 40)
        
        # 1. Relay Race Check (5h 30m)
        if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
            print("[🚨] Relay Timer Reached (5h 30m). Executing hand-off...")
            trigger_next_run()
            next_run_triggered = True 
            
        # 2. Suicide Check (5h 50m - Stop before GitHub forcefully kills it)
        if elapsed_time > END_TIME_LIMIT:
            print("\n[🛑] MAXIMUM LIFETIME REACHED (5h 50m). Naya bot pichay start ho chuka hai. Main gracefully band ho raha hoon.")
            break
        
        # 3. Link Expiry Check (2 Min pehle)
        if time_left_seconds <= 120:
            print("\n[🚨 ALERT] Link expire hone wala hai. Pausing operations to fetch new link...")
            new_data = get_link_with_headers()
            if new_data:
                data = new_data
                expiry_dt = calculate_expiry_time(data['url'])
                print("[+] Expiry parameters updated successfully.")
            else:
                print("[⚠️] Failed to fetch new link. Retrying in 60 seconds...")
                time.sleep(60); continue 
        
        raw_vid = f"raw_{clip_counter}.mp4"
        final_vid = f"final_{clip_counter}.mp4"
        
        # Action Flow
        if worker_1_capture_video(data, raw_vid, duration=10):
            if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
                worker_3_upload(final_vid, page_id, clip_counter)
        
        # 🧹 GARBAGE COLLECTOR (RAM Hack)
        print("\n[🧹 Cleanup Engine Started]")
        if os.path.exists(raw_vid): 
            os.remove(raw_vid)
            print(f"  [-] Deleted: {raw_vid}")
        if os.path.exists(final_vid): 
            os.remove(final_vid)
            print(f"  [-] Deleted: {final_vid}")
        print("[🧹] Temporary videos hard-drive se ura di gayi hain. RAM freed.")
            
        clip_counter += 1
        print(f"\n[⏳] Cycle Complete. Agli video ke liye {WAIT_TIME_SECONDS} seconds wait kar raha hoon...")
        time.sleep(WAIT_TIME_SECONDS)

if __name__ == "__main__":
    main()















# ====================== ============================


# import os
# import time
# import subprocess
# import urllib.parse
# import traceback
# import requests
# import random 
# import numpy as np
# from PIL import Image, ImageFilter
# # ==========================================
# # 🦸‍♂️ THE SUPERMAN PATCH (For Pillow 10+)
# # ==========================================
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
# FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

# MATCH_TITLE = os.environ.get('MATCH_TITLE', 'Live Match').strip()
# MATCH_DESC = os.environ.get('MATCH_DESC', 'Watch Live Now').strip()
# HASHTAGS = os.environ.get('HASHTAGS', '#Live').strip()

# # Proxy Settings
# PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
# PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
# PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
# PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
# PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

# PKT = timezone(timedelta(hours=5))
# WAIT_TIME_SECONDS = 300  # Har 5 minute baad nayi 10-sec video banayega (Taa ke Facebook block na kare)

# # Relay Race Timers (5.5 Hours limit)
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) # 5h 30m baad naya bot
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) # 5h 50m par khud mar jayega

# # ==========================================
# # 🧠 ANTI-SPAM (SPINTAX) GENERATOR
# # ==========================================
# def generate_unique_metadata(clip_number):
#     tags_list = HASHTAGS.split()
#     random.shuffle(tags_list)
#     shuffled_tags = " ".join(tags_list)
    
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")
    
#     titles = [
#         f"🔴 LIVE: {MATCH_TITLE} {emo[0]}",
#         f"{emo[1]} EXCLUSIVE HIGHLIGHT: {MATCH_TITLE}",
#         f"⚡ {MATCH_TITLE} - Best Moment {emo[2]}"
#     ]
    
#     descriptions = [
#         f"{MATCH_DESC}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{shuffled_tags}",
#         f"Current match situation! {emo[1]}\n\n{shuffled_tags}\n\n{MATCH_DESC}\n\n🎥 Frame: {clip_number} (Time: {current_time})\nCheck comments for 0 buffering stream link! 👇"
#     ]
    
#     return random.choice(titles), random.choice(descriptions)

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n" + "="*50)
#     print(" ⏰ RELAY RACE: STARTING NEXT GITHUB BOT ⏰")
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
    
#     url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
#     headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
#     data = {
#         "ref": branch,
#         "inputs": {
#             "target_url": TARGET_WEBSITE, "match_title": MATCH_TITLE,
#             "match_desc": MATCH_DESC, "hashtags": HASHTAGS,
#             "proxy_ip": PROXY_IP, "proxy_port": PROXY_PORT,
#             "proxy_user": PROXY_USER, "proxy_pass": PROXY_PASS
#         }
#     }
#     try:
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204: print("[✅] Naya Bot Background Mein Start Ho Gaya!")
#     except Exception as e:
#         print(f"[💥] Relay Race Failed: {e}")

# # ==========================================
# # STEP 1: LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print(f"\n[🔍] Proxy lag kar Target URL check ho raha hai...")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
#         driver.get(TARGET_WEBSITE)
#         time.sleep(5)
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 data = {"url": request.url, "ua": request.headers.get('User-Agent', ''), "cookie": request.headers.get('Cookie', ''), "referer": request.headers.get('Referer', TARGET_WEBSITE)}
#                 print(f"🎉 [BINGO] M3U8 Link Bypassed & Captured!")
#                 break
#     except: pass
#     finally:
#         if driver: driver.quit()
#     return data

# def calculate_expiry_time(url):
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: return datetime.fromtimestamp(exp, PKT)
#     except: pass
#     return datetime.now(PKT) + timedelta(hours=2)

# def get_page_id():
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id"}).json()
#         return res.get('id')
#     except: return None

# # ==========================================
# # WORKER 1: 10 SECONDS VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"[🎥 Worker 1] Stream se {duration} sec ki video record ho rahi hai...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     return os.path.exists(filename)

# # ==========================================
# # WORKER 2: VIDEO EDITING (Blur + Merge + Audio)
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"[🎬 Worker 2] Video Edit ho rahi hai (Blur + Custom Audio)...")
#     try:
#         dyn_clip = VideoFileClip(dynamic_vid)
#         stat_clip = VideoFileClip(static_vid)
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame):
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(30)))

#         dyn_clip = dyn_clip.fl_image(blur)
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
#         final_video = merged.set_audio(final_audio)

#         # Ultra-fast rendering taake GitHub server par load na pare
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)

#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 2] Edit Error: {e}")
#         return False

# # ==========================================
# # WORKER 3: FACEBOOK UPLOAD & COMMENT
# # ==========================================

# # ==========================================
# # WORKER 3: FACEBOOK UPLOAD & COMMENT WITH IMAGE
# # ==========================================
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
            
#             # --- COMMENT WITH IMAGE LOGIC ---
#             time.sleep(15) # Video processing ke liye thora aur wait (15 sec)
#             print("[💬 Worker 3] Comment mein Photo aur Link upload ho raha hai...")
            
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
#             comment_img_path = "comment_image.jpeg" # Repo mein mojood static image
            
#             # Check karega agar repo mein picture hai, toh picture ke sath comment karega
#             if os.path.exists(comment_img_path):
#                 with open(comment_img_path, "rb") as img:
#                     requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 print("[✅ Worker 3] Photo wala Comment SUCCESS!")
#             else:
#                 # Agar ghalti se picture upload nahi ki, toh error nahi dega, sirf text post kar dega
#                 print("[⚠️] comment_image.jpeg nahi mili! Sirf text comment kar raha hoon...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
            
#             return True
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Error: {e}")
#     return False





# # ========================================

# # def worker_3_upload(video_path, page_id, clip_number):
# #     print(f"[📤 Worker 3] Facebook par Video post ki ja rahi hai...")
# #     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
# #     title, desc = generate_unique_metadata(clip_number)
    
# #     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
# #     try:
# #         with open(video_path, "rb") as f:
# #             res = requests.post(url, data=payload, files={"source": f}).json()
# #         if "id" in res:
# #             print(f"[✅ Worker 3] Video Upload SUCCESS! (ID: {res['id']})")
            
# #             # Commenting
# #             time.sleep(10) # Video process hone ka chota sa wait
# #             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
# #             requests.post(comment_url, data={"message": f"📺 Watch Full Match Here: https://bulbul4u-live.xyz", "access_token": FB_ACCESS_TOKEN})
# #             print("[💬 Worker 3] Comment Placed!")
# #             return True
# #     except Exception as e:
# #         print(f"[💥 Worker 3] Upload Error: {e}")
# #     return False

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("========================================")
#     print("   🚀 ULTIMATE CLOUD VIDEO BOT STARTED")
#     print("========================================")
    
#     page_id = get_page_id()
#     if not page_id: return print("[❌] Token invalid!")

#     data = get_link_with_headers()
#     if not data: return print("[❌] Link nahi mila.")
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         # 1. Relay Race Check (5h 30m)
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             trigger_next_run()
#             next_run_triggered = True 
            
#         # 2. Suicide Check (5h 50m - Stop before GitHub forcefully kills it)
#         if elapsed_time > END_TIME_LIMIT:
#             print("[🛑] Time khatam! Naya bot pichay start ho chuka hai. Main band ho raha hoon.")
#             break
        
#         # 3. Link Expiry Check (2 Min pehle)
#         if time_left_seconds <= 120:
#             print("[🚨 ALERT] Link expire hone wala hai. Naya link fetch ho raha hai...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#             else:
#                 time.sleep(60); continue 
        
#         print(f"\n--- Video Cycle #{clip_counter} ---")
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # Action Flow
#         if worker_1_capture_video(data, raw_vid, duration=10):
#             if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                 worker_3_upload(final_vid, page_id, clip_counter)
        
#         # 🧹 GARBAGE COLLECTOR (RAM Hack)
#         if os.path.exists(raw_vid): os.remove(raw_vid)
#         if os.path.exists(final_vid): os.remove(final_vid)
#         print("[🧹 Cleanup] Temporary videos hard-drive se ura di gayi hain.")
            
#         clip_counter += 1
#         print(f"[⏳] Agli video ke liye {WAIT_TIME_SECONDS} seconds wait kar raha hoon...")
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()
