import tkinter as tk
from tkinter import ttk, messagebox
from business import tracker, accumulator_tracker
from business.chart import show_profit_chart

# ── CULORI ──────────────────────────────────────────────────────
BG          = "#0d1117"
SIDEBAR_BG  = "#161b22"
CARD_BG     = "#1c2128"
ACCENT      = "#00ff88"
ACCENT2     = "#00cc6a"
TEXT        = "#e6edf3"
TEXT_MUTED  = "#7d8590"
RED         = "#ff4444"
YELLOW      = "#ffa500"
BORDER      = "#30363d"

def styled_button(parent, text, command, color=ACCENT, text_color=BG, width=None):
    btn = tk.Button(parent, text=text, command=command,
                    bg=color, fg=text_color, relief="flat",
                    font=("Consolas", 11, "bold"),
                    padx=15, pady=8, cursor="hand2",
                    activebackground=ACCENT2, activeforeground=BG)
    if width:
        btn.config(width=width)
    return btn

def styled_entry(parent, width=30):
    return tk.Entry(parent, width=width, bg=CARD_BG, fg=TEXT,
                    insertbackground=ACCENT, relief="flat",
                    font=("Consolas", 12),
                    highlightthickness=1, highlightcolor=ACCENT,
                    highlightbackground=BORDER)

def styled_label(parent, text, size=12, bold=False, color=TEXT, bg=None):
    font = ("Consolas", size, "bold") if bold else ("Consolas", size)
    return tk.Label(parent, text=text, font=font, fg=color,
                    bg=bg or parent.cget("bg"))

def section_title(parent, text):
    f = tk.Frame(parent, bg=parent.cget("bg"))
    tk.Label(f, text=text, font=("Consolas", 14, "bold"),
             fg=ACCENT, bg=f.cget("bg")).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=10, pady=7)
    return f


class BettingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽ Betting Tracker Pro")
        self.root.geometry("1280x750")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.overrideredirect(True)

        self.current_page = None
        self.pages = {}
        self._collapsed_accs = set()

        # custom titlebar
        titlebar = tk.Frame(self.root, bg="#0a0a0a", height=32)
        titlebar.pack(fill="x", side="top")
        titlebar.pack_propagate(False)

        tk.Label(titlebar, text="⚽ Betting Tracker Pro",
                 font=("Consolas", 10, "bold"),
                 bg="#0a0a0a", fg=ACCENT).pack(side="left", padx=15)

        tk.Button(titlebar, text="✕", command=self.root.destroy,
                  bg="#0a0a0a", fg=TEXT_MUTED, relief="flat",
                  font=("Consolas", 12), cursor="hand2",
                  activebackground=RED, activeforeground="white",
                  padx=10).pack(side="right")

        tk.Button(titlebar, text="─", command=lambda: self.root.iconify(),
                  bg="#0a0a0a", fg=TEXT_MUTED, relief="flat",
                  font=("Consolas", 12), cursor="hand2",
                  activebackground=CARD_BG, activeforeground=TEXT,
                  padx=10).pack(side="right")

        def start_drag(e):
            self.root._drag_x = e.x
            self.root._drag_y = e.y

        def do_drag(e):
            x = self.root.winfo_x() + e.x - self.root._drag_x
            y = self.root.winfo_y() + e.y - self.root._drag_y
            self.root.geometry(f"+{x}+{y}")

        titlebar.bind("<ButtonPress-1>", start_drag)
        titlebar.bind("<B1-Motion>", do_drag)

        self._build_layout()
        self.show_page("dashboard")
        from business.weekly_summary import is_monday, was_summary_shown_today
        if is_monday() and not was_summary_shown_today():
            self.root.after(1000, self.show_weekly_summary)

    def _build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="⚽", font=("Arial", 28),
                 bg=SIDEBAR_BG, fg=ACCENT).pack(pady=(25, 0))
        tk.Label(self.sidebar, text="BETTING\nTRACKER", font=("Consolas", 11, "bold"),
                 bg=SIDEBAR_BG, fg=ACCENT, justify="center").pack()
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=15, pady=15)

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("pariuri",   "🎯  Pariuri"),
            ("meciuri",   "⚽  Meciuri"),
            ("grafic",    "📈  Grafic"),
            ("value",     "💰  Value Bet"),
            ("bank",      "🏦  Bank"),
            ("analiza",   "🔍  Analiză Tip"),
            ("istoric",   "📜  Istoric"),
        ]
        for key, label in nav_items:
            btn = tk.Button(self.sidebar, text=label,
                            command=lambda k=key: self.show_page(k),
                            bg=SIDEBAR_BG, fg=TEXT_MUTED, relief="flat",
                            font=("Consolas", 11), anchor="w", padx=20, pady=12,
                            cursor="hand2", activebackground=CARD_BG,
                            activeforeground=ACCENT, width=20)
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        tk.Label(self.sidebar, text="v1.0.0", font=("Consolas", 8),
                 bg=SIDEBAR_BG, fg=BORDER).pack(side="bottom", pady=10)

        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

        for key in ["dashboard", "pariuri", "meciuri", "grafic", "value", "bank", "analiza", "istoric"]:
            page = tk.Frame(self.content, bg=BG)
            self.pages[key] = page
            getattr(self, f"build_{key}")(page)

    def show_page(self, key):
        if self.current_page:
            self.pages[self.current_page].pack_forget()
            self.nav_buttons[self.current_page].config(bg=SIDEBAR_BG, fg=TEXT_MUTED)
        self.pages[key].pack(fill="both", expand=True)
        self.nav_buttons[key].config(bg=CARD_BG, fg=ACCENT)
        self.current_page = key

    # ── DASHBOARD ───────────────────────────────────────────────
    def build_dashboard(self, frame):
        header = tk.Frame(frame, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 10))
        styled_label(header, "Dashboard", 20, bold=True, color=TEXT).pack(side="left")
        styled_button(header, "🔄 Refresh", self.refresh_dashboard, width=12).pack(side="right")

        cards_frame = tk.Frame(frame, bg=BG)
        cards_frame.pack(fill="x", padx=30, pady=10)

        self.stat_labels = {}
        stats = [
            ("💼 Pariuri Simple", "simple", ACCENT),
            ("🎰 Acumulatori",    "acc",    ACCENT),
            ("💰 Profit Total",   "profit", ACCENT),
            ("🏆 Win Rate",       "winrate",ACCENT),
            ("📈 ROI",            "roi",    ACCENT),
        ]

        for i, (title, key, color) in enumerate(stats):
            card = tk.Frame(cards_frame, bg=CARD_BG,
                            highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=0, column=i, padx=8, pady=8, sticky="ew")
            cards_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=title, font=("Consolas", 9),
                     bg=CARD_BG, fg=TEXT_MUTED).pack(pady=(15, 5), padx=15, anchor="w")
            lbl = tk.Label(card, text="...", font=("Consolas", 18, "bold"),
                           bg=CARD_BG, fg=color)
            lbl.pack(pady=(0, 15), padx=15, anchor="w")
            self.stat_labels[key] = lbl

        section_title(frame, "Pariuri Recente").pack(fill="x", padx=30, pady=(20, 5))

        list_frame = tk.Frame(frame, bg=CARD_BG,
                              highlightthickness=1, highlightbackground=BORDER)
        list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.recent_listbox = tk.Listbox(list_frame, bg=CARD_BG, fg=TEXT,
                                         relief="flat", font=("Consolas", 10),
                                         selectbackground=ACCENT, selectforeground=BG,
                                         borderwidth=0, highlightthickness=0)
        self.recent_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_dashboard()

    def refresh_dashboard(self):
        bets = tracker.get_all_bets()
        accs = accumulator_tracker.get_all()

        finished_bets = [b for b in bets if b.result is not None]
        finished_accs = [a for a in accs if a.result is not None]
        all_finished  = finished_bets + finished_accs

        total_profit = sum(b.profit for b in all_finished)
        total_staked = sum(b.stake  for b in all_finished)
        wins         = [b for b in all_finished if b.result == "win"]
        win_rate     = len(wins) / len(all_finished) * 100 if all_finished else 0
        roi          = total_profit / total_staked * 100   if total_staked  else 0

        self.stat_labels["simple"].config(text=str(len(bets)))
        self.stat_labels["acc"].config(text=str(len(accs)))
        self.stat_labels["profit"].config(
            text=f"{total_profit:+.2f}",
            fg=ACCENT if total_profit >= 0 else RED)
        self.stat_labels["winrate"].config(text=f"{win_rate:.1f}%")
        self.stat_labels["roi"].config(
            text=f"{roi:.1f}%",
            fg=ACCENT if roi >= 0 else RED)

        self.recent_listbox.delete(0, "end")
        for b in reversed(bets[-5:]):
            icon = "✅" if b.result == "win" else "❌" if b.result == "lose" else "⏳"
            self.recent_listbox.insert("end", f"  {icon}  {b.match[:35]:<35} {b.odds}x   {b.stake} RON")
            if b.result == "win":
                self.recent_listbox.itemconfig(self.recent_listbox.size()-1, fg="#00ff88")
            elif b.result == "lose":
                self.recent_listbox.itemconfig(self.recent_listbox.size()-1, fg="#ff4444")

        for a in reversed(accs[-5:]):
            icon = "✅" if a.result == "win" else "❌" if a.result == "lose" else "⏳"
            self.recent_listbox.insert("end", f"  {icon}  ACUMULATOR {a.total_odds}x   {a.stake} RON")
            if a.result == "win":
                self.recent_listbox.itemconfig(self.recent_listbox.size()-1, fg="#00ff88")
            elif a.result == "lose":
                self.recent_listbox.itemconfig(self.recent_listbox.size()-1, fg="#ff4444")
            for match, odds in zip(a.matches, a.odds_list):
                self.recent_listbox.insert("end", f"       ↳ {match[:35]} @ {odds}")

    # ── PARIURI ─────────────────────────────────────────────────
    def build_pariuri(self, frame):
        left = tk.Frame(frame, bg=CARD_BG, width=370,
                        highlightthickness=1, highlightbackground=BORDER)
        left.pack(side="left", fill="y", padx=(20,10), pady=20)
        left.pack_propagate(False)

        section_title(left, "Adaugă Bilet").pack(fill="x", padx=15, pady=(15,5))

        styled_label(left, "Meci:", color=TEXT_MUTED).pack(anchor="w", padx=15)
        self.entry_match = styled_entry(left, 35)
        self.entry_match.pack(padx=15, pady=5, fill="x")

        styled_label(left, "Cotă:", color=TEXT_MUTED).pack(anchor="w", padx=15)
        self.entry_odds = styled_entry(left, 35)
        self.entry_odds.pack(padx=15, pady=5, fill="x")

        styled_label(left, "Tip pariu:", color=TEXT_MUTED).pack(anchor="w", padx=15)
        self.selected_bet_type = tk.StringVar(value="1X2")
        type_frame = tk.Frame(left, bg=CARD_BG)
        type_frame.pack(padx=15, pady=5, fill="x")
        for bt in ["1X2", "Peste/Sub", "BTTS"]:
            tk.Radiobutton(type_frame, text=bt, variable=self.selected_bet_type,
                           value=bt, bg=CARD_BG, fg=TEXT, selectcolor=BG,
                           activebackground=CARD_BG, activeforeground=ACCENT,
                           font=("Consolas", 10)).pack(side="left", padx=5)

        styled_button(left, "+ Adaugă meci la bilet",
                      self.add_match_to_ticket,
                      color=CARD_BG, text_color=ACCENT).pack(padx=15, pady=8, fill="x")

        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=15, pady=5)

        styled_label(left, "Meciuri pe bilet:", color=TEXT_MUTED).pack(anchor="w", padx=15)
        self.ticket_listbox = tk.Listbox(left, bg=BG, fg=TEXT, height=4,
                                         relief="flat", font=("Consolas", 10),
                                         selectbackground=ACCENT, selectforeground=BG,
                                         borderwidth=0, highlightthickness=0)
        self.ticket_listbox.pack(padx=15, pady=5, fill="x")

        self.label_tip = tk.Label(left, text="Tip: —", bg=CARD_BG,
                                  fg=ACCENT, font=("Consolas", 10, "bold"))
        self.label_tip.pack(pady=3)

        styled_label(left, "Miză (RON):", color=TEXT_MUTED).pack(anchor="w", padx=15)
        self.entry_stake = styled_entry(left, 35)
        self.entry_stake.pack(padx=15, pady=5, fill="x")

        self.label_potential = tk.Label(left, text="Câștig potențial: —",
                                        bg=CARD_BG, fg=ACCENT,
                                        font=("Consolas", 10))
        self.label_potential.pack(pady=3)

        self.entry_stake.bind("<KeyRelease>", self.update_potential)

        styled_button(left, "💾 Salvează biletul",
                      self.save_ticket).pack(padx=15, pady=8, fill="x")
        styled_button(left, "🗑 Resetează",
                      self.reset_ticket,
                      color="#2d1f1f", text_color=RED).pack(padx=15, fill="x")

        right = tk.Frame(frame, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=(10,20), pady=20)

        section_title(right, "Pariuri Salvate").pack(fill="x", pady=(15,5))

        self.bets_listbox = tk.Listbox(right, bg=CARD_BG, fg=TEXT,
                                       relief="flat", font=("Consolas", 10),
                                       selectbackground=ACCENT, selectforeground=BG,
                                       borderwidth=0, highlightthickness=1,
                                       highlightbackground=BORDER)
        self.bets_listbox.pack(fill="both", expand=True)
        self.bets_listbox.bind("<Double-Button-1>", self._toggle_accumulator)

        btn_row = tk.Frame(right, bg=BG)
        btn_row.pack(pady=10)

        styled_button(btn_row, "✅ Win",
                      lambda: self.set_result("win"),
                      color="#1a3a2a", text_color=ACCENT).pack(side="left", padx=5)
        styled_button(btn_row, "❌ Lose",
                      lambda: self.set_result("lose"),
                      color="#2d1f1f", text_color=RED).pack(side="left", padx=5)
        styled_button(btn_row, "🗑 Șterge",
                      self.delete_bet_gui,
                      color=CARD_BG, text_color=TEXT_MUTED).pack(side="left", padx=5)
        styled_button(btn_row, "🔄 Refresh",
                      self.refresh_bets).pack(side="left", padx=5)

        self.bet_matches = []
        self.refresh_bets()

    def update_potential(self, event=None):
        try:
            stake = float(self.entry_stake.get())
            total_odds = 1
            for _, odds, _ in self.bet_matches:
                total_odds *= odds
            potential = round(stake * total_odds - stake, 2)
            self.label_potential.config(text=f"Câștig potențial: {potential:.2f} RON")
        except:
            self.label_potential.config(text="Câștig potențial: —")

    def add_match_to_ticket(self):
        match = self.entry_match.get().strip()
        odds  = self.entry_odds.get().strip()
        if not match or not odds:
            messagebox.showwarning("Atenție", "Completează meciul și cota!")
            return
        try:
            odds = float(odds)
        except ValueError:
            messagebox.showerror("Eroare", "Cota trebuie să fie un număr!")
            return
        self.bet_matches.append((match, odds, self.selected_bet_type.get()))
        self.ticket_listbox.insert("end", f"  [{self.selected_bet_type.get()}] {match} @ {odds}")
        self.entry_match.delete(0, "end")
        self.entry_odds.delete(0, "end")
        tip = "Pariu Simplu" if len(self.bet_matches) == 1 else f"Acumulator ({len(self.bet_matches)} meciuri)"
        self.label_tip.config(text=f"Tip: {tip}")
        self.update_potential()

    def open_bet_builder(self):
        win = tk.Toplevel(self.root)
        win.geometry("650x780")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.overrideredirect(True)

        # titlebar custom identic cu main window
        titlebar = tk.Frame(win, bg="#0a0a0a", height=32)
        titlebar.pack(fill="x", side="top")
        titlebar.pack_propagate(False)
        tk.Label(titlebar, text="🔨 Bet Builder",
                 font=("Consolas", 10, "bold"),
                 bg="#0a0a0a", fg=ACCENT).pack(side="left", padx=15)
        tk.Button(titlebar, text="✕", command=win.destroy,
                  bg="#0a0a0a", fg=TEXT_MUTED, relief="flat",
                  font=("Consolas", 12), cursor="hand2",
                  activebackground=RED, activeforeground="white",
                  padx=10).pack(side="right")
        def start_drag(e): win._x = e.x; win._y = e.y
        def do_drag(e): win.geometry(f"+{win.winfo_x()+e.x-win._x}+{win.winfo_y()+e.y-win._y}")
        titlebar.bind("<ButtonPress-1>", start_drag)
        titlebar.bind("<B1-Motion>", do_drag)

        # meci — full width
        meci_inner = tk.Frame(win, bg=CARD_BG)
        meci_inner.pack(fill="x")
        styled_label(meci_inner, "Meci:", color=TEXT_MUTED, size=10).pack(side="left", padx=15, pady=10)
        entry_meci = styled_entry(meci_inner, 50)
        entry_meci.pack(side="left", fill="x", expand=True, padx=(0,15))
        if self.entry_match.get().strip():
            entry_meci.insert(0, self.entry_match.get().strip())

        # scroll area — fara padx
        outer = tk.Frame(win, bg=BG)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        selectii = {}

        def make_cat_simple(title, opts):
            f = tk.Frame(sf, bg=CARD_BG)
            f.pack(fill="x", pady=1)
            tk.Label(f, text=title, font=("Consolas", 11, "bold"),
                     bg=CARD_BG, fg=TEXT).pack(anchor="w", padx=15, pady=(10,6))
            row = tk.Frame(f, bg=CARD_BG)
            row.pack(fill="x", pady=(0,10))
            btns = []
            for opt in opts:
                key = f"{title}_{opt}"
                sel_var = tk.StringVar(value="")
                cota_var = tk.StringVar(value="")
                selectii[key] = (sel_var, cota_var, opt)
                col = tk.Frame(row, bg="#1a1f2a")
                col.pack(side="left", fill="x", expand=True, padx=1)
                btn = tk.Button(col, text=opt, bg="#1a1f2a", fg=TEXT_MUTED,
                                relief="flat", font=("Consolas", 11, "bold"),
                                pady=8, cursor="hand2", bd=0)
                btn.pack(fill="x")
                e = tk.Entry(col, textvariable=cota_var, width=8,
                             bg="#1a1f2a", fg=ACCENT, insertbackground=ACCENT,
                             relief="flat", font=("Consolas", 12, "bold"),
                             justify="center", highlightthickness=0)
                e.pack(fill="x", pady=2)
                e.insert(0, "—")
                e.bind("<FocusIn>", lambda ev, en=e: en.delete(0,"end") if en.get()=="—" else None)
                btns.append((btn, e, sel_var, key))
                def toggle(k=key, b=btn, en=e, sv=sel_var, all_b=btns):
                    if sv.get() == "on":
                        sv.set(""); b.config(bg="#1a1f2a", fg=TEXT_MUTED); en.config(bg="#1a1f2a")
                    else:
                        for bb,ee,sv2,kk in all_b:
                            if kk != k: sv2.set(""); bb.config(bg="#1a1f2a", fg=TEXT_MUTED); ee.config(bg="#1a1f2a")
                        sv.set("on"); b.config(bg=ACCENT, fg=BG); en.config(bg=ACCENT2)
                btn.config(command=toggle)
            tk.Frame(f, bg=BORDER, height=1).pack(fill="x")

        def make_cat_table(title, linii):
            f = tk.Frame(sf, bg=CARD_BG)
            f.pack(fill="x", pady=1)
            hdr = tk.Frame(f, bg=CARD_BG)
            hdr.pack(fill="x")
            tk.Label(hdr, text=title, font=("Consolas", 11, "bold"),
                     bg=CARD_BG, fg=TEXT, width=14, anchor="w").pack(side="left", padx=15, pady=(10,6))
            tk.Label(hdr, text="SUB", font=("Consolas", 10, "bold"),
                     bg=CARD_BG, fg=TEXT_MUTED).pack(side="left", fill="x", expand=True)
            tk.Label(hdr, text="PESTE", font=("Consolas", 10, "bold"),
                     bg=CARD_BG, fg=TEXT_MUTED).pack(side="left", fill="x", expand=True)
            for nr in linii:
                row = tk.Frame(f, bg=CARD_BG)
                row.pack(fill="x", pady=1)
                tk.Label(row, text=str(nr), font=("Consolas", 10),
                         bg=CARD_BG, fg=TEXT_MUTED, width=8, anchor="w").pack(side="left", padx=15)
                for opt in ["Sub", "Peste"]:
                    key = f"{title}_{nr}_{opt}"
                    sel_var = tk.StringVar(value="")
                    cota_var = tk.StringVar(value="")
                    selectii[key] = (sel_var, cota_var, f"{opt} {nr}")
                    col = tk.Frame(row, bg="#1a1f2a")
                    col.pack(side="left", fill="x", expand=True, padx=1)
                    btn = tk.Button(col, text=opt, bg="#1a1f2a", fg=TEXT_MUTED,
                                    relief="flat", font=("Consolas", 10),
                                    pady=5, cursor="hand2", bd=0)
                    btn.pack(fill="x")
                    e = tk.Entry(col, textvariable=cota_var, width=7,
                                 bg="#1a1f2a", fg=ACCENT, insertbackground=ACCENT,
                                 relief="flat", font=("Consolas", 11, "bold"),
                                 justify="center", highlightthickness=0)
                    e.pack(fill="x", pady=2)
                    e.insert(0, "—")
                    e.bind("<FocusIn>", lambda ev,en=e: en.delete(0,"end") if en.get()=="—" else None)
                    def toggle(k=key, b=btn, en=e, sv=sel_var):
                        if sv.get() == "on":
                            sv.set(""); b.config(bg="#1a1f2a", fg=TEXT_MUTED); en.config(bg="#1a1f2a")
                        else:
                            sv.set("on"); b.config(bg=ACCENT, fg=BG); en.config(bg=ACCENT2)
                    btn.config(command=toggle)
            tk.Frame(f, bg=BORDER, height=1).pack(fill="x")

        make_cat_simple("Final", ["1", "X", "2"])
        make_cat_simple("Șansă Dublă", ["1X", "12", "X2"])
        make_cat_simple("GG / NGG", ["GG", "NGG"])
        make_cat_table("Total Goluri", [0.5, 1.5, 2.5, 3.5, 4.5])
        make_cat_table("Total Cornere", [7.5, 8.5, 9.5, 10.5])

        # bottom — full width, fara padx
        bot = tk.Frame(win, bg=CARD_BG)
        bot.pack(fill="x")
        preview = tk.Label(bot, text="  Nicio selecție", bg=CARD_BG, fg=TEXT_MUTED,
                           font=("Consolas", 9), wraplength=620, justify="left", anchor="w")
        preview.pack(fill="x", padx=15, pady=(8,4))
        cota_row = tk.Frame(bot, bg=CARD_BG)
        cota_row.pack(fill="x", padx=15, pady=(0,8))
        styled_label(cota_row, "Cotă totală:", color=TEXT_MUTED, size=10).pack(side="left", padx=(0,10))
        entry_cota = styled_entry(cota_row, 10)
        entry_cota.pack(side="left")

        def update_preview(*args):
            sel = [disp for k,(sv,cv,disp) in selectii.items() if sv.get()=="on"]
            preview.config(text="  "+" | ".join(sel) if sel else "  Nicio selecție",
                           fg=ACCENT if sel else TEXT_MUTED)
        for sv,cv,_ in selectii.values():
            sv.trace("w", update_preview)

        def adauga():
            meci = entry_meci.get().strip()
            cota_str = entry_cota.get().strip()
            if not meci:
                messagebox.showwarning("Atenție", "Completează meciul!", parent=win); return
            try:
                cota = float(cota_str)
            except ValueError:
                messagebox.showerror("Eroare", "Cotă totală invalidă!", parent=win); return
            sel = [disp for k,(sv,cv,disp) in selectii.items() if sv.get()=="on"]
            if not sel:
                messagebox.showwarning("Atenție", "Alege cel puțin o selecție!", parent=win); return
            label = f"{meci} ({', '.join(sel)})"
            self.bet_matches.append((label, cota, "BetBuilder"))
            self.ticket_listbox.insert("end", f"  [BB] {meci} @ {cota}")
            tip = "Pariu Simplu" if len(self.bet_matches)==1 else f"Acumulator ({len(self.bet_matches)} meciuri)"
            self.label_tip.config(text=f"Tip: {tip}")
            self.update_potential()
            messagebox.showinfo("✅", "Adăugat la bilet!", parent=win)
            win.destroy()

        styled_button(win, "➕ Adaugă la bilet", adauga).pack(fill="x")
        styled_button(win, "✕ Închide", win.destroy,
                      color=CARD_BG, text_color=TEXT_MUTED).pack(fill="x")

    def save_ticket(self):
        if not self.bet_matches:
            messagebox.showwarning("Atenție", "Adaugă cel puțin un meci!")
            return
        try:
            stake = float(self.entry_stake.get())
        except ValueError:
            messagebox.showerror("Eroare", "Miza trebuie să fie un număr!")
            return
        if len(self.bet_matches) == 1:
            match, odds, bet_type = self.bet_matches[0]
            tracker.add_bet(match, stake, odds, bet_type)
        else:
            matches     = [m for m, o, t in self.bet_matches]
            odds_list   = [o for m, o, t in self.bet_matches]
            match_types = [t for m, o, t in self.bet_matches]
            accumulator_tracker.add_accumulator(matches, odds_list, stake, match_types)
        messagebox.showinfo("✅ Succes", "Bilet salvat!")
        self.reset_ticket()
        self.refresh_bets()
        self.refresh_dashboard()

    def reset_ticket(self):
        self.bet_matches = []
        self.ticket_listbox.delete(0, "end")
        self.entry_match.delete(0, "end")
        self.entry_odds.delete(0, "end")
        self.entry_stake.delete(0, "end")
        self.label_tip.config(text="Tip: —")
        self.label_potential.config(text="Câștig potențial: —")

    def refresh_bets(self):
        self.bets_listbox.delete(0, "end")
        bets = tracker.get_all_bets()
        for i, b in enumerate(bets):
            if b.result is not None:
                continue
            tip  = f"[{b.bet_type}]" if b.bet_type else "[--]"
            line = f"  [S{i}]  ⏳  {tip:<12}  {b.match[:35]:<35}  {b.odds}x  {b.stake} RON"
            self.bets_listbox.insert("end", line)
            self.bets_listbox.insert("end", "")

        accs = accumulator_tracker.get_all()
        for i, a in enumerate(accs):
            if a.result is not None:
                continue
            collapsed = i in self._collapsed_accs
            arrow     = "▶" if collapsed else "▼"
            line = f"  [A{i}]  ⏳  {arrow}  ACUMULATOR  {a.total_odds}x  {a.stake} RON"
            self.bets_listbox.insert("end", line)
            self.bets_listbox.itemconfig(self.bets_listbox.size()-1, fg=ACCENT)

            if not collapsed:
                for match, odds, mresult, mtype in zip(a.matches, a.odds_list, a.match_results, a.match_types):
                    micon = "✅" if mresult == "win" else "❌" if mresult == "lose" else "⏳"
                    tip   = f"[{mtype}]" if mtype else "[--]"
                    mline = f"      ↳  {tip:<12}  {match[:35]:<35}  {odds}x"
                    self.bets_listbox.insert("end", mline)
                    if mresult == "win":
                        self.bets_listbox.itemconfig(self.bets_listbox.size()-1, fg="#00ff88")
                    elif mresult == "lose":
                        self.bets_listbox.itemconfig(self.bets_listbox.size()-1, fg="#ff4444")
                    else:
                        self.bets_listbox.itemconfig(self.bets_listbox.size()-1, fg=TEXT_MUTED)
            self.bets_listbox.insert("end", "")

    def _toggle_accumulator(self, event):
        selection = self.bets_listbox.curselection()
        if not selection:
            return
        item = self.bets_listbox.get(selection[0]).strip()
        if item.startswith("[A") and ("▶" in item or "▼" in item):
            acc_index = int(item[2:item.index("]")])
            if acc_index in self._collapsed_accs:
                self._collapsed_accs.discard(acc_index)
            else:
                self._collapsed_accs.add(acc_index)
            self.refresh_bets()

    def set_result(self, result):
        selection = self.bets_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenție", "Selectează un pariu!")
            return
        item = self.bets_listbox.get(selection[0])
        stripped = item.strip()

        if stripped.startswith("↳"):
            acc_index = None
            match_index = 0
            for row in range(selection[0] - 1, -1, -1):
                line = self.bets_listbox.get(row).strip()
                if line.startswith("[A"):
                    acc_index = int(line[2:line.index("]")])
                    count = 0
                    for r in range(row + 1, selection[0]):
                        if self.bets_listbox.get(r).strip().startswith("↳"):
                            count += 1
                    match_index = count
                    break
            if acc_index is None:
                messagebox.showwarning("Atenție", "Nu s-a găsit acumulatorul!")
                return
            accumulator_tracker.update_match_result(acc_index, match_index, result)
            self.refresh_bets()
            self.refresh_dashboard()
            return

        if not stripped or stripped[0] != "[":
            messagebox.showwarning("Atenție", "Selectează linia principală sau un meci ↳!")
            return
        prefix = stripped[1]
        index  = int(stripped[2:stripped.index("]")])
        if prefix == "S":
            tracker.update_result(index, result)
        else:
            accumulator_tracker.update_result(index, result)
        self.refresh_bets()
        self.refresh_dashboard()

    def delete_bet_gui(self):
        selection = self.bets_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenție", "Selectează un pariu!")
            return
        item = self.bets_listbox.get(selection[0])
        stripped = item.strip()
        if not stripped or stripped[0] != "[":
            messagebox.showwarning("Atenție", "Selectează linia principală a pariului!")
            return
        prefix = stripped[1]
        index  = int(stripped[2:stripped.index("]")])
        if messagebox.askyesno("Confirmare", "Ștergi pariul selectat?"):
            if prefix == "S":
                tracker.delete_bet(index)
            else:
                accumulator_tracker.delete_accumulator(index)
            self.refresh_bets()
            self.refresh_dashboard()

    # ── MECIURI ─────────────────────────────────────────────────
    def build_meciuri(self, frame):
        left = tk.Frame(frame, bg=CARD_BG, width=380,
                        highlightthickness=1, highlightbackground=BORDER)
        left.pack(side="left", fill="y", padx=(20,10), pady=20)
        left.pack_propagate(False)

        section_title(left, "Meciuri Viitoare").pack(fill="x", padx=15, pady=(15,5))

        from repository.api_repo import LEAGUES
        self.leagues_list    = list(LEAGUES.items())
        self.selected_league = tk.StringVar(value=self.leagues_list[0][0])

        league_names = [n for n, c in self.leagues_list]
        om = tk.OptionMenu(left, self.selected_league, *league_names)
        om.config(bg=CARD_BG, fg=TEXT, relief="flat",
                  font=("Consolas", 11), highlightthickness=0,
                  activebackground=BG, activeforeground=ACCENT)
        om["menu"].config(bg=CARD_BG, fg=TEXT, font=("Consolas", 10))
        om.pack(padx=15, pady=5, fill="x")

        styled_button(left, "🔍 Caută meciuri",
                      self.load_matches).pack(padx=15, pady=8, fill="x")

        self.matches_listbox = tk.Listbox(left, bg=BG, fg=TEXT, height=14,
                                          relief="flat", font=("Consolas", 10),
                                          selectbackground=ACCENT, selectforeground=BG,
                                          borderwidth=0, highlightthickness=0)
        self.matches_listbox.pack(padx=15, pady=5, fill="both", expand=True)

        styled_button(left, "➕ Adaugă la bilet",
                      self.add_match_from_list,
                      color="#1a3a2a", text_color=ACCENT).pack(padx=15, pady=8, fill="x")

        right = tk.Frame(frame, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=(10,20), pady=20)

        section_title(right, "Predicție Meci").pack(fill="x", pady=(15,5))

        row0 = tk.Frame(right, bg=BG)
        row0.pack(fill="x", pady=5)
        styled_label(row0, "Ligă:", color=TEXT_MUTED).pack(side="left", padx=(0,10))
        self.selected_pred_league = tk.StringVar(value=self.leagues_list[0][0])
        om_pred = tk.OptionMenu(row0, self.selected_pred_league, *league_names)
        om_pred.config(bg=CARD_BG, fg=TEXT, relief="flat",
                       font=("Consolas", 11), highlightthickness=0,
                       activebackground=BG, activeforeground=ACCENT)
        om_pred["menu"].config(bg=CARD_BG, fg=TEXT)
        om_pred.pack(side="left", fill="x", expand=True)

        row1 = tk.Frame(right, bg=BG)
        row1.pack(fill="x", pady=5)
        styled_label(row1, "Gazdă:", color=TEXT_MUTED).pack(side="left", padx=(0,10))
        self.selected_home = tk.StringVar(value="")
        self.dropdown_home = tk.OptionMenu(row1, self.selected_home, "")
        self.dropdown_home.config(bg=CARD_BG, fg=TEXT, relief="flat",
                                  font=("Consolas", 11), highlightthickness=0)
        self.dropdown_home["menu"].config(bg=CARD_BG, fg=TEXT)
        self.dropdown_home.pack(side="left", fill="x", expand=True)

        row2 = tk.Frame(right, bg=BG)
        row2.pack(fill="x", pady=5)
        styled_label(row2, "Oaspete:", color=TEXT_MUTED).pack(side="left", padx=(0,5))
        self.selected_away = tk.StringVar(value="")
        self.dropdown_away = tk.OptionMenu(row2, self.selected_away, "")
        self.dropdown_away.config(bg=CARD_BG, fg=TEXT, relief="flat",
                                  font=("Consolas", 11), highlightthickness=0)
        self.dropdown_away["menu"].config(bg=CARD_BG, fg=TEXT)
        self.dropdown_away.pack(side="left", fill="x", expand=True)

        btn_row = tk.Frame(right, bg=BG)
        btn_row.pack(fill="x", pady=8)
        styled_button(btn_row, "🔄 Încarcă echipe",
                      self.load_teams_for_prediction,
                      color=CARD_BG, text_color=ACCENT).pack(side="left", padx=(0,10))
        styled_button(btn_row, "🔮 Calculează",
                      self.calculate_prediction).pack(side="left")
        styled_button(btn_row, "📊 Statistici",
                      self.show_detailed_stats,
                      color="#1a2a3a", text_color="#00aaff").pack(side="left", padx=(10,0))

        self.prediction_text = tk.Text(right, bg=CARD_BG, fg=TEXT,
                                       relief="flat", font=("Consolas", 10),
                                       highlightthickness=1, highlightbackground=BORDER,
                                       insertbackground=ACCENT)
        self.prediction_text.pack(fill="both", expand=True)

    def show_detailed_stats(self):
        home_name = self.selected_home.get()
        away_name = self.selected_away.get()

        if not home_name or not away_name:
            messagebox.showwarning("Atenție", "Încarcă echipele mai întâi!")
            return
        if home_name == away_name:
            messagebox.showwarning("Atenție", "Alege echipe diferite!")
            return

        home_id = self.teams_dict.get(home_name)
        away_id = self.teams_dict.get(away_name)

        win = tk.Toplevel(self.root)
        win.title(f"📊 Statistici: {home_name} vs {away_name}")
        win.geometry("650x600")
        win.configure(bg=BG)

        section_title(win, "Statistici Detaliate").pack(fill="x", padx=20, pady=(15,5))

        self._home_stats = None
        self._away_stats = None

        btn_frame = tk.Frame(win, bg=BG)
        btn_frame.pack(fill="x", padx=20, pady=5)

        text = tk.Text(win, bg=CARD_BG, fg=TEXT, relief="flat",
                       font=("Consolas", 10), padx=15, pady=15,
                       highlightthickness=1, highlightbackground=BORDER)
        text.pack(fill="both", expand=True, padx=20, pady=(5,15))
        text.insert("end", "Apasă butoanele de mai sus pentru a încărca statisticile.\n"
                           "⚠️ Încarcă o echipă, așteaptă, apoi încarcă cealaltă!\n"
                           "(limită API: 10 requesturi/minut)")
        text.config(state="disabled")

        def load_home():
            from business.stats_analyzer import get_team_stats, format_team_stats
            text.config(state="normal")
            text.delete("1.0", "end")
            text.insert("end", f"Se încarcă {home_name}...\n")
            win.update()
            self._home_stats = get_team_stats(home_id)
            result = format_team_stats(self._home_stats, home_name)
            text.delete("1.0", "end")
            text.insert("end", result)
            if self._away_stats:
                show_combined()
            text.config(state="disabled")

        def load_away():
            from business.stats_analyzer import get_team_stats, format_team_stats
            text.config(state="normal")
            text.delete("1.0", "end")
            text.insert("end", f"Se încarcă {away_name}...\n")
            win.update()
            self._away_stats = get_team_stats(away_id)
            result = format_team_stats(self._away_stats, away_name)
            text.delete("1.0", "end")
            text.insert("end", result)
            if self._home_stats:
                show_combined()
            text.config(state="disabled")

        def show_combined():
            from business.stats_analyzer import combine_stats, format_combined_stats, format_team_stats
            combined      = combine_stats(self._home_stats, self._away_stats)
            home_text     = format_team_stats(self._home_stats, home_name)
            away_text     = format_team_stats(self._away_stats, away_name)
            combined_text = format_combined_stats(combined, home_name, away_name)
            text.config(state="normal")
            text.delete("1.0", "end")
            text.insert("end", home_text + "\n\n" + away_text + combined_text)
            text.config(state="disabled")

        styled_button(btn_frame, f"📊 Încarcă {home_name[:15]}",
                      load_home, color=CARD_BG, text_color=ACCENT).pack(side="left", padx=(0,10))
        styled_button(btn_frame, f"📊 Încarcă {away_name[:15]}",
                      load_away, color=CARD_BG, text_color=ACCENT).pack(side="left")

    def load_matches(self):
        from repository.api_repo import get_upcoming_matches
        code = dict(self.leagues_list)[self.selected_league.get()]
        self.matches_listbox.delete(0, "end")
        self.matches_listbox.insert("end", "  Se încarcă...")
        self.root.update()
        matches = get_upcoming_matches(code)
        self.loaded_matches = matches
        self.matches_listbox.delete(0, "end")
        for m in matches:
            self.matches_listbox.insert("end", f"  {m}")

    def add_match_from_list(self):
        selection = self.matches_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenție", "Selectează un meci!")
            return
        match_str = self.loaded_matches[selection[0]].split(" | ")[1]
        self.entry_match.delete(0, "end")
        self.entry_match.insert(0, match_str)
        self.show_page("pariuri")
        messagebox.showinfo("✅", f"Meci adăugat:\n{match_str}\nIntroduce cota și miza!")

    def load_teams_for_prediction(self):
        from repository.api_repo import get_teams
        code = dict(self.leagues_list)[self.selected_pred_league.get()]
        self.prediction_text.delete("1.0", "end")
        self.prediction_text.insert("end", "Se încarcă echipele...\n")
        self.root.update()
        self.teams_dict = get_teams(code)
        team_names = list(self.teams_dict.keys())
        self.selected_home.set(team_names[0])
        menu_home = self.dropdown_home["menu"]
        menu_home.delete(0, "end")
        for name in team_names:
            menu_home.add_command(label=name, command=lambda n=name: self.selected_home.set(n))
        self.selected_away.set(team_names[1])
        menu_away = self.dropdown_away["menu"]
        menu_away.delete(0, "end")
        for name in team_names:
            menu_away.add_command(label=name, command=lambda n=name: self.selected_away.set(n))
        self.prediction_text.delete("1.0", "end")
        self.prediction_text.insert("end", f"✅ Încărcate {len(team_names)} echipe!\n")

    def calculate_prediction(self):
        from business.predictor import predict_match
        home_name = self.selected_home.get()
        away_name = self.selected_away.get()
        code = dict(self.leagues_list)[self.selected_pred_league.get()]
        if not home_name or not away_name:
            messagebox.showwarning("Atenție", "Încarcă echipele mai întâi!")
            return
        if home_name == away_name:
            messagebox.showwarning("Atenție", "Alege echipe diferite!")
            return
        home_id = self.teams_dict.get(home_name)
        away_id = self.teams_dict.get(away_name)
        self.prediction_text.delete("1.0", "end")
        self.prediction_text.insert("end", "Se calculează...\n")
        self.root.update()
        result = predict_match(home_id, away_id, code)
        self.prediction_text.delete("1.0", "end")
        self.prediction_text.insert("end", result)

    # ── GRAFIC ──────────────────────────────────────────────────
    def build_grafic(self, frame):
        tk.Label(frame, text="", bg=BG).pack(pady=40)
        section_title(frame, "Grafic Profit").pack(fill="x", padx=30)

        card = tk.Frame(frame, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=30, pady=20, fill="x")

        tk.Label(card, text="📈", font=("Arial", 48),
                 bg=CARD_BG, fg=ACCENT).pack(pady=(30,10))
        styled_label(card, "Vizualizează evoluția profitului tău în timp",
                     color=TEXT_MUTED).pack(pady=5)
        styled_label(card, "Graficul include atât pariuri simple cât și acumulatori",
                     size=9, color=TEXT_MUTED).pack(pady=2)

        styled_button(card, "📈 Afișează Grafic",
                      show_profit_chart).pack(pady=25, padx=30, fill="x")

        tk.Label(card, text="* Se deschide într-o fereastră separată",
                 font=("Consolas", 8), bg=CARD_BG, fg=BORDER).pack(pady=(0,15))

    # ── VALUE BET ───────────────────────────────────────────────
    def build_value(self, frame):
        tk.Label(frame, text="", bg=BG).pack(pady=20)
        section_title(frame, "Value Bet Calculator").pack(fill="x", padx=30)

        card = tk.Frame(frame, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=30, pady=15, fill="x")

        fields = [
            ("Șansa ta estimată (%):", "entry_prob",       "ex: 60"),
            ("Cota bookmakerului:",    "entry_book_odds",  "ex: 2.10"),
            ("Miză (RON):",           "entry_book_stake", "ex: 50"),
        ]
        for label, attr, placeholder in fields:
            styled_label(card, label, color=TEXT_MUTED).pack(anchor="w", padx=25, pady=(12,0))
            entry = styled_entry(card, 40)
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, en=entry, ph=placeholder: en.delete(0, "end") if en.get() == ph else None)
            entry.pack(padx=25, pady=3, fill="x")
            setattr(self, attr, entry)

        styled_button(card, "💰 Calculează Value",
                      self.calculate_value).pack(padx=25, pady=20, fill="x")

        self.value_result = tk.Label(frame, text="", bg=BG, fg=TEXT,
                                     font=("Consolas", 13), justify="left")
        self.value_result.pack(pady=20, padx=30, anchor="w")

    def calculate_value(self):
        from business.calculator import odds_to_probability, has_value, expected_value
        try:
            prob  = float(self.entry_prob.get())
            odds  = float(self.entry_book_odds.get())
            stake = float(self.entry_book_stake.get())
        except ValueError:
            messagebox.showerror("Eroare", "Completează toate câmpurile corect!")
            return
        implied     = odds_to_probability(odds)
        value, is_v = has_value(prob, odds)
        ev          = expected_value(stake, prob, odds)
        color       = ACCENT if is_v else RED
        verdict     = "✅ Pariu cu VALUE — merită!" if is_v else "❌ Fără value — skip!"
        self.value_result.config(
            text=(f"  Prob. implicită bookmaker : {implied}%\n"
                  f"  Probabilitatea ta          : {prob}%\n"
                  f"  Value                      : {value:+.1f}%\n"
                  f"  Expected Value             : {ev:+.2f} RON\n\n"
                  f"  {verdict}"),
            fg=color)

    # ── BANK ────────────────────────────────────────────────────
    def build_bank(self, frame):
        header = tk.Frame(frame, bg=BG)
        header.pack(fill="x", padx=30, pady=(25,10))
        styled_label(header, "Bank Management", 20, bold=True, color=TEXT).pack(side="left")

        card = tk.Frame(frame, bg=CARD_BG,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", padx=30, pady=10)

        row = tk.Frame(card, bg=CARD_BG)
        row.pack(fill="x", padx=20, pady=15)
        styled_label(row, "Buget initial (RON):", color=TEXT_MUTED).pack(side="left", padx=(0,10))
        self.entry_buget = styled_entry(row, 15)
        self.entry_buget.pack(side="left", padx=(0,10))
        styled_button(row, "💾 Setează", self.save_buget).pack(side="left")

        row2 = tk.Frame(card, bg=CARD_BG)
        row2.pack(fill="x", padx=20, pady=(0,15))
        styled_label(row2, "Adauga Fonduri:", color=TEXT_MUTED).pack(side="left", padx=(0,10))
        self.entry_adauga = styled_entry(row2, 15)
        self.entry_adauga.pack(side="left", padx=(0,10))
        styled_button(row2, "➕ Adaugă", self.adauga_fonduri).pack(side="left")

        stats_frame = tk.Frame(frame, bg=BG)
        stats_frame.pack(fill="x", padx=30, pady=10)

        self.bank_labels = {}
        bank_stats = [
            ("💰 Buget Inițial",   "initial", ACCENT),
            ("🏦 Buget Curent",    "curent",  ACCENT),
            ("📈 Profit/Pierdere", "profit",  ACCENT),
        ]

        for i, (title, key, color) in enumerate(bank_stats):
            c = tk.Frame(stats_frame, bg=CARD_BG,
                         highlightthickness=1, highlightbackground=BORDER)
            c.grid(row=0, column=i, padx=8, pady=8, sticky="ew")
            stats_frame.columnconfigure(i, weight=1)
            tk.Label(c, text=title, font=("Consolas", 9),
                     bg=CARD_BG, fg=TEXT_MUTED).pack(pady=(15,5), padx=15, anchor="w")
            lbl = tk.Label(c, text="—", font=("Consolas", 18, "bold"),
                           bg=CARD_BG, fg=color)
            lbl.pack(pady=(0,15), padx=15, anchor="w")
            self.bank_labels[key] = lbl

        styled_button(frame, "🔄 Refresh & Grafic",
                      self.refresh_bank).pack(padx=30, pady=10, fill="x")

        self.refresh_bank()

    def adauga_fonduri(self):
        from repository.bank_repo import load_bank, save_bank
        try:
            suma = float(self.entry_adauga.get())
            data = load_bank()
            data["buget_initial"] = round(data["buget_initial"] + suma, 2)
            save_bank(data)
            messagebox.showinfo("✅", f"+{suma} RON adăugați la buget!")
            self.entry_adauga.delete(0, "end")
            self.refresh_bank()
        except ValueError:
            messagebox.showerror("Eroare", "Introdu un număr valid!")

    def save_buget(self):
        from business.bank_manager import set_buget_initial
        try:
            suma = float(self.entry_buget.get())
            set_buget_initial(suma)
            messagebox.showinfo("✅", "Buget setat!")
            self.refresh_bank()
        except ValueError:
            messagebox.showerror("Eroare", "Introdu un număr valid!")

    def refresh_bank(self):
        from business.bank_manager import get_status, get_evolutie
        import matplotlib.pyplot as plt

        status = get_status()

        self.bank_labels["initial"].config(text=f"{status['buget_initial']:.2f} RON")
        self.bank_labels["curent"].config(text=f"{status['buget_curent']:.2f} RON")
        self.bank_labels["profit"].config(
            text=f"{status['profit']:+.2f} RON",
            fg=ACCENT if status["profit"] >= 0 else RED)

        valori, labels = get_evolutie()
        if len(valori) < 2:
            return

        plt.figure(figsize=(12, 5))
        plt.plot(valori, marker="o", linewidth=2, color="#00ff88")
        plt.fill_between(range(len(valori)), valori, valori[0],
                         where=[v >= valori[0] for v in valori],
                         alpha=0.2, color="#00ff88")
        plt.fill_between(range(len(valori)), valori, valori[0],
                         where=[v < valori[0] for v in valori],
                         alpha=0.2, color="#ff4444")
        plt.axhline(y=valori[0], color="gray", linestyle="--", linewidth=1)
        plt.xticks(range(len(labels)), labels, rotation=45, ha="right", fontsize=8)
        plt.title("Evoluție Buget", fontsize=14, color="white")
        plt.gca().set_facecolor("#1c2128")
        plt.gcf().set_facecolor("#0d1117")
        plt.tick_params(colors="white")
        plt.ylabel("RON", color="white")
        plt.tight_layout()
        plt.show()

    # ── ISTORIC ─────────────────────────────────────────────────
    def build_istoric(self, frame):
        header = tk.Frame(frame, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 10))
        styled_label(header, "Istoric Pariuri", 20, bold=True, color=TEXT).pack(side="left")

        filter_frame = tk.Frame(frame, bg=CARD_BG,
                                highlightthickness=1, highlightbackground=BORDER)
        filter_frame.pack(fill="x", padx=30, pady=5)

        inner = tk.Frame(filter_frame, bg=CARD_BG)
        inner.pack(fill="x", padx=15, pady=10)

        styled_label(inner, "Rezultat:", color=TEXT_MUTED, size=10).pack(side="left", padx=(0, 5))
        self.filter_result = tk.StringVar(value="Toate")
        for opt in ["Toate", "Win", "Lose"]:
            tk.Radiobutton(inner, text=opt, variable=self.filter_result,
                           value=opt, bg=CARD_BG, fg=TEXT, selectcolor=BG,
                           activebackground=CARD_BG, activeforeground=ACCENT,
                           font=("Consolas", 10),
                           command=self.refresh_istoric).pack(side="left", padx=5)

        tk.Frame(inner, bg=BORDER, width=1).pack(side="left", padx=10, fill="y")

        styled_label(inner, "Tip:", color=TEXT_MUTED, size=10).pack(side="left", padx=(0, 5))
        self.filter_type = tk.StringVar(value="Toate")
        for opt in ["Toate", "Simplu", "Acumulator"]:
            tk.Radiobutton(inner, text=opt, variable=self.filter_type,
                           value=opt, bg=CARD_BG, fg=TEXT, selectcolor=BG,
                           activebackground=CARD_BG, activeforeground=ACCENT,
                           font=("Consolas", 10),
                           command=self.refresh_istoric).pack(side="left", padx=5)

        styled_button(inner, "🔄", self.refresh_istoric,
                      color=CARD_BG, text_color=ACCENT).pack(side="right")

        self.istoric_sumar = tk.Frame(frame, bg=BG)
        self.istoric_sumar.pack(fill="x", padx=30, pady=5)

        list_frame = tk.Frame(frame, bg=CARD_BG,
                              highlightthickness=1, highlightbackground=BORDER)
        list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 5))

        self.istoric_listbox = tk.Listbox(list_frame, bg=CARD_BG, fg=TEXT,
                                          relief="flat", font=("Consolas", 10),
                                          selectbackground=ACCENT, selectforeground=BG,
                                          borderwidth=0, highlightthickness=0)
        self.istoric_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        btn_row = tk.Frame(frame, bg=BG)
        btn_row.pack(fill="x", padx=30, pady=(0, 15))

        styled_button(btn_row, "✅ Win",
                      lambda: self.set_result_istoric("win"),
                      color="#1a3a2a", text_color=ACCENT).pack(side="left", padx=5)
        styled_button(btn_row, "❌ Lose",
                      lambda: self.set_result_istoric("lose"),
                      color="#2d1f1f", text_color=RED).pack(side="left", padx=5)

        self.refresh_istoric()

    def set_result_istoric(self, result):
        import re
        selection = self.istoric_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenție", "Selectează un pariu!")
            return
        item = self.istoric_listbox.get(selection[0]).strip()

        if not item or item.startswith("─"):
            messagebox.showwarning("Atenție", "Selectează un pariu sau meci!")
            return

        # cazul liniei ↳ din acumulator — contine [Ax] embedded
        if item.startswith("↳"):
            match = re.search(r'\[A(\d+)\]', item)
            if not match:
                messagebox.showwarning("Atenție", "Nu s-a găsit acumulatorul!")
                return
            acc_index = int(match.group(1))

            # calculeaza match_index numarand liniile ↳ de la linia principala
            match_index = 0
            for row in range(selection[0] - 1, -1, -1):
                line = self.istoric_listbox.get(row).strip()
                if "Acumulator" in line or "[ACC]" in line:
                    match_index = selection[0] - row - 1
                    break

            accumulator_tracker.update_match_result(acc_index, match_index, result)
            self.refresh_istoric()
            self.refresh_dashboard()
            return

        # cazul liniei principale simplu — contine [Sx] embedded
        s_match = re.search(r'\[S(\d+)\]', item)
        if s_match:
            idx = int(s_match.group(1))
            tracker.update_result(idx, result)
            self.refresh_istoric()
            self.refresh_dashboard()
            messagebox.showinfo("✅", f"Rezultat actualizat: {result}!")
            return

        # cazul liniei principale acumulator — contine [Ax] embedded
        a_match = re.search(r'\[A(\d+)\]', item)
        if a_match:
            idx = int(a_match.group(1))
            accumulator_tracker.update_result(idx, result)
            self.refresh_istoric()
            self.refresh_dashboard()
            messagebox.showinfo("✅", f"Rezultat actualizat: {result}!")
            return

        messagebox.showwarning("Atenție", "Nu s-a găsit pariul!")

    def refresh_istoric(self):
        for w in self.istoric_sumar.winfo_children():
            w.destroy()

        self.istoric_listbox.delete(0, "end")

        bets = tracker.get_all_bets()
        accs = accumulator_tracker.get_all()

        f_result = self.filter_result.get()
        f_type   = self.filter_type.get()

        entries = []

        if f_type in ("Toate", "Simplu"):
            for idx, b in enumerate(bets):
                if b.result is None:
                    continue
                if f_result == "Win" and b.result != "win":
                    continue
                if f_result == "Lose" and b.result != "lose":
                    continue
                entries.append({
                    "date":       b.date,
                    "label":      b.match[:35],
                    "odds":       b.odds,
                    "stake":      b.stake,
                    "profit":     b.profit,
                    "result":     b.result,
                    "tip":        f"[{b.bet_type}]" if b.bet_type else "[--]",
                    "type":       "S",
                    "real_index": idx,
                })

        if f_type in ("Toate", "Acumulator"):
            for idx, a in enumerate(accs):
                if a.result is None:
                    continue
                if f_result == "Win" and a.result != "win":
                    continue
                if f_result == "Lose" and a.result != "lose":
                    continue
                entries.append({
                    "date":       a.date,
                    "label":      f"Acumulator ({len(a.matches)} meciuri)",
                    "odds":       a.total_odds,
                    "stake":      a.stake,
                    "profit":     a.profit,
                    "result":     a.result,
                    "tip":        "[ACC]",
                    "type":       "A",
                    "real_index": idx,
                    "matches":    a.matches,
                    "odds_list":  a.odds_list,
                })

        entries.sort(key=lambda e: e["date"], reverse=True)

        # sumar
        if entries:
            total_profit = round(sum(e["profit"] for e in entries), 2)
            wins         = sum(1 for e in entries if e["result"] == "win")
            win_rate     = round(wins / len(entries) * 100, 1)

            sumar_items = [
                ("Total",     str(len(entries))),
                ("Câștigate", str(wins)),
                ("Win Rate",  f"{win_rate}%"),
                ("Profit",    f"{total_profit:+.2f} RON"),
            ]
            for label, value in sumar_items:
                c = tk.Frame(self.istoric_sumar, bg=CARD_BG,
                             highlightthickness=1, highlightbackground=BORDER)
                c.pack(side="left", padx=5, pady=5)
                styled_label(c, label, size=9, color=TEXT_MUTED).pack(padx=10, pady=(8, 2))
                color = ACCENT if "+" in value or "%" in value else TEXT
                if label == "Profit":
                    color = ACCENT if total_profit >= 0 else RED
                styled_label(c, value, size=13, bold=True, color=color).pack(padx=10, pady=(0, 8))

        # afiseaza — includem real_index in linie ca [Sx] sau [Ax]
        for e in entries:
            icon = "✅" if e["result"] == "win" else "❌"
            idx  = e["real_index"]
            tag  = f"[S{idx}]" if e["type"] == "S" else f"[A{idx}]"
            line = f"  {e['date']}  {icon}  {tag}  {e['tip']:<6} {e['label']:<35} {e['odds']:<6}x  {e['stake']} RON  {e['profit']:+.2f} RON"
            self.istoric_listbox.insert("end", line)
            if e["result"] == "win":
                self.istoric_listbox.itemconfig(self.istoric_listbox.size()-1, fg="#00ff88")
            else:
                self.istoric_listbox.itemconfig(self.istoric_listbox.size()-1, fg="#ff4444")

            if e["type"] == "A":
                accs = accumulator_tracker.get_all()
                a = accs[e["real_index"]]
                for match, odds, mresult in zip(e["matches"], e["odds_list"], a.match_results):
                    micon = "✅" if mresult == "win" else "❌" if mresult == "lose" else "⏳"
                    self.istoric_listbox.insert("end", f"       ↳ [A{idx}] {micon} {match[:35]:<35} @ {odds}")
                    if mresult == "win":
                        self.istoric_listbox.itemconfig(self.istoric_listbox.size() - 1, fg="#00ff88")
                    elif mresult == "lose":
                        self.istoric_listbox.itemconfig(self.istoric_listbox.size() - 1, fg="#ff4444")
                    else:
                        self.istoric_listbox.itemconfig(self.istoric_listbox.size() - 1, fg=TEXT_MUTED)
                self.istoric_listbox.insert("end", "  " + "─" * 70)
                self.istoric_listbox.itemconfig(self.istoric_listbox.size() - 1, fg=BORDER)
            else:
                self.istoric_listbox.insert("end", "  " + "─" * 70)
                self.istoric_listbox.itemconfig(self.istoric_listbox.size() - 1, fg=BORDER)

    # ── ANALIZĂ TIP ─────────────────────────────────────────────
    def build_analiza(self, frame):
        header = tk.Frame(frame, bg=BG)
        header.pack(fill="x", padx=30, pady=(25,10))
        styled_label(header, "Analiză pe Tip Pariu", 20, bold=True, color=TEXT).pack(side="left")
        styled_button(header, "🔄 Refresh", self.refresh_analiza, width=12).pack(side="right")

        self.analiza_frame = tk.Frame(frame, bg=BG)
        self.analiza_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.refresh_analiza()

    def show_weekly_summary(self):
        from business.weekly_summary import get_weekly_summary, mark_summary_shown
        mark_summary_shown()

        summary = get_weekly_summary()
        if not summary:
            return

        win = tk.Toplevel(self.root)
        win.title("📅 Rezumat Săptămânal")
        win.geometry("550x480")
        win.configure(bg=BG)
        win.grab_set()

        header = tk.Frame(win, bg=ACCENT, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📅 Rezumat Săptămânal",
                 font=("Consolas", 14, "bold"),
                 bg=ACCENT, fg=BG).pack(side="left", padx=20, pady=15)
        tk.Label(header, text=f"{summary['week_start']} — {summary['week_end']}",
                 font=("Consolas", 11),
                 bg=ACCENT, fg=BG).pack(side="right", padx=20)

        cards = tk.Frame(win, bg=BG)
        cards.pack(fill="x", padx=20, pady=15)

        stats = [
            ("🎯 Pariuri",   str(summary["total"])),
            ("✅ Câștigate", str(summary["wins"])),
            ("🏆 Win Rate",  f"{summary['win_rate']}%"),
            ("💰 Profit",    f"{summary['profit']:+.2f} RON"),
        ]

        for i, (label, value) in enumerate(stats):
            c = tk.Frame(cards, bg=CARD_BG,
                         highlightthickness=1, highlightbackground=BORDER)
            c.grid(row=0, column=i, padx=5, sticky="ew")
            cards.columnconfigure(i, weight=1)
            tk.Label(c, text=label, font=("Consolas", 9),
                     bg=CARD_BG, fg=TEXT_MUTED).pack(pady=(10, 3), padx=10, anchor="w")
            color = ACCENT if "+" in value or value not in ["-", "0%"] else RED
            if "Profit" in label:
                color = ACCENT if summary["profit"] >= 0 else RED
            tk.Label(c, text=value, font=("Consolas", 14, "bold"),
                     bg=CARD_BG, fg=color).pack(pady=(0, 10), padx=10, anchor="w")

        bank_frame = tk.Frame(win, bg=CARD_BG,
                              highlightthickness=1, highlightbackground=BORDER)
        bank_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(bank_frame, text="🏦 Evoluție Bankroll",
                 font=("Consolas", 10, "bold"),
                 bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=15, pady=(10, 5))
        bank_row = tk.Frame(bank_frame, bg=CARD_BG)
        bank_row.pack(fill="x", padx=15, pady=(0, 10))
        tk.Label(bank_row, text=f"Început săptămână: {summary['buget_initial']:.2f} RON",
                 font=("Consolas", 10), bg=CARD_BG, fg=TEXT_MUTED).pack(side="left")
        tk.Label(bank_row, text=f"  →  {summary['buget_curent']:.2f} RON",
                 font=("Consolas", 10, "bold"), bg=CARD_BG,
                 fg=ACCENT if summary["buget_curent"] >= summary["buget_initial"] else RED).pack(side="left")

        for title, entry, color in [
            ("🏆 Cel mai bun pariu", summary["best"], ACCENT),
            ("💀 Cel mai rău pariu", summary["worst"], RED),
        ]:
            f = tk.Frame(win, bg=CARD_BG,
                         highlightthickness=1, highlightbackground=BORDER)
            f.pack(fill="x", padx=20, pady=5)
            tk.Label(f, text=title, font=("Consolas", 10, "bold"),
                     bg=CARD_BG, fg=color).pack(anchor="w", padx=15, pady=(10, 3))
            tk.Label(f, text=f"  {entry['match'][:45]}",
                     font=("Consolas", 10), bg=CARD_BG, fg=TEXT).pack(anchor="w", padx=15)
            tk.Label(f, text=f"  Profit: {entry['profit']:+.2f} RON | Cotă: {entry['odds']}x",
                     font=("Consolas", 9), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 10))

        styled_button(win, "✅ Închide", win.destroy).pack(pady=15, padx=20, fill="x")

    def refresh_analiza(self):
        from business.type_analyzer import get_stats_by_type

        for widget in self.analiza_frame.winfo_children():
            widget.destroy()

        stats = get_stats_by_type()
        has_data = any(v is not None for v in stats.values())

        if not has_data:
            styled_label(self.analiza_frame,
                         "Nu ai pariuri finalizate cu tip specificat încă.\nAdaugă pariuri cu tip din tab-ul Pariuri!",
                         color=TEXT_MUTED).pack(pady=50)
            return

        best_type   = None
        best_profit = None
        for bt, data in stats.items():
            if data is not None:
                if best_profit is None or data["profit"] > best_profit:
                    best_profit = data["profit"]
                    best_type   = bt

        for bet_type, data in stats.items():
            is_best = bet_type == best_type and best_profit is not None and best_profit > 0

            card = tk.Frame(self.analiza_frame, bg=CARD_BG,
                            highlightthickness=2 if is_best else 1,
                            highlightbackground=ACCENT if is_best else BORDER)
            card.pack(fill="x", pady=8)

            header = tk.Frame(card, bg=CARD_BG)
            header.pack(fill="x", padx=20, pady=(15, 5))
            styled_label(header, bet_type, 14, bold=True, color=ACCENT).pack(side="left")

            if is_best:
                tk.Label(header, text="🏆 Cel mai profitabil",
                         font=("Consolas", 9, "bold"),
                         bg=CARD_BG, fg=ACCENT).pack(side="right")

            if data is None:
                styled_label(card, "  Niciun pariu finalizat.", color=TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 15))
                continue

            stats_row = tk.Frame(card, bg=CARD_BG)
            stats_row.pack(fill="x", padx=20, pady=(5, 10))

            items = [
                ("Pariuri",   str(data["total"])),
                ("Câștigate", str(data["wins"])),
                ("Win Rate",  f"{data['win_rate']}%"),
                ("Profit",    f"{data['profit']:+.2f} RON"),
                ("ROI",       f"{data['roi']:+.1f}%"),
            ]

            for label, value in items:
                col = tk.Frame(stats_row, bg=CARD_BG)
                col.pack(side="left", padx=20)
                styled_label(col, label, size=9, color=TEXT_MUTED).pack()
                if label in ("Profit", "ROI"):
                    color = ACCENT if data["profit"] >= 0 else RED
                else:
                    color = TEXT
                styled_label(col, value, size=14, bold=True, color=color).pack()

            bar_frame = tk.Frame(card, bg=CARD_BG)
            bar_frame.pack(fill="x", padx=20, pady=(0, 15))
            styled_label(bar_frame, "Win Rate: ", size=9, color=TEXT_MUTED).pack(side="left")
            total_width = 300
            filled = int(total_width * data["win_rate"] / 100)
            canvas = tk.Canvas(bar_frame, width=total_width, height=12,
                               bg=CARD_BG, highlightthickness=0)
            canvas.pack(side="left")
            canvas.create_rectangle(0, 0, total_width, 12, fill=BORDER, outline="")
            canvas.create_rectangle(0, 0, filled, 12,
                                    fill=ACCENT if data["win_rate"] >= 50 else RED,
                                    outline="")


def run():
    root = tk.Tk()
    app  = BettingApp(root)
    root.mainloop()