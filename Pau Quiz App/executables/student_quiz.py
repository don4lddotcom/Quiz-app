import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import json, os
from datetime import datetime

class QuizThingy:
    def __init__(self, root):
        self.root = root
        root.title("PAU Quiz - Student Mode")
        root.geometry("850x650")
        root.configure(bg="#f0f4ff")

        self.style = ttk.Style(root)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12), padding=8,
                           background='#1e3a8a', foreground='white')
        self.style.map('TButton', background=[('active', '#3b82f6')])
        self.style.configure('TLabel', background='#f0f4ff', font=('Helvetica', '14'))
        self.style.configure('Header.TLabel', font=('Helvetica', 20, 'bold'),
                           foreground='#1e40af')
        self.style.configure('TRadiobutton', background='#f0f4ff', font=('Helvetica', 12))

        self.questions = []
        self.user_answers = []
        self.current_q = 0
        self.score = 0
        self.time_left = 0
        self.timer = None

        self._setup_ui()

    def _setup_ui(self):
        top_bar = tk.Frame(self.root, bg="#f0f4ff")
        top_bar.pack(fill='x', padx=20, pady=10)
        ttk.Label(top_bar, text="Welcome To Pau Quiz App",
                 style='Header.TLabel').pack(side='left', expand=True)
        self.quiz_action_btn = ttk.Button(top_bar, text="Load Quiz",
                                        command=self._handle_quiz_action)
        self.quiz_action_btn.pack(side='right')

        info_panel = tk.Frame(self.root, bg="#f0f4ff")
        info_panel.pack(fill='x', padx=20)
        self.time_label = ttk.Label(info_panel, text="Time Left: --:--",
                                  foreground='#dc2626')
        self.time_label.pack(side='left')
        self.progress_bar = ttk.Progressbar(info_panel, length=200, mode='determinate')
        self.progress_bar.pack(side='right', padx=10)

        self.question_box = tk.Frame(self.root, bg='#fff', bd=2, relief='groove')
        self.question_box.pack(expand=True, fill='both', padx=20, pady=20)

        nav_buttons = tk.Frame(self.root, bg="#f0f4ff")
        nav_buttons.pack(fill='x', pady=10)

        self.prev_btn = ttk.Button(nav_buttons, text="Previous", command=self._prev_question)
        self.next_btn = ttk.Button(nav_buttons, text="Next", command=self._next_question)
        self.submit_btn = ttk.Button(nav_buttons, text="Submit", command=self._finish_quiz)

        self.prev_btn.pack(side='left', padx=5)
        self.next_btn.pack(side='left', padx=5)
        self.submit_btn.pack(side='right', padx=5)

        self._update_nav_buttons()
        self._show_welcome_screen()

    def _show_welcome_screen(self):
        self._clear_question_box()
        ttk.Label(self.question_box,
                 text="Ready to test your knowledge?\nLoad a quiz to begin!",
                 style='Header.TLabel').pack(pady=100)

    def _handle_quiz_action(self):
        if self.quiz_action_btn['text'] == "Load Quiz":
            self._load_quiz()
        else:
            if messagebox.askyesno("Hold up!", "Really end the quiz early?"):
                self._end_quiz_early()

    def _load_quiz(self):
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file:
            return
        try:
            with open(file) as f:
                quiz_raw = json.load(f)
        except Exception as e:
            messagebox.showerror("Oops", f"Couldn't load that:\n{e}")
            return

        if not quiz_raw or not all('q' in q and 'opts' in q and 'ans' in q for q in quiz_raw):
            messagebox.showwarning("Hmm", "This doesn't look like a valid quiz file")
            return

        self.questions = [{
            'question': q['q'],
            'options': q['opts'],
            'answer': q['ans']
        } for q in quiz_raw]

        self.user_answers = [None] * len(self.questions)

        total_minutes = simpledialog.askinteger(
            "Set Timer",
            "How many minutes for the entire quiz?",
            initialvalue=3,
            minvalue=1,
            maxvalue=120
        )
        if total_minutes is None:
            return

        self.time_left = total_minutes * 60
        self.progress_bar['maximum'] = len(self.questions)
        self.quiz_action_btn.config(text="End Quiz")
        self._start_quiz()

    def _start_quiz(self):
        self.current_q = 0
        self._update_nav_buttons()
        self._run_timer()
        self._show_question()

    def _run_timer(self):
        mins, secs = divmod(self.time_left, 60)
        self.time_label.config(text=f"Time Left: {mins:02d}:{secs:02d}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer = self.root.after(1000, self._run_timer)
        else:
            messagebox.showinfo("Time's up!", "Auto-submitting your answers...")
            self._finish_quiz()

    def _show_question(self):
        self._clear_question_box()
        q = self.questions[self.current_q]
        q_text = f"Question {self.current_q + 1}/{len(self.questions)}: {q['question']}"
        ttk.Label(self.question_box, text=q_text, wraplength=750).pack(pady=15)

        self.selected = tk.StringVar(value=self.user_answers[self.current_q])
        letters = ['A', 'B', 'C', 'D']
        for i, option in enumerate(q['options']):
            label = f"{letters[i]}. {option}"
            ttk.Radiobutton(self.question_box, text=label, variable=self.selected, 
                          value=option, style='TRadiobutton').pack(anchor='w', padx=30, pady=5)

        self.progress_bar['value'] = self.current_q + 1
        self._update_nav_buttons()

    def _clear_question_box(self):
        for widget in self.question_box.winfo_children():
            widget.destroy()

    def _update_nav_buttons(self):
        self.prev_btn['state'] = 'normal' if self.current_q > 0 else 'disabled'
        self.next_btn['state'] = 'normal' if self.current_q < len(self.questions) - 1 else 'disabled'
        self.submit_btn['state'] = 'normal' if self.current_q == len(self.questions) - 1 else 'disabled'

    def _next_question(self):
        self.user_answers[self.current_q] = self.selected.get()
        self.current_q += 1
        self._show_question()

    def _prev_question(self):
        self.user_answers[self.current_q] = self.selected.get()
        self.current_q -= 1
        self._show_question()

    def _end_quiz_early(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        self._finish_quiz()

    def _finish_quiz(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        self.user_answers[self.current_q] = self.selected.get()

        # Calculate score
        self.correct = sum(1 for i, q in enumerate(self.questions) 
                      if self.user_answers[i] == q['answer'])
        self.total = len(self.questions)
        self.percent = self.correct / self.total * 100

        # Get wrong questions
        self.wrong_questions = []
        for i, q in enumerate(self.questions):
            if self.user_answers[i] != q['answer']:
                self.wrong_questions.append(
                    f"Q{i+1}: {q['question']}\n"
                    f"Your Answer: {self.user_answers[i]}\n"
                    f"Correct Answer: {q['answer']}\n\n"
                )

        # Show results immediately
        result_msg = (
            f"Questions: {self.total}\n"
            f"Correct: {self.correct}\n"
            f"Wrong: {self.total - self.correct}\n"
            f"Score: {self.percent:.1f}%\n\n"
        )
        
        # Add option to review if there are wrong answers
        if self.wrong_questions:
            result_msg += "Click 'Review' to see your mistakes"
            answer = messagebox.showinfo("Quiz Results", result_msg)
            self._show_review_options()
        else:
            messagebox.showinfo("Perfect Score!", "You got all questions correct! 🎉")
            self._return_to_welcome()

    def _show_review_options(self):
        self._clear_question_box()
        
        # Add review button
        ttk.Button(self.question_box,
                  text="🔍 Review Wrong Answers",
                  command=self._review_wrong_answers).pack(pady=20)
        
        # Add home button
        ttk.Button(self.question_box,
                  text="🏠 Return to Home",
                  command=self._return_to_welcome).pack(pady=10)
        
        # Auto-return after 10 seconds if no action
        self.root.after(10000, self._return_to_welcome)

    def _review_wrong_answers(self):
        self._clear_question_box()
        review_text = "Questions you missed:\n\n" + "\n".join(self.wrong_questions)
        
        text_widget = tk.Text(self.question_box, wrap='word', height=20, width=100)
        text_widget.pack(pady=20)
        text_widget.insert('1.0', review_text)
        text_widget.config(state='disabled')
        
        ttk.Button(self.question_box,
                  text="🏠 Return to Home",
                  command=self._return_to_welcome).pack(pady=10)

    def _save_results(self):
        file = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON', '.json')],
            initialfile='quiz_results.json'
        )
        if not file:
            return
        results = {
            'total': self.total,
            'correct': self.correct,
            'wrong': self.total - self.correct,
            'percentage': self.percent,
            'timestamp': str(datetime.now()),
            'wrong_questions': [
                {
                    'question': q['question'],
                    'your_answer': self.user_answers[i],
                    'correct_answer': q['answer']
                }
                for i, q in enumerate(self.questions)
                if self.user_answers[i] != q['answer']
            ]
        }
        
        try:
            with open(file, 'w') as f:
                json.dump(results, f, indent=4)
            messagebox.showinfo("Saved!", f"Results saved to {os.path.basename(file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't save results: {e}")

    def _return_to_welcome(self):
        self.questions = []
        self.user_answers = []
        self.current_q = 0
        self.time_left = 0
        self.time_label.config(text="Time Left: --:--")
        self.progress_bar['value'] = 0
        self.quiz_action_btn.config(text="Load Quiz")
        self._show_welcome_screen()

def launch_student_quiz():
    root = tk.Tk()
    QuizThingy(root)
    root.mainloop()

if __name__ == '__main__':
    launch_student_quiz()