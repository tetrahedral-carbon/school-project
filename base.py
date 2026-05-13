#modules imported
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox  #customtkinter doesnt have a messagebox
from google import genai
import mysql.connector as mcon


class DB:
    def __init__(self):
        # info about host, user, database
        self.db = mcon.connect(
            host = "localhost",
            user = "root",
            passwd = "ilikemysql",
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
    
    
    # stores user info and answers (in the form of string) in database
    def store_ans(self, data_list):
        mycursor = self.db.cursor()
        # data_list should contain 62 elements, 1 name, 1 guessed career and 60 answers
        
        # placeholders and columns generator
        placeholders = ", ".join(["%s"] * 62)
        q_columns = ", ".join([f"q{i}" for i in range(1, 61)])
        columns = "user_name, user_guess" + q_columns

        sql_query = f"INSERT INTO answers ({columns}) VALUES ({placeholders})"
        mycursor.execute(sql_query, data_list)
        self.db.commit()


class AI:
    def __init__(self, info_dict):
        self.info_dict = info_dict      # stores the dictionary of user's answers
        self.ai_result = None           # stores the output of the ai model
    
    # gives ai model the user's answers and gets the output
    def give_ai_data(self):
        client = genai.Client(api_key="AIzaSyBp5XGXWTFJ4JFXQLUpasLYcoVhP8w5SyU")
        
        # generating ai output
        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=str(self.info_dict)
        )
        self.ai_result = response.text
    
    # passes ai output for further processes
    def pass_result(self):
        return self.ai_result
    

#sample usage of AI class
#my_object = AI({"initial": "this dictionary contains a set of questions and answers on a scale of 1 to 5 (1-strongly disagree, 5-strongly agree). recommend me 3 suitable career options", 
#                 "i am very honest": 5, 
#                 "i like cars": 2, 
#                 "i am very social": 3})
#my_object.give_ai_data()
#answer = my_object.pass_result()
#print(answer)



''' USER INTERFACE PART OF THE PROGRAM '''


### use ttkbootstrap and change color palette


# Variables used for formatting
font_styles={ "labels":("Arial",25),
             "button 1":("Helvitica",20),
             "button 2":("Helvitica",10),
             "entry box":("Arial",20),
             "text box":("Park Avenue", 20, "italic")
             }

font_sizes={ "labels":25, 
            "significant_button":20,
            "insignificant button":10}

color_palette={
    "frame fg":"#0D0D0D",
    "text color 1":"#EAEAEA",
    "text color 2":"#A0A0A0",
    "border color":"#9B5DE5",
    "fg color 1":"#151515",
    "fg color 2":"#1A1A1A",
    "button hover color":"red"
              }
border_width=5

def intro_window():

    # window Initialisation and Formatting

    intro_gui = ctk.CTk()
    intro_gui.title("Career Suggestion Quiz")
    intro_gui.geometry("700X600")
    ctk.set_appearance_mode("dark")


    intro_gui_frame=ctk.CTkFrame(intro_gui, fg_color=color_palette["frame fg"])
    intro_gui_frame.pack(fill="both",expand=True)


    # variables used for storing information
    name_var = ctk.StringVar()          #varible to get username
    usernames_with_previews={}          #variable to link username wIth previews                   
    

    # Logic Functions
    def submit_details():
        username = name_var.get().strip()

        if not username:
            CTkMessagebox(title="Error", message="Please enter a valid username", icon="cancel")    #makes sure empty usernames are rejected
        elif username in usernames_with_previews:
            CTkMessagebox(title="Error", message="Username already in use!", icon="warning")        #makes sure duplication usernames are not used
            name_entry.delete(0, "end")
        else:
            preview_text = preview_textbox.get("1.0", "end-1c")     #extracts preview
            usernames_with_previews[username] = preview_text        #links username to preview
            intro_gui.destroy()                                     #destroys the window
            ###quiz_gui()                                           #calls next window

    # UI Components 
    

    #  Header 
    header_label = ctk.CTkLabel(intro_gui_frame, text="Career Guidance Quiz",
                                font=("Helvetica", 40, "bold"), corner_radius=15,
                                text_color="#230DCE", fg_color="#FFFFFF")      ###custom font style to be used
    header_label.pack(pady=(20, 10))

    # Instructions

    inst_text = (
        "WELCOME TO YOUR FUTURE\n\n"
        "1. Choose from three specialized career quizzes.\n"
        "2. Add a 'career preview' to compare your thoughts with our results.\n"
        "3. Answer truthfully—there are no wrong answers!\n"
        "4. You can always come back and try different quizzes later."
    )
    instructions_box = ctk.CTkTextbox(intro_gui_frame, width=700, height=185, 
                                      font=font_styles["text box"], corner_radius=20, 
                                      text_color=color_palette["text color 1"], fg_color=color_palette["fg color 1"], 
                                      border_color=color_palette["border color"], border_width=3)
    instructions_box.insert("0.0", inst_text)           #inserts text into textbox
    instructions_box.configure(state="disabled")        #configures it so it can't be changed
    instructions_box.pack(pady=10)


    # Input Section (Using a Frame for better grouping)
    input_frame = ctk.CTkFrame(intro_gui_frame, fg_color="transparent")
    input_frame.pack(pady=20, padx=400)


    ctk.CTkLabel(input_frame, text="Username", 
                 font=font_styles["labels"], corner_radius=15, 
                 text_color=color_palette["text color 1"], fg_color=color_palette["fg color 1"]).grid(row=0, column=4, sticky="w")
    name_entry = ctk.CTkEntry(input_frame, textvariable=name_var, 
                              width=300 , font=font_styles["entry box"],
                              fg_color=color_palette["fg color 2"], text_color=color_palette["text color 2"])
    name_entry.grid(row=1, column=4, pady=(5, 10), padx=(0, 10))


    btn_clear_name = ctk.CTkButton(input_frame, text="Clear", width=80, 
                                   fg_color=color_palette["fg color 1"],hover_color=color_palette["button hover color"],
                                   text_color=color_palette["text color 1"], border_width=1,
                                   command=lambda:name_entry.delete(0, "end"))
    btn_clear_name.grid(row=1, column=5, pady=(5, 10))


    # Career Preview Section
    ctk.CTkLabel(input_frame, text="Career Preview (Optional)", 
                 font=font_styles["labels"]
                 , text_color=color_palette["text color 1"]).grid(row=2, column=4, sticky="w")
    
    preview_textbox = ctk.CTkTextbox(input_frame, height=100,  font=font_styles["text box"],
                                     text_color=color_palette["text color 2"], fg_color=color_palette["fg color 1"], 
                                     border_color=color_palette["border color"],border_width=3)
    preview_textbox.grid(row=3, column=4, columnspan=2, pady=(5, 10), sticky="nsew")


    btn_clear_preview = ctk.CTkButton(input_frame, text="Clear Preview", width=100,
                                      fg_color=color_palette["fg color 1"], hover_color=color_palette["button hover color"],
                                        border_width=1,
                                      command=lambda:preview_textbox.delete("1.0", "end"))
    btn_clear_preview.grid(row=4, column=4, sticky="w")

    # Action Buttons 

    button_container = ctk.CTkFrame(intro_gui_frame, fg_color="transparent")
    button_container.pack(side="bottom", pady=30)


    submit_btn = ctk.CTkButton(button_container, text="Submit", 
                               width=200, height=40,
                               fg_color="#2fa572", hover_color="#106a43",
                               command=submit_details)
    submit_btn.pack(side="left", padx=10)


    quit_btn = ctk.CTkButton(button_container, text="Exit", 
                             width=100, height=40,
                             fg_color="#0f0404", hover_color="#802c2c", # Red tones
                             command=intro_gui.destroy)
    quit_btn.pack(side="left", padx=10)

    intro_gui.mainloop()

intro_window()
