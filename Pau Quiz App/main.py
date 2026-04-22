import tkinter as tk  # UI stuff 
from tkinter import ttk  # fancy widgets
from tkinter import messagebox  # for yelling at users
from executables.student_quiz import launch_student_quiz  # student thingy
from executables.teacher_creator import launch_teacher  # teacher stuff 

class LoginWindow:
    def __init__(self, root):
        self.root = root  # the big window itself
        root.title("PAU Quiz App - Login")  # title thing
        root.geometry("500x400")  # made it bigger 
        root.configure(bg="#f0f8ff")  # lighter blue because why not
        
        # Make it look less Windows 95
        style = ttk.Style()
        style.theme_use('clam')  # least ugly default theme
        
        # Fancy fonts and colors
        style.configure('TLabel', 
                       font=('Segoe UI', 12), 
                       background='#f0f8ff',
                       foreground='#333333')  # dark gray text
        
        style.configure('TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=10,
                       background='#4a6fa5',  # nice blue
                       foreground='white',
                       borderwidth=1,
                       relief='raised')
        
        style.map('TButton',
                 background=[('active', '#3a5f8a')])  # darker when clicked
        
        style.configure('Header.TLabel',
                      font=('Segoe UI', 24, 'bold'),
                      foreground='#2c5282',  # deep blue
                      background='#f0f8ff')
        
        style.configure('TRadiobutton',
                      font=('Segoe UI', 11),
                      background='#f0f8ff',
                      padding=5)
        
        # Add some padding to everything because cramped UIs suck
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        # Main container frame for centering
        main_frame = tk.Frame(root, bg='#f0f8ff')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Big welcome header with some spacing
        ttk.Label(main_frame, 
                 text="👋 Welcome to PAU Quiz App", 
                 style='Header.TLabel').pack(pady=(0, 20))
        
        # Login prompt with emoji 
        ttk.Label(main_frame, 
                 text="Who are you today? 👀").pack(pady=5)
        
        # Radio buttons in a neat frame
        role_frame = tk.Frame(main_frame, bg='#f0f8ff')
        role_frame.pack(pady=10)
        
        self.role_var = tk.StringVar(value="Student")  # default to student
        
        # Student option
        student_rb = ttk.Radiobutton(role_frame, 
                                    text="😎 Student",
                                    variable=self.role_var, 
                                    value="Student")
        student_rb.grid(row=0, column=0, padx=15, sticky='w')
        
        # Teacher option with authority
        teacher_rb = ttk.Radiobutton(role_frame, 
                                    text="🧑‍🏫 Teacher", 
                                    variable=self.role_var, 
                                    value="Teacher")
        teacher_rb.grid(row=0, column=1, padx=15, sticky='w')
        
        # Big fat continue button that looks clickable
        continue_btn = ttk.Button(main_frame,
                                text="LET'S GOOO →",
                                command=self.proceed)
        continue_btn.pack(pady=25, ipadx=20, ipady=5)
        
        #exit button for quitters
        tk.Label(main_frame, 
                text="(or just close the window if you're boring)",
                bg='#f0f8ff',
                fg='#666666',
                font=('Segoe UI', 8)).pack()

    def proceed(self):
        """Figure out who they are and send them on their way"""
        choice = self.role_var.get()
        self.root.destroy()  # peace out login window
        
        # Send them to the right place
        if choice == "Student":
            launch_student_quiz()  # party time
        else:
            launch_teacher()  # serious business

if __name__ == "__main__":
    # Fire it up!
    main_win = tk.Tk()
    LoginWindow(main_win)
    
    # Center the window 
    main_win.eval('tk::PlaceWindow . center')
    
    main_win.mainloop()