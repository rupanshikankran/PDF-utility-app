from tkinter import *
from tkinter import messagebox
import ast
import os

# Create the main window
root = Tk()
root.title('Signin')
root.geometry('900x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)
root.iconbitmap("download.ico")

# Function to handle the sign-in process
def signin():
    username = user.get()
    password = code.get()

    try:
        with open('datasheet.txt', 'r') as file:
            data = file.read()
            credentials = ast.literal_eval(data)  # Parse the string as a dictionary
    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found!")
        return
    except ValueError:
        messagebox.showerror("Error", "Data file is corrupted!")
        return

    # Check if the username and password match
    if username in credentials and credentials[username] == password:
        


    #                       <<<< Now run the PDF_utility_App.py file after Signin>>>
       os.system('python PDF_utility_App1.py')  

    else:
        messagebox.showerror("Invalid", "Invalid username or password")




#                                <<<Function to handle the sign-up process>>>      
def signup():
    root.destroy()  # Close the current window
    os.system('python signupfinal.py')  # Execute the sign-up page

    #                             ------------------------------------------

    

    
# Load and place the image
img = PhotoImage(file='image.png')  # Ensure image.png exists
Label(root, image=img, bg='white').place(x=0, y=0, relheight=1, width=450)

# Create the login frame on the right side
frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=500, y=100)

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# Username Entry
def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'username')

user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Password Entry
def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'password')

code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11), show="*")
code.place(x=30, y=150)
code.insert(0, 'password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# Sign-in Button
Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)

# Sign-up Prompt
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

# Sign-up Button
sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=signup)
sign_up.place(x=215, y=270)

root.mainloop()
