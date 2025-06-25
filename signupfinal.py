import tkinter as tk
from tkinter import messagebox
import ast
import os

window = tk.Tk()
window.title('SignUp')
window.geometry('925x500+300+200')
window.configure(bg="#fff")
window.resizable(False, False)
window.iconbitmap("download.ico")

def signup():
    username = user.get()
    password = code.get()
    confirm_password = confirm_code.get()

    if password == confirm_password:
        try:
            with open('datasheet.txt', 'r+') as file:
                d = file.read()
                try:
                    r = ast.literal_eval(d)  # Convert the content of the file into a dictionary
                except:
                    r = {}

                # Check if the username already exists
                if username in r:
                    messagebox.showerror('Invalid', 'Username already exists. Please choose another username.')
                    return

                # Check if the password already exists
                if password in r.values():
                    messagebox.showerror('Invalid', 'This password is already in use. Please choose a different password.')
                    return

                # If username and password are unique, proceed to save
                r.update({username: password})
                file.seek(0)
                file.truncate()
                file.write(str(r))

            messagebox.showinfo('SignUp', 'Successfully signed up')
            window.destroy()
            os.system('python signinfinal.py')  # Redirect to the login window
            
        except FileNotFoundError:
            # If the file doesn't exist, create it and add the new user
            with open('datasheet.txt', 'w') as file:
                file.write(str({username: password}))
            messagebox.showinfo('SignUp', 'Successfully signed up')
    else:
        messagebox.showerror('Invalid', "Passwords don't match")

def signin():
    window.destroy()  # Close the current SignUp window and open the SignIn window
    os.system('python signinfinal.py')  # Run signinfinal.py when SignIn button is clicked



img = tk.PhotoImage(file='image7.png')
tk.Label(window, image=img, border=0, bg='white').place(x=50, y=90)

frame = tk.Frame(window, width=350, height=390, bg="#fff")
frame.place(x=480, y=50)

heading = tk.Label(frame, text='Sign Up', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e, widget, placeholder):
    if widget.get() == placeholder:
        widget.delete(0, 'end')

def on_leave(e, widget, placeholder):
    if widget.get() == '':
        widget.insert(0, placeholder)

# Username Entry
user = tk.Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'username')
user.bind('<FocusIn>', lambda e: on_enter(e, user, 'username'))
user.bind('<FocusOut>', lambda e: on_leave(e, user, 'username'))
tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Password Entry
code = tk.Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11), show='*')
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', lambda e: on_enter(e, code, 'Password'))
code.bind('<FocusOut>', lambda e: on_leave(e, code, 'Password'))
tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# Confirm Password Entry
confirm_code = tk.Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11), show='*')
confirm_code.place(x=30, y=220)
confirm_code.insert(0, 'Confirm Password')
confirm_code.bind('<FocusIn>', lambda e: on_enter(e, confirm_code, 'Confirm Password'))
confirm_code.bind('<FocusOut>', lambda e: on_leave(e, confirm_code, 'Confirm Password'))
tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

# Signup Button
tk.Button(frame, width=39, pady=7, text='Sign Up', bg='#57a1f8', fg='white', border=0, command=signup).place(x=35, y=280,)

# Sign-in Option
label = tk.Label(frame, text="I have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=90, y=340)
signin = tk.Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8',command=signin)
signin.place(x=200, y=340)


window.mainloop()
