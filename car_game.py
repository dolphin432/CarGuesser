import json
import random
import os
import tkinter as tk
from tkinter import font as tkfont
import threading
import difflib

# Colors
BG      = "#0d0d0d"
BG2     = "#161616"
BG3     = "#1e1e1e"
ACCENT  = "#e8e8e8"
GREEN   = "#22c55e"
YELLOW  = "#eab308"
RED     = "#ef4444"
GRAY    = "#404040"
TEXT    = "#f0f0f0"
SUBTEXT = "#888888"
BORDER  = "#2a2a2a"

ENGINE_ORDER = ["I3", "I4", "Flat-4", "I5", "I6", "V6", "Flat-6", "V8", "V10", "V12", "V16", "W12", "W16", "Rotary", "Electric"]

CONTINENTS = {
    "Europe": ["Italy", "Germany", "UK", "France", "Sweden", "Austria",
               "Switzerland", "Czech Republic", "Denmark"],
    "North America": ["USA", "Canada"],
    "Asia": ["Japan", "South Korea", "China", "UAE"],
    "Other": []
}

LANGUAGES = {
    "en": {
        "title_sub":      "Guess the Car!",
        "normal_mode":    "▶  Normal Mode",
        "hint_mode":      "💡  Hint Mode",
        "expert_mode":    "🧠  Expert Mode",
        "classic_mode":   "⭐  Classic Mode",
        "classic_lbl":    "⭐ Classic Mode",
        "stats_btn":      "📊  Statistics",
        "settings_btn":   "⚙️  Settings",
        "guesses_left":   "Guess {}/{}",
        "correct":        "Correct",
        "close":          "Close (same continent / ±20% price / adjacent engine)",
        "wrong":          "Wrong",
        "car_col":        "Car",
        "brand_col":      "Brand",
        "engine_col":     "Engine",
        "price_col":      "Price",
        "country_col":    "Country",
        "year_col":       "Year",
        "hp_col":         "HP",
        "hint_btn":       "💡 Get Hint (i)",
        "no_hint":        "💡 No more hints!",
        "already_used":   "⚠ Already guessed this car!",
        "not_found":      "⚠ Car not found! Type the exact name.",
        "congrats":       "🎉 Correct in {} guesses!",
        "failed":         "💀 You lost! Answer:",
        "play_again":     "Play Again",
        "main_menu":      "Main Menu",
        "stats_normal":   "Normal Mode",
        "stats_classic":  "Classic Mode",
        "stats_expert":   "Expert Mode",
        "total_games":    "Total Games",
        "win_rate":       "Win Rate",
        "back":           "← Back",
        "settings_title": "⚙️ SETTINGS",
        "language_label": "Language",
        "hint_engine":    "💡 Engine: {}",
        "hint_country":   "💡 Country: {}",
        "hint_year":      "💡 Year: {}",
        "hint_brand":     "💡 Brand: {}",
        "hint_price":     "💡 Price range: ${} - ${}",
        "8_guesses":      "You have 8 guesses",
        "normal_lbl":     "▶ Normal Mode",
        "hint_lbl":       "💡 Hint Mode",
        "expert_lbl":     "🧠 Expert Mode",
        "jdm_mode":       "🇯🇵  JDM Mode",
        "jdm_lbl":        "🇯🇵 JDM Mode",
        "unknown_mode":   "🔍  Unknown Cars Mode",
        "unknown_lbl":    "🔍 Unknown Cars Mode",
        "stats_title":    "📊 STATISTICS",
    },
    "tr": {
        "title_sub":      "Arabayı Bul!",
        "normal_mode":    "▶  Normal Mod",
        "hint_mode":      "💡  İpucu Modu",
        "expert_mode":    "🧠  Uzman Mod",
        "classic_mode":   "⭐  Klasik Mod",
        "classic_lbl":    "⭐ Klasik Mod",
        "jdm_mode":       "🇯🇵  JDM Modu",
        "jdm_lbl":        "🇯🇵 JDM Modu",
        "unknown_mode":   "🔍  Az Bilinenler Modu",
        "unknown_lbl":    "🔍 Az Bilinenler Modu",
        "stats_btn":      "📊  İstatistikler",
        "settings_btn":   "⚙️  Ayarlar",
        "guesses_left":   "Tahmin {}/{}",
        "correct":        "Doğru",
        "close":          "Yakın (aynı kıta / ±%20 fiyat / komşu motor)",
        "wrong":          "Yanlış",
        "car_col":        "Araba",
        "brand_col":      "Marka",
        "engine_col":     "Motor",
        "price_col":      "Fiyat",
        "country_col":    "Ülke",
        "year_col":       "Yıl",
        "hp_col":         "HP",
        "hint_btn":       "💡 İpucu Al (i)",
        "no_hint":        "💡 Başka ipucu kalmadı!",
        "already_used":   "⚠ Bu arabayı zaten tahmin ettin!",
        "not_found":      "⚠ Araba bulunamadı! Tam ismini yaz.",
        "congrats":       "🎉 {} tahminde buldun!",
        "failed":         "💀 Bilemedin! Cevap:",
        "play_again":     "Tekrar Oyna",
        "main_menu":      "Ana Menü",
        "stats_title":    "📊 İSTATİSTİKLER",
        "stats_normal":   "Normal Mod",
        "stats_classic":  "Klasik Mod",
        "stats_expert":   "Uzman Mod",
        "total_games":    "Toplam Oyun",
        "win_rate":       "Kazanma Oranı",
        "back":           "← Geri",
        "settings_title": "⚙️ AYARLAR",
        "language_label": "Dil",
        "hint_engine":    "💡 Motor: {}",
        "hint_country":   "💡 Ülke: {}",
        "hint_year":      "💡 Yıl: {}",
        "hint_brand":     "💡 Marka: {}",
        "hint_price":     "💡 Fiyat aralığı: ${} - ${}",
        "8_guesses":      "8 tahmin hakkın var",
        "normal_lbl":     "▶ Normal Mod",
        "hint_lbl":       "💡 İpucu Modu",
        "expert_lbl":     "🧠 Uzman Mod",
    },
    "de": {
        "title_sub":      "Rate das Auto!",
        "normal_mode":    "▶  Normaler Modus",
        "hint_mode":      "💡  Hinweis-Modus",
        "expert_mode":    "🧠  Experten-Modus",
        "classic_mode":   "⭐  Klassischer Modus",
        "classic_lbl":    "⭐ Klassischer Modus",
        "jdm_mode":       "🇯🇵  JDM-Modus",
        "jdm_lbl":        "🇯🇵 JDM-Modus",
        "unknown_mode":   "🔍  Unbekannte Autos",
        "unknown_lbl":    "🔍 Unbekannte Autos",
        "stats_btn":      "📊  Statistiken",
        "settings_btn":   "⚙️  Einstellungen",
        "guesses_left":   "Versuch {}/{}",
        "correct":        "Richtig",
        "close":          "Nah (gleicher Kontinent / ±20% Preis / benachbarter Motor)",
        "wrong":          "Falsch",
        "car_col":        "Auto",
        "brand_col":      "Marke",
        "engine_col":     "Motor",
        "price_col":      "Preis",
        "country_col":    "Land",
        "year_col":       "Jahr",
        "hp_col":         "PS",
        "hint_btn":       "💡 Hinweis holen (i)",
        "no_hint":        "💡 Keine Hinweise mehr!",
        "already_used":   "⚠ Dieses Auto wurde bereits geraten!",
        "not_found":      "⚠ Auto nicht gefunden! Genauenamen eingeben.",
        "congrats":       "🎉 Richtig in {} Versuchen!",
        "failed":         "💀 Verloren! Antwort:",
        "play_again":     "Nochmal spielen",
        "main_menu":      "Hauptmenü",
        "stats_title":    "📊 STATISTIKEN",
        "stats_normal":   "Normaler Modus",
        "stats_classic":  "Klassischer Modus",
        "stats_expert":   "Experten-Modus",
        "total_games":    "Spiele gesamt",
        "win_rate":       "Gewinnrate",
        "back":           "← Zurück",
        "settings_title": "⚙️ EINSTELLUNGEN",
        "language_label": "Sprache",
        "hint_engine":    "💡 Motor: {}",
        "hint_country":   "💡 Land: {}",
        "hint_year":      "💡 Jahr: {}",
        "hint_brand":     "💡 Marke: {}",
        "hint_price":     "💡 Preisbereich: ${} - ${}",
        "8_guesses":      "Du hast 8 Versuche",
        "normal_lbl":     "▶ Normaler Modus",
        "hint_lbl":       "💡 Hinweis-Modus",
        "expert_lbl":     "🧠 Experten-Modus",
    },
    "pl": {
        "title_sub":      "Zgadnij auto!",
        "normal_mode":    "▶  Tryb normalny",
        "hint_mode":      "💡  Tryb podpowiedzi",
        "expert_mode":    "🧠  Tryb eksperta",
        "classic_mode":   "⭐  Tryb klasyczny",
        "classic_lbl":    "⭐ Tryb klasyczny",
        "jdm_mode":       "🇯🇵  Tryb JDM",
        "jdm_lbl":        "🇯🇵 Tryb JDM",
        "unknown_mode":   "🔍  Nieznane Auta",
        "unknown_lbl":    "🔍 Nieznane Auta",
        "stats_btn":      "📊  Statystyki",
        "settings_btn":   "⚙️  Ustawienia",
        "guesses_left":   "Próba {}/{}",
        "correct":        "Poprawnie",
        "close":          "Blisko (ten sam kontynent / ±20% ceny / sąsiedni silnik)",
        "wrong":          "Błędnie",
        "car_col":        "Auto",
        "brand_col":      "Marka",
        "engine_col":     "Silnik",
        "price_col":      "Cena",
        "country_col":    "Kraj",
        "year_col":       "Rok",
        "hp_col":         "KM",
        "hint_btn":       "💡 Podpowiedź (i)",
        "no_hint":        "💡 Brak podpowiedzi!",
        "already_used":   "⚠ To auto już zostało zgadnięte!",
        "not_found":      "⚠ Nie znaleziono auta! Wpisz dokładną nazwę.",
        "congrats":       "🎉 Poprawnie w {} próbach!",
        "failed":         "💀 Przegrałeś! Odpowiedź:",
        "play_again":     "Zagraj ponownie",
        "main_menu":      "Menu główne",
        "stats_title":    "📊 STATYSTYKI",
        "stats_normal":   "Tryb normalny",
        "stats_classic":  "Tryb klasyczny",
        "stats_expert":   "Tryb eksperta",
        "total_games":    "Łączna liczba gier",
        "win_rate":       "Wskaźnik wygranych",
        "back":           "← Wróć",
        "settings_title": "⚙️ USTAWIENIA",
        "language_label": "Język",
        "hint_engine":    "💡 Silnik: {}",
        "hint_country":   "💡 Kraj: {}",
        "hint_year":      "💡 Rok: {}",
        "hint_brand":     "💡 Marka: {}",
        "hint_price":     "💡 Zakres cen: ${} - ${}",
        "8_guesses":      "Masz 8 prób",
        "normal_lbl":     "▶ Tryb normalny",
        "hint_lbl":       "💡 Tryb podpowiedzi",
        "expert_lbl":     "🧠 Tryb eksperta",
    },
    "zh": {
        "title_sub":      "猜猜这辆车！",
        "normal_mode":    "▶  普通模式",
        "hint_mode":      "💡  提示模式",
        "expert_mode":    "🧠  专家模式",
        "classic_mode":   "⭐  经典模式",
        "classic_lbl":    "⭐ 经典模式",
        "jdm_mode":       "🇯🇵  JDM模式",
        "jdm_lbl":        "🇯🇵 JDM模式",
        "unknown_mode":   "🔍  冷门汽车模式",
        "unknown_lbl":    "🔍 冷门汽车模式",
        "stats_btn":      "📊  统计",
        "settings_btn":   "⚙️  设置",
        "guesses_left":   "猜测 {}/{}",
        "correct":        "正确",
        "close":          "接近 (同洲 / ±20%价格 / 相邻发动机)",
        "wrong":          "错误",
        "car_col":        "车辆",
        "brand_col":      "品牌",
        "engine_col":     "发动机",
        "price_col":      "价格",
        "country_col":    "国家",
        "year_col":       "年份",
        "hp_col":         "马力",
        "hint_btn":       "💡 获取提示 (i)",
        "no_hint":        "💡 没有更多提示！",
        "already_used":   "⚠ 已经猜过这辆车！",
        "not_found":      "⚠ 未找到汽车！请输入确切名称。",
        "congrats":       "🎉 {} 次猜对！",
        "failed":         "💀 你输了！答案：",
        "play_again":     "再玩一次",
        "main_menu":      "主菜单",
        "stats_title":    "📊 统计",
        "stats_normal":   "普通模式",
        "stats_classic":  "经典模式",
        "stats_expert":   "专家模式",
        "total_games":    "总游戏数",
        "win_rate":       "胜率",
        "back":           "← 返回",
        "settings_title": "⚙️ 设置",
        "language_label": "语言",
        "hint_engine":    "💡 发动机: {}",
        "hint_country":   "💡 国家: {}",
        "hint_year":      "💡 年份: {}",
        "hint_brand":     "💡 品牌: {}",
        "hint_price":     "💡 价格范围: ${} - ${}",
        "8_guesses":      "你有8次猜测机会",
        "normal_lbl":     "▶ 普通模式",
        "hint_lbl":       "💡 提示模式",
        "expert_lbl":     "🧠 专家模式",
    },
    "fr": {
        "title_sub":      "Devinez la voiture!",
        "normal_mode":    "▶  Mode Normal",
        "hint_mode":      "💡  Mode Indice",
        "expert_mode":    "🧠  Mode Expert",
        "classic_mode":   "⭐  Mode Classique",
        "classic_lbl":    "⭐ Mode Classique",
        "jdm_mode":       "🇯🇵  Mode JDM",
        "jdm_lbl":        "🇯🇵 Mode JDM",
        "unknown_mode":   "🔍  Voitures Inconnues",
        "unknown_lbl":    "🔍 Voitures Inconnues",
        "stats_btn":      "📊  Statistiques",
        "settings_btn":   "⚙️  Paramètres",
        "guesses_left":   "Essai {}/{}",
        "correct":        "Correct",
        "close":          "Proche (même continent / ±20% prix / moteur adjacent)",
        "wrong":          "Faux",
        "car_col":        "Voiture",
        "brand_col":      "Marque",
        "engine_col":     "Moteur",
        "price_col":      "Prix",
        "country_col":    "Pays",
        "year_col":       "Année",
        "hp_col":         "CV",
        "hint_btn":       "💡 Obtenir un indice (i)",
        "no_hint":        "💡 Plus d'indices!",
        "already_used":   "⚠ Cette voiture a déjà été devinée!",
        "not_found":      "⚠ Voiture introuvable! Tapez le nom exact.",
        "congrats":       "🎉 Correct en {} essais!",
        "failed":         "💀 Perdu! Réponse:",
        "play_again":     "Rejouer",
        "main_menu":      "Menu Principal",
        "stats_title":    "📊 STATISTIQUES",
        "stats_normal":   "Mode Normal",
        "stats_classic":  "Mode Classique",
        "stats_expert":   "Mode Expert",
        "total_games":    "Total des parties",
        "win_rate":       "Taux de victoire",
        "back":           "← Retour",
        "settings_title": "⚙️ PARAMÈTRES",
        "language_label": "Langue",
        "hint_engine":    "💡 Moteur: {}",
        "hint_country":   "💡 Pays: {}",
        "hint_year":      "💡 Année: {}",
        "hint_brand":     "💡 Marque: {}",
        "hint_price":     "💡 Fourchette de prix: ${} - ${}",
        "8_guesses":      "Vous avez 8 essais",
        "normal_lbl":     "▶ Mode Normal",
        "hint_lbl":       "💡 Mode Indice",
        "expert_lbl":     "🧠 Mode Expert",
    }
}

def fuzzy_match(query, cars, used, limit=6):
    query = query.strip().lower()
    if not query:
        return []
    results = []
    for car in cars:
        if car["name"] in used:
            continue
        name = car["name"].lower()
        # Direkt içeriyor mu
        if query in name:
            results.append((1.0, car))
            continue
        # Fuzzy benzerlik
        ratio = difflib.SequenceMatcher(None, query, name).ratio()
        # Her kelimeyi ayrı ayrı karşılaştır
        word_ratio = max(
            difflib.SequenceMatcher(None, query, word).ratio()
            for word in name.split()
        )
        best = max(ratio, word_ratio)
        if best >= 0.55:
            results.append((best, car))
    results.sort(key=lambda x: x[0], reverse=True)
    return [car for _, car in results[:limit]]

def get_continent(country):
    for continent, countries in CONTINENTS.items():
        if country in countries:
            return continent
    return "Other"

def load_cars():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "cars.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def load_stats():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "stats.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "total": 0, "wins": 0,
        "normal": {"total": 0, "wins": 0},
        "classic": {"total": 0, "wins": 0},
        "expert": {"total": 0, "wins": 0},
    }

def save_stats(stats):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "stats.json"), "w") as f:
        json.dump(stats, f)

def load_settings():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "settings.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"lang": "en"}

def save_settings(settings):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "settings.json"), "w") as f:
        json.dump(settings, f)

def compare(guess, target):
    result = {}
    result["brand"] = "green" if guess["brand"] == target["brand"] else "red"

    g_eng = guess.get("engine", "")
    t_eng = target.get("engine", "")
    if g_eng == t_eng:
        result["engine"] = "green"
    elif g_eng in ENGINE_ORDER and t_eng in ENGINE_ORDER:
        diff = abs(ENGINE_ORDER.index(g_eng) - ENGINE_ORDER.index(t_eng))
        result["engine"] = "yellow" if diff == 1 else "red"
    else:
        result["engine"] = "red"

    g_price = guess.get("price", 0)
    t_price = target.get("price", 1)
    if g_price == t_price:
        result["price"] = "green"
    elif abs(g_price - t_price) / t_price <= 0.20:
        result["price"] = "yellow"
    else:
        result["price"] = "red"

    g_country = guess.get("country", "")
    t_country = target.get("country", "")
    if g_country == t_country:
        result["country"] = "green"
    elif get_continent(g_country) == get_continent(t_country):
        result["country"] = "yellow"
    else:
        result["country"] = "red"

    g_year = guess.get("year", 0)
    t_year = target.get("year", 0)
    if g_year == t_year:
        result["year"] = "green"
    elif abs(g_year - t_year) <= 3:
        result["year"] = "yellow"
    else:
        result["year"] = "red"

    g_hp = guess.get("hp", 0)
    t_hp = target.get("hp", 1)
    if g_hp == t_hp:
        result["hp"] = "green"
    elif abs(g_hp - t_hp) / t_hp <= 0.15:
        result["hp"] = "yellow"
    else:
        result["hp"] = "red"

    return result

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CarGuesser")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.cars     = load_cars()
        self.stats    = load_stats()
        self.settings = load_settings()
        self._center(600, 640)
        self.show_menu()

    def t(self, key, *args):
        lang = self.settings.get("lang", "en")
        txt  = LANGUAGES[lang].get(key, LANGUAGES["en"].get(key, key))
        if args:
            txt = txt.format(*args)
        return txt

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear()
        self._center(600, 720)

        tk.Label(self, text="🏎", font=("Segoe UI Emoji", 48), bg=BG, fg=ACCENT).pack(pady=(30, 0))
        tk.Label(self, text="CARGUESSER", font=("Courier New", 24, "bold"), bg=BG, fg=ACCENT).pack()
        tk.Label(self, text=self.t("title_sub"), font=("Courier New", 11), bg=BG, fg=SUBTEXT).pack(pady=(2, 20))

        for key, cmd in [
            ("normal_mode",  lambda: self.start_game(False, False, "normal")),
            ("classic_mode", lambda: self.start_game(False, False, "classic")),
            ("hint_mode",    lambda: self.start_game(True,  False, "normal")),
            ("expert_mode",  lambda: self.start_game(False, True,  "normal")),
            ("jdm_mode",     lambda: self.start_game(False, False, "jdm")),
            ("unknown_mode", lambda: self.start_game(False, False, "unknown")),
            ("stats_btn",    self.show_stats),
            ("settings_btn", self.show_settings),
        ]:
            btn = tk.Button(
                self, text=self.t(key),
                font=("Courier New", 13, "bold"),
                bg=BG3, fg=TEXT,
                activebackground=GRAY, activeforeground=TEXT,
                relief="flat", bd=0,
                width=24, height=2,
                cursor="hand2",
                command=cmd
            )
            btn.pack(pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=GRAY))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG3))

        tk.Label(self, text=self.t("8_guesses"), font=("Courier New", 9), bg=BG, fg=SUBTEXT).pack(pady=(16, 0))

    def show_stats(self):
        self.clear()
        self._center(480, 420)
        tk.Label(self, text=self.t("stats_title"), font=("Courier New", 16, "bold"), bg=BG, fg=ACCENT).pack(pady=(30, 16))

        total = self.stats.get("total", 0)
        wins  = self.stats.get("wins", 0)
        rate  = f"%{int(wins/total*100)}" if total > 0 else "-%"

        frame = tk.Frame(self, bg=BG2, padx=30, pady=16)
        frame.pack(padx=30, fill="x")

        # Genel istatistik
        for label_key, val in [(self.t("total_games"), str(total)), (self.t("win_rate"), rate)]:
            row = tk.Frame(frame, bg=BG2)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label_key, font=("Courier New", 11), bg=BG2, fg=SUBTEXT, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=("Courier New", 13, "bold"), bg=BG2, fg=ACCENT, anchor="e").pack(side="right")

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", pady=10)

        # Mod bazlı istatistikler
        for mode_key, label in [("normal", self.t("stats_normal")), ("classic", self.t("stats_classic")), ("expert", self.t("stats_expert"))]:
            mode_stats = self.stats.get(mode_key, {"total": 0, "wins": 0})
            mt = mode_stats.get("total", 0)
            mw = mode_stats.get("wins", 0)
            mr = f"%{int(mw/mt*100)}" if mt > 0 else "-%"
            row = tk.Frame(frame, bg=BG2)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=("Courier New", 10), bg=BG2, fg=SUBTEXT, anchor="w").pack(side="left")
            tk.Label(row, text=f"{mt} oyun  {mr}", font=("Courier New", 11, "bold"), bg=BG2, fg=ACCENT, anchor="e").pack(side="right")

        tk.Button(self, text=self.t("back"), font=("Courier New", 11),
                  bg=BG3, fg=TEXT, activebackground=GRAY, activeforeground=TEXT,
                  relief="flat", bd=0, padx=20, pady=8, cursor="hand2",
                  command=self.show_menu).pack(pady=20)

    def show_settings(self):
        self.clear()
        self._center(420, 340)
        tk.Label(self, text=self.t("settings_title"), font=("Courier New", 16, "bold"), bg=BG, fg=ACCENT).pack(pady=(40, 20))

        frame = tk.Frame(self, bg=BG2, padx=30, pady=20)
        frame.pack(padx=40, fill="x")

        tk.Label(frame, text=self.t("language_label"), font=("Courier New", 12),
                 bg=BG2, fg=SUBTEXT).pack(anchor="w", pady=(0, 8))

        lang_frame1 = tk.Frame(frame, bg=BG2)
        lang_frame1.pack(anchor="w", pady=(0,4))
        lang_frame2 = tk.Frame(frame, bg=BG2)
        lang_frame2.pack(anchor="w")

        current_lang = self.settings.get("lang", "en")
        langs = [("en", "English"), ("tr", "Türkçe"), ("de", "Deutsch"), ("pl", "Polski"), ("zh", "中文"), ("fr", "Français")]
        for i, (lang_code, lang_name) in enumerate(langs):
            is_active = current_lang == lang_code
            parent = lang_frame1 if i < 3 else lang_frame2
            tk.Button(
                parent, text=lang_name,
                font=("Courier New", 11, "bold"),
                bg=ACCENT if is_active else BG3,
                fg=BG if is_active else TEXT,
                activebackground=GRAY, activeforeground=TEXT,
                relief="flat", bd=0, padx=20, pady=6, cursor="hand2",
                command=lambda lc=lang_code: self._set_lang(lc)
            ).pack(side="left", padx=4)

        tk.Button(self, text=self.t("back"), font=("Courier New", 11),
                  bg=BG3, fg=TEXT, activebackground=GRAY, activeforeground=TEXT,
                  relief="flat", bd=0, padx=20, pady=8, cursor="hand2",
                  command=self.show_menu).pack(pady=24)

    def _set_lang(self, lang_code):
        self.settings["lang"] = lang_code
        save_settings(self.settings)
        self.show_settings()

    def start_game(self, hint_mode=False, expert_mode=False, game_mode="normal"):
        self.clear()
        GameScreen(self, self.cars, self.stats, hint_mode, expert_mode, game_mode)


class GameScreen(tk.Frame):
    MAX_GUESSES = 8

    def __init__(self, master, cars, stats, hint_mode, expert_mode=False, game_mode="normal"):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True)
        self.master      = master
        self.stats       = stats
        self.hint_mode   = hint_mode
        self.expert_mode = expert_mode
        self.game_mode   = game_mode
        # Moda göre arabaları filtrele
        if game_mode == "classic":
            self.cars = [c for c in cars if "normal" in c.get("modes", ["normal"])][:65]
        elif game_mode == "unknown":
            self.cars = [c for c in cars if "unknown" in c.get("modes", [])]
        else:
            self.cars = [c for c in cars if game_mode in c.get("modes", ["normal"])]
        self.target      = random.choice(self.cars)
        self.guesses     = []
        self.used        = []
        self.hints_used  = 0
        self.won         = False
        master._center(1100, 780)
        self._build_ui()

    def t(self, key, *args):
        return self.master.t(key, *args)

    def _build_ui(self):
        top = tk.Frame(self, bg=BG, pady=8)
        top.pack(fill="x", padx=16)

        tk.Button(top, text="←", font=("Courier New", 13), bg=BG, fg=SUBTEXT,
                  relief="flat", bd=0, cursor="hand2",
                  command=self.master.show_menu).pack(side="left")

        if self.hint_mode:
            mode_txt = self.t("hint_lbl")
        elif self.expert_mode:
            mode_txt = self.t("expert_lbl")
        elif self.game_mode == "jdm":
            mode_txt = self.t("jdm_lbl")
        elif self.game_mode == "classic":
            mode_txt = self.t("classic_lbl")
        elif self.game_mode == "unknown":
            mode_txt = self.t("unknown_lbl")
        else:
            mode_txt = self.t("normal_lbl")

        tk.Label(top, text=mode_txt, font=("Courier New", 12, "bold"), bg=BG, fg=ACCENT).pack(side="left", padx=12)

        self.turn_label = tk.Label(top, text=self.t("guesses_left", 1, self.MAX_GUESSES),
                                   font=("Courier New", 11), bg=BG, fg=SUBTEXT)
        self.turn_label.pack(side="right")

        legend = tk.Frame(self, bg=BG)
        legend.pack(pady=(0, 6))
        for col, key in [(GREEN, "correct"), (YELLOW, "close"), (RED, "wrong")]:
            tk.Label(legend, text="  ", bg=col, width=2).pack(side="left", padx=2)
            tk.Label(legend, text=self.t(key), font=("Courier New", 9), bg=BG, fg=SUBTEXT).pack(side="left", padx=(0, 8))

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=12)
        cols   = ["car_col", "brand_col", "engine_col", "price_col", "country_col", "year_col", "hp_col"]
        widths = [22, 14, 8, 10, 10, 6, 7]
        for col_key, w in zip(cols, widths):
            tk.Label(header, text=self.t(col_key), font=("Courier New", 9),
                     bg=BG, fg=SUBTEXT, width=w, anchor="center").pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=12, pady=2)

        self.rows_frame = tk.Frame(self, bg=BG)
        self.rows_frame.pack(fill="x", padx=12)

        search_frame = tk.Frame(self, bg=BG2, pady=10)
        search_frame.pack(fill="x", padx=12, pady=(8, 0))

        self.search_var = tk.StringVar()
        self.entry = tk.Entry(search_frame, textvariable=self.search_var,
                              font=("Courier New", 13), bg=BG3, fg=TEXT,
                              insertbackground=TEXT, relief="flat", bd=0)
        self.entry.pack(fill="x", padx=12, ipady=8)
        self.entry.focus()
        self.entry.bind("<Return>", self._on_enter)

        if not self.expert_mode:
            self.search_var.trace("w", self._on_search)
            self.entry.bind("<Up>",   self._suggest_up)
            self.entry.bind("<Down>", self._suggest_down)
            self.entry.bind("<Tab>",  self._on_tab)

        self.suggest_frame = tk.Frame(self, bg=BG2)
        self.suggest_frame.pack(fill="x", padx=12)
        self.suggest_labels = []
        self.suggest_idx    = -1
        self.suggest_cars   = []

        self.info_label = tk.Label(self, text="", font=("Courier New", 10), bg=BG, fg=YELLOW)
        self.info_label.pack(pady=4)

        if self.hint_mode:
            hint_btn = tk.Button(self, text=self.t("hint_btn"),
                                 font=("Courier New", 10), bg=BG3, fg=YELLOW,
                                 activebackground=GRAY, activeforeground=YELLOW,
                                 relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
                                 command=self._give_hint)
            hint_btn.pack()
            self.master.bind("i", lambda e: self._give_hint())

    def _on_search(self, *args):
        query = self.search_var.get().strip().lower()
        for lbl in self.suggest_labels:
            lbl.destroy()
        self.suggest_labels = []
        self.suggest_idx    = -1
        if not query:
            self.suggest_cars = []
            return
        self.suggest_cars = fuzzy_match(query, self.cars, self.used)
        for i, car in enumerate(self.suggest_cars):
            lbl = tk.Label(self.suggest_frame, text=car["name"],
                           font=("Courier New", 11), bg=BG2, fg=TEXT,
                           anchor="w", padx=12, pady=4, cursor="hand2")
            lbl.pack(fill="x")
            lbl.bind("<Button-1>", lambda e, c=car: self._select_car(c))
            lbl.bind("<Enter>", lambda e, l=lbl, j=i: self._hover(l, j))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(bg=BG2))
            self.suggest_labels.append(lbl)

    def _hover(self, lbl, idx):
        for i, l in enumerate(self.suggest_labels):
            l.config(bg=GRAY if i == idx else BG2)
        self.suggest_idx = idx

    def _suggest_up(self, e):
        if self.suggest_idx > 0:
            self.suggest_idx -= 1
            self._hover(self.suggest_labels[self.suggest_idx], self.suggest_idx)

    def _suggest_down(self, e):
        if self.suggest_idx < len(self.suggest_labels) - 1:
            self.suggest_idx += 1
            self._hover(self.suggest_labels[self.suggest_idx], self.suggest_idx)

    def _on_tab(self, e):
        if self.suggest_cars:
            self._select_car(self.suggest_cars[max(0, self.suggest_idx)])
        return "break"

    def _on_enter(self, e):
        if self.expert_mode:
            typed = self.search_var.get().strip()
            # Önce tam eşleşme dene
            match = next((c for c in self.cars if c["name"].lower() == typed.lower()), None)
            # Tam eşleşme yoksa fuzzy dene
            if not match:
                fuzzy = fuzzy_match(typed, self.cars, self.used, limit=1)
                if fuzzy:
                    ratio = difflib.SequenceMatcher(None, typed.lower(), fuzzy[0]["name"].lower()).ratio()
                    if ratio >= 0.65:
                        match = fuzzy[0]
            if match:
                if match["name"] in self.used:
                    self.info_label.config(text=self.t("already_used"))
                else:
                    self.search_var.set("")
                    self._make_guess(match)
            else:
                self.info_label.config(text=self.t("not_found"))
        else:
            if 0 <= self.suggest_idx < len(self.suggest_cars):
                self._select_car(self.suggest_cars[self.suggest_idx])
            elif len(self.suggest_cars) == 1:
                self._select_car(self.suggest_cars[0])

    def _select_car(self, car):
        for lbl in self.suggest_labels:
            lbl.destroy()
        self.suggest_labels = []
        self.search_var.set("")
        self.suggest_cars = []
        self._make_guess(car)

    def _make_guess(self, guess):
        if len(self.guesses) >= self.MAX_GUESSES or self.won:
            return
        self.used.append(guess["name"])
        result = compare(guess, self.target)
        self.guesses.append((guess, result))
        self._add_row(guess, result)
        turn = len(self.guesses)
        self.turn_label.config(text=self.t("guesses_left", min(turn + 1, self.MAX_GUESSES), self.MAX_GUESSES))
        if all(v == "green" for v in result.values()):
            self.won = True
            self.stats["total"] = self.stats.get("total", 0) + 1
            self.stats["wins"]  = self.stats.get("wins", 0) + 1
            # Mod istatistiği
            stat_key = "expert" if self.expert_mode else ("classic" if self.game_mode == "classic" else "normal")
            if stat_key not in self.stats:
                self.stats[stat_key] = {"total": 0, "wins": 0}
            self.stats[stat_key]["total"] += 1
            self.stats[stat_key]["wins"]  += 1
            save_stats(self.stats)
            self._end_screen(True, turn)
        elif turn >= self.MAX_GUESSES:
            self.stats["total"] = self.stats.get("total", 0) + 1
            stat_key = "expert" if self.expert_mode else ("classic" if self.game_mode == "classic" else "normal")
            if stat_key not in self.stats:
                self.stats[stat_key] = {"total": 0, "wins": 0}
            self.stats[stat_key]["total"] += 1
            save_stats(self.stats)
            self._end_screen(False, turn)

    def _add_row(self, guess, result):
        COLOR_MAP = {"green": GREEN, "yellow": YELLOW, "red": RED}
        row = tk.Frame(self.rows_frame, bg=BG, pady=2)
        row.pack(fill="x")
        tk.Label(row, text=guess["name"][:22], font=("Courier New", 10, "bold"),
                 bg=BG, fg=TEXT, width=22, anchor="w").pack(side="left")
        fields = [
            ("brand",   guess.get("brand", ""),        8),
            ("engine",  guess.get("engine", ""),       7),
            ("price",   f"${guess.get('price',0):,}",  9),
            ("country", guess.get("country", ""),      9),
            ("year",    str(guess.get("year", "?")),   5),
            ("hp",      f"{guess.get('hp','?')}hp",    6),
        ]
        for key, val, w in fields:
            col = COLOR_MAP.get(result.get(key, "red"), RED)
            tk.Label(row, text=val[:w], font=("Courier New", 9, "bold"),
                     bg=col, fg="black" if col == YELLOW else "white",
                     width=w + 1, pady=3, relief="flat").pack(side="left", padx=2)

    def _give_hint(self):
        if self.won or len(self.guesses) >= self.MAX_GUESSES:
            return
        hints = [
            self.t("hint_engine",  self.target.get("engine",  "?")),
            self.t("hint_country", self.target.get("country", "?")),
            self.t("hint_year",    self.target.get("year",    "?")),
            self.t("hint_brand",   self.target.get("brand",   "?")),
            self.t("hint_price",
                   f"{self.target.get('price', 0) * 0.8:,.0f}",
                   f"{self.target.get('price', 0) * 1.2:,.0f}"),
        ]
        if self.hints_used < len(hints):
            self.info_label.config(text=hints[self.hints_used])
            self.hints_used += 1
        else:
            self.info_label.config(text=self.t("no_hint"))

    def _end_screen(self, won, turns):
        self.entry.config(state="disabled")
        for lbl in self.suggest_labels:
            lbl.destroy()
        popup = tk.Toplevel(self.master)
        popup.configure(bg=BG)
        popup.resizable(False, False)
        popup.grab_set()
        w, h = 400, 270
        px = self.master.winfo_x() + (self.master.winfo_width()  - w) // 2
        py = self.master.winfo_y() + (self.master.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{px}+{py}")
        if won:
            tk.Label(popup, text="🎉", font=("Segoe UI Emoji", 36), bg=BG).pack(pady=(24, 4))
            tk.Label(popup, text=self.t("congrats", turns),
                     font=("Courier New", 14, "bold"), bg=BG, fg=GREEN).pack()
        else:
            tk.Label(popup, text="💀", font=("Segoe UI Emoji", 36), bg=BG).pack(pady=(24, 4))
            tk.Label(popup, text=self.t("failed"),
                     font=("Courier New", 14, "bold"), bg=BG, fg=RED).pack()
            tk.Label(popup, text=self.target["name"],
                     font=("Courier New", 12), bg=BG, fg=ACCENT).pack()
        tk.Frame(popup, bg=BORDER, height=1).pack(fill="x", padx=24, pady=12)
        btn_frame = tk.Frame(popup, bg=BG)
        btn_frame.pack()

        def play_again():
            popup.destroy()
            self.master.start_game(hint_mode=self.hint_mode, expert_mode=self.expert_mode, game_mode=self.game_mode)

        for txt_key, cmd in [
            ("play_again", play_again),
            ("main_menu",  lambda: [popup.destroy(), self.master.show_menu()])
        ]:
            tk.Button(btn_frame, text=self.t(txt_key), font=("Courier New", 11),
                      bg=BG3, fg=TEXT, activebackground=GRAY, activeforeground=TEXT,
                      relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
                      command=cmd).pack(side="left", padx=8)

if __name__ == "__main__":
    app = App()
    app.mainloop()
