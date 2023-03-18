import sys
import tkinter.messagebox
import hashlib
import pymysql
from tkinter import messagebox
import pandas

duplicate = False


class SqlData:
    def __init__(self):

        #  Create a Database
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',            # Your database password
                charset='utf8mb4'
            )

            self.cursor = self.conn.cursor()
            self.create_db()
            self.create_tables()
        except Exception as e:  # If the database exists or the table exists then just skip the above steps and continue
            pass

        # Connect to the MySQL server
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',        # Your Database Password
                charset='utf8mb4'
            )

            self.cursor = self.conn.cursor()
            self.cursor.execute("USE gamedata")
        except Exception as e:
            messagebox.showerror("Error",
                                 "Cannot connect to the database.\n Please Restart the game and check the 'Database'")
            sys.exit()
        # Connect to the database

    def create_db(self):
        self.cursor.execute("CREATE DATABASE gamedata")
        # Use the Game_data database

    def create_tables(self):
        self.cursor.execute("USE gamedata")
        self.user_data_sql = """
                CREATE TABLE user_data (
                  id INT NOT NULL AUTO_INCREMENT,
                  name VARCHAR(255) NOT NULL,
                  username VARCHAR(255) NOT NULL UNIQUE,
                  email VARCHAR(255) NOT NULL UNIQUE,
                  password VARCHAR(255) NOT NULL,
                  PRIMARY KEY (id)
                );
                """

        # Define the black_pieces table SQL statement
        self.black_pieces_sql = """
        CREATE TABLE black_pieces (
          pawn1 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn2 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn3 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn4 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn5 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn6 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn7 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn8 VARCHAR(255) NOT NULL DEFAULT '0',
          rook1 VARCHAR(255) NOT NULL DEFAULT '0',
          rook2 VARCHAR(255) NOT NULL DEFAULT '0',
          bishop1 VARCHAR(255) NOT NULL DEFAULT '0',
          bishop2 VARCHAR(255) NOT NULL DEFAULT '0',
          knight1 VARCHAR(255) NOT NULL DEFAULT '0',
          knight2 VARCHAR(255) NOT NULL DEFAULT '0',
          king1 VARCHAR(255) NOT NULL DEFAULT '0',
          queen1 VARCHAR(255) NOT NULL DEFAULT '0',
          user_id INT NOT NULL UNIQUE,
                  FOREIGN KEY (user_id) REFERENCES user_data(id)
                );
                """

        # Execute the black_pieces table SQL statement

        self.white_pieces_sql = """
                CREATE TABLE white_pieces (
                  pawn1 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn2 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn3 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn4 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn5 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn6 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn7 VARCHAR(255) NOT NULL DEFAULT '0',
          pawn8 VARCHAR(255) NOT NULL DEFAULT '0',
          rook1 VARCHAR(255) NOT NULL DEFAULT '0',
          rook2 VARCHAR(255) NOT NULL DEFAULT '0',
          bishop1 VARCHAR(255) NOT NULL DEFAULT '0',
          bishop2 VARCHAR(255) NOT NULL DEFAULT '0',
          knight1 VARCHAR(255) NOT NULL DEFAULT '0',
          knight2 VARCHAR(255) NOT NULL DEFAULT '0',
          king1 VARCHAR(255) NOT NULL DEFAULT '0',
          queen1 VARCHAR(255) NOT NULL DEFAULT '0',
          user_id INT NOT NULL UNIQUE,
                  FOREIGN KEY (user_id) REFERENCES user_data(id)
                );
                """

        self.cursor.execute(self.user_data_sql)
        self.cursor.execute(self.black_pieces_sql)
        self.cursor.execute(self.white_pieces_sql)

    def check_for_duplicate(self, username=None, email=None):
        global duplicate
        if None != username:

            query = f"SELECT * FROM user_data WHERE username = %s"
            self.cursor.execute(query, (username,))

        elif None != email:

            query = f"SELECT * FROM user_data WHERE email = %s"
            self.cursor.execute(query, (email,))

        # Fetch the results
        self.cursor.fetchall()

        if self.cursor.rowcount == 0:
            return False
        else:
            duplicate = True
            return True

    def check_mail(self, email):
        self.cursor.execute('SELECT * FROM user_data')

        # Iterate over the rows of the result
        for row in self.cursor:
            # Check if the username and password match the given values
            if row[3] == email:
                return True

    def check_same_pass(self, password, email):
        query = 'SELECT * FROM user_data WHERE email = %s'
        self.cursor.execute(query, (email,))

        # Iterate over the rows of the result
        for row in self.cursor:
            # Check if the username and password match the given values
            if row[4] == password:
                return True

    def reset_password(self, email, password):
        hashed_pass = self.my_hash(password)
        # Check if the email is present in the table
        query = "SELECT * FROM user_data WHERE email = %s"
        self.cursor.execute(query, (email,))

        # If the email is present, update the password
        if self.cursor.rowcount > 0:
            try:
                query = "UPDATE user_data SET password = %s WHERE email = %s"
                self.cursor.execute(query, (hashed_pass, email))
                self.conn.commit()
                return 0
            except Exception as e:
                return -1
        else:
            return -1

    def insert_for_register(self, name, password, email, username):
        hashed_pass = self.my_hash(password)
        global duplicate

        if not duplicate:
            self.cursor.execute(
                f"INSERT INTO user_data (name, username, email, password) VALUES ('{name}', '{username}', '{email}', '{hashed_pass}');"
            )
            self.conn.commit()
        # Commit the changes to the database

    def close_connection(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def my_hash(self, password):
        sha256_hash = hashlib.sha256(password.encode()).hexdigest()

        # Truncate the hash to the desired length (16 characters)
        truncated_hash = sha256_hash[:16]

        return truncated_hash

    def user_login(self, usn, password):

        hashed_pass = self.my_hash(password)
        self.cursor.execute('SELECT * FROM user_data')

        # Iterate over the rows of the result
        for row in self.cursor:
            # Check if the username and password match the given values
            if str(row[2]) == usn and str(row[4]) == hashed_pass:
                return row[0]

        return None

    def save_func(self, white, black, user_id):

        pawns_pos = []
        rook_pos = []
        knight_pos = []
        bishop_pos = []
        queen_pos = 0
        king_pos = 0
        st_row = 0
        st_col = 0

        #   SAVING WHITE PIECES DATA
        try:

            for i in range(1, 9, +1):  # Block to load Pawns both white
                try:
                    st_row = white[f"pawn{i}"][0]
                    st_col = white[f"pawn{i}"][1]
                except KeyError as e:
                    tkinter.messagebox.showerror("Invalid", f"Something Went Wrong. The game cannot be saved\n{e}")

                row = int(st_row)
                col = int(st_col)

                if white[f"pawn{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)

                pawns_pos.append(pos)

            for i in range(1, 3, +1):  # Block to load rook both white
                try:
                    st_row = white[f"rook{i}"][0]
                    st_col = white[f"rook{i}"][1]
                except KeyError as e:
                    tkinter.messagebox.showerror("Invalid", f"Something Went Wrong. Try again\n {e}")

                row = int(st_row)
                col = int(st_col)

                if white[f"rook{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)

                rook_pos.append(pos)

            for i in range(1, 3, +1):  # Block to load knights both white and black
                try:
                    st_row = white[f"knight{i}"][0]
                    st_col = white[f"knight{i}"][1]
                except KeyError as e:
                    tkinter.messagebox.showerror("Invalid", f"Something Went Wrong. Try again\n {e}")

                row = int(st_row)
                col = int(st_col)

                if white[f"knight{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)
                knight_pos.append(pos)

            for i in range(1, 3, +1):  # Block to load bishop both white and black
                try:
                    st_row = white[f"bishop{i}"][0]
                    st_col = white[f"bishop{i}"][1]
                except KeyError as e:
                    tkinter.messagebox.showerror("Invalid", f"Something Went Wrong. Try again\n {e}")

                row = int(st_row)
                col = int(st_col)

                if white[f"bishop{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)

                bishop_pos.append(pos)

            #  Block to save Queen Pos
            q_st_row = 0
            q_st_col = 0

            try:
                q_st_row = white[f"queen{1}"][0]
                q_st_col = white[f"queen{1}"][1]
            except KeyError as e:
                tkinter.messagebox.showerror("Invalid", f"Something Went Wrong. Try again\n {e}")

            row = int(q_st_row)
            col = int(q_st_col)

            if white[f"queen{1}"][2] == "False":
                cap = 1
            else:
                cap = 0

            pos = str(row) + str(col) + str(cap)
            queen_pos = pos

            #  Block to save king pos

            try:
                st_row = white[f"king{1}"][0]
                st_col = white[f"king{1}"][1]
            except KeyError as e:
                tkinter.messagebox.showerror("Invalid", f"Something Went Wrong. Try again\n {e}")

            row = int(st_row)
            col = int(st_col)

            if white[f"king{1}"][2] == "False":
                cap = 1
            else:
                cap = 0

            pos = str(row) + str(col) + str(cap)
            king_pos = pos
        except Exception as e:
            tkinter.messagebox.showerror("Invalid", f"Something Went Wrong. Try again\n {e}")

        def save_pos(color):

            # Execute the statement
            try:
                self.cursor.execute(f"INSERT INTO {color}_pieces (pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, "
                                    f"pawn8, rook1, rook2, bishop1, bishop2, knight1, knight2, queen1, king1, user_id) "
                                    f"VALUES ({pawns_pos[0]}, {pawns_pos[1]}, {pawns_pos[2]}, {pawns_pos[3]}, {pawns_pos[4]}, "
                                    f"{pawns_pos[5]}, {pawns_pos[6]}, {pawns_pos[7]}, {rook_pos[0]}, {rook_pos[1]}, {bishop_pos[0]},"
                                    f" {bishop_pos[1]}, {knight_pos[0]}, {knight_pos[1]}, {queen_pos}, {king_pos}, {user_id}) "
                                    f"ON DUPLICATE KEY UPDATE "
                                    f"pawn1={pawns_pos[0]}, pawn2={pawns_pos[1]}, pawn3={pawns_pos[2]}, pawn4={pawns_pos[3]}, "
                                    f"pawn5={pawns_pos[4]},pawn6={pawns_pos[5]}, pawn7={pawns_pos[6]}, pawn8={pawns_pos[7]}, "
                                    f"rook1={rook_pos[0]}, rook2={rook_pos[1]},"
                                    f"bishop1={bishop_pos[0]}, bishop2={bishop_pos[1]}, knight1={knight_pos[0]}, knight2={knight_pos[1]},"
                                    f" queen1={queen_pos}, king1={king_pos}")
            except pymysql.err.IntegrityError as e:

                tkinter.messagebox.showerror("Invalid", f"Unable to make a save. Please try Again! \n{e}")

            # Commit the changes to the database
            self.conn.commit()

        save_pos("white")  # Finally saves the data into the db

        # Reset every list to empty
        pawns_pos = []
        rook_pos = []
        knight_pos = []
        bishop_pos = []
        queen_pos = 0
        king_pos = 0
        try:

            #    SAVING BLACK PIECES DATA
            for i in range(1, 9, +1):  # Block to load Pawns black
                try:
                    st_row = black[f"pawn{i}"][0]
                    st_col = black[f"pawn{i}"][1]
                except KeyError:
                    tkinter.messagebox.showerror("Invalid", "Something Went Wrong. Try again")

                row = int(st_row)
                col = int(st_col)

                if black[f"pawn{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)

                pawns_pos.append(pos)

            # Block to load rook black
            for i in range(1, 3, +1):
                try:
                    st_row = black[f"rook{i}"][0]
                    st_col = black[f"rook{i}"][1]
                except KeyError:
                    tkinter.messagebox.showerror("Invalid", "Something Went Wrong. Try again")

                row = int(st_row)
                col = int(st_col)

                if black[f"rook{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)

                rook_pos.append(pos)

            # Block to load knights both white and black
            for i in range(1, 3, +1):
                try:
                    st_row = black[f"knight{i}"][0]
                    st_col = black[f"knight{i}"][1]
                except KeyError:
                    tkinter.messagebox.showerror("Invalid", "Something Went Wrong. Try again")

                row = int(st_row)
                col = int(st_col)

                if black[f"knight{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)

                knight_pos.append(pos)

            for i in range(1, 3, +1):  # Block to load bishop black
                try:
                    st_row = black[f"bishop{i}"][0]
                    st_col = black[f"bishop{i}"][1]
                except KeyError:
                    tkinter.messagebox.showerror("Invalid", "Something Went Wrong. Try again")

                row = int(st_row)
                col = int(st_col)

                if black[f"bishop{i}"][2] == "False":
                    cap = 1
                else:
                    cap = 0

                pos = str(row) + str(col) + str(cap)

                bishop_pos.append(pos)

            #  Block to save Queen Pos
            try:
                q_st_row = black[f"queen{1}"][0]
                q_st_col = black[f"queen{1}"][1]
            except KeyError:
                tkinter.messagebox.showerror("Invalid", "Something Went Wrong. Try again")

            row = int(q_st_row)
            col = int(q_st_col)

            if black[f"queen{1}"][2] == "False":
                cap = 1
            else:
                cap = 0

            pos = str(row) + str(col) + str(cap)
            queen_pos = pos

            #  Block to save king pos
            try:
                st_row = black[f"king{1}"][0]
                st_col = black[f"king{1}"][1]
            except KeyError:
                tkinter.messagebox.showerror("Invalid", "Something Went Wrong. Try again")

            row = int(st_row)
            col = int(st_col)

            if black[f"king{1}"][2] == "False":
                cap = 1
            else:
                cap = 0

            pos = str(row) + str(col) + str(cap)
            king_pos = pos

            save_pos("black")  # Finally saves the data into the Database for black pieces
            tkinter.messagebox.showinfo("Save Complete", f"Game Save Complete")
        except Exception:
            tkinter.messagebox.showerror("Invalid", "Something Went Wrong. Try again")


    def load_data(self, color, user_id):
        white_data = {}
        black_data = {}
        pieces_loc = []

        self.cursor.execute(f'SELECT * FROM {color}_pieces WHERE user_id = {user_id}')
        row = self.cursor.fetchone()

        if row is not None:
            for i in range(0, 16, +1):
                pieces_loc.append(row[i])

        i = 0
        col = 0
        cap = 0

        for pos in pieces_loc:
            i += 1
            if i <= 8:
                try:
                    if pos[2] == "1":
                        row = int(pos[0])
                        col = int(pos[1])
                        cap = int(pos[2])

                except IndexError:
                    if len(pos) == 1:
                        row = 0
                        col = 0
                        cap = int(pos[0])
                    elif len(pos) == 2:
                        row = 0
                        col = int(pos[0])
                        cap = int(pos[1])
                finally:
                    if color == "white":  # save the piece data in variable white and black data
                        white_data[f"pawn{i}"] = row, col, cap
                    else:
                        black_data[f"pawn{i}"] = row, col, cap

        # TO load data of rooks
        i = 0
        j = 8
        for pos in pieces_loc:
            i += 1
            if 9 <= i <= 10:

                try:
                    row = int(pos[0])
                    col = int(pos[1])
                    cap = int(pos[2])
                except IndexError:
                    if len(pos) == 1:
                        row = 0
                        col = 0
                        cap = int(pos[0])
                    elif len(pos) == 2:
                        row = 0
                        col = int(pos[0])
                        cap = int(pos[1])

                if color == "white":  # save the piece data in variable white and black data
                    white_data[f"rook{i - j}"] = row, col, cap
                else:
                    black_data[f"rook{i - j}"] = row, col, cap

        if color == "white":
            white_pieces_data1 = pandas.DataFrame(white_data)
            white_pieces_data1.to_csv("../../data/white_data.csv")
        else:
            black_pieces_data = pandas.DataFrame(black_data)
            black_pieces_data.to_csv("../../data/black_data.csv")

        # TO LOAD BISHOP DATA
        i = 0
        j = 10
        for pos in pieces_loc:
            i += 1
            if 11 <= i <= 12:

                try:
                    row = int(pos[0])
                    col = int(pos[1])
                    cap = int(pos[2])
                except IndexError:
                    if len(pos) == 1:
                        row = 0
                        col = 0
                        cap = int(pos[0])
                    elif len(pos) == 2:
                        row = 0
                        col = int(pos[0])
                        cap = int(pos[1])

                if color == "white":  # save the piece data in variable white and black data
                    white_data[f"bishop{i - j}"] = row, col, cap
                else:
                    black_data[f"bishop{i - j}"] = row, col, cap

        if color == "white":
            white_pieces_data1 = pandas.DataFrame(white_data)
            white_pieces_data1.to_csv("../../data/white_data.csv")
        else:
            black_pieces_data = pandas.DataFrame(black_data)
            black_pieces_data.to_csv("../../data/black_data.csv")

        # TO LOAD KNIGHT DATA
        i = 0
        j = 12
        for pos in pieces_loc:
            i += 1
            if 13 <= i <= 14:

                try:
                    row = int(pos[0])
                    col = int(pos[1])
                    cap = int(pos[2])
                except IndexError:
                    if len(pos) == 1:
                        row = 0
                        col = 0
                        cap = int(pos[0])
                    elif len(pos) == 2:
                        row = 0
                        col = int(pos[0])
                        cap = int(pos[1])

                if color == "white":  # save the piece data in variable white and black data
                    white_data[f"knight{i - j}"] = row, col, cap
                else:
                    black_data[f"knight{i - j}"] = row, col, cap

        if color == "white":
            white_pieces_data1 = pandas.DataFrame(white_data)
            white_pieces_data1.to_csv("../../data/white_data.csv")
        else:
            black_pieces_data = pandas.DataFrame(black_data)
            black_pieces_data.to_csv("../../data/black_data.csv")

        # TO LOAD QUEEN DATA
        i = 0
        j = 14
        for pos in pieces_loc:
            i += 1
            if i == 15:
                try:
                    row = int(pos[0])
                    col = int(pos[1])
                    cap = int(pos[2])

                except IndexError:
                    if len(pos) == 1:
                        row = 0
                        col = 0
                        cap = int(pos[0])
                    elif len(pos) == 2:
                        row = 0
                        col = int(pos[0])

                        cap = int(pos[1])

                if color == "white":  # save the piece data in variable white and black data
                    white_data[f"king{i - j}"] = row, col, cap
                else:
                    black_data[f"king{i - j}"] = row, col, cap

        if color == "white":
            white_pieces_data1 = pandas.DataFrame(white_data)
            white_pieces_data1.to_csv("../../data/white_data.csv")
        else:
            black_pieces_data = pandas.DataFrame(black_data)
            black_pieces_data.to_csv("../../data/black_data.csv")

        # TO LOAD KING DATA
        i = 0
        j = 15
        for pos in pieces_loc:
            i += 1
            if i == 16:

                try:
                    row = int(pos[0])
                    col = int(pos[1])
                    cap = int(pos[2])
                except IndexError:
                    if len(pos) == 1:
                        row = 0
                        col = 0
                        cap = int(pos[0])
                    elif len(pos) == 2:
                        row = 0
                        col = int(pos[0])
                        cap = int(pos[1])

                if color == "white":  # save the piece data in variable white and black data
                    white_data[f"queen{i - j}"] = row, col, cap
                else:
                    black_data[f"queen{i - j}"] = row, col, cap

        if color == "white":
            white_pieces_data1 = pandas.DataFrame(white_data)
            white_pieces_data1.to_csv("../../data/white_data.csv")
        else:
            black_pieces_data = pandas.DataFrame(black_data)
            black_pieces_data.to_csv("../../data/black_data.csv")




