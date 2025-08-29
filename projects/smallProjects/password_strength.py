import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.configure("TLabel", padding=5, font=('Helvetica', 10))
        style.configure("TButton", padding=5, font=('Helvetica', 10))
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Password entry
        ttk.Label(main_frame, text="Enter your password:").pack(pady=(0, 5), anchor='w')
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="•", font=('Helvetica', 12))
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        self.password_entry.bind('<KeyRelease>', self.check_strength)
        
        # Show password checkbox
        self.show_var = tk.BooleanVar()
        self.show_check = ttk.Checkbutton(main_frame, text="Show password", variable=self.show_var, 
                                         command=self.toggle_password_visibility)
        self.show_check.pack(pady=(0, 20))
        
        # Strength indicator
        self.strength_frame = ttk.LabelFrame(main_frame, text="Password Strength", padding=10)
        self.strength_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.strength_meter = ttk.Progressbar(self.strength_frame, length=350, mode='determinate',
                                           style="TProgressbar")
        self.strength_meter.pack(fill=tk.X, pady=5)
        
        self.strength_label = ttk.Label(self.strength_frame, text="", font=('Helvetica', 10, 'bold'))
        self.strength_label.pack()
        
        # Feedback frame
        self.feedback_frame = ttk.LabelFrame(main_frame, text="Requirements", padding=10)
        self.feedback_frame.pack(fill=tk.BOTH, expand=True)
        
        # Feedback labels
        self.length_label = ttk.Label(self.feedback_frame, text="✓ At least 8 characters", foreground="gray")
        self.upper_label = ttk.Label(self.feedback_frame, text="✓ Contains uppercase letter", foreground="gray")
        self.lower_label = ttk.Label(self.feedback_frame, text="✓ Contains lowercase letter", foreground="gray")
        self.digit_label = ttk.Label(self.feedback_frame, text="✓ Contains number", foreground="gray")
        self.special_label = ttk.Label(self.feedback_frame, text="✓ Contains special character", foreground="gray")
        
        self.length_label.pack(anchor='w', pady=2)
        self.upper_label.pack(anchor='w', pady=2)
        self.lower_label.pack(anchor='w', pady=2)
        self.digit_label.pack(anchor='w', pady=2)
        self.special_label.pack(anchor='w', pady=2)
        
        # Set initial state
        self.update_feedback("", 0)
    
    def toggle_password_visibility(self):
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def check_strength(self, event=None):
        password = self.password_var.get()
        strength = 0
        feedback = {
            'length': False,
            'upper': False,
            'lower': False,
            'digit': False,
            'special': False
        }
        
        # Check each requirement
        if len(password) >= 8:
            strength += 1
            feedback['length'] = True
        if re.search(r'[A-Z]', password):
            strength += 1
            feedback['upper'] = True
        if re.search(r'[a-z]', password):
            strength += 1
            feedback['lower'] = True
        if re.search(r'[0-9]', password):
            strength += 1
            feedback['digit'] = True
        if re.search(r'[^A-Za-z0-9]', password):
            strength += 1
            feedback['special'] = True
        
        # Update UI
        self.update_feedback(feedback, strength)
    
    def update_feedback(self, feedback, strength):
        if strength == 0:
            # Reset all to gray
            for label in [self.length_label, self.upper_label, self.lower_label, 
                         self.digit_label, self.special_label]:
                label.config(foreground="gray")
            self.strength_meter['value'] = 0
            self.strength_label.config(text="", foreground="black")
            return
            
        # Update requirement labels
        self.length_label.config(foreground="green" if feedback['length'] else "red")
        self.upper_label.config(foreground="green" if feedback['upper'] else "red")
        self.lower_label.config(foreground="green" if feedback['lower'] else "red")
        self.digit_label.config(foreground="green" if feedback['digit'] else "red")
        self.special_label.config(foreground="green" if feedback['special'] else "red")
        
        # Update strength meter
        strength_percent = (strength / 5) * 100
        self.strength_meter['value'] = strength_percent
        
        # Update strength label
        if strength <= 1:
            strength_text = "Very Weak"
            color = "red"
        elif strength == 2:
            strength_text = "Weak"
            color = "orange"
        elif strength == 3:
            strength_text = "Moderate"
            color = "#FFD700"  # Gold
        elif strength == 4:
            strength_text = "Strong"
            color = "#90EE90"  # Light Green
        else:
            strength_text = "Very Strong"
            color = "green"
            
        self.strength_label.config(text=strength_text, foreground=color)
        self.strength_meter['style'] = f"{color}.Horizontal.TProgressbar"

def main():
    try:
        # Try to create the root window first
        root = tk.Tk()
        print("Tkinter window created successfully")
        
        # Set a default window size and position
        window_width = 450
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        root.title("Password Strength Checker")
        
        # Create the application
        print("Creating PasswordStrengthChecker instance...")
        app = PasswordStrengthChecker(root)
        print("PasswordStrengthChecker instance created")
        
        # Set custom styles
        print("Configuring styles...")
        style = ttk.Style()
        
        # Configure the default style first
        style.theme_use('clam')  # Try a different theme
        
        # Configure the progressbar style
        style.layout('TProgressbar',
                    [('Horizontal.Progressbar.trough',
                      {'children': [('Horizontal.Progressbar.pbar',
                                   {'side': 'left', 'sticky': 'ns'})],
                       'sticky': 'nsew'}),
                     ('Horizontal.Progressbar.label', {'sticky': ''})])
        
        # Define progress bar colors
        for color in ['red', 'orange', '#FFD700', '#90EE90', 'green']:
            style.configure(f"{color}.Horizontal.TProgressbar",
                          troughcolor='#f0f0f0',
                          background=color,
                          bordercolor='#f0f0f0',
                          lightcolor=color,
                          darkcolor=color)
        
        print("Starting mainloop...")
        root.mainloop()
        
    except Exception as e:
        import traceback
        print("An error occurred:")
        print(traceback.format_exc())
        input("Press Enter to exit...")  # Keep the window open to see the error

if __name__ == "__main__":
    print("Starting password strength checker...")
    main()
