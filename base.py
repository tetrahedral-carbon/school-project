#modules imported
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox  #customtkinter doesnt have a messagebox
from google import genai
import mysql.connector as mcon
from PIL import Image


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
    
    # retrieves career options from database based on username
    def get_result(self, username):
        mycursor = self.db.cursor()

        sql_query = "SELECT career1, career2, career3 FROM answers WHERE username = \"" + username + "\""
        mycursor.execute(sql_query)
        
        career_tuple = ()
        for career in mycursor:
            career_tuple += career
        
        return career_tuple         # returns tuple containing the 3 career options



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
#my_object = AI({"initial": "this dictionary contains a set of questions and answers on a scale of 1 to 5 (1-strongly disagree, 5-strongly agree). recommend me 3 suitable career options. at the end give me a string of the 3 options in python syntax", 
#                 "i am very honest": 5, 
#                 "i like cars": 2, 
#                 "i am very social": 3})
#my_object.give_ai_data()
#answer = my_object.pass_result()
#print(answer)


''' USER INTERFACE PART OF THE PROGRAM '''


### use ttkbootstrap and change color palette


# Variables used for formatting
font_styles={
            #intro window                                   #register label not present
            "heading intro":("Helvetica", 30, "bold"),          
            "instructions intro":("Park Avenue", 20, "italic"),
            "labels intro":("Arial",25),
            "entry intro":("Arial",15),

            #quiz window
            "quiz window heading":("Helvetica", 40, "bold"),    
            "quiz heading":("Helvetica", 50, "bold"),
            "quiz instructions":("Helvetica", 25, "normal"),
            "quiz button": ("Helvetica", 15, "bold"),
            
            #interest and skills quiz
            "questions":("Arial",25),
            "instructions":("Arial",25),
            "number headers":("Arial",25),
            "button size":(25,25,15) ,#height and width and selected ring size

            #personality quiz
            "questions p":("Arial",25),
            "instructions p":("Arial",32),
            "options p":("Arial",15)
             }



                

color_palette={
    "frame fg":"#000000",
    # intro window              #submit ,quit , check button not added
    "heading text intro":"blue",
    "heading bg intro":"white",
    "instructions text intro":"green",
    "instructions fg intro":"black",
    "labels text intro":"white",
    "labels fg intro":"black",
    "entry text intro":"white",
    "entry fg intro":"black",
    "clear button text intro":"white",
    "clear button fg intro":"black",            
    "clear button hover color intro":"red",
    "border intro":"yellow",
    # quiz window
    "heading quiz text":"white",
    "heading quiz fg":"black",

    "interests card": "#1B2E24",
    "interests head":"green",     
    "interests btn fg": "#0CB943",
    "interests instructions":"green",
    "interests btn hover":"light green",

    "personality card": "#2B1B3A", 
    "personality head":"pink",
    "personality btn fg": "#C148E6",
    "personality instructions":"pink",
    "personality btn hover":"light pink",

    "skills card": "#1B2D3A",    
    "skills head":"blue",
    "skills btn fg": "#53DFEC",
    "skills instructions":"blue",
    "skills btn hover":"cyan",

    "quiz button text":"black",

    #interest quiz
    "heading 1":"#00FF48",
    "question 1":"#65F775",
    "button hover 1":"green",
    "selected button color 1":"green",
    "unselected button color 1":"light green",
    #skills quiz
    "heading 2":"#3590E5",
    "question 2":"#65E4F7",
    "button hover 2":"cyan",
    "selected button color 2":"blue",
    "unselected button color 2":"cyan",

    #personality quiz
    "heading 3":"#E81616",
    "question 3":"red",
    "button hover 3":"pink",
    "selected button color 3":"pink",
    "unselected button color 3":"pink",
    "options color":"pink"
    }



def intro_window():
    global user
    # window Initialisation and Formatting
    
    intro_gui = ctk.CTk()
    intro_gui.title("Career Compass")
    intro_gui.title("Career Compass")
    intro_gui.geometry("700X600")
    ctk.set_appearance_mode("dark")
    intro_gui.after(0, lambda: intro_gui.state('zoomed'))       #sets full screen default

    intro_gui_frame=ctk.CTkFrame(intro_gui, fg_color="#A6D2E6")
    intro_gui_frame.pack(side="left", fill="both", expand=True, padx=(30, 10), pady=10)

    image_frame = ctk.CTkFrame(intro_gui_frame, fg_color="transparent")
    image_frame.pack(side="right", fill="both", expand=True, padx=(10, 30), pady=10)

    # variables used for storing information and formatting
    name_var = ctk.StringVar()          #varible to get username
    usernames_with_previews={}          #variable to link username wIth previews                   

    # Logic Functions
    def submit_details():
        username = name_var.get().strip()

        if not username:        #checks if username is empty
            CTkMessagebox(title="Error", message="Please enter a valid username", icon="cancel")    #makes sure empty usernames are rejected
        elif username in usernames_with_previews:   ###change to DB
            CTkMessagebox(title="Error", message="Username already in use!", icon="warning")        #makes sure duplication usernames are not used
            name_entry.delete(0, "end")
        else:
            preview_text = preview_textbox.get("1.0", "end-1c")     
            usernames_with_previews[username] = preview_text        ###change to DB
            intro_gui.destroy()                              
            quiz_window()                                           

    
    def check_username():       #user can check if their previous results
        check_name_input=ctk.CTkInputDialog(title="check Username",text="Enter your registered username") 
        check_name=check_name_input.get_input()

        if check_name==None: 
            return          # exits function if window closed 
        
        if not check_name:      #checks if username is empty
            CTkMessagebox(title="Error", message="Invalid username", icon="cancel")    
        elif check_name not in usernames_with_previews: ###change to DB
            CTkMessagebox(title="Error", message="Username not found!", icon="cancel")
        else:
            pass ###choice window to continue or go back

    # UI Components 

    #  Header 
    header_label = ctk.CTkLabel(intro_gui_frame, text="Career Guidance Quiz",
                                font=font_styles["heading intro"], corner_radius=15,
                                text_color=color_palette["heading text intro"], fg_color=color_palette["heading bg intro"])      
    header_label.pack(pady=(20, 10))    # tuple to pad from top and bottom

    # Image

    try:
        intro_image = ctk.CTkImage(dark_image=Image.open('intro image.png'), size=(600, 600))
        intro_image_label = ctk.CTkLabel(image_frame, text="", image=intro_image)   #label to hold image
    except:
        intro_image_label = ctk.CTkLabel(image_frame, text="[🤖]", font=("Helvetica", 24))#incase image not found
    intro_image_label.pack(expand=True, fill="both")
    
    # Instructions

    inst_text = (
        "WELCOME TO YOUR FUTURE\n\n"
        "1. Choose from three specialized career quizzes.\n"
        "2. Add a 'career preview' to compare your thoughts with our results.\n"
        "3. Answer truthfully—there are no wrong answers!\n"
        "4. You can always come back and try different quizzes later."
    )
    instructions_box = ctk.CTkTextbox(intro_gui_frame, width=700, height=185, 
                                      font=font_styles["instructions intro"], corner_radius=20, 
                                      text_color=color_palette["instructions text intro"], fg_color=color_palette["instructions fg intro"], 
                                      border_color=color_palette["border intro"], border_width=3)
    instructions_box.insert("0.0", inst_text)           # inserts text into textbox
    instructions_box.configure(state="disabled")        # configures it so it can't be changed
    instructions_box.pack(pady=5, anchor="w")


    # Input Section (Using a Frame for better grouping)
    input_frame = ctk.CTkFrame(intro_gui_frame, fg_color="transparent")
    input_frame.pack(pady=20, anchor="w")


    ctk.CTkLabel(input_frame, text="Username",      #username text
                 font=font_styles["labels intro"], corner_radius=15, 
                 text_color=color_palette["labels text intro"], fg_color=color_palette["labels fg intro"]).grid(row=0, column=0, sticky="w", pady=5)
    name_entry = ctk.CTkEntry(input_frame, textvariable=name_var,           #username entry
                              width=300 , font=font_styles["entry intro"],
                              fg_color=color_palette["entry fg intro"], text_color=color_palette["entry text intro"])
    name_entry.grid(row=1, column=0, sticky="w", pady=5, padx=(10, 5))


    btn_clear_name = ctk.CTkButton(input_frame, text="Clear", width=80, 
                                   fg_color=color_palette["clear button fg intro"],hover_color=color_palette["clear button hover color intro"],
                                   text_color=color_palette["clear button text intro"], border_width=1,
                                   command=lambda:name_entry.delete(0, "end"))
    btn_clear_name.grid(row=1, column=1, sticky="w", pady=5)

    ctk.CTkLabel(input_frame, text="User Already registered? click here", 
                 font=("Arial",15), corner_radius=15, 
                 text_color=color_palette["labels text intro"], fg_color=color_palette["labels fg intro"]).grid(row=2, column=0, sticky="w",padx=(25,5), pady=5)
    
    check_button = ctk.CTkButton(input_frame, text="Enter", 
                               width=80, height=15,
                               fg_color="#2fa572", hover_color="#106a43",
                               command=check_username)
    check_button.grid(row=2, column =1, sticky="w", pady=5)

    # Career Preview Section
    ctk.CTkLabel(input_frame, text="Career Preview (Optional)", 
                 font=font_styles["labels intro"],
                 text_color=color_palette["labels text intro"],
                 fg_color=color_palette["labels fg intro"]).grid(row=3, column=0, sticky="w", pady=2)
    
    preview_textbox = ctk.CTkTextbox(input_frame, height=100,  font=font_styles["entry intro"],
                                     text_color=color_palette["entry text intro"], fg_color=color_palette["entry fg intro"], 
                                     border_color=color_palette["border intro"],border_width=3)
    preview_textbox.grid(row=4, column=0, columnspan=2, pady=2, sticky="nsew") #sticky nsew expands all directions


    btn_clear_preview = ctk.CTkButton(input_frame, text="Clear Preview", width=100,
                                      fg_color=color_palette["clear button fg intro"], hover_color=color_palette["clear button hover color intro"],
                                      text_color=color_palette["clear button text intro"],
                                        border_width=1,
                                      command=lambda:preview_textbox.delete("1.0", "end"))
    btn_clear_preview.grid(row=5, column=0, sticky="w", pady=2)

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


def quiz_window():
    # Window initialising and formatting
    quiz_gui = ctk.CTk()
    quiz_gui.title("Career Compass")
    quiz_gui.geometry("1000x1000") 
    ctk.set_appearance_mode("dark")
    quiz_gui.after(0, lambda: quiz_gui.state('zoomed'))

    # Main Background Frame
    quiz_gui_frame = ctk.CTkFrame(quiz_gui, fg_color=color_palette["frame fg"])
    quiz_gui_frame.pack(fill="both", expand=True)

    def personality_quiz():
        quiz_gui.withdraw()

        personality_gui = ctk.CTk()
        personality_gui.title("Career Compass")
        personality_gui.geometry("700x600")
        ctk.set_appearance_mode("dark")
        personality_gui.after(0, lambda: personality_gui.state('zoomed'))
        personality_gui.grid_columnconfigure(0, weight=1) 

        personality_gui_frame = ctk.CTkScrollableFrame(personality_gui, fg_color=color_palette["frame fg"])
        personality_gui_frame.pack(fill="both", expand=True)
        personality_gui_frame.grid_columnconfigure(0, weight=1)

        def on_close_shortcut():        # function to close the program and return
            personality_gui.destroy()
            quiz_gui.deiconify()

        personality_gui.protocol("WM_DELETE_WINDOW", on_close_shortcut)
    
        def submit_answers():
            # Check if question has been answered
            unanswered=[]
            for i, var in enumerate(linking_list): #enumerate gives index and variable at a time 
                if var.get() ==-1: #not answered
                    unanswered.append("Q"+str(i+1)) #notes the Q no
            if unanswered:      #checks if list is empty
                CTkMessagebox(title="Question(s) unanswered", message="Please answer the question(s)"+str(unanswered).strip("[]") , icon="warning")
                return #function exit

            # question and answer dictionary
            questions_and_answers = {
                questions[j]: linking_list[j].get()
                for j in range(20)
            }
        ###store answers in db

            personality_gui.destroy()    


        linking_list = [ctk.IntVar(value=-1) for _ in range(20)]
        personality_q= DB()
        q_and_o=personality_q.get_qo_personality()      # tuples of questions
        questions=q_and_o[0]
        options=q_and_o[1]
        

        #  Instructions (row 0) 
        instructions = ctk.CTkLabel(
            personality_gui_frame,
            text="Answer each question accurately based of your preferences.\nif nothing matches choose a option that resembles you closely",
            font=font_styles["instructions p"],
            text_color=color_palette["heading 3"]
        )
        instructions.grid(row=0, column=0, columnspan=7, padx=10, pady=(10, 0), sticky="w")

        for q in range(20):
            question_block=ctk.CTkFrame(personality_gui_frame, 
                                        fg_color="transparent")
            question_block.grid(row=q+1, column=0, padx=15, pady=15, sticky="ew")

            question_block.grid_columnconfigure(0, weight=1)
            question_block.grid_columnconfigure(1, weight=1)

            question_label = ctk.CTkLabel(
                question_block,
                text= "Q"+str(q+1)+")  "+questions[q], #accesses questions from index 0
                font=font_styles["questions p"],
                justify="left",
                wraplength=900,
                text_color=color_palette["question 3"]
                )
            question_label.grid(row=0, column=0, columnspan=4, padx=5, pady=(0, 8), sticky="w")
                
            personality_gui_frame.grid_columnconfigure(0, weight=1)
            
            

            for button_value in range(1, 5):
                row_pos = (button_value - 1) // 2   # 0 or 1  → row 1 or row 2
                col_pos = (button_value - 1) % 2    # 0 or 1  → left or right column
                radio_button = ctk.CTkRadioButton(
                question_block,
                text=options[q][button_value-1]+".",                          
                variable=linking_list[q],
                value=button_value,
                width=400,
                radiobutton_height=font_styles["button size"][0],
                radiobutton_width=font_styles["button size"][1],
                border_width_checked=font_styles["button size"][2],
                hover_color=color_palette["button hover 3"],
                fg_color=color_palette["selected button color 3"],
                border_color=color_palette["unselected button color 3"],
                text_color=color_palette["options color"],
                font=font_styles["options p"],
                        )
            
                radio_button.grid(row=row_pos + 1, column=col_pos, padx=(15, 5), pady=5, sticky="w")

        submit_btn = ctk.CTkButton(
            personality_gui_frame,
            text="Submit",
            width=200,
            height=40,
            fg_color="#2fa572",
            hover_color="#106a43",
            command=submit_answers,
            )
        submit_btn.grid(row=21, column=0, pady=(25, 35))

        personality_gui.mainloop()





    def skills_quiz():
        quiz_gui.withdraw() # keeps the quiz window hidden

        skills_gui = ctk.CTk()
        skills_gui.title("Career Compass")
        skills_gui.geometry("700x600")
        ctk.set_appearance_mode("dark")
        skills_gui.after(0, lambda: skills_gui.state('zoomed'))

        skills_gui_frame = ctk.CTkScrollableFrame(skills_gui, fg_color=color_palette["frame fg"])
        skills_gui_frame.pack(fill="both", expand=True)

        # coloumn weights
        skills_gui_frame.columnconfigure(0, weight=2, minsize=500)   #for questions 
        for col in range(1, 7):          
            skills_gui_frame.columnconfigure(col, weight=1)          #for buttons

        def on_close_shortcut():        # function to close the program and return
            skills_gui.destroy()
            quiz_gui.deiconify()

        skills_gui.protocol("WM_DELETE_WINDOW", on_close_shortcut)

        #button list and question access
        linking_list = [ctk.IntVar(value=-1) for _ in range(20)]    #creates 20 variables for buttons
        total_questions = DB()
        questions = total_questions.get_q()


        def submit_answers():
            # Check if question has been answered
            unanswered=[]
            for i, var in enumerate(linking_list): #enumerate gives index and variable at a time 
                if var.get() ==-1: #not answered
                    unanswered.append("Q"+str(i+1)) #notes the Q no
            if unanswered:      #checks if list is empty
                CTkMessagebox(title="Question(s) unanswered", message="Please answer the question(s)"+str(unanswered).strip("[]") , icon="warning")
                return #function exit

            # question and answer dictionary
            questions_and_answers = {
                questions[j + 20]: linking_list[j].get()
                for j in range(20)
            }
        ###store answers in db

            skills_gui.destroy()
            

        #  Instructions (row 0) 
        instructions = ctk.CTkLabel(
            skills_gui_frame,
            text="Answer each question by rating from 1 (Strongly Disagree) to 5 (Strongly Agree).",
            font=font_styles["instructions"],
            text_color=color_palette["heading 2"]
        )
        instructions.grid(row=0, column=0, columnspan=7, padx=10, pady=(10, 0), sticky="w")

        # Column headers for 1-5 (row 1)
        for val in range(1, 6):
            header = ctk.CTkLabel(skills_gui_frame, text=str(val), font=font_styles["number headers"], text_color=color_palette["heading 2"])
            header.grid(row=1, column=val, padx=(5,110), pady=(6, 0), sticky="n")

        # Questions + radio buttons (rows 2-21) 
        for q in range(20):
            question_label = ctk.CTkLabel(
                skills_gui_frame,
                text= "Q"+str(q+1)+")  "+questions[q], #accesses questions from index 0
                font=font_styles["questions"],
                justify="left",
                anchor="w",
                text_color=color_palette["question 2"]
            )
            question_label.grid(row=q + 2, column=0, padx=(5, 5), pady=(12, 4), sticky="w")

            for button_value in range(1, 6):
                radio_button = ctk.CTkRadioButton(
                    skills_gui_frame,
                    text="",                          # header already created
                    variable=linking_list[q],
                    value=button_value,
                    width=30,
                    radiobutton_height=font_styles["button size"][0],
                    radiobutton_width=font_styles["button size"][1],
                    border_width_checked=font_styles["button size"][2],
                    hover_color=color_palette["button hover 2"],
                    fg_color=color_palette["selected button color 2"],
                    border_color=color_palette["unselected button color 2"]
                )
                radio_button.grid(row=q + 2, column=button_value, padx=(5,100), pady=(6, 4), sticky="n")


        # Submit button (row 22)
        submit_btn = ctk.CTkButton(
            skills_gui_frame,
            text="Submit",
            width=200,
            height=40,
            fg_color="#2fa572",
            hover_color="#106a43",
            command=submit_answers,
        )
        submit_btn.grid(row=23, column=0, columnspan=7, pady=(10, 15))

        skills_gui.mainloop()

    def interests_quiz():

        quiz_gui.withdraw() # keeps the quiz window hidden

        interests_gui = ctk.CTk()
        interests_gui.title("Career Compass")
        interests_gui.geometry("700x600")
        ctk.set_appearance_mode("dark")
        interests_gui.after(0, lambda: interests_gui.state('zoomed'))

        interests_gui_frame = ctk.CTkScrollableFrame(interests_gui, fg_color=color_palette["frame fg"])
        interests_gui_frame.pack(fill="both", expand=True)

        # coloumn weights
        interests_gui_frame.columnconfigure(0, weight=2, minsize=500)   #for questions 
        for col in range(1, 7):          
            interests_gui_frame.columnconfigure(col, weight=1)          #for buttons

        def on_close_shortcut():        # function to close the program and return
            interests_gui.destroy()
            quiz_gui.deiconify()

        interests_gui.protocol("WM_DELETE_WINDOW", on_close_shortcut)

        #button list and question access
        linking_list = [ctk.IntVar(value=-1) for _ in range(20)]    #creates 20 variables for buttons
        total_questions = DB()
        questions = total_questions.get_q()


        def submit_answers():
            # Check if question has been answered
            unanswered=[]
            for i, var in enumerate(linking_list): #enumerate gives index and variable at a time 
                if var.get() ==-1: #not answered
                    unanswered.append("Q"+str(i+1)) #notes the Q no
            if unanswered:      #checks if list is empty
                CTkMessagebox(title="Question(s) unanswered", message="Please answer the question(s)"+str(unanswered).strip("[]") , icon="warning")
                return #function exit

            # question and answer dictionary
            questions_and_answers = {
                questions[i + 20]: linking_list[i].get()
                for i in range(20)
            }
        ###store answers in db

            interests_gui.destroy()
            

        #  Instructions (row 0) 
        instructions = ctk.CTkLabel(
            interests_gui_frame,
            text="Answer each question by rating from 1 (Strongly Disagree) to 5 (Strongly Agree).",
            font=font_styles["instructions"],
            text_color=color_palette["heading 1"]
        )
        instructions.grid(row=0, column=0, columnspan=7, padx=10, pady=(10, 0), sticky="w")

        # Column headers for 1-5 (row 1)
        for val in range(1, 6):
            header = ctk.CTkLabel(interests_gui_frame, text=str(val), font=font_styles["number headers"], text_color=color_palette["heading 1"])
            header.grid(row=1, column=val, padx=(5,110), pady=(6, 0), sticky="n")

        # Questions + radio buttons (rows 2-21) 
        for q in range(20):
            question_label = ctk.CTkLabel(
                interests_gui_frame,
                text= "Q"+str(q+1)+")  "+questions[q+20], #accesses questions from index 21
                font=font_styles["questions"],
                justify="left",
                anchor="w",
                text_color=color_palette["question 1"]
            )
            question_label.grid(row=q + 2, column=0, padx=(5, 5), pady=(12, 4), sticky="w")

            for button_value in range(1, 6):
                radio_button = ctk.CTkRadioButton(
                    interests_gui_frame,
                    text="",                          # header already created
                    variable=linking_list[q],
                    value=button_value,
                    width=30,
                    radiobutton_height=font_styles["button size"][0],
                    radiobutton_width=font_styles["button size"][1],
                    border_width_checked=font_styles["button size"][2],
                    hover_color=color_palette["button hover 1"],
                    fg_color=color_palette["selected button color 1"],
                    border_color=color_palette["unselected button color 1"]
                )
                radio_button.grid(row=q + 2, column=button_value, padx=(5,100), pady=(6, 4), sticky="n")


        # Submit button (row 22)
        submit_btn = ctk.CTkButton(
            interests_gui_frame,
            text="Submit",
            width=200,
            height=40,
            fg_color="#2fa572",
            hover_color="#106a43",
            command=submit_answers,
        )
        submit_btn.grid(row=23, column=0, columnspan=7, pady=(10, 15))

        interests_gui.mainloop()


    # Header 
    heading_label = ctk.CTkLabel(
        quiz_gui_frame, 
        text="Let the compass point to your future",
        font=font_styles["quiz window heading"], 
        text_color=color_palette["heading quiz text"],
        fg_color=color_palette["heading quiz fg"]
    )
    heading_label.pack(pady=(40, 20))

    # Container for the 3 Quiz Cards 
    cards_container = ctk.CTkFrame(quiz_gui_frame, fg_color="transparent")
    cards_container.pack(fill="both", expand=True, padx=30, pady=(10, 40))

    # INTERESTS QUIZ CARD
    interests_quiz_frame = ctk.CTkFrame(cards_container, fg_color=color_palette["interests card"], corner_radius=15)
    interests_quiz_frame.pack(side="left", fill="both", expand=True, padx=15)

    interests_quiz_header = ctk.CTkLabel(interests_quiz_frame, text="Interests Quiz", text_color=color_palette["interests head"], font=font_styles["quiz heading"])
    interests_quiz_header.pack(pady=(25, 10))

    try:
        interests_quiz_image = ctk.CTkImage(dark_image=Image.open('icons for quiz/interests quiz icon.png'), size=(100, 100))
        interests_quiz_image_label = ctk.CTkLabel(interests_quiz_frame, text="", image=interests_quiz_image)
    except:
        interests_quiz_image_label = ctk.CTkLabel(interests_quiz_frame, text="[🎨]", font=("Helvetica", 24))
    interests_quiz_image_label.pack(pady=10)

    interests_quiz_instructions = ctk.CTkLabel(
        interests_quiz_frame, 
        text_color=color_palette["interests instructions"], 
        font=font_styles["quiz instructions"],
        justify="center",
        text=
''' What do you live to Do?

This quick 20-question quiz 
dives past your current skillset
to discover your genuine passions.

Click here and Rate the interests 1 to 5
to reveal a deeply fulfilling and
rewarding career path you’ll
actually love waking up to every day!
'''
    )
    interests_quiz_instructions.pack(pady=15, fill="x")

    interests_quiz_button = ctk.CTkButton(
        interests_quiz_frame, text="Start Quiz",
        fg_color=color_palette["interests btn fg"], text_color=color_palette["quiz button text"], 
        font=font_styles["quiz button"], hover_color=color_palette["interests btn hover"], height=35, corner_radius=8,
        command=interests_quiz
    )
    interests_quiz_button.pack(side="bottom", pady=25, padx=20, fill="x")


    #  PERSONALITY QUIZ CARD 
    personality_quiz_frame = ctk.CTkFrame(cards_container, fg_color=color_palette["personality card"], corner_radius=15)
    personality_quiz_frame.pack(side="left", fill="both", expand=True, padx=15)

    personality_quiz_header = ctk.CTkLabel(personality_quiz_frame, text="Personality Quiz", text_color=color_palette["personality head"], font=font_styles["quiz heading"])
    personality_quiz_header.pack(pady=(25, 10))

    extra_note=ctk.CTkLabel(personality_quiz_frame,text="(RECOMMENDED)", text_color="#F50D0D", font=("Arial",15))
    extra_note.pack()

    try:
        personality_quiz_image = ctk.CTkImage(dark_image=Image.open('icons for quiz/personality icon.png'), size=(100, 100))
        personality_quiz_image_label = ctk.CTkLabel(personality_quiz_frame, text="", image=personality_quiz_image)
    except Exception:
        personality_quiz_image_label = ctk.CTkLabel(personality_quiz_frame, text="[🧠]", font=("Helvetica", 24))
    personality_quiz_image_label.pack(pady=10)

    personality_quiz_instructions = ctk.CTkLabel(
        personality_quiz_frame,  
        text_color="#A0A0A0", 
        font=font_styles["quiz instructions"],
        justify="center",
        text=
'''Discover how your unique 
nature shapes your future!

20-question quiz that uses
real-world scenarios to analyze
your natural instincts, decision
making style, and social traits.
           
Click here to find the ideal workplace
environments and careers for you.''',
    )
    personality_quiz_instructions.pack(pady=15, fill="x")

    personality_quiz_button = ctk.CTkButton(
        personality_quiz_frame, text="Start Quiz",
        fg_color=color_palette["personality btn fg"], text_color=color_palette["quiz button text"], 
        font=font_styles["quiz button"], hover_color=color_palette["personality btn hover"], height=35, corner_radius=8,
        command=personality_quiz
    )
    personality_quiz_button.pack(side="bottom", pady=25, padx=20, fill="x")


    #  SKILLS QUIZ CARD 
    skills_quiz_frame = ctk.CTkFrame(cards_container, fg_color=color_palette["skills card"], corner_radius=15)
    skills_quiz_frame.pack(side="left", fill="both", expand=True, padx=15)

    skills_quiz_header = ctk.CTkLabel(skills_quiz_frame, text="Skills Quiz", text_color=color_palette["skills head"], font=font_styles["quiz heading"])
    skills_quiz_header.pack(pady=(25, 10))

    try:
        skills_quiz_image = ctk.CTkImage(dark_image=Image.open("icons for quiz/skills quiz icon.png"), size=(100, 100))
        skills_quiz_image_label = ctk.CTkLabel(skills_quiz_frame, text="", image=skills_quiz_image)
    except:
        skills_quiz_image_label = ctk.CTkLabel(skills_quiz_frame, text="[🛠️]", font=("Helvetica", 24))
    skills_quiz_image_label.pack(pady=10)

    skills_quiz_instructions = ctk.CTkLabel(
        skills_quiz_frame, 
        text_color="#A0A0A0", 
        font=font_styles["quiz instructions"],
        justify="center",
        text=
'''
Ready to find a career 
you will excel in?

20-question quiz to evaluate
your core strengths from technical 
logic to unmatched creation.

Click here and Simply rate your 
confidence in various skills
from 1 to 5 to find out.''', 
    )
    skills_quiz_instructions.pack(pady=15, fill="x")

    skills_quiz_button = ctk.CTkButton(
        skills_quiz_frame, text="Start Quiz",
        fg_color=color_palette["skills btn fg"], text_color=color_palette["quiz button text"], 
        font=font_styles["quiz button"], hover_color=color_palette["skills btn hover"], height=35, corner_radius=8,
        command=skills_quiz
    )
    skills_quiz_button.pack(side="bottom", pady=25, padx=20, fill="x")

    quiz_gui.mainloop()

quiz_window()
