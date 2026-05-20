



        #modules imported
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox  #customtkinter doesnt have a messagebox
from google import genai
import mysql.connector as mcon
from PIL import Image
from PIL import Image

font_styles={ "labels":("Arial",25),
             "quiz header":("Helvetica", 50, "bold"),
             "quiz instructions":("Helvetica", 25, "normal"),
             "button 1": ("Helvetica", 15, "bold"),
             "quiz header":("Helvetica", 50, "bold"),
             "quiz instructions":("Helvetica", 25, "normal"),
             "button 1": ("Helvetica", 15, "bold"),
             "button 2":("Helvitica",10),
             "entry box":("Arial",20),
             "text box":("Park Avenue", 20, "italic")
             }
class DB:
    def __init__(self):
        # info about host, user, database
        self.db = mcon.connect(
            host = "localhost",
            user = "root",
            passwd = "dharun123",
            database = "mydb"
        )

        self.mycursor = self.db.cursor()     # mycursor is used execute read and write queries   

    # retrieves questions from database (APART FROM PERSONALITY)
    def get_q(self):
        mycursor = self.db.cursor()

        # each question comes in the form of a single-element tuple
        
        q_list = []     # creating list to contain all questions

        # second table - skills questions
        mycursor.execute("SELECT question FROM skills_questions")
        
        for qt in mycursor:
            q_list.append(qt[0])
        
        # third table - interest questions
        mycursor.execute("SELECT question FROM interest_questions")
        
        for qt in mycursor:
            q_list.append(qt[0])

        # returning list of questions for further processing
        return q_list


    # retrieves personality questions and options from personality table
    def get_qo_personality(self):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT question, option1, option2, option3, option4 FROM personality_questions")

        qp_list = []            # creating list to store personality questions
        qp_options = []         # creating list to store options

        for qot in mycursor:
            qp_list.append(qot[0])
            qp_options.append((qot[1], qot[2], qot[3], qot[4]))
        
        # returning tuple of questions, options for further processing
        return (qp_list, qp_options)
    
    
    # stores user info, answers and carer options (in the form of string) in database
    def store_ans(self, data_list):
        mycursor = self.db.cursor()
        # data_list should contain 65 elements, 1 username, 1 guessed career, 60 answers and 3 career options
        
        # placeholders and columns generator
        placeholders = ", ".join(["%s"] * 65)
        q_columns = ", ".join([f"q{i}" for i in range(1, 61)])
        columns = "username, user_guess" + q_columns + "career1, career2, career3"

        sql_query = f"INSERT INTO answers ({columns}) VALUES ({placeholders})"
        mycursor.execute(sql_query, data_list)
        self.db.commit()
        self.db.commit()

def interests_quiz():
        quiz_gui=ctk.CTk()
        # 1. Hide the original main screen
        quiz_gui.withdraw()

        # 2. Use CTkToplevel instead of ctk.CTk() for secondary windows
        interests_gui = ctk.CTkToplevel(quiz_gui)
        interests_gui.title("Career Compass")
        interests_gui.geometry("700x600")
        
        # Ensures the sub-window appears on top focus
        interests_gui.lift()
        interests_gui.attributes("-topmost", True)

        # 3. Handle what happens if the user closes the window with the 'X' button
        def on_close_shortcut():
            interests_gui.destroy()
            quiz_gui.deiconify() # Bring back original window

        interests_gui.protocol("WM_DELETE_WINDOW", on_close_shortcut)

        # Scrollable Frame Content Container
        interests_gui_frame = ctk.CTkScrollableFrame(interests_gui, fg_color="black")
        interests_gui_frame.pack(fill="both", expand=True)

        # Grid system column weights to align everything
        interests_gui_frame.grid_columnconfigure(0, weight=1)
        for c in range(1, 6):
            interests_gui_frame.grid_columnconfigure(c, minsize=50)

        # Instructions label
        instructions_text = (
            "Welcome to The Interests Quiz\n"
            "Choose a value from 1 to 5 for each question.\n\n"
            "1: almost never | 2: very rarely | 3: neutral | 4: i enjoy it | 5: highly interested"
        )
        instructions = ctk.CTkLabel(interests_gui_frame, text=instructions_text, font="red", justify="left")
        instructions.grid(row=0, column=0, columnspan=6, sticky="w", padx=10, pady=10)
        
        # Variables configuration
        linking_list = [ctk.IntVar(value=-1) for _ in range(20)]
        total_questions = DB()
        questions = total_questions.get_q()
        
        # Build layout elements
        for q in range(20):
            question_label = ctk.CTkLabel(interests_gui_frame, text=f"{q+1}). {questions[q+20]}", font=font_styles["labels"])
            question_label.grid(row=q+2, column=0, pady=(20, 5), padx=10, sticky="w")
            
            for button_value in range(1, 6):
                radio_button = ctk.CTkRadioButton(interests_gui_frame, text=str(button_value), variable=linking_list[q], value=button_value)
                radio_button.grid(row=q+2, column=button_value, sticky="c", pady=(20, 5), padx=5)

        # 4. Submit button action to save and route back home
        def submit_quiz_data():
            # ... process details or database push statements here ...
            
            # Clean exit out of the sub-window and show the home page again
            interests_gui.destroy()
            quiz_gui.deiconify()

        submit_btn = ctk.CTkButton(interests_gui_frame, text="Submit Answers", command=submit_quiz_data)
        submit_btn.grid(row=23, column=0, columnspan=6, pady=30)
interests_quiz()