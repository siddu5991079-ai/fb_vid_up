




# ============= thsi code very good work, yeh comment bey karta hai and thumbnail bey successfully apply akrta hai lekin maney thumbnail waley ko commnet kya hai qunky yeh 2 aab mei try karta hu k yeh "FB-Hybrid-Cloud_2" iss me karo , iss ko isliye comment kya hai qunky yeh wallah srf iss repo mei joo image hai "thumbnail.png" name se srf usko apply kar hai . mei dynamic bana chta hu ====================== 



import os
import time
import requests
from datetime import datetime, timezone

print("\n" + "="*50)
print("   🚀 FACEBOOK PAGE MONITOR (THUMBNAIL + COMMENT EDITION)")
print("="*50)

# ==========================================
# ⚙️ SETTINGS & TOKENS
# ==========================================
COMMENT_TEXT = "📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
COMMENT_IMG_PATH = "comment_image.jpeg"
VIDEO_THUMBNAIL_PATH = "thumbnail.png" # 🖼️ Yeh video ke cover par lagegi

START_TIME = time.time()
END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60)  # 5 hours 50 mins limit
WAIT_TIME = 300  # 5 Minutes wait between checks

# 🎯 USER SELECTION PULL KARNA
TARGET_PAGE = os.environ.get('TARGET_PAGE', 'Primary Page')
CUSTOM_TOKEN = os.environ.get('CUSTOM_TOKEN', '').strip()

# 🗄️ TOKENS DICTIONARY
AVAILABLE_TOKENS = {
    'Primary Page': os.environ.get('PRIMARY_TOKEN', '').strip(),
    'Secondary Page': os.environ.get('SECONDARY_TOKEN', '').strip(),
    'Page 3': os.environ.get('TOKEN_3', '').strip(),
    'Page 4': os.environ.get('TOKEN_4', '').strip(),
}

# 🧠 SMART SELECTION LOGIC
ACTIVE_TOKEN = ""
if TARGET_PAGE == 'Custom Token (Below)':
    ACTIVE_TOKEN = CUSTOM_TOKEN
    print(f"[⚙️] Mode: Custom Token Provide kiya gaya hai.")
else:
    ACTIVE_TOKEN = AVAILABLE_TOKENS.get(TARGET_PAGE, "")
    print(f"[⚙️] Mode: '{TARGET_PAGE}' Select kiya gaya hai.")

# ==========================================
# 🛠️ CORE FUNCTIONS
# ==========================================
def get_page_info(token):
    try:
        res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": token, "fields": "id,name"}).json()
        if 'id' in res: return res['id'], res['name']
    except Exception as e:
        print(f"  [❌] Token verification failed: {e}")
    return None, None

def post_comment(post_id, token):
    print(f"  [>] Posting promotional comment on {post_id}...")
    comment_url = f"https://graph.facebook.com/v18.0/{post_id}/comments"
    
    try:
        if os.path.exists(COMMENT_IMG_PATH):
            print("  [📸] Comment Image found! Posting Comment WITH Photo...")
            with open(COMMENT_IMG_PATH, "rb") as img:
                res = requests.post(comment_url, data={"message": COMMENT_TEXT, "access_token": token}, files={"source": img}).json()
        else:
            print("  [📝] No comment image found. Posting TEXT-ONLY Comment...")
            res = requests.post(comment_url, data={"message": COMMENT_TEXT, "access_token": token}).json()

        if 'id' in res:
            print(f"  [✅] Comment Placed Successfully! Comment ID: {res['id']}")
        else:
            print(f"  [❌] Error posting comment: {res}")
    except Exception as e:
        print(f"  [❌] Crash while posting comment: {e}")

# 🚀 FORCE THUMBNAIL FUNCTION (REEL & UPLOADED VIDEO FIX)
# def update_video_thumbnail(post_id, token):
#     if not os.path.exists(VIDEO_THUMBNAIL_PATH):
#         print(f"  [⚠️] '{VIDEO_THUMBNAIL_PATH}' repo mein nahi mili. Thumbnail update skip kar raha hoon.")
#         return

#     print(f"  [🖼️] Checking if post contains a video to update its thumbnail...")
#     try:
#         attach_url = f"https://graph.facebook.com/v18.0/{post_id}?fields=attachments&access_token={token}"
#         attach_data = requests.get(attach_url).json()
        
#         video_id = None
#         attachments = attach_data.get('attachments', {}).get('data', [])
        
#         if attachments and 'target' in attachments[0] and 'id' in attachments[0]['target']:
#             video_id = attachments[0]['target']['id']
            
#         if video_id:
#             print(f"  [>] Video ID found: {video_id}. Uploading new Thumbnail and forcing it as default...")
            
#             with open(VIDEO_THUMBNAIL_PATH, "rb") as thumb_file:
#                 # 🛠️ THE FIX: Uploaded Videos aur Reels ke liye direct '/thumbnails' par hit karna zaroori hai
#                 files = {"source": ("thumbnail.png", thumb_file, "image/png")}
                
#                 # is_preferred=true forces FB to set this specific upload as the cover
#                 res = requests.post(
#                     f"https://graph.facebook.com/v18.0/{video_id}/thumbnails", 
#                     data={"access_token": token, "is_preferred": "true"}, 
#                     files=files
#                 ).json()
                
#             if res.get('success'):
#                 print("  [✅] Video Thumbnail (Cover Photo) Updated Successfully!")
#             else:
#                 print(f"  [❌] Thumbnail update failed: {res}")
#         else:
#             print("  [⚠️] Koi Video attach nahi mili (Yeh shayad text/photo post hai).")
            
#     except Exception as e:
#         print(f"  [❌] Crash while updating thumbnail: {e}")

def check_and_comment(token):
    page_id, page_name = get_page_info(token)
    if not page_id:
        print(f"  [❌] Invalid Token! Could not authenticate with Facebook API.")
        return

    print(f"\n[🔍] Monitoring Page: {page_name} (ID: {page_id})")
    
    try:
        posts_url = f"https://graph.facebook.com/v18.0/{page_id}/posts?fields=id,created_time&access_token={token}"
        posts_data = requests.get(posts_url).json()
        
        if 'data' not in posts_data:
            print(f"  [⚠️] Could not fetch posts. API Response: {posts_data}")
            return
            
        posts = posts_data['data']
        now_utc = datetime.now(timezone.utc)
        
        recent_posts = []
        for post in posts:
            post_time = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S%z")
            age_seconds = (now_utc - post_time).total_seconds()
            if age_seconds <= 3600:
                recent_posts.append(post)

        print(f"  [📊] Found {len(recent_posts)} post(s) created in the last 1 hour.")

        for post in recent_posts:
            post_id = post['id']
            print(f"  [👉] Checking Post ID: {post_id}")
            
            comments_url = f"https://graph.facebook.com/v18.0/{post_id}/comments?fields=from&access_token={token}"
            comments_data = requests.get(comments_url).json()
            
            already_commented = False
            if 'data' in comments_data:
                for comment in comments_data['data']:
                    if 'from' in comment and comment['from'].get('id') == page_id:
                        already_commented = True
                        break
            
            if already_commented:
                print("  [✅] Author (Page) has ALREADY commented on this post. Skipping.")
            else:
                print("  [🚨] Author comment NOT FOUND! Placing Comment & Thumbnail now...")
                post_comment(post_id, token)
                update_video_thumbnail(post_id, token)

    except Exception as e:
        print(f"  [❌] Error while monitoring: {e}")

# ==========================================
# 🚀 MAIN LOOP
# ==========================================
def main():
    if not ACTIVE_TOKEN:
        print("\n[🛑 System] ERROR: Token is missing!")
        print("Agar aapne 'Custom Token' select kiya hai, toh box mein token paste karna zaroori hai.")
        print("Agar aapne koi aur Page select kiya hai, toh check karein ke Github Secrets mein token save hai ya nahi.")
        return

    print(f"\n[⏳] Monitoring loop started for '{TARGET_PAGE}'. Bot will check every 5 minutes...")
    
    cycle = 1
    while True:
        elapsed_time = time.time() - START_TIME
        if elapsed_time > END_TIME_LIMIT:
            print("\n[🛑 System] 6 Hours Limit Reached. Closing bot gracefully.")
            break

        print(f"\n{'-'*50}")
        print(f"--- 🔄 SCAN CYCLE #{cycle} ---")
        print(f"{'-'*50}")

        check_and_comment(ACTIVE_TOKEN)

        print(f"\n[💤] Cycle #{cycle} complete. Sleeping for 5 minutes...")
        time.sleep(WAIT_TIME)
        cycle += 1

if __name__ == "__main__":
    main()
















# import os
# import time
# import requests
# from datetime import datetime, timezone

# print("\n" + "="*50)
# print("   🚀 FACEBOOK PAGE MONITOR (THUMBNAIL + COMMENT EDITION)")
# print("="*50)

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# COMMENT_TEXT = "📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
# COMMENT_IMG_PATH = "comment_image.jpeg"
# VIDEO_THUMBNAIL_PATH = "thumbnail.png" # 🖼️ Yeh video ke cover par lagegi

# START_TIME = time.time()
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60)  # 5 hours 50 mins limit
# WAIT_TIME = 300  # 5 Minutes wait between checks

# # 🎯 USER SELECTION PULL KARNA
# TARGET_PAGE = os.environ.get('TARGET_PAGE', 'Primary Page')
# CUSTOM_TOKEN = os.environ.get('CUSTOM_TOKEN', '').strip()

# # 🗄️ TOKENS DICTIONARY
# AVAILABLE_TOKENS = {
#     'Primary Page': os.environ.get('PRIMARY_TOKEN', '').strip(),
#     'Secondary Page': os.environ.get('SECONDARY_TOKEN', '').strip(),
#     'Page 3': os.environ.get('TOKEN_3', '').strip(),
#     'Page 4': os.environ.get('TOKEN_4', '').strip(),
# }

# # 🧠 SMART SELECTION LOGIC
# ACTIVE_TOKEN = ""
# if TARGET_PAGE == 'Custom Token (Below)':
#     ACTIVE_TOKEN = CUSTOM_TOKEN
#     print(f"[⚙️] Mode: Custom Token Provide kiya gaya hai.")
# else:
#     ACTIVE_TOKEN = AVAILABLE_TOKENS.get(TARGET_PAGE, "")
#     print(f"[⚙️] Mode: '{TARGET_PAGE}' Select kiya gaya hai.")

# # ==========================================
# # 🛠️ CORE FUNCTIONS
# # ==========================================
# def get_page_info(token):
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": token, "fields": "id,name"}).json()
#         if 'id' in res: return res['id'], res['name']
#     except Exception as e:
#         print(f"  [❌] Token verification failed: {e}")
#     return None, None

# def post_comment(post_id, token):
#     print(f"  [>] Posting promotional comment on {post_id}...")
#     comment_url = f"https://graph.facebook.com/v18.0/{post_id}/comments"
    
#     try:
#         if os.path.exists(COMMENT_IMG_PATH):
#             print("  [📸] Comment Image found! Posting Comment WITH Photo...")
#             with open(COMMENT_IMG_PATH, "rb") as img:
#                 # 🛠️ FIX: Proper MIME type add kiya gaya hai
#                 files = {"source": ("comment_image.jpeg", img, "image/jpeg")}
#                 res = requests.post(comment_url, data={"message": COMMENT_TEXT, "access_token": token}, files=files).json()
#         else:
#             print("  [📝] No comment image found. Posting TEXT-ONLY Comment...")
#             res = requests.post(comment_url, data={"message": COMMENT_TEXT, "access_token": token}).json()

#         if 'id' in res:
#             print(f"  [✅] Comment Placed Successfully! Comment ID: {res['id']}")
#         else:
#             print(f"  [❌] Error posting comment: {res}")
#     except Exception as e:
#         print(f"  [❌] Crash while posting comment: {e}")

# # 🚀 THUMBNAIL ENGINE (WITH MIME TYPE FIX)
# def update_video_thumbnail(post_id, token):
#     if not os.path.exists(VIDEO_THUMBNAIL_PATH):
#         print(f"  [⚠️] '{VIDEO_THUMBNAIL_PATH}' repo mein nahi mili. Thumbnail update skip kar raha hoon.")
#         return

#     print(f"  [🖼️] Checking if post contains a video to update its thumbnail...")
#     try:
#         attach_url = f"https://graph.facebook.com/v18.0/{post_id}?fields=attachments&access_token={token}"
#         attach_data = requests.get(attach_url).json()
        
#         video_id = None
#         attachments = attach_data.get('attachments', {}).get('data', [])
        
#         if attachments and 'target' in attachments[0] and 'id' in attachments[0]['target']:
#             video_id = attachments[0]['target']['id']
            
#         if video_id:
#             print(f"  [>] Video ID found: {video_id}. Uploading new Thumbnail...")
            
#             with open(VIDEO_THUMBNAIL_PATH, "rb") as thumb_file:
#                 # 🛠️ THE FIX: Facebook ko explicitly batana ke yeh PNG Image hai warna wo ignore kar dega!
#                 files = {"thumb": ("thumbnail.png", thumb_file, "image/png")}
                
#                 res = requests.post(
#                     f"https://graph.facebook.com/v18.0/{video_id}", 
#                     data={"access_token": token}, 
#                     files=files
#                 ).json()
                
#             if res.get('success'):
#                 print("  [✅] Video Thumbnail (Cover Photo) Updated Successfully!")
#                 print("  [💡] Note: Agar video abhi LIVE hai, toh Facebook isay dikhane mein 1-2 minute le sakta hai. Page refresh karein.")
#             else:
#                 print(f"  [❌] Thumbnail update failed: {res}")
#         else:
#             print("  [⚠️] Koi Video attach nahi mili (Yeh shayad text/photo post hai).")
            
#     except Exception as e:
#         print(f"  [❌] Crash while updating thumbnail: {e}")

# def check_and_comment(token):
#     page_id, page_name = get_page_info(token)
#     if not page_id:
#         print(f"  [❌] Invalid Token! Could not authenticate with Facebook API.")
#         return

#     print(f"\n[🔍] Monitoring Page: {page_name} (ID: {page_id})")
    
#     try:
#         posts_url = f"https://graph.facebook.com/v18.0/{page_id}/posts?fields=id,created_time&access_token={token}"
#         posts_data = requests.get(posts_url).json()
        
#         if 'data' not in posts_data:
#             print(f"  [⚠️] Could not fetch posts. API Response: {posts_data}")
#             return
            
#         posts = posts_data['data']
#         now_utc = datetime.now(timezone.utc)
        
#         recent_posts = []
#         for post in posts:
#             post_time = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S%z")
#             age_seconds = (now_utc - post_time).total_seconds()
#             if age_seconds <= 3600: # Sirf pichle 1 ghante ki posts
#                 recent_posts.append(post)

#         print(f"  [📊] Found {len(recent_posts)} post(s) created in the last 1 hour.")

#         for post in recent_posts:
#             post_id = post['id']
#             print(f"  [👉] Checking Post ID: {post_id}")
            
#             comments_url = f"https://graph.facebook.com/v18.0/{post_id}/comments?fields=from&access_token={token}"
#             comments_data = requests.get(comments_url).json()
            
#             already_commented = False
#             if 'data' in comments_data:
#                 for comment in comments_data['data']:
#                     if 'from' in comment and comment['from'].get('id') == page_id:
#                         already_commented = True
#                         break
            
#             if already_commented:
#                 print("  [✅] Author (Page) has ALREADY commented on this post. Skipping.")
#             else:
#                 print("  [🚨] Author comment NOT FOUND! Placing Comment & Thumbnail now...")
                
#                 # 1. Pehle comment karega
#                 post_comment(post_id, token)
                
#                 # 2. Phir Thumbnail update karega!
#                 update_video_thumbnail(post_id, token)

#     except Exception as e:
#         print(f"  [❌] Error while monitoring: {e}")

# # ==========================================
# # 🚀 MAIN LOOP
# # ==========================================
# def main():
#     if not ACTIVE_TOKEN:
#         print("\n[🛑 System] ERROR: Token is missing!")
#         print("Agar aapne 'Custom Token' select kiya hai, toh box mein token paste karna zaroori hai.")
#         print("Agar aapne koi aur Page select kiya hai, toh check karein ke Github Secrets mein token save hai ya nahi.")
#         return

#     print(f"\n[⏳] Monitoring loop started for '{TARGET_PAGE}'. Bot will check every 5 minutes...")
    
#     cycle = 1
#     while True:
#         elapsed_time = time.time() - START_TIME
#         if elapsed_time > END_TIME_LIMIT:
#             print("\n[🛑 System] 6 Hours Limit Reached. Closing bot gracefully.")
#             break

#         print(f"\n{'-'*50}")
#         print(f"--- 🔄 SCAN CYCLE #{cycle} ---")
#         print(f"{'-'*50}")

#         check_and_comment(ACTIVE_TOKEN)

#         print(f"\n[💤] Cycle #{cycle} complete. Sleeping for 5 minutes...")
#         time.sleep(WAIT_TIME)
#         cycle += 1

# if __name__ == "__main__":
#     main()

















# ======== done commnet done , aab thumbnail ==========================



# import os
# import time
# import requests
# from datetime import datetime, timezone

# print("\n" + "="*50)
# print("   🚀 FACEBOOK PAGE MONITOR (SMART SELECTOR EDITION)")
# print("="*50)

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# COMMENT_TEXT = "📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
# COMMENT_IMG_PATH = "comment_image.jpeg"

# START_TIME = time.time()
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60)  # 5 hours 50 mins limit
# WAIT_TIME = 300  # 5 Minutes wait between checks

# # 🎯 USER SELECTION PULL KARNA
# TARGET_PAGE = os.environ.get('TARGET_PAGE', 'Primary Page')
# CUSTOM_TOKEN = os.environ.get('CUSTOM_TOKEN', '').strip()

# # 🗄️ TOKENS DICTIONARY (Sare available tokens yahan map hain)
# AVAILABLE_TOKENS = {
#     'Primary Page': os.environ.get('PRIMARY_TOKEN', '').strip(),
#     'Secondary Page': os.environ.get('SECONDARY_TOKEN', '').strip(),
#     'Page 3': os.environ.get('TOKEN_3', '').strip(),
#     'Page 4': os.environ.get('TOKEN_4', '').strip(),
# }

# # 🧠 SMART SELECTION LOGIC
# ACTIVE_TOKEN = ""
# if TARGET_PAGE == 'Custom Token (Below)':
#     ACTIVE_TOKEN = CUSTOM_TOKEN
#     print(f"[⚙️] Mode: Custom Token Provide kiya gaya hai.")
# else:
#     ACTIVE_TOKEN = AVAILABLE_TOKENS.get(TARGET_PAGE, "")
#     print(f"[⚙️] Mode: '{TARGET_PAGE}' Select kiya gaya hai.")

# # ==========================================
# # 🛠️ CORE FUNCTIONS
# # ==========================================
# def get_page_info(token):
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": token, "fields": "id,name"}).json()
#         if 'id' in res: return res['id'], res['name']
#     except Exception as e:
#         print(f"  [❌] Token verification failed: {e}")
#     return None, None

# def post_comment(post_id, token):
#     print(f"  [>] Posting promotional comment on {post_id}...")
#     comment_url = f"https://graph.facebook.com/v18.0/{post_id}/comments"
    
#     try:
#         if os.path.exists(COMMENT_IMG_PATH):
#             print("  [📸] Image found! Posting Comment WITH Photo...")
#             with open(COMMENT_IMG_PATH, "rb") as img:
#                 res = requests.post(comment_url, data={"message": COMMENT_TEXT, "access_token": token}, files={"source": img}).json()
#         else:
#             print("  [📝] No image found. Posting TEXT-ONLY Comment...")
#             res = requests.post(comment_url, data={"message": COMMENT_TEXT, "access_token": token}).json()

#         if 'id' in res:
#             print(f"  [✅] Comment Placed Successfully! Comment ID: {res['id']}")
#         else:
#             print(f"  [❌] Error posting comment: {res}")
#     except Exception as e:
#         print(f"  [❌] Crash while posting comment: {e}")

# def check_and_comment(token):
#     page_id, page_name = get_page_info(token)
#     if not page_id:
#         print(f"  [❌] Invalid Token! Could not authenticate with Facebook API.")
#         return

#     print(f"\n[🔍] Monitoring Page: {page_name} (ID: {page_id})")
    
#     try:
#         posts_url = f"https://graph.facebook.com/v18.0/{page_id}/posts?fields=id,created_time&access_token={token}"
#         posts_data = requests.get(posts_url).json()
        
#         if 'data' not in posts_data:
#             print(f"  [⚠️] Could not fetch posts. API Response: {posts_data}")
#             return
            
#         posts = posts_data['data']
#         now_utc = datetime.now(timezone.utc)
        
#         recent_posts = []
#         for post in posts:
#             post_time = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S%z")
#             age_seconds = (now_utc - post_time).total_seconds()
#             if age_seconds <= 3600: # Sirf pichle 1 ghante ki posts
#                 recent_posts.append(post)

#         print(f"  [📊] Found {len(recent_posts)} post(s) created in the last 1 hour.")

#         for post in recent_posts:
#             post_id = post['id']
#             print(f"  [👉] Checking Post ID: {post_id}")
            
#             comments_url = f"https://graph.facebook.com/v18.0/{post_id}/comments?fields=from&access_token={token}"
#             comments_data = requests.get(comments_url).json()
            
#             already_commented = False
#             if 'data' in comments_data:
#                 for comment in comments_data['data']:
#                     if 'from' in comment and comment['from'].get('id') == page_id:
#                         already_commented = True
#                         break
            
#             if already_commented:
#                 print("  [✅] Author (Page) has ALREADY commented on this post. Skipping.")
#             else:
#                 print("  [🚨] Author comment NOT FOUND! Placing Comment now...")
#                 post_comment(post_id, token)

#     except Exception as e:
#         print(f"  [❌] Error while monitoring: {e}")

# # ==========================================
# # 🚀 MAIN LOOP
# # ==========================================
# def main():
#     if not ACTIVE_TOKEN:
#         print("\n[🛑 System] ERROR: Token is missing!")
#         print("Agar aapne 'Custom Token' select kiya hai, toh box mein token paste karna zaroori hai.")
#         print("Agar aapne koi aur Page select kiya hai, toh check karein ke Github Secrets mein token save hai ya nahi.")
#         return

#     print(f"\n[⏳] Monitoring loop started for {TARGET_PAGE}. Bot will check every 5 minutes...")
    
#     cycle = 1
#     while True:
#         elapsed_time = time.time() - START_TIME
#         if elapsed_time > END_TIME_LIMIT:
#             print("\n[🛑 System] 6 Hours Limit Reached. Closing bot gracefully.")
#             break

#         print(f"\n{'-'*50}")
#         print(f"--- 🔄 SCAN CYCLE #{cycle} ---")
#         print(f"{'-'*50}")

#         check_and_comment(ACTIVE_TOKEN)

#         print(f"\n[💤] Cycle #{cycle} complete. Sleeping for 5 minutes...")
#         time.sleep(WAIT_TIME)
#         cycle += 1

# if __name__ == "__main__":
#     main()
































# ============================================ main code below starts, lekin iss me pthon m3u8 link capture nahey kar raha hai, iss liye isko maney javascript mei kar deya hai dai khaisra sra and aab oopper wala code srf facebook page mei post ko monitor karey ga and post par commnet karey ga 1 hour waley latest post and 5 min k break between   ==================================





# import mimetypes 
# import os
# import time
# import subprocess
# import urllib.parse
# import traceback
# import requests
# import random 
# import numpy as np
# import base64
# from html2image import Html2Image
# from PIL import Image, ImageFilter

# # ==========================================
# # 🦸‍♂️ THE SUPERMAN PATCH (For Pillow 10+)
# # ==========================================
# print("[⚙️ System] Checking Pillow version...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅ System] Superman Patch Applied for Pillow.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[⚙️ System] Loading MoviePy modules (This might take a second)...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip
# import moviepy.audio.fx.all as afx
# print("[✅ System] MoviePy modules loaded successfully.")

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[⚙️ System] Initializing Settings and Environment Variables...")
# TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
# FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

# TITLES_INPUT = os.environ.get('TITLES_LIST', 'Live Match Today,,Watch Full Match DC vs GT').strip()
# DESCS_INPUT = os.environ.get('DESCS_LIST', 'Watch the live action here').strip()
# HASHTAGS = os.environ.get('HASHTAGS', '#IPL2026 #DCvsGT #CricketLovers #LiveMatch').strip()

# PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
# PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
# PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
# PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
# PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

# PKT = timezone(timedelta(hours=5))
# WAIT_TIME_SECONDS = 300  
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 
# print("[✅ System] All Environment Variables Loaded.")

# # ==========================================
# # 🌐 HTML2IMAGE THUMBNAIL ENGINE (PROJECT 5)
# # ==========================================
# print("[⚙️ System] Initializing HTML2Image Engine for Thumbnails...")
# hti = Html2Image(size=(1280, 720), custom_flags=['--hide-scrollbars', '--no-sandbox', '--disable-gpu'])

# def get_image_base64(image_path):
#     print(f"  [>] Converting image '{image_path}' to Base64 format...")
#     with open(image_path, "rb") as img_file:
#         b64_string = base64.b64encode(img_file.read()).decode('utf-8')
#         ext = image_path.split('.')[-1].lower()
#         print(f"  [>] Conversion done. Extension detected: {ext}")
#         if ext == 'png': return f"data:image/png;base64,{b64_string}"
#         else: return f"data:image/jpeg;base64,{b64_string}"

# def worker_0_5_generate_thumbnail(central_image_path, match_name_text, output_image_path):
#     print(f"\n[🎨 Worker 0.5] Rendering Studio Thumbnail for: '{match_name_text}'")
    
#     print(f"  [>] Checking if central image '{central_image_path}' exists...")
#     if not os.path.exists(central_image_path): 
#         print(f"  [❌ Worker 0.5] Central image NOT FOUND! Aborting thumbnail creation.")
#         return False
        
#     try:
#         b64_image = get_image_base64(central_image_path)
#         print("  [>] Generating HTML/CSS template...")
        
#         html_code = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap');
#                 body {{ margin: 0; padding: 0; width: 1280px; height: 720px; background-color: #0f0f0f; font-family: 'Roboto', sans-serif; color: white; display: flex; flex-direction: column; overflow: hidden; }}
#                 .header {{ height: 100px; display: flex; align-items: center; padding: 0 40px; justify-content: space-between; z-index: 10; }}
#                 .logo-container {{ display: flex; align-items: center; gap: 20px; }}
#                 .hamburger {{ display: flex; flex-direction: column; gap: 6px; }}
#                 .hamburger div {{ width: 40px; height: 6px; background: white; }}
#                 .logo {{ font-size: 50px; font-weight: 900; letter-spacing: 1px; text-shadow: 0 0 10px rgba(255,255,255,0.8), 0 0 20px rgba(255,255,255,0.6); }}
#                 .live-badge {{ border: 4px solid #cc0000; border-radius: 12px; padding: 5px 20px; font-size: 40px; font-weight: 700; display: flex; align-items: center; gap: 10px; box-shadow: 0 0 15px rgba(204,0,0,0.4); }}
#                 .dot {{ color: #cc0000; text-shadow: 0 0 10px #cc0000; }}
#                 .hero-container {{ position: relative; width: 100%; height: 440px; }}
#                 .hero-img {{ width: 100%; height: 100%; object-fit: cover; }}
#                 .gradient-fade {{ position: absolute; bottom: 0; width: 100%; height: 150px; background: linear-gradient(to bottom, transparent, #0f0f0f); }}
#                 .pip-img {{ position: absolute; top: 30px; right: 40px; width: 40%; border: 6px solid white; box-shadow: -15px 15px 30px rgba(0,0,0,0.8); }}
#                 .text-container {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 10px 40px; }}
#                 .main-title {{ font-size: 80px; font-weight: 900; line-height: 1.1; text-shadow: 6px 6px 15px rgba(0,0,0,0.9); }}
#                 .live-text {{ color: #cc0000; text-shadow: 6px 6px 15px rgba(0,0,0,0.9), 0 0 15px rgba(204,0,0,0.8), 0 0 30px rgba(204,0,0,0.5); }}
#                 .match-text {{ color: white; }}
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <div class="logo-container"><div class="hamburger"><div></div><div></div><div></div></div><div class="logo">SPORTSHUB</div></div>
#                 <div class="live-badge"><span class="dot">●</span> LIVE</div>
#             </div>
#             <div class="hero-container">
#                 <img src="{b64_image}" class="hero-img">
#                 <div class="gradient-fade"></div> 
#                 <img src="{b64_image}" class="pip-img">
#             </div>
#             <div class="text-container">
#                 <div class="main-title">
#                     <span class="live-text">LIVE NOW HERE: </span>
#                     <span class="match-text">{match_name_text}</span>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
        
#         print(f"  [>] Ordering Html2Image to take screenshot and save as '{output_image_path}'...")
#         hti.screenshot(html_str=html_code, save_as=output_image_path)
#         print(f"[✅ Worker 0.5] Thumbnail successfully generated: {output_image_path}")
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 0.5] Thumbnail Gen Error: {e}")
#         return False

# # ==========================================
# # 🧠 ANTI-SPAM METADATA
# # ==========================================
# def generate_unique_metadata(clip_number):
#     print(f"\n[🧠 Metadata] Generating Unique Titles and Descriptions for Clip #{clip_number}...")
    
#     all_titles = [t.strip() for t in TITLES_INPUT.split(',,') if t.strip()]
#     all_descriptions = [d.strip() for d in DESCS_INPUT.split(',,') if d.strip()]
    
#     if not all_titles: 
#         print("  [>] Titles array empty, using fallback.")
#         all_titles = ["Live Match Today"]
#     if not all_descriptions: 
#         print("  [>] Descriptions array empty, using fallback.")
#         all_descriptions = ["Watch the live action here!"]
    
#     chosen_base_title = random.choice(all_titles)
#     chosen_desc_body = random.choice(all_descriptions)
#     chosen_title = f"{chosen_base_title}" 
    
#     print(f"  [>] Selected Title: {chosen_title}")
    
#     if len(chosen_title) > 250: 
#         print("  [>] Title exceeds 250 characters. Trimming to safe size...")
#         chosen_title = chosen_title[:247] + "..."
        
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")

#     tags_list = HASHTAGS.split() 
#     random.shuffle(tags_list)    
#     selected_4_tags = " ".join(tags_list[:4]) 
#     print(f"  [>] Selected Hashtags: {selected_4_tags}")
    
#     final_description = f"{chosen_title} {emo[0]} {emo[1]} {emo[2]}\n\n{chosen_desc_body}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{selected_4_tags}"
#     print("[✅ Metadata] Metadata generation complete.")
#     return chosen_title, final_description

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n[⏰ Relay Race] Attempting to trigger the next bot run via GitHub API...")
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
#     url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
#     headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
#     data = {
#         "ref": branch,
#         "inputs": {
#             "target_url": TARGET_WEBSITE, "proxy_ip": PROXY_IP, "proxy_port": PROXY_PORT,
#             "proxy_user": PROXY_USER, "proxy_pass": PROXY_PASS,
#             "titles_list": TITLES_INPUT, "descs_list": DESCS_INPUT, "hashtags": HASHTAGS
#         }
#     }
#     try: 
#         print(f"  [>] Sending POST request to {url}...")
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204:
#             print("[✅ Relay Race] Next Bot Triggered Successfully (Status 204).")
#         else:
#             print(f"[⚠️ Relay Race] Trigger sent but got unexpected status: {res.status_code}")
#     except Exception as e: 
#         print(f"[❌ Relay Race] Request failed: {e}")

# # ==========================================
# # STEP 1: SELENIUM LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print("\n[🔍 Selenium] Starting Chrome to steal M3U8 link...")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         print("  [>] Launching webdriver...")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
#         print(f"  [>] Hitting Target URL: {TARGET_WEBSITE}")
#         driver.get(TARGET_WEBSITE)
        
#         print("  [⏳] Sleeping for 5 seconds to bypass Cloudflare/Loading...")
#         time.sleep(5)
        
#         print("  [>] Scanning network requests for .m3u8 token...")
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 print("  [✅ BINGO] M3U8 link found in requests!")
#                 data = {
#                     "url": request.url, 
#                     "ua": request.headers.get('User-Agent', ''), 
#                     "cookie": request.headers.get('Cookie', ''), 
#                     "referer": request.headers.get('Referer', TARGET_WEBSITE)
#                 }
#                 break
                
#         if not data:
#             print("  [❌] M3U8 link NOT FOUND after scanning.")
            
#     except Exception as e: 
#         print(f"[❌ Selenium] Crashed during execution: {e}")
#     finally:
#         if driver: 
#             print("  [>] Quitting driver and closing browser...")
#             driver.quit()
            
#     return data

# def calculate_expiry_time(url):
#     print("\n[⏰ Expiry Check] Calculating Token Expiry Time...")
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: 
#             exp_time = datetime.fromtimestamp(exp, PKT)
#             print(f"  [✅] Extracted Expiry: {exp_time.strftime('%I:%M:%S %p PKT')}")
#             return exp_time
#     except Exception as e: 
#         print(f"  [⚠️] Failed to extract expiry from URL: {e}")
#         pass
        
#     fallback = datetime.now(PKT) + timedelta(hours=2)
#     print(f"  [>] Using fallback expiry time: {fallback.strftime('%I:%M:%S %p PKT')}")
#     return fallback

# def get_page_id():
#     print("\n[🔍 FB Auth] Verifying Facebook Access Token...")
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res: 
#             print(f"  [✅] Token is VALID. Connected to Page: {res.get('name')}")
#             return res.get('id')
#         else:
#             print(f"  [❌] Invalid Token response: {res}")
#     except Exception as e: 
#         print(f"  [❌ FB Auth] Request failed: {e}")
#     return None

# # ==========================================
# # WORKER 0: SCREENSHOT CAPTURE
# # ==========================================
# def worker_0_capture_frame(data, output_img):
#     print(f"\n[📸 Worker 0] Capturing a single frame from live stream...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
    
#     # [✅ FIX] cmd list is now fully complete
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-vframes', '1', '-q:v', '2', output_img]
    
#     print(f"  [>] Running FFmpeg command to save '{output_img}'...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(output_img):
#         print(f"[✅ Worker 0] Screenshot captured successfully.")
#         return True
#     else:
#         print(f"[❌ Worker 0] Failed to capture screenshot.")
#         return False

# # ==========================================
# # WORKER 1: VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥 Worker 1] Capturing {duration} seconds of video from live stream...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
    
#     # [✅ FIX] cmd list is now fully complete
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
#     print(f"  [>] Running FFmpeg command to save '{filename}'...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(filename):
#         print(f"[✅ Worker 1] Video chunk captured successfully.")
#         return True
#     else:
#         print(f"[❌ Worker 1] Failed to capture video chunk.")
#         return False

# # ==========================================
# # WORKER 2: VIDEO EDITING
# # ==========================================

# # ==========================================
# # WORKER 2: VIDEO EDITING (PiP + Blur Engine)
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬 Worker 2] Starting Video Editor Engine with PiP Logic...")
#     try:
#         print(f"  [>] Loading dynamic clip '{dynamic_vid}' and static clip '{static_vid}'...")
#         dyn_clip = VideoFileClip(dynamic_vid)
#         stat_clip = VideoFileClip(static_vid)
        
#         # --- NEW LOGIC: Picture-in-Picture (PiP) Setup ---
#         bg_image_path = "website_frame.png"
        
#         if os.path.exists(bg_image_path):
#             print(f"  [>] Background Image '{bg_image_path}' found! Applying PiP...")
            
#             # Step 1: Create a VideoClip from the background image
#             # Iski duration dynamic clip ke barabar set karenge
#             bg_clip = ImageClip(bg_image_path).set_duration(dyn_clip.duration)
            
#             # Step 2: Calculate dimensions from coordinates
#             # Left Top: (0, 250) -> x=0, y=250
#             # Right Bottom: (1064, 815) -> Width = 1064 - 0, Height = 815 - 250
#             target_x = 0
#             target_y = 250
#             target_width = 1064
#             target_height = 815 - 250  # 565
            
#             print(f"  [>] Resizing live video to fit coordinates: Width={target_width}, Height={target_height}...")
#             # Video ko target size par resize karo aur position set karo
#             pip_video = dyn_clip.resize((target_width, target_height)).set_position((target_x, target_y))
            
#             print("  [>] Compositing live video onto the background image...")
#             # Step 3: Mix the background and the video
#             dyn_clip = CompositeVideoClip([bg_clip, pip_video])
#         else:
#             print(f"  [⚠️] Background Image '{bg_image_path}' NOT FOUND! Proceeding without PiP...")
#             # Agar image nahi milti toh simple resize kar do
#             print("  [>] Resizing dynamic clip to match static clip...")
#             dyn_clip = dyn_clip.resize(stat_clip.size)

#         # --- Remaining Logic (Blurring and Merging) ---
#         def blur(frame): 
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(20)))

#         print("  [>] Applying Gaussian Blur (radius 20) on the composite video...")
#         dyn_clip = dyn_clip.fl_image(blur)
        
#         print("  [>] Concatenating (merging) clips...")
#         # stat_clip aur nai dyn_clip ko jodna
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         print(f"  [>] Loading custom audio '{custom_audio}' and looping it...")
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
        
#         print("  [>] Setting final audio track on merged video...")
#         final_video = merged.set_audio(final_audio)

#         print(f"  [>] Rendering final video '{output_vid}' (Preset: ultrafast)...")
#         # Ensure FPS matches the static clip to avoid errors
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)
        
#         print("  [>] Closing resources and freeing memory...")
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
        
#         # Agar bg_clip bani thi toh use bhi close karo
#         if 'bg_clip' in locals():
#             bg_clip.close()

#         print("[✅ Worker 2] Video edited successfully with PiP and Blur.")
#         return True
#     except Exception as e: 
#         print(f"[❌ Worker 2] Editing Crashed: {e}")
#         return False

# # ==========================================
# # WORKER 3: 1-STEP FACEBOOK UPLOAD
# # ==========================================
# def worker_3_upload(video_path, page_id, title, desc, dynamic_thumb_path):
#     print(f"\n[📤 Worker 3] Preparing Facebook Upload (1-Step Method)...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     files_to_open = []
#     try:
#         print(f"  [>] Opening video file '{video_path}'...")
#         f_vid = open(video_path, "rb")
#         files_to_open.append(f_vid)
#         files = {"source": ("video.mp4", f_vid, "video/mp4")}
        
#         print("  [>] Checking for dynamic thumbnail...")
#         if dynamic_thumb_path and os.path.exists(dynamic_thumb_path):
#             print(f"  [>] Thumbnail '{dynamic_thumb_path}' found! Opening file...")
#             f_thumb = open(dynamic_thumb_path, "rb")
#             files_to_open.append(f_thumb)
#             print("  [>] Attaching thumbnail as 'image/png' to payload...")
#             files["thumb"] = (os.path.basename(dynamic_thumb_path), f_thumb, "image/png")
#         else:
#             print(f"  [⚠️] No dynamic thumbnail found. Proceeding without thumbnail.")

#         print("  [>] Sending POST request to Facebook Graph API...")
#         res = requests.post(url, data=payload, files=files).json()
        
#         if "id" in res:
#             print(f"[✅ Worker 3] Video & Thumbnail Upload SUCCESS! (Post ID: {res['id']})")
            
#             print("  [⏳] Waiting 15 seconds for FB processing before dropping comment...")
#             time.sleep(15) 
            
#             print("  [>] Posting promotional comment...")
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
            
#             comment_img_path = "comment_image.jpeg" 
#             if os.path.exists(comment_img_path):
#                 print("  [>] Comment image found, attaching to comment...")
#                 with open(comment_img_path, "rb") as img:
#                     requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 print("[✅ Worker 3] Photo Comment Placed.")
#             else:
#                 print("  [>] Comment image NOT found, posting text-only comment...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅ Worker 3] Text Comment Placed.")
#             return True
#         else:
#              print(f"[❌ Worker 3] API Error from Facebook: {res}")
#              return False
             
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Crash: {e}")
#         return False
#     finally:
#         print("  [>] Closing file pointers...")
#         for f in files_to_open: f.close()

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE HYBRID CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: 
#         print("[🛑 System] Failed to get Page ID. Exiting.")
#         return 

#     data = get_link_with_headers()
#     if not data: 
#         print("[🛑 System] Failed to get initial M3U8 link. Exiting.")
#         return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     print("\n[⚙️ System] Beginning Main Loop...")
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*50)
#         print(f"--- 🔄 STARTING VIDEO CYCLE #{clip_counter} ---")
#         print(f"  [-] Bot Uptime: {int(elapsed_time/60)} minutes")
#         print(f"  [-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
#         print("-" * 50)
        
#         print("  [>] Checking Relay Race logic...")
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             print("  [🚨] Trigger time reached! Executing handoff...")
#             trigger_next_run()
#             next_run_triggered = True 
            
#         print("  [>] Checking Suicide limits...")
#         if elapsed_time > END_TIME_LIMIT: 
#             print("[🛑 System] Max Lifetime Reached. Exiting script gracefully.")
#             break
        
#         print("  [>] Checking link expiry...")
#         if time_left_seconds <= 120:
#             print("  [🚨] Link is expiring soon! Pausing to fetch new link...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 print("  [✅] New link acquired.")
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#             else:
#                 print("  [⚠️] Failed to get new link. Retrying in 60 seconds...")
#                 time.sleep(60); continue 
        
#         title, desc = generate_unique_metadata(clip_counter)
        
#         raw_frame = f"live_frame_{clip_counter}.jpg"
#         generated_thumb = f"studio_thumb_{clip_counter}.png"
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # 🔗 HYBRID ACTION FLOW
#         print("\n[⚡ Flow] Executing the Hybrid Action Flow...")
        
#         if worker_0_capture_frame(data, raw_frame):
#             if worker_0_5_generate_thumbnail(raw_frame, title, generated_thumb):
#                 if worker_1_capture_video(data, raw_vid, duration=10):
#                     if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                         worker_3_upload(final_vid, page_id, title, desc, generated_thumb)
#                     else:
#                         print("  [❌ Flow Broken] Worker 2 (Edit) failed.")
#                 else:
#                     print("  [❌ Flow Broken] Worker 1 (Video Capture) failed.")
#             else:
#                 print("  [❌ Flow Broken] Worker 0.5 (Thumbnail Gen) failed.")
#         else:
#             print("  [❌ Flow Broken] Worker 0 (Screenshot) failed.")
        
#         print("\n[🧹 Cleanup] Running Garbage Collector...")
        
#         # [✅ FIX] temp_file list is now fully complete
#         for temp_file in [raw_frame, generated_thumb, raw_vid, final_vid]:
#             if os.path.exists(temp_file): 
#                 os.remove(temp_file)
#                 print(f"  [-] Deleted: {temp_file}")
            
#         print(f"\n[⏳ Cycle End] Cycle #{clip_counter} Complete. Waiting {WAIT_TIME_SECONDS} seconds before next run...")
#         clip_counter += 1
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()



























# ==================== the below code is good, uplaod and thumbnail done(but few videos thumbnail setup well) ==========================



# import mimetypes 
# import os
# import time
# import subprocess
# import urllib.parse
# import traceback
# import requests
# import random 
# import numpy as np
# import base64
# from html2image import Html2Image
# from PIL import Image, ImageFilter

# # ==========================================
# # 🦸‍♂️ THE SUPERMAN PATCH (For Pillow 10+)
# # ==========================================
# print("[⚙️ System] Checking Pillow version...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅ System] Superman Patch Applied for Pillow.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[⚙️ System] Loading MoviePy modules (This might take a second)...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx
# print("[✅ System] MoviePy modules loaded successfully.")

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[⚙️ System] Initializing Settings and Environment Variables...")
# TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
# FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

# TITLES_INPUT = os.environ.get('TITLES_LIST', 'Live Match Today,,Watch Full Match DC vs GT').strip()
# DESCS_INPUT = os.environ.get('DESCS_LIST', 'Watch the live action here').strip()
# HASHTAGS = os.environ.get('HASHTAGS', '#IPL2026 #DCvsGT #CricketLovers #LiveMatch').strip()

# PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
# PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
# PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
# PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
# PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

# PKT = timezone(timedelta(hours=5))
# WAIT_TIME_SECONDS = 300  
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 
# print("[✅ System] All Environment Variables Loaded.")

# # ==========================================
# # 🌐 HTML2IMAGE THUMBNAIL ENGINE (PROJECT 5)
# # ==========================================
# print("[⚙️ System] Initializing HTML2Image Engine for Thumbnails...")
# hti = Html2Image(size=(1280, 720), custom_flags=['--hide-scrollbars', '--no-sandbox', '--disable-gpu'])

# def get_image_base64(image_path):
#     print(f"  [>] Converting image '{image_path}' to Base64 format...")
#     with open(image_path, "rb") as img_file:
#         b64_string = base64.b64encode(img_file.read()).decode('utf-8')
#         ext = image_path.split('.')[-1].lower()
#         print(f"  [>] Conversion done. Extension detected: {ext}")
#         if ext == 'png': return f"data:image/png;base64,{b64_string}"
#         else: return f"data:image/jpeg;base64,{b64_string}"

# def worker_0_5_generate_thumbnail(central_image_path, match_name_text, output_image_path):
#     print(f"\n[🎨 Worker 0.5] Rendering Studio Thumbnail for: '{match_name_text}'")
    
#     print(f"  [>] Checking if central image '{central_image_path}' exists...")
#     if not os.path.exists(central_image_path): 
#         print(f"  [❌ Worker 0.5] Central image NOT FOUND! Aborting thumbnail creation.")
#         return False
        
#     try:
#         b64_image = get_image_base64(central_image_path)
#         print("  [>] Generating HTML/CSS template...")
        
#         html_code = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap');
#                 body {{ margin: 0; padding: 0; width: 1280px; height: 720px; background-color: #0f0f0f; font-family: 'Roboto', sans-serif; color: white; display: flex; flex-direction: column; overflow: hidden; }}
#                 .header {{ height: 100px; display: flex; align-items: center; padding: 0 40px; justify-content: space-between; z-index: 10; }}
#                 .logo-container {{ display: flex; align-items: center; gap: 20px; }}
#                 .hamburger {{ display: flex; flex-direction: column; gap: 6px; }}
#                 .hamburger div {{ width: 40px; height: 6px; background: white; }}
#                 .logo {{ font-size: 50px; font-weight: 900; letter-spacing: 1px; text-shadow: 0 0 10px rgba(255,255,255,0.8), 0 0 20px rgba(255,255,255,0.6); }}
#                 .live-badge {{ border: 4px solid #cc0000; border-radius: 12px; padding: 5px 20px; font-size: 40px; font-weight: 700; display: flex; align-items: center; gap: 10px; box-shadow: 0 0 15px rgba(204,0,0,0.4); }}
#                 .dot {{ color: #cc0000; text-shadow: 0 0 10px #cc0000; }}
#                 .hero-container {{ position: relative; width: 100%; height: 440px; }}
#                 .hero-img {{ width: 100%; height: 100%; object-fit: cover; }}
#                 .gradient-fade {{ position: absolute; bottom: 0; width: 100%; height: 150px; background: linear-gradient(to bottom, transparent, #0f0f0f); }}
#                 .pip-img {{ position: absolute; top: 30px; right: 40px; width: 40%; border: 6px solid white; box-shadow: -15px 15px 30px rgba(0,0,0,0.8); }}
#                 .text-container {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 10px 40px; }}
#                 .main-title {{ font-size: 80px; font-weight: 900; line-height: 1.1; text-shadow: 6px 6px 15px rgba(0,0,0,0.9); }}
#                 .live-text {{ color: #cc0000; text-shadow: 6px 6px 15px rgba(0,0,0,0.9), 0 0 15px rgba(204,0,0,0.8), 0 0 30px rgba(204,0,0,0.5); }}
#                 .match-text {{ color: white; }}
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <div class="logo-container"><div class="hamburger"><div></div><div></div><div></div></div><div class="logo">SPORTSHUB</div></div>
#                 <div class="live-badge"><span class="dot">●</span> LIVE</div>
#             </div>
#             <div class="hero-container">
#                 <img src="{b64_image}" class="hero-img">
#                 <div class="gradient-fade"></div> 
#                 <img src="{b64_image}" class="pip-img">
#             </div>
#             <div class="text-container">
#                 <div class="main-title">
#                     <span class="live-text">LIVE NOW HERE: </span>
#                     <span class="match-text">{match_name_text}</span>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
        
#         print(f"  [>] Ordering Html2Image to take screenshot and save as '{output_image_path}'...")
#         hti.screenshot(html_str=html_code, save_as=output_image_path)
#         print(f"[✅ Worker 0.5] Thumbnail successfully generated: {output_image_path}")
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 0.5] Thumbnail Gen Error: {e}")
#         return False

# # ==========================================
# # 🧠 ANTI-SPAM METADATA
# # ==========================================
# def generate_unique_metadata(clip_number):
#     print(f"\n[🧠 Metadata] Generating Unique Titles and Descriptions for Clip #{clip_number}...")
    
#     all_titles = [t.strip() for t in TITLES_INPUT.split(',,') if t.strip()]
#     all_descriptions = [d.strip() for d in DESCS_INPUT.split(',,') if d.strip()]
    
#     if not all_titles: 
#         print("  [>] Titles array empty, using fallback.")
#         all_titles = ["Live Match Today"]
#     if not all_descriptions: 
#         print("  [>] Descriptions array empty, using fallback.")
#         all_descriptions = ["Watch the live action here!"]
    
#     chosen_base_title = random.choice(all_titles)
#     chosen_desc_body = random.choice(all_descriptions)
#     chosen_title = f"{chosen_base_title}" 
    
#     print(f"  [>] Selected Title: {chosen_title}")
    
#     if len(chosen_title) > 250: 
#         print("  [>] Title exceeds 250 characters. Trimming to safe size...")
#         chosen_title = chosen_title[:247] + "..."
        
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")

#     tags_list = HASHTAGS.split() 
#     random.shuffle(tags_list)    
#     selected_4_tags = " ".join(tags_list[:4]) 
#     print(f"  [>] Selected Hashtags: {selected_4_tags}")
    
#     final_description = f"{chosen_title} {emo[0]} {emo[1]} {emo[2]}\n\n{chosen_desc_body}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{selected_4_tags}"
#     print("[✅ Metadata] Metadata generation complete.")
#     return chosen_title, final_description

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n[⏰ Relay Race] Attempting to trigger the next bot run via GitHub API...")
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
#     url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
#     headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
#     data = {
#         "ref": branch,
#         "inputs": {
#             "target_url": TARGET_WEBSITE, "proxy_ip": PROXY_IP, "proxy_port": PROXY_PORT,
#             "proxy_user": PROXY_USER, "proxy_pass": PROXY_PASS,
#             "titles_list": TITLES_INPUT, "descs_list": DESCS_INPUT, "hashtags": HASHTAGS
#         }
#     }
#     try: 
#         print(f"  [>] Sending POST request to {url}...")
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204:
#             print("[✅ Relay Race] Next Bot Triggered Successfully (Status 204).")
#         else:
#             print(f"[⚠️ Relay Race] Trigger sent but got unexpected status: {res.status_code}")
#     except Exception as e: 
#         print(f"[❌ Relay Race] Request failed: {e}")

# # ==========================================
# # STEP 1: SELENIUM LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print("\n[🔍 Selenium] Starting Chrome to steal M3U8 link...")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         print("  [>] Launching webdriver...")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
#         print(f"  [>] Hitting Target URL: {TARGET_WEBSITE}")
#         driver.get(TARGET_WEBSITE)
        
#         print("  [⏳] Sleeping for 5 seconds to bypass Cloudflare/Loading...")
#         time.sleep(5)
        
#         print("  [>] Scanning network requests for .m3u8 token...")
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 print("  [✅ BINGO] M3U8 link found in requests!")
#                 data = {
#                     "url": request.url, 
#                     "ua": request.headers.get('User-Agent', ''), 
#                     "cookie": request.headers.get('Cookie', ''), 
#                     "referer": request.headers.get('Referer', TARGET_WEBSITE)
#                 }
#                 break
                
#         if not data:
#             print("  [❌] M3U8 link NOT FOUND after scanning.")
            
#     except Exception as e: 
#         print(f"[❌ Selenium] Crashed during execution: {e}")
#     finally:
#         if driver: 
#             print("  [>] Quitting driver and closing browser...")
#             driver.quit()
            
#     return data

# def calculate_expiry_time(url):
#     print("\n[⏰ Expiry Check] Calculating Token Expiry Time...")
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: 
#             exp_time = datetime.fromtimestamp(exp, PKT)
#             print(f"  [✅] Extracted Expiry: {exp_time.strftime('%I:%M:%S %p PKT')}")
#             return exp_time
#     except Exception as e: 
#         print(f"  [⚠️] Failed to extract expiry from URL: {e}")
#         pass
        
#     fallback = datetime.now(PKT) + timedelta(hours=2)
#     print(f"  [>] Using fallback expiry time: {fallback.strftime('%I:%M:%S %p PKT')}")
#     return fallback

# def get_page_id():
#     print("\n[🔍 FB Auth] Verifying Facebook Access Token...")
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res: 
#             print(f"  [✅] Token is VALID. Connected to Page: {res.get('name')}")
#             return res.get('id')
#         else:
#             print(f"  [❌] Invalid Token response: {res}")
#     except Exception as e: 
#         print(f"  [❌ FB Auth] Request failed: {e}")
#     return None

# # ==========================================
# # WORKER 0: SCREENSHOT CAPTURE
# # ==========================================
# def worker_0_capture_frame(data, output_img):
#     print(f"\n[📸 Worker 0] Capturing a single frame from live stream...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
    
#     # [✅ FIX] cmd list is now fully complete
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-vframes', '1', '-q:v', '2', output_img]
    
#     print(f"  [>] Running FFmpeg command to save '{output_img}'...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(output_img):
#         print(f"[✅ Worker 0] Screenshot captured successfully.")
#         return True
#     else:
#         print(f"[❌ Worker 0] Failed to capture screenshot.")
#         return False

# # ==========================================
# # WORKER 1: VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥 Worker 1] Capturing {duration} seconds of video from live stream...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
    
#     # [✅ FIX] cmd list is now fully complete
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
#     print(f"  [>] Running FFmpeg command to save '{filename}'...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(filename):
#         print(f"[✅ Worker 1] Video chunk captured successfully.")
#         return True
#     else:
#         print(f"[❌ Worker 1] Failed to capture video chunk.")
#         return False

# # ==========================================
# # WORKER 2: VIDEO EDITING
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬 Worker 2] Starting Video Editor Engine...")
#     try:
#         print(f"  [>] Loading dynamic clip '{dynamic_vid}' and static clip '{static_vid}'...")
#         dyn_clip = VideoFileClip(dynamic_vid)
#         stat_clip = VideoFileClip(static_vid)
        
#         print("  [>] Resizing dynamic clip to match static clip...")
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame): 
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(20)))

#         print("  [>] Applying Gaussian Blur (radius 20) on dynamic clip...")
#         dyn_clip = dyn_clip.fl_image(blur)
        
#         print("  [>] Concatenating (merging) clips...")
        
#         # [✅ FIX] concatenate_videoclips function call is now complete
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         print(f"  [>] Loading custom audio '{custom_audio}' and looping it...")
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
        
#         print("  [>] Setting final audio track on merged video...")
#         final_video = merged.set_audio(final_audio)

#         print(f"  [>] Rendering final video '{output_vid}' (Preset: ultrafast)...")
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)
        
#         print("  [>] Closing resources and freeing memory...")
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
#         print("[✅ Worker 2] Video edited successfully.")
#         return True
#     except Exception as e: 
#         print(f"[❌ Worker 2] Editing Crashed: {e}")
#         return False

# # ==========================================
# # WORKER 3: 1-STEP FACEBOOK UPLOAD
# # ==========================================
# def worker_3_upload(video_path, page_id, title, desc, dynamic_thumb_path):
#     print(f"\n[📤 Worker 3] Preparing Facebook Upload (1-Step Method)...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     files_to_open = []
#     try:
#         print(f"  [>] Opening video file '{video_path}'...")
#         f_vid = open(video_path, "rb")
#         files_to_open.append(f_vid)
#         files = {"source": ("video.mp4", f_vid, "video/mp4")}
        
#         print("  [>] Checking for dynamic thumbnail...")
#         if dynamic_thumb_path and os.path.exists(dynamic_thumb_path):
#             print(f"  [>] Thumbnail '{dynamic_thumb_path}' found! Opening file...")
#             f_thumb = open(dynamic_thumb_path, "rb")
#             files_to_open.append(f_thumb)
#             print("  [>] Attaching thumbnail as 'image/png' to payload...")
#             files["thumb"] = (os.path.basename(dynamic_thumb_path), f_thumb, "image/png")
#         else:
#             print(f"  [⚠️] No dynamic thumbnail found. Proceeding without thumbnail.")

#         print("  [>] Sending POST request to Facebook Graph API...")
#         res = requests.post(url, data=payload, files=files).json()
        
#         if "id" in res:
#             print(f"[✅ Worker 3] Video & Thumbnail Upload SUCCESS! (Post ID: {res['id']})")
            
#             print("  [⏳] Waiting 15 seconds for FB processing before dropping comment...")
#             time.sleep(15) 
            
#             print("  [>] Posting promotional comment...")
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
            
#             comment_img_path = "comment_image.jpeg" 
#             if os.path.exists(comment_img_path):
#                 print("  [>] Comment image found, attaching to comment...")
#                 with open(comment_img_path, "rb") as img:
#                     requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 print("[✅ Worker 3] Photo Comment Placed.")
#             else:
#                 print("  [>] Comment image NOT found, posting text-only comment...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅ Worker 3] Text Comment Placed.")
#             return True
#         else:
#              print(f"[❌ Worker 3] API Error from Facebook: {res}")
#              return False
             
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Crash: {e}")
#         return False
#     finally:
#         print("  [>] Closing file pointers...")
#         for f in files_to_open: f.close()

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE HYBRID CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: 
#         print("[🛑 System] Failed to get Page ID. Exiting.")
#         return 

#     data = get_link_with_headers()
#     if not data: 
#         print("[🛑 System] Failed to get initial M3U8 link. Exiting.")
#         return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     print("\n[⚙️ System] Beginning Main Loop...")
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*50)
#         print(f"--- 🔄 STARTING VIDEO CYCLE #{clip_counter} ---")
#         print(f"  [-] Bot Uptime: {int(elapsed_time/60)} minutes")
#         print(f"  [-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
#         print("-" * 50)
        
#         print("  [>] Checking Relay Race logic...")
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             print("  [🚨] Trigger time reached! Executing handoff...")
#             trigger_next_run()
#             next_run_triggered = True 
            
#         print("  [>] Checking Suicide limits...")
#         if elapsed_time > END_TIME_LIMIT: 
#             print("[🛑 System] Max Lifetime Reached. Exiting script gracefully.")
#             break
        
#         print("  [>] Checking link expiry...")
#         if time_left_seconds <= 120:
#             print("  [🚨] Link is expiring soon! Pausing to fetch new link...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 print("  [✅] New link acquired.")
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#             else:
#                 print("  [⚠️] Failed to get new link. Retrying in 60 seconds...")
#                 time.sleep(60); continue 
        
#         title, desc = generate_unique_metadata(clip_counter)
        
#         raw_frame = f"live_frame_{clip_counter}.jpg"
#         generated_thumb = f"studio_thumb_{clip_counter}.png"
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # 🔗 HYBRID ACTION FLOW
#         print("\n[⚡ Flow] Executing the Hybrid Action Flow...")
        
#         if worker_0_capture_frame(data, raw_frame):
#             if worker_0_5_generate_thumbnail(raw_frame, title, generated_thumb):
#                 if worker_1_capture_video(data, raw_vid, duration=10):
#                     if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                         worker_3_upload(final_vid, page_id, title, desc, generated_thumb)
#                     else:
#                         print("  [❌ Flow Broken] Worker 2 (Edit) failed.")
#                 else:
#                     print("  [❌ Flow Broken] Worker 1 (Video Capture) failed.")
#             else:
#                 print("  [❌ Flow Broken] Worker 0.5 (Thumbnail Gen) failed.")
#         else:
#             print("  [❌ Flow Broken] Worker 0 (Screenshot) failed.")
        
#         print("\n[🧹 Cleanup] Running Garbage Collector...")
        
#         # [✅ FIX] temp_file list is now fully complete
#         for temp_file in [raw_frame, generated_thumb, raw_vid, final_vid]:
#             if os.path.exists(temp_file): 
#                 os.remove(temp_file)
#                 print(f"  [-] Deleted: {temp_file}")
            
#         print(f"\n[⏳ Cycle End] Cycle #{clip_counter} Complete. Waiting {WAIT_TIME_SECONDS} seconds before next run...")
#         clip_counter += 1
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()





























# import mimetypes 
# import os
# import time
# import subprocess
# import urllib.parse
# import traceback
# import requests
# import random 
# import numpy as np
# import base64
# from html2image import Html2Image
# from PIL import Image, ImageFilter

# # ==========================================
# # 🦸‍♂️ THE SUPERMAN PATCH (For Pillow 10+)
# # ==========================================
# print("[⚙️ System] Checking Pillow version...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅ System] Superman Patch Applied for Pillow.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[⚙️ System] Loading MoviePy modules (This might take a second)...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx
# print("[✅ System] MoviePy modules loaded successfully.")

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[⚙️ System] Initializing Settings and Environment Variables...")
# TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
# FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

# TITLES_INPUT = os.environ.get('TITLES_LIST', 'Live Match Today,,Watch Full Match DC vs GT').strip()
# DESCS_INPUT = os.environ.get('DESCS_LIST', 'Watch the live action here').strip()
# HASHTAGS = os.environ.get('HASHTAGS', '#IPL2026 #DCvsGT #CricketLovers #LiveMatch').strip()

# PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
# PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
# PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
# PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
# PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

# PKT = timezone(timedelta(hours=5))
# WAIT_TIME_SECONDS = 300  
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 
# print("[✅ System] All Environment Variables Loaded.")

# # ==========================================
# # 🌐 HTML2IMAGE THUMBNAIL ENGINE (PROJECT 5)
# # ==========================================
# print("[⚙️ System] Initializing HTML2Image Engine for Thumbnails...")
# hti = Html2Image(size=(1280, 1000), custom_flags=['--hide-scrollbars', '--no-sandbox', '--disable-gpu'])

# def get_image_base64(image_path):
#     print(f"  [>] Converting image '{image_path}' to Base64 format...")
#     with open(image_path, "rb") as img_file:
#         b64_string = base64.b64encode(img_file.read()).decode('utf-8')
#         ext = image_path.split('.')[-1].lower()
#         print(f"  [>] Conversion done. Extension detected: {ext}")
#         if ext == 'png': return f"data:image/png;base64,{b64_string}"
#         else: return f"data:image/jpeg;base64,{b64_string}"

# def worker_0_5_generate_thumbnail(central_image_path, match_name_text, output_image_path):
#     print(f"\n[🎨 Worker 0.5] Rendering Studio Thumbnail for: '{match_name_text}'")
    
#     print(f"  [>] Checking if central image '{central_image_path}' exists...")
#     if not os.path.exists(central_image_path): 
#         print(f"  [❌ Worker 0.5] Central image NOT FOUND! Aborting thumbnail creation.")
#         return False
        
#     try:
#         b64_image = get_image_base64(central_image_path)
#         print("  [>] Generating HTML/CSS template...")
        
#         html_code = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap');
#                 body {{ margin: 0; padding: 0; width: 1280px; height: 1000px; background-color: #0f0f0f; font-family: 'Roboto', sans-serif; color: white; display: flex; flex-direction: column; overflow: hidden; }}
#                 .header {{ height: 120px; display: flex; align-items: center; padding: 0 40px; justify-content: space-between; z-index: 10; }}
#                 .logo-container {{ display: flex; align-items: center; gap: 20px; }}
#                 .hamburger {{ display: flex; flex-direction: column; gap: 6px; }}
#                 .hamburger div {{ width: 40px; height: 6px; background: white; }}
#                 .logo {{ font-size: 55px; font-weight: 900; letter-spacing: 1px; text-shadow: 0 0 10px rgba(255,255,255,0.8), 0 0 20px rgba(255,255,255,0.6); }}
#                 .live-badge {{ border: 4px solid #cc0000; border-radius: 12px; padding: 5px 20px; font-size: 45px; font-weight: 700; display: flex; align-items: center; gap: 10px; box-shadow: 0 0 15px rgba(204,0,0,0.4); }}
#                 .dot {{ color: #cc0000; text-shadow: 0 0 10px #cc0000; }}
#                 .hero-container {{ position: relative; width: 100%; height: 600px; }}
#                 .hero-img {{ width: 100%; height: 100%; object-fit: cover; }}
#                 .gradient-fade {{ position: absolute; bottom: 0; width: 100%; height: 150px; background: linear-gradient(to bottom, transparent, #0f0f0f); }}
#                 .pip-img {{ position: absolute; top: 40px; right: 40px; width: 50%; border: 6px solid white; box-shadow: -15px 15px 30px rgba(0,0,0,0.8); }}
#                 .text-container {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px 40px; }}
#                 .main-title {{ font-size: 100px; font-weight: 900; line-height: 1.1; text-shadow: 6px 6px 15px rgba(0,0,0,0.9); }}
#                 .live-text {{ color: #cc0000; text-shadow: 6px 6px 15px rgba(0,0,0,0.9), 0 0 15px rgba(204,0,0,0.8), 0 0 30px rgba(204,0,0,0.5); }}
#                 .match-text {{ color: white; }}
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <div class="logo-container"><div class="hamburger"><div></div><div></div><div></div></div><div class="logo">SPORTSHUB</div></div>
#                 <div class="live-badge"><span class="dot">●</span> LIVE</div>
#             </div>
#             <div class="hero-container">
#                 <img src="{b64_image}" class="hero-img">
#                 <div class="gradient-fade"></div> 
#                 <img src="{b64_image}" class="pip-img">
#             </div>
#             <div class="text-container">
#                 <div class="main-title"><span class="live-text">LIVE NOW: </span><span class="match-text">{match_name_text}</span></div>
#             </div>
#         </body>
#         </html>
#         """
        
#         print(f"  [>] Ordering Html2Image to take screenshot and save as '{output_image_path}'...")
#         hti.screenshot(html_str=html_code, save_as=output_image_path)
#         print(f"[✅ Worker 0.5] Thumbnail successfully generated: {output_image_path}")
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 0.5] Thumbnail Gen Error: {e}")
#         return False

# # ==========================================
# # 🧠 ANTI-SPAM METADATA
# # ==========================================
# def generate_unique_metadata(clip_number):
#     print(f"\n[🧠 Metadata] Generating Unique Titles and Descriptions for Clip #{clip_number}...")
    
#     all_titles = [t.strip() for t in TITLES_INPUT.split(',,') if t.strip()]
#     all_descriptions = [d.strip() for d in DESCS_INPUT.split(',,') if d.strip()]
    
#     if not all_titles: 
#         print("  [>] Titles array empty, using fallback.")
#         all_titles = ["Live Match Today"]
#     if not all_descriptions: 
#         print("  [>] Descriptions array empty, using fallback.")
#         all_descriptions = ["Watch the live action here!"]
    
#     chosen_base_title = random.choice(all_titles)
#     chosen_desc_body = random.choice(all_descriptions)
#     chosen_title = f"{chosen_base_title}" 
    
#     print(f"  [>] Selected Title: {chosen_title}")
    
#     if len(chosen_title) > 250: 
#         print("  [>] Title exceeds 250 characters. Trimming to safe size...")
#         chosen_title = chosen_title[:247] + "..."
        
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")

#     tags_list = HASHTAGS.split() 
#     random.shuffle(tags_list)    
#     selected_4_tags = " ".join(tags_list[:4]) 
#     print(f"  [>] Selected Hashtags: {selected_4_tags}")
    
#     final_description = f"{chosen_title} {emo[0]} {emo[1]} {emo[2]}\n\n{chosen_desc_body}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{selected_4_tags}"
#     print("[✅ Metadata] Metadata generation complete.")
#     return chosen_title, final_description

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n[⏰ Relay Race] Attempting to trigger the next bot run via GitHub API...")
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
#     url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
#     headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
#     data = {
#         "ref": branch,
#         "inputs": {
#             "target_url": TARGET_WEBSITE, "proxy_ip": PROXY_IP, "proxy_port": PROXY_PORT,
#             "proxy_user": PROXY_USER, "proxy_pass": PROXY_PASS,
#             "titles_list": TITLES_INPUT, "descs_list": DESCS_INPUT, "hashtags": HASHTAGS
#         }
#     }
#     try: 
#         print(f"  [>] Sending POST request to {url}...")
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204:
#             print("[✅ Relay Race] Next Bot Triggered Successfully (Status 204).")
#         else:
#             print(f"[⚠️ Relay Race] Trigger sent but got unexpected status: {res.status_code}")
#     except Exception as e: 
#         print(f"[❌ Relay Race] Request failed: {e}")

# # ==========================================
# # STEP 1: SELENIUM LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print("\n[🔍 Selenium] Starting Chrome to steal M3U8 link...")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         print("  [>] Launching webdriver...")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
#         print(f"  [>] Hitting Target URL: {TARGET_WEBSITE}")
#         driver.get(TARGET_WEBSITE)
        
#         print("  [⏳] Sleeping for 5 seconds to bypass Cloudflare/Loading...")
#         time.sleep(5)
        
#         print("  [>] Scanning network requests for .m3u8 token...")
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 print("  [✅ BINGO] M3U8 link found in requests!")
#                 data = {
#                     "url": request.url, 
#                     "ua": request.headers.get('User-Agent', ''), 
#                     "cookie": request.headers.get('Cookie', ''), 
#                     "referer": request.headers.get('Referer', TARGET_WEBSITE)
#                 }
#                 break
                
#         if not data:
#             print("  [❌] M3U8 link NOT FOUND after scanning.")
            
#     except Exception as e: 
#         print(f"[❌ Selenium] Crashed during execution: {e}")
#     finally:
#         if driver: 
#             print("  [>] Quitting driver and closing browser...")
#             driver.quit()
            
#     return data

# def calculate_expiry_time(url):
#     print("\n[⏰ Expiry Check] Calculating Token Expiry Time...")
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: 
#             exp_time = datetime.fromtimestamp(exp, PKT)
#             print(f"  [✅] Extracted Expiry: {exp_time.strftime('%I:%M:%S %p PKT')}")
#             return exp_time
#     except Exception as e: 
#         print(f"  [⚠️] Failed to extract expiry from URL: {e}")
#         pass
        
#     fallback = datetime.now(PKT) + timedelta(hours=2)
#     print(f"  [>] Using fallback expiry time: {fallback.strftime('%I:%M:%S %p PKT')}")
#     return fallback

# def get_page_id():
#     print("\n[🔍 FB Auth] Verifying Facebook Access Token...")
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res: 
#             print(f"  [✅] Token is VALID. Connected to Page: {res.get('name')}")
#             return res.get('id')
#         else:
#             print(f"  [❌] Invalid Token response: {res}")
#     except Exception as e: 
#         print(f"  [❌ FB Auth] Request failed: {e}")
#     return None

# # ==========================================
# # WORKER 0: SCREENSHOT CAPTURE
# # ==========================================
# def worker_0_capture_frame(data, output_img):
#     print(f"\n[📸 Worker 0] Capturing a single frame from live stream...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-vframes', '1', '-q:v', '2', output_img]
    
#     print(f"  [>] Running FFmpeg command to save '{output_img}'...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(output_img):
#         print(f"[✅ Worker 0] Screenshot captured successfully.")
#         return True
#     else:
#         print(f"[❌ Worker 0] Failed to capture screenshot.")
#         return False

# # ==========================================
# # WORKER 1: VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥 Worker 1] Capturing {duration} seconds of video from live stream...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
#     print(f"  [>] Running FFmpeg command to save '{filename}'...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(filename):
#         print(f"[✅ Worker 1] Video chunk captured successfully.")
#         return True
#     else:
#         print(f"[❌ Worker 1] Failed to capture video chunk.")
#         return False

# # ==========================================
# # WORKER 2: VIDEO EDITING
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬 Worker 2] Starting Video Editor Engine...")
#     try:
#         print(f"  [>] Loading dynamic clip '{dynamic_vid}' and static clip '{static_vid}'...")
#         dyn_clip = VideoFileClip(dynamic_vid)
#         stat_clip = VideoFileClip(static_vid)
        
#         print("  [>] Resizing dynamic clip to match static clip...")
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame): 
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(20)))

#         print("  [>] Applying Gaussian Blur (radius 20) on dynamic clip...")
#         dyn_clip = dyn_clip.fl_image(blur)
        
#         print("  [>] Concatenating (merging) clips...")
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         print(f"  [>] Loading custom audio '{custom_audio}' and looping it...")
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
        
#         print("  [>] Setting final audio track on merged video...")
#         final_video = merged.set_audio(final_audio)

#         print(f"  [>] Rendering final video '{output_vid}' (Preset: ultrafast)...")
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)
        
#         print("  [>] Closing resources and freeing memory...")
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
#         print("[✅ Worker 2] Video edited successfully.")
#         return True
#     except Exception as e: 
#         print(f"[❌ Worker 2] Editing Crashed: {e}")
#         return False

# # ==========================================
# # WORKER 3: 1-STEP FACEBOOK UPLOAD
# # ==========================================
# def worker_3_upload(video_path, page_id, title, desc, dynamic_thumb_path):
#     print(f"\n[📤 Worker 3] Preparing Facebook Upload (1-Step Method)...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     files_to_open = []
#     try:
#         print(f"  [>] Opening video file '{video_path}'...")
#         f_vid = open(video_path, "rb")
#         files_to_open.append(f_vid)
#         files = {"source": ("video.mp4", f_vid, "video/mp4")}
        
#         print("  [>] Checking for dynamic thumbnail...")
#         if dynamic_thumb_path and os.path.exists(dynamic_thumb_path):
#             print(f"  [>] Thumbnail '{dynamic_thumb_path}' found! Opening file...")
#             f_thumb = open(dynamic_thumb_path, "rb")
#             files_to_open.append(f_thumb)
#             print("  [>] Attaching thumbnail as 'image/png' to payload...")
#             files["thumb"] = (dynamic_thumb_path, f_thumb, "image/png")
#         else:
#             print(f"  [⚠️] No dynamic thumbnail found. Proceeding without thumbnail.")

#         print("  [>] Sending POST request to Facebook Graph API...")
#         res = requests.post(url, data=payload, files=files).json()
        
#         if "id" in res:
#             print(f"[✅ Worker 3] Video & Thumbnail Upload SUCCESS! (Post ID: {res['id']})")
            
#             print("  [⏳] Waiting 15 seconds for FB processing before dropping comment...")
#             time.sleep(15) 
            
#             print("  [>] Posting promotional comment...")
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
            
#             comment_img_path = "comment_image.jpeg" 
#             if os.path.exists(comment_img_path):
#                 print("  [>] Comment image found, attaching to comment...")
#                 with open(comment_img_path, "rb") as img:
#                     requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 print("[✅ Worker 3] Photo Comment Placed.")
#             else:
#                 print("  [>] Comment image NOT found, posting text-only comment...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅ Worker 3] Text Comment Placed.")
#             return True
#         else:
#              print(f"[❌ Worker 3] API Error from Facebook: {res}")
#              return False
             
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Crash: {e}")
#         return False
#     finally:
#         print("  [>] Closing file pointers...")
#         for f in files_to_open: f.close()

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE HYBRID CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: 
#         print("[🛑 System] Failed to get Page ID. Exiting.")
#         return 

#     data = get_link_with_headers()
#     if not data: 
#         print("[🛑 System] Failed to get initial M3U8 link. Exiting.")
#         return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     print("\n[⚙️ System] Beginning Main Loop...")
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*50)
#         print(f"--- 🔄 STARTING VIDEO CYCLE #{clip_counter} ---")
#         print(f"  [-] Bot Uptime: {int(elapsed_time/60)} minutes")
#         print(f"  [-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
#         print("-" * 50)
        
#         print("  [>] Checking Relay Race logic...")
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             print("  [🚨] Trigger time reached! Executing handoff...")
#             trigger_next_run()
#             next_run_triggered = True 
            
#         print("  [>] Checking Suicide limits...")
#         if elapsed_time > END_TIME_LIMIT: 
#             print("[🛑 System] Max Lifetime Reached. Exiting script gracefully.")
#             break
        
#         print("  [>] Checking link expiry...")
#         if time_left_seconds <= 120:
#             print("  [🚨] Link is expiring soon! Pausing to fetch new link...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 print("  [✅] New link acquired.")
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#             else:
#                 print("  [⚠️] Failed to get new link. Retrying in 60 seconds...")
#                 time.sleep(60); continue 
        
#         title, desc = generate_unique_metadata(clip_counter)
        
#         raw_frame = f"live_frame_{clip_counter}.jpg"
#         generated_thumb = f"studio_thumb_{clip_counter}.png"
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # 🔗 HYBRID ACTION FLOW
#         print("\n[⚡ Flow] Executing the Hybrid Action Flow...")
        
#         if worker_0_capture_frame(data, raw_frame):
#             if worker_0_5_generate_thumbnail(raw_frame, title, generated_thumb):
#                 if worker_1_capture_video(data, raw_vid, duration=10):
#                     if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                         worker_3_upload(final_vid, page_id, title, desc, generated_thumb)
#                     else:
#                         print("  [❌ Flow Broken] Worker 2 (Edit) failed.")
#                 else:
#                     print("  [❌ Flow Broken] Worker 1 (Video Capture) failed.")
#             else:
#                 print("  [❌ Flow Broken] Worker 0.5 (Thumbnail Gen) failed.")
#         else:
#             print("  [❌ Flow Broken] Worker 0 (Screenshot) failed.")
        
#         print("\n[🧹 Cleanup] Running Garbage Collector...")
#         for temp_file in [raw_frame, generated_thumb, raw_vid, final_vid]:
#             if os.path.exists(temp_file): 
#                 os.remove(temp_file)
#                 print(f"  [-] Deleted: {temp_file}")
            
#         print(f"\n[⏳ Cycle End] Cycle #{clip_counter} Complete. Waiting {WAIT_TIME_SECONDS} seconds before next run...")
#         clip_counter += 1
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()



































# import mimetypes 
# import os
# import time
# import subprocess
# import urllib.parse
# import traceback
# import requests
# import random 
# import numpy as np
# import base64
# from html2image import Html2Image
# from PIL import Image, ImageFilter

# # ==========================================
# # 🦸‍♂️ THE SUPERMAN PATCH (For Pillow 10+)
# # ==========================================
# print("[*] Checking Pillow version and applying Superman Patch if needed...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅] Superman Patch Applied.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[*] Loading MoviePy modules...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[*] Initializing Settings and Environment Variables...")
# TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
# FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

# TITLES_INPUT = os.environ.get('TITLES_LIST', 'Live Match Today,,Watch Full Match DC vs GT').strip()
# DESCS_INPUT = os.environ.get('DESCS_LIST', 'Watch the live action here').strip()
# HASHTAGS = os.environ.get('HASHTAGS', '#IPL2026 #DCvsGT #CricketLovers #LiveMatch').strip()

# PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
# PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
# PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
# PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
# PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

# PKT = timezone(timedelta(hours=5))
# WAIT_TIME_SECONDS = 300  
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 

# # ==========================================
# # 🌐 HTML2IMAGE THUMBNAIL ENGINE (PROJECT 5)
# # ==========================================
# hti = Html2Image(size=(1280, 1000), custom_flags=['--hide-scrollbars', '--no-sandbox', '--disable-gpu'])

# def get_image_base64(image_path):
#     with open(image_path, "rb") as img_file:
#         b64_string = base64.b64encode(img_file.read()).decode('utf-8')
#         ext = image_path.split('.')[-1].lower()
#         if ext == 'png': return f"data:image/png;base64,{b64_string}"
#         else: return f"data:image/jpeg;base64,{b64_string}"

# def worker_0_5_generate_thumbnail(central_image_path, match_name_text, output_image_path):
#     print(f"\n[🎨] Rendering Studio Thumbnail for: {match_name_text}...")
#     if not os.path.exists(central_image_path): return False
#     try:
#         b64_image = get_image_base64(central_image_path)
#         html_code = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap');
#                 body {{ margin: 0; padding: 0; width: 1280px; height: 1000px; background-color: #0f0f0f; font-family: 'Roboto', sans-serif; color: white; display: flex; flex-direction: column; overflow: hidden; }}
#                 .header {{ height: 120px; display: flex; align-items: center; padding: 0 40px; justify-content: space-between; z-index: 10; }}
#                 .logo-container {{ display: flex; align-items: center; gap: 20px; }}
#                 .hamburger {{ display: flex; flex-direction: column; gap: 6px; }}
#                 .hamburger div {{ width: 40px; height: 6px; background: white; }}
#                 .logo {{ font-size: 55px; font-weight: 900; letter-spacing: 1px; text-shadow: 0 0 10px rgba(255,255,255,0.8), 0 0 20px rgba(255,255,255,0.6); }}
#                 .live-badge {{ border: 4px solid #cc0000; border-radius: 12px; padding: 5px 20px; font-size: 45px; font-weight: 700; display: flex; align-items: center; gap: 10px; box-shadow: 0 0 15px rgba(204,0,0,0.4); }}
#                 .dot {{ color: #cc0000; text-shadow: 0 0 10px #cc0000; }}
#                 .hero-container {{ position: relative; width: 100%; height: 600px; }}
#                 .hero-img {{ width: 100%; height: 100%; object-fit: cover; }}
#                 .gradient-fade {{ position: absolute; bottom: 0; width: 100%; height: 150px; background: linear-gradient(to bottom, transparent, #0f0f0f); }}
#                 .pip-img {{ position: absolute; top: 40px; right: 40px; width: 50%; border: 6px solid white; box-shadow: -15px 15px 30px rgba(0,0,0,0.8); }}
#                 .text-container {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px 40px; }}
#                 .main-title {{ font-size: 100px; font-weight: 900; line-height: 1.1; text-shadow: 6px 6px 15px rgba(0,0,0,0.9); }}
#                 .live-text {{ color: #cc0000; text-shadow: 6px 6px 15px rgba(0,0,0,0.9), 0 0 15px rgba(204,0,0,0.8), 0 0 30px rgba(204,0,0,0.5); }}
#                 .match-text {{ color: white; }}
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <div class="logo-container"><div class="hamburger"><div></div><div></div><div></div></div><div class="logo">SPORTSHUB</div></div>
#                 <div class="live-badge"><span class="dot">●</span> LIVE</div>
#             </div>
#             <div class="hero-container">
#                 <img src="{b64_image}" class="hero-img">
#                 <div class="gradient-fade"></div> 
#                 <img src="{b64_image}" class="pip-img">
#             </div>
#             <div class="text-container">
#                 <div class="main-title"><span class="live-text">LIVE NOW: </span><span class="match-text">{match_name_text}</span></div>
#             </div>
#         </body>
#         </html>
#         """
#         hti.screenshot(html_str=html_code, save_as=output_image_path)
#         print(f"[✅] Thumbnail Ready: {output_image_path}")
#         return True
#     except Exception as e:
#         print(f"[❌] Thumbnail Gen Error: {e}")
#         return False

# # ==========================================
# # 🧠 ANTI-SPAM METADATA
# # ==========================================
# def generate_unique_metadata(clip_number):
#     all_titles = [t.strip() for t in TITLES_INPUT.split(',,') if t.strip()]
#     all_descriptions = [d.strip() for d in DESCS_INPUT.split(',,') if d.strip()]
#     if not all_titles: all_titles = ["Live Match Today"]
#     if not all_descriptions: all_descriptions = ["Watch the live action here!"]
    
#     chosen_base_title = random.choice(all_titles)
#     chosen_desc_body = random.choice(all_descriptions)
#     chosen_title = f"{chosen_base_title}" 
    
#     if len(chosen_title) > 250: chosen_title = chosen_title[:247] + "..."
        
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")

#     tags_list = HASHTAGS.split() 
#     random.shuffle(tags_list)    
#     selected_4_tags = " ".join(tags_list[:4]) 
    
#     final_description = f"{chosen_title} {emo[0]} {emo[1]} {emo[2]}\n\n{chosen_desc_body}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{selected_4_tags}"
#     return chosen_title, final_description

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
#     url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
#     headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
#     data = {
#         "ref": branch,
#         "inputs": {
#             "target_url": TARGET_WEBSITE, "proxy_ip": PROXY_IP, "proxy_port": PROXY_PORT,
#             "proxy_user": PROXY_USER, "proxy_pass": PROXY_PASS,
#             "titles_list": TITLES_INPUT, "descs_list": DESCS_INPUT, "hashtags": HASHTAGS
#         }
#     }
#     try: requests.post(url, headers=headers, json=data)
#     except: pass

# # ==========================================
# # STEP 1: SELENIUM LINK CHURANA
# # ==========================================
# def get_link_with_headers():
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
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res: return res.get('id')
#     except: pass
#     return None

# # ==========================================
# # WORKER 0: SCREENSHOT CAPTURE
# # ==========================================
# def worker_0_capture_frame(data, output_img):
#     print(f"\n[📸] Capturing screenshot from live stream...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-vframes', '1', '-q:v', '2', output_img]
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     return os.path.exists(output_img)

# # ==========================================
# # WORKER 1: VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥] Initiating Stream Capture...")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     return os.path.exists(filename)

# # ==========================================
# # WORKER 2: VIDEO EDITING
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬] Starting Video Editing Engine...")
#     try:
#         dyn_clip = VideoFileClip(dynamic_vid)
#         stat_clip = VideoFileClip(static_vid)
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame): return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(20)))

#         dyn_clip = dyn_clip.fl_image(blur)
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
#         final_video = merged.set_audio(final_audio)

#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
#         return True
#     except: return False

# # ==========================================
# # WORKER 3: AAPKA 100% WORKING 1-STEP UPLOAD
# # ==========================================
# def worker_3_upload(video_path, page_id, title, desc, dynamic_thumb_path):
#     print(f"\n[📤] Preparing Facebook Upload (1-Step Method)...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     files_to_open = []
#     try:
#         f_vid = open(video_path, "rb")
#         files_to_open.append(f_vid)
#         files = {"source": ("video.mp4", f_vid, "video/mp4")}
        
#         # Yahan hum wo auto-generated thumbnail attach kar rahe hain
#         if dynamic_thumb_path and os.path.exists(dynamic_thumb_path):
#             print(f"[*] Dynamic Thumbnail found: '{dynamic_thumb_path}'. Attaching directly to upload...")
#             f_thumb = open(dynamic_thumb_path, "rb")
#             files_to_open.append(f_thumb)
            
#             # HTML2IMAGE se hamesha .png ati hai, isliye explicitly image/png de rahe hain
#             files["thumb"] = (dynamic_thumb_path, f_thumb, "image/png")
#         else:
#             print(f"[⚠️] No dynamic thumbnail found. Uploading video only.")

#         print(f"[*] Pushing video & thumbnail together to Graph API...")
#         res = requests.post(url, data=payload, files=files).json()
        
#         if "id" in res:
#             print(f"[✅] Video & Thumbnail Upload SUCCESS! (Post ID: {res['id']})")
            
#             print("[⏳] Waiting 15 seconds for processing before commenting...")
#             time.sleep(15) 
            
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
            
#             comment_img_path = "comment_image.jpeg" 
#             if os.path.exists(comment_img_path):
#                 with open(comment_img_path, "rb") as img:
#                     requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 print("[✅] Photo Comment Placed.")
#             else:
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅] Text Comment Placed.")
#             return True
#         else:
#              print(f"[❌] Facebook API Error: {res}")
#              return False
             
#     except Exception as e:
#         print(f"[💥] Upload Crash: {e}")
#         return False
#     finally:
#         for f in files_to_open: f.close()

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE HYBRID CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: return 

#     data = get_link_with_headers()
#     if not data: return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*40)
#         print(f"--- 🔄 Starting Video Cycle #{clip_counter} ---")
        
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             trigger_next_run()
#             next_run_triggered = True 
            
#         if elapsed_time > END_TIME_LIMIT: break
        
#         if time_left_seconds <= 120:
#             new_data = get_link_with_headers()
#             if new_data:
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#             else:
#                 time.sleep(60); continue 
        
#         title, desc = generate_unique_metadata(clip_counter)
        
#         raw_frame = f"live_frame_{clip_counter}.jpg"
#         generated_thumb = f"studio_thumb_{clip_counter}.png"
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # 🔗 HYBRID ACTION FLOW
#         if worker_0_capture_frame(data, raw_frame):
#             worker_0_5_generate_thumbnail(raw_frame, title, generated_thumb)
#             if worker_1_capture_video(data, raw_vid, duration=10):
#                 if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                     # Passing generated_thumb to your working upload logic!
#                     worker_3_upload(final_vid, page_id, title, desc, generated_thumb)
        
#         print("\n[🧹] Cleanup Engine Started")
#         for temp_file in [raw_frame, generated_thumb, raw_vid, final_vid]:
#             if os.path.exists(temp_file): 
#                 os.remove(temp_file)
#                 print(f"  [-] Deleted: {temp_file}")
            
#         clip_counter += 1
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()



























# =============== yeh bilkul teek hai , bas dynamic thumbnail create karna upper code mei test kar rahey hai ===============================




# import mimetypes # NEW import for guessing mime type from extension
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
# print("[*] Checking Pillow version and applying Superman Patch if needed...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅] Superman Patch Applied: ANTIALIAS redirected to LANCZOS.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[*] Loading MoviePy modules...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[*] Initializing Settings and Environment Variables...")
# TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
# FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

# # ⚠️ YAHAN GITHUB SE DYNAMIC ARRAYS AAYENGE
# TITLES_INPUT = os.environ.get('TITLES_LIST', 'Live Match Today,,Watch Full Match DC vs GT,,Blockbuster IPL Showdown').strip()
# DESCS_INPUT = os.environ.get('DESCS_LIST', 'DC take on GT in the latest IPL match. Watch the live action here,,The best IPL teams DC and GT face off. Click the link in comments for full buffer-free stream,,DC vs GT is a high-voltage clash. Witness every boundary and wicket. Full details in comments!').strip()
# HASHTAGS = os.environ.get('HASHTAGS', '#IPL2026 #DCvsGT #DelhiCapitals #GujaratTitans #IPLLive #TataIPL #T20Cricket #CricketLovers #LiveMatch').strip()
# THUMBNAIL_IMAGE_NAME = os.environ.get('THUMBNAIL_IMAGE_NAME', '').strip() # NEW environment variable

# # Proxy Settings
# PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
# PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
# PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
# PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
# PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

# PKT = timezone(timedelta(hours=5))
# WAIT_TIME_SECONDS = 300  
# print(f"[*] System Timezone set to PKT (+5).")
# print(f"[*] Loop Wait Time set to {WAIT_TIME_SECONDS} seconds.")

# # Relay Race Timers
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 

# # ==========================================
# # 🧠 ANTI-SPAM (DYNAMIC GITHUB INPUT ARRAY)
# # ==========================================
# def generate_unique_metadata(clip_number):
#     print(f"\n[🧠] Generating Array-Based Metadata for Clip #{clip_number}...")
    
#     # 1. Input ko ',,' se tod kar Array banana
#     all_titles = [t.strip() for t in TITLES_INPUT.split(',,') if t.strip()]
#     all_descriptions = [d.strip() for d in DESCS_INPUT.split(',,') if d.strip()]
    
#     # Fallback agar user form khali chhor de
#     if not all_titles: all_titles = ["Live Match Today"]
#     if not all_descriptions: all_descriptions = ["Watch the live stream action now!"]
    
#     # 2. Random Pick (Bot 100 mein se 1 uthayega)
#     chosen_base_title = random.choice(all_titles)
#     chosen_desc_body = random.choice(all_descriptions)
    
#     # Title Hameshachosen_base_title (e.g., Delhi Capitals vs Gujarat Titans) se shuru hoga
#     # chosen_title = f"{MATCH_TITLE} - {dynamic_suffix}"
    
#     # We need to get titles array from the user's input
#     all_titles = [t.strip() for t in TITLES_INPUT.split(',,') if t.strip()]
#     chosen_base_title = random.choice(all_titles)
    
#     # chosen_title = f"{chosen_base_title} - {dynamic_suffix}"
#     chosen_title = f"{chosen_base_title}" # Keeping only the base dynamic title
    
#     # ✂️ THE SMART TRIMMER (Facebook API Byte Limit Fix - User requested 250 character limit)
#     if len(chosen_title) > 250:
#         print(f"[⚠️] Title lamba tha. Safe size par trim kar raha hoon...")
#         chosen_title = chosen_title[:247] + "..."
        
#     # 3. Emojis (Sirf Description ke liye)
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")

#     # 4. HASHTAGS LOGIC (Sirf 4 Random Hashtags)
#     tags_list = HASHTAGS.split() 
#     random.shuffle(tags_list)    
#     selected_4_tags = " ".join(tags_list[:4]) 
    
#     # 5. Description Generator (Title -> Emojis -> Desc -> Tags)
#     final_description = f"{chosen_title} {emo[0]} {emo[1]} {emo[2]}\n\n{chosen_desc_body}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{selected_4_tags}"
    
#     print(f"  --> Total Titles Loaded: {len(all_titles)}")
#     print(f"  --> Selected Title (No Emojis): {chosen_title}")
#     print(f"  --> 4 Hashtags Used: {selected_4_tags}")
    
#     return chosen_title, final_description

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n" + "="*50)
#     print(" ⏰ RELAY RACE: STARTING NEXT GITHUB BOT ⏰")
#     print("="*50)
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
    
#     print(f"[*] Preparing API Request for Repo: {repo}, Branch: {branch}...")
#     url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
#     headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
#     # YAHAN NAYE VARIABLES BHEJ RAHE HAIN
#     data = {
#         "ref": branch,
#         "inputs": {
#             "target_url": TARGET_WEBSITE,
#             "proxy_ip": PROXY_IP, 
#             "proxy_port": PROXY_PORT,
#             "proxy_user": PROXY_USER, 
#             "proxy_pass": PROXY_PASS,
#             "titles_list": TITLES_INPUT, 
#             "descs_list": DESCS_INPUT, 
#             "hashtags": HASHTAGS,
#             "thumbnail_image_name": THUMBNAIL_IMAGE_NAME # NEW workflow input
#         }
#     }
#     try:
#         print("[*] Sending dispatch trigger to GitHub API...")
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204: 
#             print("[✅] SUCCESS! Naya Bot Background Mein Start Ho Gaya Hai!")
#         else:
#             print(f"[⚠️] Unexpected Status Code: {res.status_code} - {res.text}")
#     except Exception as e:
#         print(f"[💥] Relay Race Failed: {e}")

# # ==========================================
# # STEP 1: LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print(f"\n[🔍] Starting Selenium Webdriver with Proxy...")
#     print(f"[*] Target URL: {TARGET_WEBSITE}")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         print("[*] Initializing ChromeDriverManager...")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
#         print("[*] Loading Website...")
#         driver.get(TARGET_WEBSITE)
        
#         print("[⏳] Waiting 5 seconds for page load and Cloudflare bypass...")
#         time.sleep(5)
        
#         print("[*] Scanning Network Requests for .m3u8 token...")
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 data = {"url": request.url, "ua": request.headers.get('User-Agent', ''), "cookie": request.headers.get('Cookie', ''), "referer": request.headers.get('Referer', TARGET_WEBSITE)}
#                 print(f"🎉 [BINGO] M3U8 Link Bypassed & Captured!")
#                 print(f"  --> Found URL: {request.url[:80]}...") 
#                 break
                
#         if not data:
#             print("[⚠️] M3U8 link NOT found in network requests.")
            
#     except Exception as e: 
#         print(f"[💥] Selenium Error: {e}")
#     finally:
#         if driver: 
#             print("[*] Closing Chrome browser and releasing proxy...")
#             driver.quit()
#     return data

# def calculate_expiry_time(url):
#     print("[*] Calculating Link Expiry Time...")
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: 
#             exp_time = datetime.fromtimestamp(exp, PKT)
#             print(f"[⏰] Link will expire at: {exp_time.strftime('%I:%M:%S %p PKT')}")
#             return exp_time
#     except Exception as e: 
#         print(f"[-] Could not parse expiry: {e}")
#         pass
    
#     fallback_time = datetime.now(PKT) + timedelta(hours=2)
#     print(f"[⚠️] Setting Fallback Expiry Time: {fallback_time.strftime('%I:%M:%S %p PKT')}")
#     return fallback_time

# def get_page_id():
#     print("[*] Verifying Facebook Access Token...")
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res:
#             print(f"[+] Connected successfully to Page: {res.get('name', 'Unknown')} (ID: {res['id']})")
#             return res.get('id')
#         else:
#             print(f"[-] API Response error: {res}")
#     except Exception as e: 
#         print(f"[💥] Token Check Error: {e}")
#     return None

# # ==========================================
# # WORKER 1: 10 SECONDS VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥 Worker 1] Initiating Stream Capture...")
#     print(f"[*] Target File: {filename} | Duration: {duration} seconds")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
#     print("[*] Executing FFmpeg command...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(filename):
#         print(f"[✅ Worker 1] Capture successful! File saved.")
#         return True
#     else:
#         print(f"[❌ Worker 1] Capture failed! File not created.")
#         return False

# # ==========================================
# # WORKER 2: VIDEO EDITING (Blur + Merge + Audio)
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬 Worker 2] Starting Video Editing Engine (MoviePy)...")
#     try:
#         print(f"[*] Loading Dynamic Clip: {dynamic_vid}")
#         dyn_clip = VideoFileClip(dynamic_vid)
        
#         print(f"[*] Loading Static Clip: {static_vid}")
#         stat_clip = VideoFileClip(static_vid)
        
#         print(f"[*] Resizing dynamic clip to match static clip size: {stat_clip.size}")
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame):
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(20)))

#         print("[*] Applying Gaussian Blur (Radius: 20) to dynamic clip...")
#         dyn_clip = dyn_clip.fl_image(blur)
        
#         print("[*] Concatenating (Merging) dynamic and static clips...")
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         print(f"[*] Loading Custom Audio: {custom_audio} and looping to match video duration...")
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
        
#         print("[*] Setting final audio track...")
#         final_video = merged.set_audio(final_audio)

#         print(f"[*] Rendering Final Video to: {output_vid}")
#         print("[*] Settings: codec=libx264, audio=aac, preset=ultrafast")
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)

#         print("[*] Closing resources and freeing up RAM...")
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
        
#         print("[✅ Worker 2] Editing Completed Successfully!")
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 2] Edit Error: {e}")
#         return False

# # ==========================================
# # WORKER 3: FACEBOOK UPLOAD & COMMENT WITH IMAGE
# # ==========================================
# def worker_3_upload(video_path, page_id, clip_number):
#     print(f"\n[📤 Worker 3] Preparing Facebook Upload...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     title, desc = generate_unique_metadata(clip_number)
    
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     # Prepare files dictionary conditionally
#     files_to_open = []
#     try:
#         print(f"[*] Preparing files for upload...")
#         f_vid = open(video_path, "rb")
#         files_to_open.append(f_vid)
#         files = {"source": ("video.mp4", f_vid, "video/mp4")}
        
#         # Check for thumbnail and add to files dictionary if found
#         if THUMBNAIL_IMAGE_NAME and os.path.exists(THUMBNAIL_IMAGE_NAME):
#             print(f"[+] Thumbnail found: '{THUMBNAIL_IMAGE_NAME}'. Attaching for upload...")
#             f_thumb = open(THUMBNAIL_IMAGE_NAME, "rb")
#             files_to_open.append(f_thumb)
            
#             # Infer mime type for the thumbnail from the filename extension
#             thumb_mime, _ = mimetypes.guess_type(THUMBNAIL_IMAGE_NAME)
#             if not thumb_mime:
#                 thumb_mime = "application/octet-stream" # Fallback mime type
                
#             files["thumb"] = (THUMBNAIL_IMAGE_NAME, f_thumb, thumb_mime)
#         else:
#             if THUMBNAIL_IMAGE_NAME:
#                 print(f"[⚠️] Thumbnail file not found: '{THUMBNAIL_IMAGE_NAME}'. Uploading without thumbnail.")
#             else:
#                 print(f"[*] No thumbnail specified. Uploading without thumbnail.")

#         print(f"[*] Pushing video file '{video_path}' to Graph API...")
#         # Facebok Graph Video API post call
#         res = requests.post(url, data=payload, files=files).json()
        
#         if "id" in res:
#             print(f"[✅ Worker 3] Video Upload SUCCESS! (Post ID: {res['id']})")
            
#             # --- COMMENT WITH IMAGE LOGIC ---
#             print("[⏳] Waiting 15 seconds for Facebook to process the video before commenting...")
#             time.sleep(15) 
            
#             print("[💬 Worker 3] Preparing Comment with Promotional Image and Link...")
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
#             comment_img_path = "comment_image.jpeg" 
            
#             print(f"[*] Checking for '{comment_img_path}' in directory...")
#             if os.path.exists(comment_img_path):
#                 print(f"[+] Image found! Uploading comment with image...")
#                 with open(comment_img_path, "rb") as img:
#                     comment_res = requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 if 'id' in comment_res.json():
#                     print("[✅ Worker 3] Photo Comment SUCCESS!")
#                 else:
#                     print(f"[⚠️ Worker 3] Comment failed: {comment_res.json()}")
#             else:
#                 print(f"[⚠️] '{comment_img_path}' NOT FOUND! Proceeding with Text-Only comment...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅ Worker 3] Text Comment Placed.")
            
#             return True
#         else:
#              print(f"[❌ Worker 3] Facebook API Error: {res}")
#              return False
             
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Crash: {e}")
#         return False
#     finally:
#         # Conditional closing of files to free up resources
#         print("[*] Closing resources for upload...")
#         for f in files_to_open:
#             f.close()

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: 
#         print("[❌] FATAL: Token invalid! Halting script.")
#         return 

#     print("[*] Initiating First Link Fetch Cycle...")
#     data = get_link_with_headers()
#     if not data: 
#         print("[❌] FATAL: M3U8 Link nahi mila. Halting script.")
#         return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     print("[*] Checking required local assets...")
#     if not os.path.exists(static_video) or not os.path.exists(audio_file):
#          print(f"[⚠️] WARNING: Missing '{static_video}' or '{audio_file}'. Worker 2 WILL fail!")
#     else:
#          print(f"[+] Local assets found.")
    
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*40)
#         print(f"--- 🔄 Starting Video Cycle #{clip_counter} ---")
#         print(f"[-] Bot Uptime: {int(elapsed_time/60)} minutes")
#         print(f"[-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
#         print("-" * 40)
        
#         # 1. Relay Race Check (5h 30m)
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             print("[🚨] Relay Timer Reached (5h 30m). Executing hand-off...")
#             trigger_next_run()
#             next_run_triggered = True 
            
#         # 2. Suicide Check (5h 50m - Stop before GitHub forcefully kills it)
#         if elapsed_time > END_TIME_LIMIT:
#             print("\n[🛑] MAXIMUM LIFETIME REACHED (5h 50m). Naya bot pichay start ho chuka hai. Main gracefully band ho raha hoon.")
#             break
        
#         # 3. Link Expiry Check (2 Min pehle)
#         if time_left_seconds <= 120:
#             print("\n[🚨 ALERT] Link expire hone wala hai. Pausing operations to fetch new link...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#                 print("[+] Expiry parameters updated successfully.")
#             else:
#                 print("[⚠️] Failed to fetch new link. Retrying in 60 seconds...")
#                 time.sleep(60); continue 
        
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # Action Flow
#         if worker_1_capture_video(data, raw_vid, duration=10):
#             if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                 worker_3_upload(final_vid, page_id, clip_counter)
        
#         # 🧹 GARBAGE COLLECTOR (RAM Hack)
#         print("\n[🧹 Cleanup Engine Started]")
#         if os.path.exists(raw_vid): 
#             os.remove(raw_vid)
#             print(f"  [-] Deleted: {raw_vid}")
#         if os.path.exists(final_vid): 
#             os.remove(final_vid)
#             print(f"  [-] Deleted: {final_vid}")
#         print("[🧹] Temporary videos hard-drive se ura di gayi hain. RAM freed.")
            
#         clip_counter += 1
#         print(f"\n[⏳] Cycle Complete. Agli video ke liye {WAIT_TIME_SECONDS} seconds wait kar raha hoon...")
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()












    















# ============================ yahaa par project full kaam kar raha hai and eek new functionality upper code mei add karty hai k yeh facebook video mei thumbnail add karey ========================================

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
# print("[*] Checking Pillow version and applying Superman Patch if needed...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅] Superman Patch Applied: ANTIALIAS redirected to LANCZOS.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[*] Loading MoviePy modules...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[*] Initializing Settings and Environment Variables...")
# TARGET_WEBSITE = os.environ.get('TARGET_URL', '').strip()
# FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN', '').strip()

# # ⚠️ YAHAN GITHUB SE DYNAMIC ARRAYS AAYENGE
# TITLES_INPUT = os.environ.get('TITLES_LIST', 'Live Match').strip()
# DESCS_INPUT = os.environ.get('DESCS_LIST', 'Watch Live Now').strip()
# HASHTAGS = os.environ.get('HASHTAGS', '#Live').strip()

# # Proxy Settings
# PROXY_IP = os.environ.get('PROXY_IP', '31.59.20.176')
# PROXY_PORT = os.environ.get('PROXY_PORT', '6754')
# PROXY_USER = os.environ.get('PROXY_USER', 'ehhppbec')
# PROXY_PASS = os.environ.get('PROXY_PASS', '5f69y4wngj70')
# PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}"

# PKT = timezone(timedelta(hours=5))
# WAIT_TIME_SECONDS = 300  
# print(f"[*] System Timezone set to PKT (+5).")
# print(f"[*] Loop Wait Time set to {WAIT_TIME_SECONDS} seconds.")

# # Relay Race Timers
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 

# # ==========================================
# # 🧠 ANTI-SPAM (DYNAMIC GITHUB INPUT ARRAY)
# # ==========================================
# def generate_unique_metadata(clip_number):
#     print(f"\n[🧠] Generating Array-Based Metadata for Clip #{clip_number}...")
    
#     # 1. Input ko ',,' se tod kar Array banana
#     all_titles = [t.strip() for t in TITLES_INPUT.split(',,') if t.strip()]
#     all_descriptions = [d.strip() for d in DESCS_INPUT.split(',,') if d.strip()]
    
#     # Fallback agar user form khali chhor de
#     if not all_titles: all_titles = ["Live Match Today"]
#     if not all_descriptions: all_descriptions = ["Watch the live stream action now!"]
    
#     # 2. Random Pick (Bot 100 mein se 1 uthayega)
#     chosen_title = random.choice(all_titles)
#     chosen_desc_body = random.choice(all_descriptions)
    
#     # ✂️ THE SMART TRIMMER (Facebook API Byte Limit Fix - No Emojis here)
#     if len(chosen_title) > 255:
#         print(f"[⚠️] Title lamba tha. Safe size par trim kar raha hoon...")
#         chosen_title = chosen_title[:92] + "..."
        
#     # 3. Emojis (Sirf Description ke liye)
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")

#     # 4. HASHTAGS LOGIC (Sirf 4 Random Hashtags)
#     tags_list = HASHTAGS.split() 
#     random.shuffle(tags_list)    
#     selected_4_tags = " ".join(tags_list[:4]) 
    
#     # 5. Final Description Assembly (Title -> Emojis -> Desc -> Tags)
#     final_description = f"{chosen_title} {emo[0]} {emo[1]} {emo[2]}\n\n{chosen_desc_body}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{selected_4_tags}"
    
#     print(f"  --> Total Titles Loaded: {len(all_titles)}")
#     print(f"  --> Selected Title (No Emojis): {chosen_title}")
#     print(f"  --> 4 Hashtags Used: {selected_4_tags}")
    
#     return chosen_title, final_description

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n" + "="*50)
#     print(" ⏰ RELAY RACE: STARTING NEXT GITHUB BOT ⏰")
#     print("="*50)
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
    
#     print(f"[*] Preparing API Request for Repo: {repo}, Branch: {branch}...")
#     url = f"https://api.github.com/repos/{repo}/actions/workflows/video_loop.yml/dispatches"
#     headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    
#     # YAHAN NAYE VARIABLES BHEJ RAHE HAIN
#     data = {
#         "ref": branch,
#         "inputs": {
#             "titles_list": TITLES_INPUT, 
#             "descs_list": DESCS_INPUT, 
#             "hashtags": HASHTAGS, 
#             "target_url": TARGET_WEBSITE, 
#             "proxy_ip": PROXY_IP, 
#             "proxy_port": PROXY_PORT,
#             "proxy_user": PROXY_USER, 
#             "proxy_pass": PROXY_PASS
#         }
#     }
#     try:
#         print("[*] Sending dispatch trigger to GitHub API...")
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204: 
#             print("[✅] SUCCESS! Naya Bot Background Mein Start Ho Gaya Hai!")
#         else:
#             print(f"[⚠️] Unexpected Status Code: {res.status_code} - {res.text}")
#     except Exception as e:
#         print(f"[💥] Relay Race Failed: {e}")

# # ==========================================
# # STEP 1: LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print(f"\n[🔍] Starting Selenium Webdriver with Proxy...")
#     print(f"[*] Target URL: {TARGET_WEBSITE}")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         print("[*] Initializing ChromeDriverManager...")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
#         print("[*] Loading Website...")
#         driver.get(TARGET_WEBSITE)
        
#         print("[⏳] Waiting 5 seconds for page load and Cloudflare bypass...")
#         time.sleep(5)
        
#         print("[*] Scanning Network Requests for .m3u8 token...")
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 data = {"url": request.url, "ua": request.headers.get('User-Agent', ''), "cookie": request.headers.get('Cookie', ''), "referer": request.headers.get('Referer', TARGET_WEBSITE)}
#                 print(f"🎉 [BINGO] M3U8 Link Bypassed & Captured!")
#                 print(f"  --> Found URL: {request.url[:80]}...") 
#                 break
                
#         if not data:
#             print("[⚠️] M3U8 link NOT found in network requests.")
            
#     except Exception as e: 
#         print(f"[💥] Selenium Error: {e}")
#     finally:
#         if driver: 
#             print("[*] Closing Chrome browser and releasing proxy...")
#             driver.quit()
#     return data

# def calculate_expiry_time(url):
#     print("[*] Calculating Link Expiry Time...")
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: 
#             exp_time = datetime.fromtimestamp(exp, PKT)
#             print(f"[⏰] Link will expire at: {exp_time.strftime('%I:%M:%S %p PKT')}")
#             return exp_time
#     except Exception as e: 
#         print(f"[-] Could not parse expiry: {e}")
#         pass
    
#     fallback_time = datetime.now(PKT) + timedelta(hours=2)
#     print(f"[⚠️] Setting Fallback Expiry Time: {fallback_time.strftime('%I:%M:%S %p PKT')}")
#     return fallback_time

# def get_page_id():
#     print("[*] Verifying Facebook Access Token...")
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res:
#             print(f"[+] Connected successfully to Page: {res.get('name', 'Unknown')} (ID: {res['id']})")
#             return res.get('id')
#         else:
#             print(f"[-] API Response error: {res}")
#     except Exception as e: 
#         print(f"[💥] Token Check Error: {e}")
#     return None

# # ==========================================
# # WORKER 1: 10 SECONDS VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥 Worker 1] Initiating Stream Capture...")
#     print(f"[*] Target File: {filename} | Duration: {duration} seconds")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
#     print("[*] Executing FFmpeg command...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(filename):
#         print(f"[✅ Worker 1] Capture successful! File saved.")
#         return True
#     else:
#         print(f"[❌ Worker 1] Capture failed! File not created.")
#         return False

# # ==========================================
# # WORKER 2: VIDEO EDITING (Blur + Merge + Audio)
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬 Worker 2] Starting Video Editing Engine (MoviePy)...")
#     try:
#         print(f"[*] Loading Dynamic Clip: {dynamic_vid}")
#         dyn_clip = VideoFileClip(dynamic_vid)
        
#         print(f"[*] Loading Static Clip: {static_vid}")
#         stat_clip = VideoFileClip(static_vid)
        
#         print(f"[*] Resizing dynamic clip to match static clip size: {stat_clip.size}")
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame):
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(20)))

#         print("[*] Applying Gaussian Blur (Radius: 20) to dynamic clip...")
#         dyn_clip = dyn_clip.fl_image(blur)
        
#         print("[*] Concatenating (Merging) dynamic and static clips...")
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         print(f"[*] Loading Custom Audio: {custom_audio} and looping to match video duration...")
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
        
#         print("[*] Setting final audio track...")
#         final_video = merged.set_audio(final_audio)

#         print(f"[*] Rendering Final Video to: {output_vid}")
#         print("[*] Settings: codec=libx264, audio=aac, preset=ultrafast")
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)

#         print("[*] Closing resources and freeing up RAM...")
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
        
#         print("[✅ Worker 2] Editing Completed Successfully!")
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 2] Edit Error: {e}")
#         return False

# # ==========================================
# # WORKER 3: FACEBOOK UPLOAD & COMMENT WITH IMAGE
# # ==========================================
# def worker_3_upload(video_path, page_id, clip_number):
#     print(f"\n[📤 Worker 3] Preparing Facebook Upload...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     title, desc = generate_unique_metadata(clip_number)
    
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     try:
#         print(f"[*] Pushing video file '{video_path}' to Graph API...")
#         # ⚠️ 'video.mp4' taake Facebook Filename Too Long error na de
#         with open(video_path, "rb") as f:
#             res = requests.post(url, data=payload, files={"source": ("video.mp4", f, "video/mp4")}).json()
            
#         if "id" in res:
#             print(f"[✅ Worker 3] Video Upload SUCCESS! (Post ID: {res['id']})")
            
#             # --- COMMENT WITH IMAGE LOGIC ---
#             print("[⏳] Waiting 15 seconds for Facebook to process the video before commenting...")
#             time.sleep(15) 
            
#             print("[💬 Worker 3] Preparing Comment with Promotional Image and Link...")
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
#             comment_img_path = "comment_image.jpeg" 
            
#             print(f"[*] Checking for '{comment_img_path}' in directory...")
#             if os.path.exists(comment_img_path):
#                 print(f"[+] Image found! Uploading comment with image...")
#                 with open(comment_img_path, "rb") as img:
#                     comment_res = requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 if 'id' in comment_res.json():
#                     print("[✅ Worker 3] Photo Comment SUCCESS!")
#                 else:
#                     print(f"[⚠️ Worker 3] Comment failed: {comment_res.json()}")
#             else:
#                 print(f"[⚠️] '{comment_img_path}' NOT FOUND! Proceeding with Text-Only comment...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅ Worker 3] Text Comment Placed.")
            
#             return True
#         else:
#              print(f"[❌ Worker 3] Facebook API Error: {res}")
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Crash: {e}")
#     return False

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: 
#         print("[❌] FATAL: Token invalid! Halting script.")
#         return 

#     print("[*] Initiating First Link Fetch Cycle...")
#     data = get_link_with_headers()
#     if not data: 
#         print("[❌] FATAL: M3U8 Link nahi mila. Halting script.")
#         return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     print("[*] Checking required local assets...")
#     if not os.path.exists(static_video) or not os.path.exists(audio_file):
#          print(f"[⚠️] WARNING: Missing '{static_video}' or '{audio_file}'. Worker 2 WILL fail!")
#     else:
#          print(f"[+] Local assets found.")
    
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*40)
#         print(f"--- 🔄 Starting Video Cycle #{clip_counter} ---")
#         print(f"[-] Bot Uptime: {int(elapsed_time/60)} minutes")
#         print(f"[-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
#         print("-" * 40)
        
#         # 1. Relay Race Check (5h 30m)
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             print("[🚨] Relay Timer Reached (5h 30m). Executing hand-off...")
#             trigger_next_run()
#             next_run_triggered = True 
            
#         # 2. Suicide Check (5h 50m - Stop before GitHub forcefully kills it)
#         if elapsed_time > END_TIME_LIMIT:
#             print("\n[🛑] MAXIMUM LIFETIME REACHED (5h 50m). Naya bot pichay start ho chuka hai. Main gracefully band ho raha hoon.")
#             break
        
#         # 3. Link Expiry Check (2 Min pehle)
#         if time_left_seconds <= 120:
#             print("\n[🚨 ALERT] Link expire hone wala hai. Pausing operations to fetch new link...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#                 print("[+] Expiry parameters updated successfully.")
#             else:
#                 print("[⚠️] Failed to fetch new link. Retrying in 60 seconds...")
#                 time.sleep(60); continue 
        
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # Action Flow
#         if worker_1_capture_video(data, raw_vid, duration=10):
#             if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                 worker_3_upload(final_vid, page_id, clip_counter)
        
#         # 🧹 GARBAGE COLLECTOR (RAM Hack)
#         print("\n[🧹 Cleanup Engine Started]")
#         if os.path.exists(raw_vid): 
#             os.remove(raw_vid)
#             print(f"  [-] Deleted: {raw_vid}")
#         if os.path.exists(final_vid): 
#             os.remove(final_vid)
#             print(f"  [-] Deleted: {final_vid}")
#         print("[🧹] Temporary videos hard-drive se ura di gayi hain. RAM freed.")
            
#         clip_counter += 1
#         print(f"\n[⏳] Cycle Complete. Agli video ke liye {WAIT_TIME_SECONDS} seconds wait kar raha hoon...")
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()








































































# ================= good , upper waley mei just 100 title and 100 description add kar rahey hai =======================


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
# print("[*] Checking Pillow version and applying Superman Patch if needed...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅] Superman Patch Applied: ANTIALIAS redirected to LANCZOS.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[*] Loading MoviePy modules...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[*] Initializing Settings and Environment Variables...")
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
# WAIT_TIME_SECONDS = 300  
# print(f"[*] System Timezone set to PKT (+5).")
# print(f"[*] Loop Wait Time set to {WAIT_TIME_SECONDS} seconds.")

# # Relay Race Timers
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 

# # ==========================================
# # 🧠 ANTI-SPAM (SPINTAX) GENERATOR
# # ==========================================

# # ==========================================
# # 🧠 ANTI-SPAM (SPINTAX) GENERATOR (UPDATED)
# # ==========================================
# def generate_unique_metadata(clip_number):
#     print(f"\n[🧠] Generating Unique Metadata (Spintax) for Clip #{clip_number}...")
    
#     # 1. Hashtags Shuffle
#     tags_list = HASHTAGS.split()
#     random.shuffle(tags_list)
#     shuffled_tags = " ".join(tags_list)
    
#     # 2. Dynamic Title Generator (NO EMOJIS, Team A vs Team B FIRST)
#     # Yeh words har dafa aagay peechay honge taake title naya lagay
#     title_buzzwords = ["Live Action", "Today Match", "Exclusive", "Highlights", "Full Coverage", "Stream"]
#     random.shuffle(title_buzzwords)
#     dynamic_suffix = " | ".join(title_buzzwords[:2]) # Koi se 2 random words utha kar jor dega
    
#     # Title Hamesha MATCH_TITLE (Team A vs Team B) se shuru hoga
#     chosen_title = f"{MATCH_TITLE} - {dynamic_suffix}"
    
#     # ✂️ THE SMART TRIMMER (Facebook API Byte Limit Fix - 100 Chars)
#     if len(chosen_title) > 240:
#         print(f"[⚠️] Title lamba tha. Safe size par trim kar raha hoon...")
#         chosen_title = chosen_title[:97] + "..."
        
#     # 3. Emojis (Sirf Description ke liye)
#     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
#     emo = random.sample(emojis, 3) 
#     current_time = datetime.now(PKT).strftime("%I:%M %p")
    
#     # 4. Description Generator
#     # Rule Followed: Start with Exact Title -> Emojis -> Description Body
#     descriptions = [
#         f"{chosen_title} {emo[0]} {emo[1]}\n\n{MATCH_DESC}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{shuffled_tags}",
#         f"{chosen_title} {emo[2]} {emo[0]}\n\n{shuffled_tags}\n\n{MATCH_DESC}\n\n🎥 Frame: {clip_number} (Time: {current_time})\nCheck comments for 0 buffering stream link! 👇"
#     ]
    
#     chosen_desc = random.choice(descriptions)
    
#     print(f"  --> Selected Title (No Emojis): {chosen_title}")
#     print(f"  --> Emojis Used in Desc: {emo}")
#     return chosen_title, chosen_desc








# # ================

# # def generate_unique_metadata(clip_number):
# #     print(f"\n[🧠] Generating Unique Metadata (Spintax) for Clip #{clip_number}...")
# #     tags_list = HASHTAGS.split()
# #     random.shuffle(tags_list)
# #     shuffled_tags = " ".join(tags_list)
    
# #     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
# #     emo = random.sample(emojis, 3) 
# #     current_time = datetime.now(PKT).strftime("%I:%M %p")
    
# #     titles = [
# #         f"🔴 LIVE: {MATCH_TITLE} {emo[0]}",
# #         f"{emo[1]} EXCLUSIVE HIGHLIGHT: {MATCH_TITLE}",
# #         f"⚡ {MATCH_TITLE} - Best Moment {emo[2]}"
# #     ]
    
# #     descriptions = [
# #         f"{MATCH_DESC}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{shuffled_tags}",
# #         f"Current match situation! {emo[1]}\n\n{shuffled_tags}\n\n{MATCH_DESC}\n\n🎥 Frame: {clip_number} (Time: {current_time})\nCheck comments for 0 buffering stream link! 👇"
# #     ]
    
# #     chosen_title = random.choice(titles)
# #     chosen_desc = random.choice(descriptions)
    
# #     # ✂️ THE SMART TRIMMER (Facebook API Byte Limit Fix)
# #     if len(chosen_title) > 240:
# #         print(f"[⚠️] Title lamba tha. Facebook ke byte-limit ke liye safe size par trim kar raha hoon...")
# #         # 97 characters tak rakho aur aagay 3 dots lagao
# #         chosen_title = chosen_title[:97] + "..."
        
# #     print(f"  --> Selected Title: {chosen_title}")
# #     print(f"  --> Emojis Used: {emo}")
# #     return chosen_title, chosen_desc

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n" + "="*50)
#     print(" ⏰ RELAY RACE: STARTING NEXT GITHUB BOT ⏰")
#     print("="*50)
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
    
#     print(f"[*] Preparing API Request for Repo: {repo}, Branch: {branch}...")
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
#         print("[*] Sending dispatch trigger to GitHub API...")
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204: 
#             print("[✅] SUCCESS! Naya Bot Background Mein Start Ho Gaya Hai!")
#         else:
#             print(f"[⚠️] Unexpected Status Code: {res.status_code} - {res.text}")
#     except Exception as e:
#         print(f"[💥] Relay Race Failed: {e}")

# # ==========================================
# # STEP 1: LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print(f"\n[🔍] Starting Selenium Webdriver with Proxy...")
#     print(f"[*] Target URL: {TARGET_WEBSITE}")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         print("[*] Initializing ChromeDriverManager...")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
#         print("[*] Loading Website...")
#         driver.get(TARGET_WEBSITE)
        
#         print("[⏳] Waiting 5 seconds for page load and Cloudflare bypass...")
#         time.sleep(5)
        
#         print("[*] Scanning Network Requests for .m3u8 token...")
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 data = {"url": request.url, "ua": request.headers.get('User-Agent', ''), "cookie": request.headers.get('Cookie', ''), "referer": request.headers.get('Referer', TARGET_WEBSITE)}
#                 print(f"🎉 [BINGO] M3U8 Link Bypassed & Captured!")
#                 print(f"  --> Found URL: {request.url[:80]}...") 
#                 break
                
#         if not data:
#             print("[⚠️] M3U8 link NOT found in network requests.")
            
#     except Exception as e: 
#         print(f"[💥] Selenium Error: {e}")
#     finally:
#         if driver: 
#             print("[*] Closing Chrome browser and releasing proxy...")
#             driver.quit()
#     return data

# def calculate_expiry_time(url):
#     print("[*] Calculating Link Expiry Time...")
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: 
#             exp_time = datetime.fromtimestamp(exp, PKT)
#             print(f"[⏰] Link will expire at: {exp_time.strftime('%I:%M:%S %p PKT')}")
#             return exp_time
#     except Exception as e: 
#         print(f"[-] Could not parse expiry: {e}")
#         pass
    
#     fallback_time = datetime.now(PKT) + timedelta(hours=2)
#     print(f"[⚠️] Setting Fallback Expiry Time: {fallback_time.strftime('%I:%M:%S %p PKT')}")
#     return fallback_time

# def get_page_id():
#     print("[*] Verifying Facebook Access Token...")
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res:
#             print(f"[+] Connected successfully to Page: {res.get('name', 'Unknown')} (ID: {res['id']})")
#             return res.get('id')
#         else:
#             print(f"[-] API Response error: {res}")
#     except Exception as e: 
#         print(f"[💥] Token Check Error: {e}")
#     return None

# # ==========================================
# # WORKER 1: 10 SECONDS VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥 Worker 1] Initiating Stream Capture...")
#     print(f"[*] Target File: {filename} | Duration: {duration} seconds")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
#     print("[*] Executing FFmpeg command...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(filename):
#         print(f"[✅ Worker 1] Capture successful! File saved.")
#         return True
#     else:
#         print(f"[❌ Worker 1] Capture failed! File not created.")
#         return False

# # ==========================================
# # WORKER 2: VIDEO EDITING (Blur + Merge + Audio)
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬 Worker 2] Starting Video Editing Engine (MoviePy)...")
#     try:
#         print(f"[*] Loading Dynamic Clip: {dynamic_vid}")
#         dyn_clip = VideoFileClip(dynamic_vid)
        
#         print(f"[*] Loading Static Clip: {static_vid}")
#         stat_clip = VideoFileClip(static_vid)
        
#         print(f"[*] Resizing dynamic clip to match static clip size: {stat_clip.size}")
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame):
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(20)))

#         print("[*] Applying Gaussian Blur (Radius: 20) to dynamic clip...")
#         dyn_clip = dyn_clip.fl_image(blur)
        
#         print("[*] Concatenating (Merging) dynamic and static clips...")
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         print(f"[*] Loading Custom Audio: {custom_audio} and looping to match video duration...")
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
        
#         print("[*] Setting final audio track...")
#         final_video = merged.set_audio(final_audio)

#         print(f"[*] Rendering Final Video to: {output_vid}")
#         print("[*] Settings: codec=libx264, audio=aac, preset=ultrafast")
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)

#         print("[*] Closing resources and freeing up RAM...")
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
        
#         print("[✅ Worker 2] Editing Completed Successfully!")
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 2] Edit Error: {e}")
#         return False

# # ==========================================
# # WORKER 3: FACEBOOK UPLOAD & COMMENT WITH IMAGE
# # ==========================================
# def worker_3_upload(video_path, page_id, clip_number):
#     print(f"\n[📤 Worker 3] Preparing Facebook Upload...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     title, desc = generate_unique_metadata(clip_number)
    
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     try:
#         print(f"[*] Pushing video file '{video_path}' to Graph API...")
#         # ⚠️ YAHAN FIX HAI: 'video.mp4' taake Facebook Filename Too Long error na de
#         with open(video_path, "rb") as f:
#             res = requests.post(url, data=payload, files={"source": ("video.mp4", f, "video/mp4")}).json()
            
#         if "id" in res:
#             print(f"[✅ Worker 3] Video Upload SUCCESS! (Post ID: {res['id']})")
            
#             # --- COMMENT WITH IMAGE LOGIC ---
#             print("[⏳] Waiting 15 seconds for Facebook to process the video before commenting...")
#             time.sleep(15) 
            
#             print("[💬 Worker 3] Preparing Comment with Promotional Image and Link...")
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
#             comment_img_path = "comment_image.jpeg" 
            
#             print(f"[*] Checking for '{comment_img_path}' in directory...")
#             if os.path.exists(comment_img_path):
#                 print(f"[+] Image found! Uploading comment with image...")
#                 with open(comment_img_path, "rb") as img:
#                     comment_res = requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 if 'id' in comment_res.json():
#                     print("[✅ Worker 3] Photo Comment SUCCESS!")
#                 else:
#                     print(f"[⚠️ Worker 3] Comment failed: {comment_res.json()}")
#             else:
#                 print(f"[⚠️] '{comment_img_path}' NOT FOUND! Proceeding with Text-Only comment...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅ Worker 3] Text Comment Placed.")
            
#             return True
#         else:
#              print(f"[❌ Worker 3] Facebook API Error: {res}")
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Crash: {e}")
#     return False

# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: 
#         print("[❌] FATAL: Token invalid! Halting script.")
#         return 

#     print("[*] Initiating First Link Fetch Cycle...")
#     data = get_link_with_headers()
#     if not data: 
#         print("[❌] FATAL: M3U8 Link nahi mila. Halting script.")
#         return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     print("[*] Checking required local assets...")
#     if not os.path.exists(static_video) or not os.path.exists(audio_file):
#          print(f"[⚠️] WARNING: Missing '{static_video}' or '{audio_file}'. Worker 2 WILL fail!")
#     else:
#          print(f"[+] Local assets found.")
    
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*40)
#         print(f"--- 🔄 Starting Video Cycle #{clip_counter} ---")
#         print(f"[-] Bot Uptime: {int(elapsed_time/60)} minutes")
#         print(f"[-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
#         print("-" * 40)
        
#         # 1. Relay Race Check (5h 30m)
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             print("[🚨] Relay Timer Reached (5h 30m). Executing hand-off...")
#             trigger_next_run()
#             next_run_triggered = True 
            
#         # 2. Suicide Check (5h 50m - Stop before GitHub forcefully kills it)
#         if elapsed_time > END_TIME_LIMIT:
#             print("\n[🛑] MAXIMUM LIFETIME REACHED (5h 50m). Naya bot pichay start ho chuka hai. Main gracefully band ho raha hoon.")
#             break
        
#         # 3. Link Expiry Check (2 Min pehle)
#         if time_left_seconds <= 120:
#             print("\n[🚨 ALERT] Link expire hone wala hai. Pausing operations to fetch new link...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#                 print("[+] Expiry parameters updated successfully.")
#             else:
#                 print("[⚠️] Failed to fetch new link. Retrying in 60 seconds...")
#                 time.sleep(60); continue 
        
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # Action Flow
#         if worker_1_capture_video(data, raw_vid, duration=10):
#             if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                 worker_3_upload(final_vid, page_id, clip_counter)
        
#         # 🧹 GARBAGE COLLECTOR (RAM Hack)
#         print("\n[🧹 Cleanup Engine Started]")
#         if os.path.exists(raw_vid): 
#             os.remove(raw_vid)
#             print(f"  [-] Deleted: {raw_vid}")
#         if os.path.exists(final_vid): 
#             os.remove(final_vid)
#             print(f"  [-] Deleted: {final_vid}")
#         print("[🧹] Temporary videos hard-drive se ura di gayi hain. RAM freed.")
            
#         clip_counter += 1
#         print(f"\n[⏳] Cycle Complete. Agli video ke liye {WAIT_TIME_SECONDS} seconds wait kar raha hoon...")
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()
































































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
# print("[*] Checking Pillow version and applying Superman Patch if needed...")
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
#     print("[✅] Superman Patch Applied: ANTIALIAS redirected to LANCZOS.")

# from datetime import datetime, timezone, timedelta
# from seleniumwire import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# # MoviePy for Video Editing
# print("[*] Loading MoviePy modules...")
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# import moviepy.audio.fx.all as afx

# # ==========================================
# # ⚙️ SETTINGS & TOKENS
# # ==========================================
# print("\n[*] Initializing Settings and Environment Variables...")
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
# WAIT_TIME_SECONDS = 300  
# print(f"[*] System Timezone set to PKT (+5).")
# print(f"[*] Loop Wait Time set to {WAIT_TIME_SECONDS} seconds.")

# # Relay Race Timers
# START_TIME = time.time()
# RESTART_TRIGGER_TIME = (5 * 60 * 60) + (30 * 60) 
# END_TIME_LIMIT = (5 * 60 * 60) + (50 * 60) 

# # ==========================================
# # 🧠 ANTI-SPAM (SPINTAX) GENERATOR
# # ==========================================


# # ==========================================
# # 🧠 ANTI-SPAM (SPINTAX) GENERATOR
# # ==========================================
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
    
#     # ✂️ THE SMART TRIMMER (Facebook API 255 Char Limit Fix)
#     if len(chosen_title) > 250:
#         print(f"[⚠️] Title lamba ho gaya tha ({len(chosen_title)} chars). Facebook ke liye trim kar raha hoon...")
#         # 247 characters tak rakho aur aagay 3 dots lagao taake total 250 rahay
#         chosen_title = chosen_title[:247] + "..."
        
#     print(f"  --> Selected Title: {chosen_title}")
#     print(f"  --> Emojis Used: {emo}")
#     return chosen_title, chosen_desc








# # ===============================================

# # def generate_unique_metadata(clip_number):
# #     print(f"\n[🧠] Generating Unique Metadata (Spintax) for Clip #{clip_number}...")
# #     tags_list = HASHTAGS.split()
# #     random.shuffle(tags_list)
# #     shuffled_tags = " ".join(tags_list)
    
# #     emojis = ["🔥", "🏏", "⚡", "🏆", "💥", "😱", "📺", "🚀"]
# #     emo = random.sample(emojis, 3) 
# #     current_time = datetime.now(PKT).strftime("%I:%M %p")
    
# #     titles = [
# #         f"🔴 LIVE: {MATCH_TITLE} {emo[0]}",
# #         f"{emo[1]} EXCLUSIVE HIGHLIGHT: {MATCH_TITLE}",
# #         f"⚡ {MATCH_TITLE} - Best Moment {emo[2]}"
# #     ]
    
# #     descriptions = [
# #         f"{MATCH_DESC}\n\n⏱️ Update: {current_time} | Clip #{clip_number}\n\n👇 Watch Full Match Link in First Comment!\n\n{shuffled_tags}",
# #         f"Current match situation! {emo[1]}\n\n{shuffled_tags}\n\n{MATCH_DESC}\n\n🎥 Frame: {clip_number} (Time: {current_time})\nCheck comments for 0 buffering stream link! 👇"
# #     ]
    
# #     chosen_title = random.choice(titles)
# #     chosen_desc = random.choice(descriptions)
    
# #     print(f"  --> Selected Title: {chosen_title}")
# #     print(f"  --> Emojis Used: {emo}")
# #     return chosen_title, chosen_desc

# # ==========================================
# # 🔄 RELAY RACE (AUTO RESTART)
# # ==========================================
# def trigger_next_run():
#     print("\n" + "="*50)
#     print(" ⏰ RELAY RACE: STARTING NEXT GITHUB BOT ⏰")
#     print("="*50)
#     token = os.environ.get('GH_PAT')
#     repo = os.environ.get('GITHUB_REPOSITORY') 
#     branch = os.environ.get('GITHUB_REF_NAME', 'main')
    
#     print(f"[*] Preparing API Request for Repo: {repo}, Branch: {branch}...")
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
#         print("[*] Sending dispatch trigger to GitHub API...")
#         res = requests.post(url, headers=headers, json=data)
#         if res.status_code == 204: 
#             print("[✅] SUCCESS! Naya Bot Background Mein Start Ho Gaya Hai!")
#         else:
#             print(f"[⚠️] Unexpected Status Code: {res.status_code} - {res.text}")
#     except Exception as e:
#         print(f"[💥] Relay Race Failed: {e}")

# # ==========================================
# # STEP 1: LINK CHURANA
# # ==========================================
# def get_link_with_headers():
#     print(f"\n[🔍] Starting Selenium Webdriver with Proxy...")
#     print(f"[*] Target URL: {TARGET_WEBSITE}")
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless=new') 
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--mute-audio')
#     seleniumwire_options = {'proxy': {'http': PROXY_URL, 'https': PROXY_URL, 'no_proxy': 'localhost,127.0.0.1'}, 'disable_encoding': True}

#     driver = None; data = None
#     try:
#         print("[*] Initializing ChromeDriverManager...")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
        
#         print("[*] Loading Website...")
#         driver.get(TARGET_WEBSITE)
        
#         print("[⏳] Waiting 5 seconds for page load and Cloudflare bypass...")
#         time.sleep(5)
        
#         print("[*] Scanning Network Requests for .m3u8 token...")
#         for request in driver.requests:
#             if request.response and ".m3u8" in request.url:
#                 data = {"url": request.url, "ua": request.headers.get('User-Agent', ''), "cookie": request.headers.get('Cookie', ''), "referer": request.headers.get('Referer', TARGET_WEBSITE)}
#                 print(f"🎉 [BINGO] M3U8 Link Bypassed & Captured!")
#                 print(f"  --> Found URL: {request.url[:80]}...") # Print half link for safety
#                 break
                
#         if not data:
#             print("[⚠️] M3U8 link NOT found in network requests.")
            
#     except Exception as e: 
#         print(f"[💥] Selenium Error: {e}")
#     finally:
#         if driver: 
#             print("[*] Closing Chrome browser and releasing proxy...")
#             driver.quit()
#     return data

# def calculate_expiry_time(url):
#     print("[*] Calculating Link Expiry Time...")
#     try:
#         params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
#         exp = int(params.get('expires', params.get('e', [0]))[0])
#         if exp: 
#             exp_time = datetime.fromtimestamp(exp, PKT)
#             print(f"[⏰] Link will expire at: {exp_time.strftime('%I:%M:%S %p PKT')}")
#             return exp_time
#     except Exception as e: 
#         print(f"[-] Could not parse expiry: {e}")
#         pass
    
#     fallback_time = datetime.now(PKT) + timedelta(hours=2)
#     print(f"[⚠️] Setting Fallback Expiry Time: {fallback_time.strftime('%I:%M:%S %p PKT')}")
#     return fallback_time

# def get_page_id():
#     print("[*] Verifying Facebook Access Token...")
#     try:
#         res = requests.get("https://graph.facebook.com/v18.0/me", params={"access_token": FB_ACCESS_TOKEN, "fields": "id,name"}).json()
#         if 'id' in res:
#             print(f"[+] Connected successfully to Page: {res.get('name', 'Unknown')} (ID: {res['id']})")
#             return res.get('id')
#         else:
#             print(f"[-] API Response error: {res}")
#     except Exception as e: 
#         print(f"[💥] Token Check Error: {e}")
#     return None

# # ==========================================
# # WORKER 1: 10 SECONDS VIDEO CAPTURE
# # ==========================================
# def worker_1_capture_video(data, filename, duration=10):
#     print(f"\n[🎥 Worker 1] Initiating Stream Capture...")
#     print(f"[*] Target File: {filename} | Duration: {duration} seconds")
#     headers_cmd = f"User-Agent: {data['ua']}\r\nReferer: {data['referer']}\r\nCookie: {data['cookie']}"
#     cmd = ['ffmpeg', '-y', '-headers', headers_cmd, '-i', data['url'], '-t', str(duration), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filename]
    
#     print("[*] Executing FFmpeg command...")
#     subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
#     if os.path.exists(filename):
#         print(f"[✅ Worker 1] Capture successful! File saved.")
#         return True
#     else:
#         print(f"[❌ Worker 1] Capture failed! File not created.")
#         return False

# # ==========================================
# # WORKER 2: VIDEO EDITING (Blur + Merge + Audio)
# # ==========================================
# def worker_2_edit_video(dynamic_vid, static_vid, custom_audio, output_vid):
#     print(f"\n[🎬 Worker 2] Starting Video Editing Engine (MoviePy)...")
#     try:
#         print(f"[*] Loading Dynamic Clip: {dynamic_vid}")
#         dyn_clip = VideoFileClip(dynamic_vid)
        
#         print(f"[*] Loading Static Clip: {static_vid}")
#         stat_clip = VideoFileClip(static_vid)
        
#         print(f"[*] Resizing dynamic clip to match static clip size: {stat_clip.size}")
#         dyn_clip = dyn_clip.resize(stat_clip.size)

#         def blur(frame):
#             return np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(30)))

#         print("[*] Applying Gaussian Blur (Radius: 20) to dynamic clip...")
#         dyn_clip = dyn_clip.fl_image(blur)
        
#         print("[*] Concatenating (Merging) dynamic and static clips...")
#         merged = concatenate_videoclips([dyn_clip, stat_clip])
        
#         print(f"[*] Loading Custom Audio: {custom_audio} and looping to match video duration...")
#         audio = AudioFileClip(custom_audio)
#         final_audio = afx.audio_loop(audio, duration=merged.duration)
        
#         print("[*] Setting final audio track...")
#         final_video = merged.set_audio(final_audio)

#         print(f"[*] Rendering Final Video to: {output_vid}")
#         print("[*] Settings: codec=libx264, audio=aac, preset=ultrafast")
#         # Ultra-fast rendering taake GitHub server par load na pare
#         final_video.write_videofile(output_vid, codec="libx264", audio_codec="aac", fps=stat_clip.fps, preset="ultrafast", logger=None)

#         print("[*] Closing resources and freeing up RAM...")
#         dyn_clip.close(); stat_clip.close(); audio.close(); final_video.close()
        
#         print("[✅ Worker 2] Editing Completed Successfully!")
#         return True
#     except Exception as e:
#         print(f"[❌ Worker 2] Edit Error: {e}")
#         return False

# # ==========================================
# # WORKER 3: FACEBOOK UPLOAD & COMMENT WITH IMAGE
# # ==========================================
# def worker_3_upload(video_path, page_id, clip_number):
#     print(f"\n[📤 Worker 3] Preparing Facebook Upload...")
#     url = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
#     title, desc = generate_unique_metadata(clip_number)
    
#     payload = {"title": title, "description": desc, "access_token": FB_ACCESS_TOKEN}
    
#     try:
#         print(f"[*] Pushing video file '{video_path}' to Graph API...")
#         with open(video_path, "rb") as f:
#             res = requests.post(url, data=payload, files={"source": f}).json()
            
#         if "id" in res:
#             print(f"[✅ Worker 3] Video Upload SUCCESS! (Post ID: {res['id']})")
            
#             # --- COMMENT WITH IMAGE LOGIC ---
#             print("[⏳] Waiting 15 seconds for Facebook to process the video before commenting...")
#             time.sleep(15) 
            
#             print("[💬 Worker 3] Preparing Comment with Promotional Image and Link...")
#             comment_url = f"https://graph.facebook.com/v18.0/{res['id']}/comments"
#             comment_text = f"📺 Watch Full Match Without Buffering Here: https://bulbul4u-live.xyz"
#             comment_img_path = "comment_image.jpeg" 
            
#             print(f"[*] Checking for '{comment_img_path}' in directory...")
#             if os.path.exists(comment_img_path):
#                 print(f"[+] Image found! Uploading comment with image...")
#                 with open(comment_img_path, "rb") as img:
#                     comment_res = requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN}, files={"source": img})
#                 if 'id' in comment_res.json():
#                     print("[✅ Worker 3] Photo Comment SUCCESS!")
#                 else:
#                     print(f"[⚠️ Worker 3] Comment failed: {comment_res.json()}")
#             else:
#                 print(f"[⚠️] '{comment_img_path}' NOT FOUND! Proceeding with Text-Only comment...")
#                 requests.post(comment_url, data={"message": comment_text, "access_token": FB_ACCESS_TOKEN})
#                 print("[✅ Worker 3] Text Comment Placed.")
            
#             return True
#         else:
#              print(f"[❌ Worker 3] Facebook API Error: {res}")
#     except Exception as e:
#         print(f"[💥 Worker 3] Upload Crash: {e}")
#     return False


# # ==========================================
# # MAIN LOOP (THE BRAIN)
# # ==========================================
# def main():
#     print("\n" + "="*50)
#     print("   🚀 ULTIMATE CLOUD VIDEO BOT STARTED")
#     print("="*50)
    
#     page_id = get_page_id()
#     if not page_id: 
#         print("[❌] FATAL: Token invalid! Halting script.")
#         return 

#     print("[*] Initiating First Link Fetch Cycle...")
#     data = get_link_with_headers()
#     if not data: 
#         print("[❌] FATAL: M3U8 Link nahi mila. Halting script.")
#         return 
        
#     expiry_dt = calculate_expiry_time(data['url'])
#     clip_counter = 1
#     next_run_triggered = False
    
#     static_video = "main_video.mp4"
#     audio_file = "marya_live.mp3"
    
#     print("[*] Checking required local assets...")
#     if not os.path.exists(static_video) or not os.path.exists(audio_file):
#          print(f"[⚠️] WARNING: Missing '{static_video}' or '{audio_file}'. Worker 2 WILL fail!")
#     else:
#          print(f"[+] Local assets found.")
    
#     while True:
#         elapsed_time = time.time() - START_TIME
#         current_time = datetime.now(PKT)
#         time_left_seconds = (expiry_dt - current_time).total_seconds()
        
#         print(f"\n" + "-"*40)
#         print(f"--- 🔄 Starting Video Cycle #{clip_counter} ---")
#         print(f"[-] Bot Uptime: {int(elapsed_time/60)} minutes")
#         print(f"[-] Link Time Remaining: {int(time_left_seconds/60)} minutes")
#         print("-" * 40)
        
#         # 1. Relay Race Check (5h 30m)
#         if elapsed_time > RESTART_TRIGGER_TIME and not next_run_triggered:
#             print("[🚨] Relay Timer Reached (5h 30m). Executing hand-off...")
#             trigger_next_run()
#             next_run_triggered = True 
            
#         # 2. Suicide Check (5h 50m - Stop before GitHub forcefully kills it)
#         if elapsed_time > END_TIME_LIMIT:
#             print("\n[🛑] MAXIMUM LIFETIME REACHED (5h 50m). Naya bot pichay start ho chuka hai. Main gracefully band ho raha hoon.")
#             break
        
#         # 3. Link Expiry Check (2 Min pehle)
#         if time_left_seconds <= 120:
#             print("\n[🚨 ALERT] Link expire hone wala hai. Pausing operations to fetch new link...")
#             new_data = get_link_with_headers()
#             if new_data:
#                 data = new_data
#                 expiry_dt = calculate_expiry_time(data['url'])
#                 print("[+] Expiry parameters updated successfully.")
#             else:
#                 print("[⚠️] Failed to fetch new link. Retrying in 60 seconds...")
#                 time.sleep(60); continue 
        
#         raw_vid = f"raw_{clip_counter}.mp4"
#         final_vid = f"final_{clip_counter}.mp4"
        
#         # Action Flow
#         if worker_1_capture_video(data, raw_vid, duration=10):
#             if worker_2_edit_video(raw_vid, static_video, audio_file, final_vid):
#                 worker_3_upload(final_vid, page_id, clip_counter)
        
#         # 🧹 GARBAGE COLLECTOR (RAM Hack)
#         print("\n[🧹 Cleanup Engine Started]")
#         if os.path.exists(raw_vid): 
#             os.remove(raw_vid)
#             print(f"  [-] Deleted: {raw_vid}")
#         if os.path.exists(final_vid): 
#             os.remove(final_vid)
#             print(f"  [-] Deleted: {final_vid}")
#         print("[🧹] Temporary videos hard-drive se ura di gayi hain. RAM freed.")
            
#         clip_counter += 1
#         print(f"\n[⏳] Cycle Complete. Agli video ke liye {WAIT_TIME_SECONDS} seconds wait kar raha hoon...")
#         time.sleep(WAIT_TIME_SECONDS)

# if __name__ == "__main__":
#     main()















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
