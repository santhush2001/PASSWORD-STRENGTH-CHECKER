import re
import tkinter as tk
from tkinter import ttk, messagebox

class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Password Strength Checker", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Password entry
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(password_frame, text="Enter Password:").pack(side=tk.LEFT)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_frame, 
            textvariable=self.password_var, 
            show="*", 
            width=30
        )
        self.password_entry.pack(side=tk.LEFT, padx=10)
        self.password_entry.bind("<KeyRelease>", self.check_strength)
        
        # Show password checkbox
        self.show_password_var = tk.IntVar()
        show_password_cb = ttk.Checkbutton(
            main_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility
        )
        show_password_cb.pack(pady=5)
        
        # Strength meter
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(strength_frame, text="Strength:").pack(side=tk.LEFT)
        
        self.strength_meter = ttk.Progressbar(
            strength_frame,
            orient=tk.HORIZONTAL,
            length=200,
            mode='determinate'
        )
        self.strength_meter.pack(side=tk.LEFT, padx=10)
        
        self.strength_label = ttk.Label(strength_frame, text="")
        self.strength_label.pack(side=tk.LEFT)
        
        # Feedback treeview
        feedback_frame = ttk.Frame(main_frame)
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(feedback_frame, text="Password Analysis:").pack(anchor=tk.W)
        
        self.feedback_tree = ttk.Treeview(
            feedback_frame,
            columns=('feedback',),
            show='headings',
            height=6
        )
        self.feedback_tree.heading('feedback', text='Criteria')
        self.feedback_tree.column('feedback', width=400)
        
        scrollbar = ttk.Scrollbar(
            feedback_frame,
            orient=tk.VERTICAL,
            command=self.feedback_tree.yview
        )
        self.feedback_tree.configure(yscrollcommand=scrollbar.set)
        
        self.feedback_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Check button
        check_button = ttk.Button(
            main_frame,
            text="Check Password",
            command=self.check_strength
        )
        check_button.pack(pady=10)
        
        # Copy to clipboard button
        copy_button = ttk.Button(
            main_frame,
            text="Copy Password to Clipboard",
            command=self.copy_to_clipboard
        )
        copy_button.pack(pady=5)
    
    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")
    
    def check_strength(self, event=None):
        password = self.password_var.get()
        
        # Clear previous feedback
        for item in self.feedback_tree.get_children():
            self.feedback_tree.delete(item)
        
        if not password:
            self.strength_meter['value'] = 0
            self.strength_label.config(text="")
            return
        
        score = 0
        max_score = 8
        feedback = []
        
        # Check length
        if len(password) >= 12:
            score += 3
            feedback.append(("✓ Good length (12+ characters)", "good"))
        elif len(password) >= 8:
            score += 2
            feedback.append(("✓ Minimum length (8+ characters)", "good"))
        else:
            feedback.append(("✗ Too short (minimum 8 characters required)", "bad"))
        
        # Check for uppercase letters
        if re.search(r'[A-Z]', password):
            score += 1
            feedback.append(("✓ Contains uppercase letters", "good"))
        else:
            feedback.append(("✗ No uppercase letters", "bad"))
        
        # Check for lowercase letters
        if re.search(r'[a-z]', password):
            score += 1
            feedback.append(("✓ Contains lowercase letters", "good"))
        else:
            feedback.append(("✗ No lowercase letters", "bad"))
        
        # Check for numbers
        if re.search(r'[0-9]', password):
            score += 1
            feedback.append(("✓ Contains numbers", "good"))
        else:
            feedback.append(("✗ No numbers", "bad"))
        
        # Check for special characters
        if re.search(r'[^A-Za-z0-9]', password):
            score += 2
            feedback.append(("✓ Contains special characters", "good"))
        else:
            feedback.append(("✗ No special characters", "bad"))
        
        # Check for common weak patterns
        weak_patterns = [
            '123', 'abc', 'qwerty', 'password', 'admin', 'welcome', 
            '111', '000', 'iloveyou', 'letmein'
        ]
        
        if any(pattern in password.lower() for pattern in weak_patterns):
            score -= 2
            feedback.append(("✗ Contains common weak patterns", "bad"))
        
        # Ensure score is within bounds
        score = max(0, min(score, max_score))
        
        # Update strength meter and label
        percentage = (score / max_score) * 100
        self.strength_meter['value'] = percentage
        
        # Determine strength level
        if percentage >= 87.5:  # 7/8 or more
            strength = "Strong"
            color = "green"
        elif percentage >= 62.5:  # 5/8 or more
            strength = "Moderate"
            color = "orange"
        elif percentage >= 37.5:  # 3/8 or more
            strength = "Weak"
            color = "#FFCC00"  # yellow-orange
        else:
            strength = "Very Weak"
            color = "red"
        
        self.strength_label.config(text=strength, foreground=color)
        
        # Add feedback to treeview
        for item, quality in feedback:
            if quality == "good":
                tag = "good"
            else:
                tag = "bad"
            self.feedback_tree.insert("", tk.END, values=(item,), tags=(tag,))
        
        # Configure tags for coloring
        self.feedback_tree.tag_configure("good", foreground="green")
        self.feedback_tree.tag_configure("bad", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    
    # Set theme (requires ttkthemes package - optional)
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="equilux")
        app = PasswordStrengthChecker(root)
    except ImportError:
        pass
    
    root.mainloop()