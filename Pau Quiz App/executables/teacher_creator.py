import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json, os, sys

class QuizMaker:  
    def __init__(self, win):  # sometimes I call it root, sometimes win
        self.win = win
        win.title("PAU Quiz Master 9000")  # keep same title
        win.geometry("900x700")
        win.configure(bg="#f8f9fa")
        # stash for questions
        self.q_list = []  # holds dicts of q/options/answer
        # set up look
        self._setup_styles()
        self._build_ui()
        # try centering; might fail quietly
        try:
            win.eval('tk::PlaceWindow . center')
        except Exception:
            pass

    def _setup_styles(self):
        """styles-ish"""
        style = ttk.Style(self.win)
        try:
            style.theme_use('clam')
        except Exception:
            pass  # ignore if not available
        # Buttons
        style.configure('TButton',
                        font=('Segoe UI', 11, 'bold'),
                        padding=8,
                        background='#4a6fa5',
                        foreground='white',
                        relief='raised')
        style.map('TButton',
                  background=[('active', '#3a5f8a')],
                  relief=[('active', 'sunken')])
        # Labels
        style.configure('TLabel',
                        font=('Segoe UI', 11),
                        background='#f8f9fa',
                        foreground='#333333')
        style.configure('Header.TLabel',
                        font=('Segoe UI', 24, 'bold'),
                        foreground='#2c5282',
                        background='#f8f9fa')
        # Entries
        style.configure('TEntry',
                        font=('Segoe UI', 11),
                        padding=4)
        # Frame defaults
        self.win.option_add('*LabelFrame*background', '#f8f9fa')
        self.win.option_add('*Frame*background', '#f8f9fa')

    def _build_ui(self):
        # header
        hdr = tk.Frame(self.win, bg="#f8f9fa")
        hdr.pack(fill='x', padx=20, pady=(20, 10))
        ttk.Label(hdr, text="✏️ Pau Quiz Creator", style='Header.TLabel').pack(side='left')
        ttk.Button(hdr, text="🚪 Exit", command=self.win.destroy).pack(side='right')

        # main area
        main = tk.Frame(self.win, bg="#f8f9fa")
        main.pack(fill='both', expand=True, padx=20, pady=10)

        # question box
        qf = tk.LabelFrame(main,
                           text=" Question Text 📝 ",
                           font=('Segoe UI', 11, 'bold'),
                           padx=10, pady=10)
        qf.configure(bg='#f8f9fa', fg='#2c5282')
        qf.pack(fill='x', pady=(0, 15))
        self.txt_q = tk.Text(qf, height=4, width=80,
                             font=('Segoe UI', 11), padx=10, pady=10, wrap=tk.WORD)
        self.txt_q.pack()

        # options area
        of = tk.LabelFrame(main,
                           text=" Multiple Choice Options 🔠 ",
                           font=('Segoe UI', 11, 'bold'),
                           padx=10, pady=10)
        of.configure(bg='#f8f9fa', fg='#2c5282')
        of.pack(fill='x', pady=(0, 15))
        self.opt_entries = []
        for idx in range(4):
            row = tk.Frame(of, bg="#f8f9fa")
            row.pack(fill='x', pady=5)
            lbl = ttk.Label(row, text=f"Option {idx+1}:", width=10)
            lbl.pack(side='left')
            ent = ttk.Entry(row, width=60, font=('Segoe UI', 11))
            ent.pack(side='left', fill='x', expand=True)
            self.opt_entries.append(ent)

        # correct answer
        af = tk.LabelFrame(main,
                           text=" Correct Answer ✅ ",
                           font=('Segoe UI', 11, 'bold'),
                           padx=10, pady=10)
        af.configure(bg='#f8f9fa', fg='#2c5282')
        af.pack(fill='x', pady=(0, 20))
        self.ent_ans = ttk.Entry(af, width=80, font=('Segoe UI', 11))
        self.ent_ans.pack(pady=5)

        # buttons
        bf = tk.Frame(main, bg="#f8f9fa")
        bf.pack(fill='x', pady=(10, 0))
        self.btn_add = ttk.Button(bf, text="➕ Add Question", command=self._add_q)
        self.btn_add.pack(side='left', padx=5, fill='x', expand=True)
        self.btn_save = ttk.Button(bf, text="💾 Save Quiz", command=self._save_qs)
        self.btn_save.pack(side='left', padx=5, fill='x', expand=True)
        self.btn_clear = ttk.Button(bf, text="🧹 Clear Fields", command=self._clear_inputs)
        self.btn_clear.pack(side='left', padx=5, fill='x', expand=True)

        # status label (sometimes helpful)
        self.status_lbl = tk.Label(self.win, text="", bg="#f8f9fa", anchor='w')
        self.status_lbl.pack(fill='x', padx=20, pady=(5, 0))

    def _add_q(self):
        q_text = self.txt_q.get("1.0", tk.END).strip()
        opts = [e.get().strip() for e in self.opt_entries]
        ans = self.ent_ans.get().strip()

        if not q_text:
            messagebox.showwarning("Oops", "Question text can't be empty, silly!")
            return
        if not all(opts):
            messagebox.showwarning("Hey now", "All options must be filled!")
            return
        if not ans:
            messagebox.showwarning("Come on", "You forgot the correct answer!")
            return
        if ans not in opts:
            # try case-insensitive match
            for o in opts:
                if o.lower() == ans.lower():
                    ans = o
                    break
            else:
                messagebox.showerror("Logic error",
                                     "The correct answer must match one of the options!\n"
                                     "This isn't quantum physics...")
                return
        # store but use short keys
        self.q_list.append({"q": q_text, "opts": opts.copy(), "ans": ans})
        # update status
        self.status_lbl.config(text=f"Total questions: {len(self.q_list)}")
        print(f"[DEBUG] Added Q #{len(self.q_list)}")  # debug-ish
        self._clear_inputs()

    def _clear_inputs(self):
        try:
            self.txt_q.delete("1.0", tk.END)
            for e in self.opt_entries:
                e.delete(0, tk.END)
            self.ent_ans.delete(0, tk.END)
            self.txt_q.focus_set()
        except Exception as e:
            print("clear issue:", e)

    def _save_qs(self):
        if not self.q_list:
            messagebox.showwarning("Empty", "Your quiz is emptier than my motivation on Mondays!")
            return
        # determine base folder
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            try:
                base = os.path.dirname(__file__)
            except Exception:
                base = os.getcwd()
        save_dir = os.path.join(os.path.abspath(os.path.join(base, "..")), "saved_quizzes")
        os.makedirs(save_dir, exist_ok=True)
        # ask where to save
        # keep same default filename
        filepath = filedialog.asksaveasfilename(
            initialdir=save_dir,
            defaultextension='.json',
            filetypes=[('JSON Quiz Files', '*.json')],
            initialfile='quiz_sample.json'
        )
        if not filepath:
            print("User canceled save")  # silent note
            return
        try:
            with open(filepath, 'w') as f:
                json.dump(self.q_list, f, indent=4)
            messagebox.showinfo("Saved!",
                                f"Quiz successfully saved to:\n{os.path.basename(filepath)}")
            # reset list
            self.q_list = []
            self.status_lbl.config(text="Quiz cleared after save")
        except Exception as ex:
            messagebox.showerror("Save failed",
                                 f"Something went wrong:\n{ex}\nMaybe try a different location?")
            print("Save error:", ex)


def launch_teacher():
    root = tk.Tk()
    QuizMaker(root)
    root.mainloop()

if __name__ == '__main__':
    launch_teacher()
