
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "13323016")

API_HASH = os.environ.get("API_HASH", "68e791e616100248b0a53ae86a661a12")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7718585217:AAF7KwY_bZA7oEw6zS4zsyceOCgrHHXSRZU") 

DB_NAME = os.environ.get("DB_NAME","xxx")     

DB_URL = os.environ.get("DB_URL","xxx")

FLOOD = int(os.environ.get("FLOOD", "10"))
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "100"))

# FOR SESSION LOGIN - ONLY OWNER CAN LOGIN 
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/nr6nqC4/IMG-20241030-153858-361.jpg")

# CAN HAVE MULTIPLE ADMINS
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6534916669 5965340120').split()]

PORT = os.environ.get("PORT", "8080")
BOT_SESSION_NAME = os.environ.get("BOT_SESSION_NAME", "Lazydeveloper")

DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002397221880"))

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
