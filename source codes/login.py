import pymysql
import random
import smtplib
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import re       # regular expression
import pandas
from database import SqlData
login_failed = False


class Login:

    def __init__(self):
        self.user_id = 0
        self.sql_data = SqlData()
        self.window = Tk()
        self.window.title("Chess Game - Login")
        self.window.geometry("925x500+300+200")
        self.window.configure(bg="#fff")
        self.window.resizable(0, 0)
        self.window.protocol("WM_DELETE_WINDOW", self.disable_event)

        self.img = ImageTk.PhotoImage(Image.open("C:/Users/dilip/PycharmProjects/chessGameAi/assets/images/background/login.png"))
        Label(self.window, image=self.img, bg='white').place(x=50, y=50)

        self.show_password = BooleanVar()
        self.show_password.set(True)

        self.frame = Frame(self.window, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        heading = Label(self.frame, text="Welcome, Login!", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        heading.place(x=35, y=5)

        self.username = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.username.place(x=30, y=80)
        self.username.insert(0, "Username")
        self.username.bind("<FocusIn>", self.on_enter)
        self.username.bind('<FocusOut>', self.on_leave)
        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=107)

        self.password = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.password.place(x=30, y=150)
        self.password.insert(0, "Password")
        self.password.bind("<FocusIn>", self.on_enter_pass)
        self.password.bind("<FocusOut>", self.on_leave_pass)
        Frame(self.frame, width=295, height=2, bg="black").place(x=25, y=177)

        self.show_password_button = Button(self.frame, text="🔒", command=self.toggle_password_visibility, bg="white")
        style = ttk.Style()
        style.configure("My.TButton", background='white', font=("Microsoft YaHei UI Light", 11))
        self.show_password_button.place(x=325 + self.password.winfo_width(), y=150)

        Button(self.frame, width=39, pady=7, text="Login", bg="#57a1f8", fg="white", border=0, command=self.login).place(x=35,
                                                                                                                         y=204)
        self.label = Label(self.frame, text="Don't have an account?", fg="black", bg="white",
                           font=("Microsoft YaHei UI Light", 9))
        self.label.place(x=75, y=270)

        self.register = Button(self.frame, width=6, text="Register", border=0, bg="white", cursor="hand2", fg="#57a1f8",
                               command=self.register_fun)
        self.register.place(x=215, y=270)

        self.reset = Button(self.frame, width=30, text="Forget Password?", border=0, bg="white", cursor="hand2", fg="#57a1f8",
                               command=self.reset_pass)
        self.reset.place(x=65, y=245)

        self.window.mainloop()

    def reset_pass(self):
        self.window.destroy()
        Reset()

    def disable_event(self):
        global login_failed
        login_failed = True
        self.window.destroy()

    def return_failed_login(self):
        if login_failed:
            return True
        else:
            return False

    def toggle_password_visibility(self):
        if self.show_password.get() is None:
            self.password.config(show="")
            self.show_password.set(True)
        elif self.show_password.get():
            self.password.config(show="*")
            self.show_password.set(False)
        else:
            self.password.config(show="")
            self.show_password.set(True)

    # ---------------------------------------------------------------------------------------------- #
    def on_enter(self, e):
        if self.username.get() == "Username":
            self.username.delete(0, "end")

    def on_leave(self, e):
        name = self.username.get()
        if name == "":
            self.username.insert(0, "Username")

    def on_enter_pass(self, e):
        if self.password.get() == "Password":
            self.password.config(show="*")
            self.show_password.set(False)
            self.password.delete(0, "end")

    def on_leave_pass(self, e):
        code = self.password.get()
        if code == "":
            self.password.config(show="")
            self.password.insert(0, "Password")

    def return_uid(self):
        return self.user_id

    def login(self):
        global login_failed
        login_failed = False

        usn = self.username.get()
        password = self.password.get()

        self.user_id = self.sql_data.user_login(usn=usn, password=password)

        if self.user_id is None:
            messagebox.showerror("Invalid Input", "Invalid Username or Passowrd")
        else:
            messagebox.showinfo("Success!", "Login Successful, Enjoy the game!")
            self.window.destroy()
            return None

    def register_fun(self):
        self.window.destroy()
        RegisterClass()


class SendOtp:   # Class to send OTP

    def __init__(self):
        self.sender_email = "princegamer48@gmail.com"
        self.sender_pass = "nwmppkfufbiynqpv"    # App password for the above email
        self.receiver_email = None
        self.sent_otp = None

    def send_mail(self, receiver):
        self.receiver_email = receiver
        self.sent_otp = random.randint(1002, 9999)
        try:
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as con:
                con.starttls()
                con.login(user=self.sender_email, password=self.sender_pass)
                con.sendmail(from_addr=self.sender_email, to_addrs=self.receiver_email,
                             msg=f"Subject: OTP\n\nYour Otp is {self.sent_otp}. "
                                 f"\nPlease do not share Your OTP with anyone.")
            return self.sent_otp

        except Exception as e:
            messagebox.showerror("Error", f"{e}")


class RegisterClass(SendOtp):

    def __init__(self):
        super().__init__()

        self.sql_data = SqlData()
        self.fullName = None
        self.email = None
        self.username = None
        self.password = None
        self.confirm_password = False
        self.otp = None
        self.received_otp = None
        self.otp_confirmed = False
        self.regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.duplicate_email = False

        self.window = Tk()
        self.window.title("Chess Game - Register")
        self.window.geometry("925x500+300+200")
        self.window.configure(bg="#fff")
        self.window.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.window.resizable(False, False)

        self.frame = Frame(self.window, width=550, height=500, bg="white")
        self.frame.place(x=180, y=60)

        self.heading = Label(self.frame, text="Register", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
        self.heading.place(x=0, y=5)

        self.register = Button(self.frame, width=7, text="Send OTP", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=self.sendotp)
        self.register.place(x=240, y=270)

        self.register = Button(self.frame, width=15, text="Confirm OTP", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=self.confirm_otp)
        self.register.place(x=300, y=270)

        self.register_button = Button(self.frame, width=39, pady=7, text="Register", bg="#57a1f8", fg="white", border=0, state="disabled", command=self.register_user)
        self.register_button.place(x=5, y=320)

        self.register = Button(self.frame, width=30, text="Have Account? Login!", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=self.go_back)
        self.register.place(x=120, y=360)

        self.mainloop()

    def disable_event(self):
        global login_failed
        login_failed = True
        self.window.destroy()

    def mainloop(self):
        if self.otp_confirmed:
            self.register_button["state"] = "normal"

        self.details_full_name()
        self.details_username()
        self.details_password()
        self.details_confirm_password()
        self.details_email()
        self.details_otp()
        self.window.mainloop()

    def register_user(self):   # Function to register user details in the database

        name = self.fullName.get()
        usn = self.username.get()
        password = self.password.get()
        email = self.email.get()

        if self.password.get() == self.confirm_password.get():
            try:
                self.sql_data.insert_for_register(name=name, username=usn, email=email, password=password)
                self.sql_data.close_connection()
                messagebox.showinfo("Success!", "Registeration Successfull \nPlease Login")
                self.window.destroy()
                Login()

            except pymysql.err.IntegrityError:
                messagebox.showerror("Error Occured", "Something Went Wrong!\nPlease Try again.")

    def sendotp(self):    # Function to send OTPs
        if self.duplicate_email:
            messagebox.showerror("Invalid Input", "This Email Already Exists")
            return None
        else:
            email = self.email.get()

            if self.fullName.get() == "Full name" or self.username.get() == "Username" or \
                    self.password.get() == "Password" or self.confirm_password.get() == "Confirm Password" or \
                    self.email.get() == "E-Mail":
                messagebox.showerror('Fields Empty', 'Fields Cannot be empty')

            elif not self.check(email):
                messagebox.showerror('Invalid Entry', 'Invalid Email, Please Enter a valid Email.\nEither @gmail.com or '
                                                      '@yahoo.com')
            else:
                self.received_otp = SendOtp.send_mail(self, receiver=self.email.get())



    def confirm_otp(self):   # Checking if the otp is correct. If yes then changing received otp to true

        try:
            if self.received_otp == int(self.otp.get()):
                self.otp_confirmed = True
                self.register_button["state"] = "normal"
            else:
                messagebox.showerror('Invalid OTP', "Invalid OTP, Please enter correct OTP or "
                                                    "check you email that you've entered")
        except ValueError:
            messagebox.showerror('Invalid OTP', "Invalid OTP, Please enter correct OTP or "
                                                "check you email that you've entered")

    def details_full_name(self):   # Displays the full name textbox
        self.fullName = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.fullName.place(x=10, y=80)
        self.fullName.insert(0, "Full name")
        self.fullName.bind("<FocusIn>", self.on_enter_name)
        self.fullName.bind('<FocusOut>', self.on_leave_name)
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=107)

    def details_username(self):  # Displays username textbox
        self.username = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.username.place(x=10, y=130)
        self.username.insert(0, "Username")
        self.username.bind("<FocusIn>", self.on_enter_user)
        self.username.bind('<FocusOut>', self.on_leave_user)
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=157)

    def details_password(self):
        self.password = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.password.place(x=10, y=180)
        self.password.insert(0, "Password")
        self.password.bind("<FocusIn>", self.on_enter_pass)
        self.password.bind('<FocusOut>', self.on_leave_pass)
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=207)

    def details_confirm_password(self):
        self.confirm_password = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.confirm_password.place(x=320, y=180)
        self.confirm_password.insert(0, "Confirm Password")
        self.confirm_password.bind("<FocusIn>", self.on_enter_con)
        self.confirm_password.bind('<FocusOut>', self.on_leave_con)
        Frame(self.frame, width=295, height=2, bg="black").place(x=320, y=207)

    def details_email(self):
        self.email = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.email.place(x=10, y=230)
        self.email.insert(0, "E-Mail")
        self.email.bind("<FocusIn>", self.on_enter_email)
        self.email.bind('<FocusOut>', self.on_leave_email)
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=260)

    def details_otp(self):
        self.otp = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.otp.place(x=320, y=230)
        self.otp.insert(0, "Enter OTP")
        self.otp.bind("<FocusIn>", self.on_enter_otp)
        self.otp.bind('<FocusOut>', self.on_leave_otp)
        Frame(self.frame, width=295, height=2, bg="black").place(x=320, y=260)

    def on_enter_name(self, e):
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=107)
        if self.fullName.get() == "Full name":
            self.fullName.delete(0, "end")

    def on_leave_name(self, e):
        name = self.fullName.get()

        if len(name) >= 3:
            Frame(self.frame, width=295, height=2, bg="green").place(x=0, y=107)
        else:
            if name == "":
                self.fullName.insert(0, "Full name")
            else:
                Frame(self.frame, width=295, height=2, bg="red").place(x=0, y=107)

    def on_enter_user(self, e):
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=157)
        if self.username.get() == "Username":
            self.username.delete(0, "end")

    def on_leave_user(self, e):
        name = self.username.get()
        if self.sql_data.check_for_duplicate(username=name):
            messagebox.showerror("Duplicate Data", f"Username '{name}' already exists.\nPlease choose another Username")
            Frame(self.frame, width=295, height=2, bg="red").place(x=0, y=157)
        else:
            if name == "":
                self.username.insert(0, "Username")
            elif len(name) >= 8:
                Frame(self.frame, width=295, height=2, bg="green").place(x=0, y=157)
            else:
                Frame(self.frame, width=295, height=2, bg="red").place(x=0, y=157)

    def on_enter_pass(self, e):
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=207)
        if self.password.get() == "Password":
            self.password.delete(0, "end")

    def on_leave_pass(self, e):
        password = self.password.get()
        if 8 <= len(password) <= 16:
            Frame(self.frame, width=295, height=2, bg="green").place(x=0, y=207)
        else:
            if password == "":
                self.password.insert(0, "Password")
            else:
                Frame(self.frame, width=295, height=2, bg="red").place(x=0, y=207)

    def on_enter_con(self, e):
        Frame(self.frame, width=295, height=2, bg="black").place(x=320, y=207)
        if self.confirm_password.get() == "Confirm Password":
            self.confirm_password.delete(0, "end")

    def on_leave_con(self, e):

        password = self.confirm_password.get()

        if password != self.password.get() or 8 >= len(password) >= 16:
            Frame(self.frame, width=295, height=2, bg="red").place(x=320, y=207)
        else:
            if password == "":
                self.confirm_password.insert(0, "Confirm Password")
                Frame(self.frame, width=295, height=2, bg="black").place(x=320, y=207)
            else:
                Frame(self.frame, width=295, height=2, bg="green").place(x=320, y=207)

    def on_enter_email(self, e):
        Frame(self.frame, width=295, height=2, bg="black").place(x=0, y=260)

        if self.email.get() == "E-Mail":
            self.email.delete(0, "end")

    def on_leave_email(self, e):
        email = self.email.get()
        if self.sql_data.check_for_duplicate(email=email):
            messagebox.showerror("Duplicate Data", f"Email '{email}' already exists.\nPlease choose another Email")
            Frame(self.frame, width=295, height=2, bg="red").place(x=0, y=260)
            self.duplicate_email = True
        else:
            self.duplicate_email = False
            if email == "":
                self.email.insert(0, "E-Mail")
            else:
                if (re.search(self.regex_email, email)):
                    Frame(self.frame, width=295, height=2, bg="green").place(x=0, y=260)
                else:
                    Frame(self.frame, width=295, height=2, bg="red").place(x=0, y=260)

    def on_enter_otp(self, e):
        if self.otp.get() == "Enter OTP":
            self.otp.delete(0, "end")

    def on_leave_otp(self, e):
        name = self.otp.get()
        if name == "":
            self.otp.insert(0, "Enter OTP")

    def go_back(self):
        self.window.destroy()
        self.sql_data.close_connection()
        Login()

    def check(self, email):
        if (re.search(self.regex_email, email)):
            return True
        else:
            return False



class Reset(RegisterClass, SendOtp):

    def __init__(self):
        self.window = Tk()
        self.window.title("Chess Game - Reset Password")
        self.window.geometry("925x500+300+200")
        self.window.configure(bg="#fff")
        self.window.resizable(0, 0)
        self.window.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.received_otp = 0
        self.data = SqlData()

        self.frame = Frame(self.window, width=550, height=500, bg="white")
        self.frame.place(x=200, y=90)

        heading = Label(self.frame, text="Reset Password", fg="#57a1f8", bg="white",
                        font=("Microsoft YaHei UI Light", 23, "bold"))
        heading.place(x=0, y=5)

        self.email = Entry(self.frame, width=25, fg="black", border=0, bg="white",
                           font=("Microsoft YaHei UI Light", 11))
        self.email.place(x=0, y=80)
        self.email.insert(0, "Email")
        self.email.bind("<FocusIn>", self.on_enter)
        self.email.bind('<FocusOut>', self.on_leave)
        Frame(self.frame, width=250, height=2, bg="black").place(x=0, y=107)

        self.send = Button(self.frame, width=20, text="Send OTP", border=0, bg="white", cursor="hand2", fg="#57a1f8",
                           command=self.reset_otp)
        self.send.place(x=146, y=110)

        self.otp = Entry(self.frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.otp.place(x=320, y=80)
        self.otp.insert(0, "Enter OTP")
        self.otp.bind("<FocusIn>", self.on_enter_otp)

        self.otp.bind("<FocusOut>", self.on_leave_otp)
        Frame(self.frame, width=250, height=2, bg="black").place(x=320, y=107)

        self.conOTP = Button(self.frame, width=20, text="Confirm OTP", border=0, bg="white", cursor="hand2",
                             fg="#57a1f8", command=self.con_otp)
        self.conOTP.place(x=285, y=110)

        self.newPassword = Entry(self.frame, width=25, fg="black", border=0, bg="white",
                                 font=("Microsoft YaHei UI Light", 11))
        self.newPassword.place(x=0, y=150)
        self.newPassword.insert(0, "New Password")
        self.newPassword.bind("<FocusIn>", self.on_enter_pass)
        self.newPassword.bind("<FocusOut>", self.on_leave_pass)
        Frame(self.frame, width=250, height=2, bg="black").place(x=0, y=177)

        self.confirm_pass = Entry(self.frame, width=25, fg="black", border=0, bg="white",
                                  font=("Microsoft YaHei UI Light", 11))
        self.confirm_pass.place(x=320, y=150)
        self.confirm_pass.insert(0, "Confirm Password")
        self.confirm_pass.bind("<FocusIn>", self.on_enter_conPass)
        self.confirm_pass.bind("<FocusOut>", self.on_leave_conPass)
        Frame(self.frame, width=250, height=2, bg="black").place(x=320, y=177)

        self.reset_button = Button(self.frame, width=35, pady=7, text="Reset", bg="#57a1f8", fg="white", border=0,
                                   command=self.reset, state="disabled")
        self.reset_button.place(x=0, y=204)

        self.go_back = Button(self.frame, width=30, text="Go back", border=0, bg="white", cursor="hand2", fg="#57a1f8",
                              command=self.go_back)
        self.go_back.place(x=120, y=245)

        self.window.mainloop()

    def on_enter(self, e):
        if self.email.get() == "Email":
            self.email.delete(0, "end")

    def on_leave(self, e):
        email = self.email.get()
        if email == "":
            self.email.insert(0, "Email")

    def on_enter_pass(self, e):
        if self.newPassword.get() == "New Password":
            self.newPassword.delete(0, "end")

    def on_leave_pass(self, e):
        code = self.newPassword.get()
        if code == "":
            self.newPassword.insert(0, "New Password")

    def on_enter_otp(self, e):
        if self.otp.get() == "Enter OTP":
            self.otp.delete(0, "end")

    def on_leave_otp(self, e):  # for otp
        code = self.otp.get()
        if code == "":
            self.otp.insert(0, "Enter OTP")

    def on_enter_conPass(self, e):
        if self.confirm_pass.get() == "Confirm Password":
            self.confirm_pass.delete(0, "end")

    def on_leave_conPass(self, e):
        code = self.confirm_pass.get()
        if code == "":
            self.confirm_pass.insert(0, "Confirm Password")

    def reset(self):
        pass1 = self.newPassword.get()
        con_pass = self.confirm_pass.get()

        if self.data.check_same_pass(pass1, self.email.get()):  # check for same password
            messagebox.showerror("Failed", "Your new password cannot be same as old password")
        elif 8 > len(pass1) < 16:  # check for length of the password
            messagebox.showerror("Password Error", "Password should be at least of 8 to 16 characters long")
        elif pass1 != con_pass:   # check for password match
            messagebox.showerror("Password Error", "Passwords do not match")
        elif pass1 == "New Password" or con_pass == "Confirm Password":
            messagebox.showerror("Invalid Entry", "Passwords Cannot be blank")
        else:
            if self.data.reset_password(self.email.get(), pass1) == 0:   # Reset Password
                messagebox.showinfo("Success", "Password Reset Successfully")
                self.window.destroy()
                Login()
            else:
                messagebox.showerror("Failed", "Failed to reset password")

    def con_otp(self):
        try:
            if self.email.get() == "Email":
                messagebox.showerror("Invalid Entry", "Email Cannot be blank")
            elif self.received_otp == int(self.otp.get()):
                self.otp_confirmed = True
                self.reset_button["state"] = "normal"
            else:
                messagebox.showerror('Invalid OTP', "Invalid OTP, Please enter correct OTP or "
                                                    "check you email that you've entered")
        except ValueError:
            messagebox.showerror('Invalid OTP', "Invalid OTP, Please enter correct OTP or "
                                                "check you email that you've entered")

    def reset_otp(self):
        email = self.email.get()
        if not self.data.check_mail(email):
            messagebox.showerror("Invalid Email", f"{email} does not exist")
        else:
            s = SendOtp()

            if not self.check(email):
                messagebox.showerror('Invalid Entry',
                                     'Invalid Email, Please Enter a valid Email.\nEither @gmail.com or '
                                     '@yahoo.com')
            else:
                self.received_otp = s.send_mail(receiver=self.email.get())

    def check(self, email):
        if (re.search(self.regex_email, email)):
            return True
        else:
            return False

    def go_back(self):
        self.window.destroy()
        Login()



