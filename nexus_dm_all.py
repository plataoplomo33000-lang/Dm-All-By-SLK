import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import asyncio
import discord
from discord.ext import commands

class NexusTool:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS - Discord DM All Tool")
        self.root.geometry("900x750")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(False, False)
        
        # Colors
        self.bg_color = '#0a0a0a'
        self.yellow = '#FFD700'
        self.dark_yellow = '#B8860B'
        self.border_color = '#FFD700'
        self.red = '#FF4444'
        self.blue = '#4444FF'
        
        # Stats
        self.sent_count = 0
        self.failed_count = 0
        self.total_count = 0
        
        # Discord bot
        self.bot = None
        self.bot_ready = False
        self.loop = None
        self.is_sending = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title Frame
        title_frame = tk.Frame(main_frame, bg=self.bg_color, highlightbackground=self.border_color, 
                              highlightthickness=2)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # URL Webshop
        url_label = tk.Label(title_frame, text="https://nexus-webshop.mysellauth.com", 
                            font=('Courier New', 9),
                            fg=self.dark_yellow, bg=self.bg_color)
        url_label.pack(pady=(10, 5))
        
        # NEXUS ASCII Art Title
        nexus_art = """███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"""
        
        title_label = tk.Label(title_frame, text=nexus_art, 
                              font=('Courier New', 8, 'bold'),
                              fg=self.yellow, bg=self.bg_color,
                              justify=tk.LEFT)
        title_label.pack(pady=8)
        
        # DM ALL ASCII Art Subtitle (encore plus réduit)
        dmall_art = """██████╗ ███╗   ███╗    ▄▄▄   ██╗     ██╗     
██╔══██╗████╗ ████║   ██╔══██╗██║     ██║     
██║  ██║██╔████╔██║   ███████║██║     ██║     
██████╔╝██║ ╚═╝ ██║   ██╔══██║███████╗███████╗
╚═════╝ ╚═╝     ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝"""
        
        subtitle_label = tk.Label(title_frame, text=dmall_art, 
                                 font=('Courier New', 4, 'bold'),
                                 fg=self.yellow, bg=self.bg_color,
                                 justify=tk.LEFT)
        subtitle_label.pack(pady=3)
        
        # BY SLK ASCII Art (très petit)
        byslk_art = """██████╗ ██╗   ██╗    ███████╗██╗     ██╗  ██╗
██╔══██╗╚██╗ ██╔╝    ██╔════╝██║     ██║ ██╔╝
██████╔╝ ╚████╔╝     ███████╗██║     █████╔╝ 
██╔══██╗  ╚██╔╝      ╚════██║██║     ██╔═██╗ 
██████╔╝   ██║       ███████║███████╗██║  ██╗
╚═════╝    ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝"""
        
        author_label = tk.Label(title_frame, text=byslk_art, 
                               font=('Courier New', 2, 'bold'),
                               fg=self.yellow, bg=self.bg_color,
                               justify=tk.LEFT)
        author_label.pack(pady=(0, 8))
        
        # Stats Frame
        stats_frame = tk.Frame(main_frame, bg=self.bg_color)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # SENT stat
        sent_frame = tk.Frame(stats_frame, bg=self.bg_color, 
                             highlightbackground=self.border_color, highlightthickness=2)
        sent_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(sent_frame, text="✓ SENT", font=('Courier New', 10),
                fg=self.yellow, bg=self.bg_color).pack(anchor=tk.W, padx=10, pady=(10, 5))
        self.sent_label = tk.Label(sent_frame, text="0", font=('Courier New', 36, 'bold'),
                                   fg=self.yellow, bg=self.bg_color)
        self.sent_label.pack(padx=10, pady=(0, 10))
        
        # FAILED stat
        failed_frame = tk.Frame(stats_frame, bg=self.bg_color,
                               highlightbackground=self.border_color, highlightthickness=2)
        failed_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(failed_frame, text="✗ FAILED", font=('Courier New', 10),
                fg=self.red, bg=self.bg_color).pack(anchor=tk.W, padx=10, pady=(10, 5))
        self.failed_label = tk.Label(failed_frame, text="0", font=('Courier New', 36, 'bold'),
                                     fg=self.red, bg=self.bg_color)
        self.failed_label.pack(padx=10, pady=(0, 10))
        
        # TOTAL stat
        total_frame = tk.Frame(stats_frame, bg=self.bg_color,
                              highlightbackground=self.border_color, highlightthickness=2)
        total_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(total_frame, text="◈ TOTAL", font=('Courier New', 10),
                fg=self.blue, bg=self.bg_color).pack(anchor=tk.W, padx=10, pady=(10, 5))
        self.total_label = tk.Label(total_frame, text="0", font=('Courier New', 36, 'bold'),
                                    fg=self.blue, bg=self.bg_color)
        self.total_label.pack(padx=10, pady=(0, 10))
        
        # Control Panel Frame
        control_frame = tk.Frame(main_frame, bg=self.bg_color,
                                highlightbackground=self.border_color, highlightthickness=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Control Panel Header
        tk.Label(control_frame, text="⚡ CONTROL PANEL", font=('Courier New', 12, 'bold'),
                fg=self.yellow, bg=self.bg_color).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Token Input
        tk.Label(control_frame, text="[?] DISCORD BOT TOKEN", font=('Courier New', 9),
                fg=self.yellow, bg=self.bg_color).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.token_entry = tk.Entry(control_frame, font=('Courier New', 10),
                                    bg='#1a1a1a', fg='#888888', 
                                    insertbackground=self.yellow,
                                    relief=tk.FLAT, bd=0, show="")
        self.token_entry.pack(fill=tk.X, padx=15, pady=(0, 15), ipady=8)
        self.token_entry.insert(0, "Enter your Discord bot token...")
        self.token_entry.bind('<FocusIn>', self.on_token_focus_in)
        self.token_entry.bind('<FocusOut>', self.on_token_focus_out)
        
        # Message Input
        tk.Label(control_frame, text="[?] MESSAGE TO SEND (DM TO ALL MEMBERS)", font=('Courier New', 9),
                fg=self.yellow, bg=self.bg_color).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Message text area
        message_frame = tk.Frame(control_frame, bg='#1a1a1a')
        message_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.message_text = scrolledtext.ScrolledText(message_frame, 
                                                      font=('Courier New', 10),
                                                      bg='#1a1a1a', fg='#888888',
                                                      insertbackground=self.yellow,
                                                      relief=tk.FLAT, bd=0,
                                                      height=4)
        self.message_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.message_text.insert(tk.END, "Enter your message here...")
        self.message_text.bind('<FocusIn>', self.on_message_focus_in)
        self.message_text.bind('<FocusOut>', self.on_message_focus_out)
        
        # Connect Button
        self.connect_btn = tk.Button(control_frame, text="CONNECT", 
                                     font=('Courier New', 12, 'bold'),
                                     bg=self.yellow, fg='#0a0a0a',
                                     activebackground=self.dark_yellow,
                                     relief=tk.FLAT, bd=0,
                                     cursor='hand2',
                                     command=self.connect_bot)
        self.connect_btn.pack(fill=tk.X, padx=15, pady=(0, 10), ipady=10)
        
        # Send Button
        self.send_btn = tk.Button(control_frame, text="DM ALL MEMBERS", 
                                 font=('Courier New', 12, 'bold'),
                                 bg='#444444', fg=self.yellow,
                                 activebackground='#555555',
                                 relief=tk.FLAT, bd=0,
                                 cursor='hand2',
                                 state=tk.DISABLED,
                                 command=self.mass_dm)
        self.send_btn.pack(fill=tk.X, padx=15, pady=(0, 15), ipady=10)
        
        # System Console Frame
        console_frame = tk.Frame(main_frame, bg=self.bg_color,
                                highlightbackground=self.border_color, highlightthickness=2)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console Header
        tk.Label(console_frame, text="⚙ SYSTEM CONSOLE", font=('Courier New', 12, 'bold'),
                fg=self.yellow, bg=self.bg_color).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Console Text Area
        self.console = scrolledtext.ScrolledText(console_frame, 
                                                font=('Courier New', 9),
                                                bg='#0a0a0a', fg=self.yellow,
                                                insertbackground=self.yellow,
                                                relief=tk.FLAT, bd=0,
                                                height=8,
                                                state=tk.NORMAL)  # IMPORTANT: Start as NORMAL
        self.console.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.console.insert(tk.END, "[SYSTEM] En attente d'initialisation...\n")
        
    def on_token_focus_in(self, event):
        if self.token_entry.get() == "Enter your Discord bot token...":
            self.token_entry.delete(0, tk.END)
            self.token_entry.config(fg=self.yellow)
    
    def on_token_focus_out(self, event):
        if self.token_entry.get() == "":
            self.token_entry.insert(0, "Enter your Discord bot token...")
            self.token_entry.config(fg='#888888')
    
    def on_message_focus_in(self, event):
        if self.message_text.get("1.0", tk.END).strip() == "Enter your message here...":
            self.message_text.delete("1.0", tk.END)
            self.message_text.config(fg=self.yellow)
    
    def on_message_focus_out(self, event):
        if self.message_text.get("1.0", tk.END).strip() == "":
            self.message_text.insert("1.0", "Enter your message here...")
            self.message_text.config(fg='#888888')
    
    def log(self, message):
        """Affiche un message dans la console EN TEMPS REEL"""
        def _add_to_console():
            timestamp = time.strftime("%H:%M:%S")
            self.console.insert(tk.END, f"[{timestamp}] {message}\n")
            self.console.see(tk.END)
            self.console.update_idletasks()  # Force le rafraîchissement immédiat
        
        # Exécute sur le thread principal tkinter
        self.root.after(0, _add_to_console)
    
    def update_stats(self):
        """Met à jour les statistiques"""
        self.sent_label.config(text=str(self.sent_count))
        self.failed_label.config(text=str(self.failed_count))
        self.total_label.config(text=str(self.total_count))
    
    def connect_bot(self):
        token = self.token_entry.get()
        if token == "Enter your Discord bot token..." or token == "":
            self.log("❌ ERREUR: Veuillez entrer un token Discord valide!")
            return
        
        self.connect_btn.config(state=tk.DISABLED, text="CONNEXION...")
        self.log("🔄 Initialisation de la connexion...")
        
        # Démarre le bot dans un thread séparé
        def run_bot():
            try:
                # Crée une nouvelle boucle d'événements pour ce thread
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                
                # Crée le bot avec TOUS les intents (nécessaire pour voir les membres)
                intents = discord.Intents.all()
                self.bot = commands.Bot(command_prefix='!', intents=intents)
                
                @self.bot.event
                async def on_ready():
                    self.bot_ready = True
                    guild_count = len(self.bot.guilds)
                    
                    # Compte le total de membres
                    total_members = 0
                    for guild in self.bot.guilds:
                        total_members += guild.member_count
                    
                    self.log(f"✅ Bot connecté: {self.bot.user.name}#{self.bot.user.discriminator}")
                    self.log(f"📊 Présent dans {guild_count} serveur(s)")
                    self.log(f"👥 Total de membres: {total_members}")
                    self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    
                    # Liste tous les serveurs
                    for guild in self.bot.guilds:
                        self.log(f"  🔸 {guild.name} ({guild.member_count} membres)")
                    
                    self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    self.log("✅ Bot prêt à envoyer des DM!")
                    self.log("⚠️  ATTENTION: Le mass DM peut déclencher des rate limits Discord!")
                    
                    self.connect_btn.config(state=tk.NORMAL, text="CONNECTÉ ✓", bg='#44FF44')
                    self.send_btn.config(state=tk.NORMAL, bg=self.yellow, fg='#0a0a0a')
                
                # Lance le bot
                self.loop.run_until_complete(self.bot.start(token))
                
            except discord.LoginFailure:
                self.log("❌ ERREUR: Token invalide! Vérifiez votre token Discord.")
                self.connect_btn.config(state=tk.NORMAL, text="CONNECT", bg=self.yellow)
            except Exception as e:
                self.log(f"❌ ERREUR de connexion: {str(e)}")
                self.connect_btn.config(state=tk.NORMAL, text="CONNECT", bg=self.yellow)
        
        threading.Thread(target=run_bot, daemon=True).start()
    
    def mass_dm(self):
        if not self.bot_ready or not self.bot:
            self.log("❌ ERREUR: Bot non connecté! Connectez-vous d'abord.")
            return
        
        if self.is_sending:
            self.log("⚠️  Envoi déjà en cours! Veuillez attendre.")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        if message == "Enter your message here..." or message == "":
            self.log("❌ ERREUR: Veuillez entrer un message à envoyer!")
            return
        
        self.is_sending = True
        self.send_btn.config(state=tk.DISABLED, text="DM ALL IN PROGRESS...")
        
        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self.log("🚀 DÉMARRAGE DE LA CAMPAGNE DM ALL")
        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self.log(f"⚡ Serveurs à traiter: {len(self.bot.guilds)}")
        self.log(f"⏱️  Délai entre les envois: 1.5 secondes")
        self.log(f"📝 Message: {message[:50]}{'...' if len(message) > 50 else ''}")
        self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Envoie les DM à tous les membres de tous les serveurs
        async def send_mass_dm():
            success_count = 0
            fail_count = 0
            processed_users = set()  # Évite d'envoyer plusieurs fois au même utilisateur
            
            for guild in self.bot.guilds:
                self.log("")
                self.log(f"🔷 SERVEUR: {guild.name}")
                self.log(f"👥 Membres dans ce serveur: {guild.member_count}")
                self.log("─────────────────────────────────────")
                
                member_count = 0
                for member in guild.members:
                    # Ignore les bots
                    if member.bot:
                        continue
                    
                    # Ignore si déjà envoyé à cet utilisateur
                    if member.id in processed_users:
                        continue
                    
                    processed_users.add(member.id)
                    member_count += 1
                    
                    # Affiche qu'on essaie d'envoyer
                    self.log(f"📤 Envoi vers: {member.name}#{member.discriminator}")
                    
                    try:
                        await member.send(message)
                        success_count += 1
                        self.log(f"   ✅ SUCCÈS - Message envoyé!")
                        
                        # Met à jour les stats EN TEMPS RÉEL
                        self.sent_count = success_count
                        self.total_count = success_count + fail_count
                        self.root.after(0, self.update_stats)
                        
                        # Délai pour éviter les rate limits Discord (5 DM / 5 secondes)
                        await asyncio.sleep(1.5)
                        
                    except discord.Forbidden:
                        fail_count += 1
                        self.log(f"   ❌ ÉCHEC - DM désactivés ou bot bloqué")
                    except discord.HTTPException as e:
                        if e.status == 429:  # Rate limit
                            self.log(f"⏸️  RATE LIMIT ATTEINT! Pause de 60 secondes...")
                            await asyncio.sleep(60)
                            self.log(f"▶️  Reprise... Nouvelle tentative pour {member.name}")
                            # Nouvelle tentative
                            try:
                                await member.send(message)
                                success_count += 1
                                self.log(f"   ✅ SUCCÈS (après retry)")
                            except:
                                fail_count += 1
                                self.log(f"   ❌ ÉCHEC (après retry)")
                        else:
                            fail_count += 1
                            self.log(f"   ❌ ERREUR HTTP: {str(e)}")
                    except Exception as e:
                        fail_count += 1
                        self.log(f"   ❌ ERREUR: {str(e)}")
                    
                    # Met à jour le compteur d'échecs
                    self.failed_count = fail_count
                    self.total_count = success_count + fail_count
                    self.root.after(0, self.update_stats)
                
                self.log(f"✔️  Serveur terminé: {member_count} membres traités")
            
            return success_count, fail_count
        
        def process_mass_dm():
            try:
                future = asyncio.run_coroutine_threadsafe(send_mass_dm(), self.loop)
                success, failed = future.result(timeout=None)
                
                self.sent_count = success
                self.failed_count = failed
                self.total_count = success + failed
                
                self.log("")
                self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                self.log("🎉 CAMPAGNE DM ALL TERMINÉE!")
                self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                self.log(f"✅ Messages envoyés avec succès: {success}")
                self.log(f"❌ Messages échoués: {failed}")
                self.log(f"📊 Total d'utilisateurs traités: {success + failed}")
                
                if (success + failed) > 0:
                    success_rate = (success / (success + failed) * 100)
                    self.log(f"📈 Taux de réussite: {success_rate:.1f}%")
                
                self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                self.update_stats()
                
            except Exception as e:
                self.log(f"❌ ERREUR lors du DM ALL: {str(e)}")
            
            finally:
                self.is_sending = False
                self.send_btn.config(state=tk.NORMAL, text="DM ALL MEMBERS")
        
        threading.Thread(target=process_mass_dm, daemon=True).start()

def main():
    root = tk.Tk()
    app = NexusTool(root)
    
    # Gère la fermeture de la fenêtre
    def on_closing():
        if app.bot:
            try:
                asyncio.run_coroutine_threadsafe(app.bot.close(), app.loop)
            except:
                pass
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
