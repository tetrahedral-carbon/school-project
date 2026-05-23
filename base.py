#modules imported
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox  #customtkinter doesnt have a messagebox
from google import genai
import mysql.connector as mcon
from PIL import Image
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
            "labels":("Arial",25),
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

font_sizes={ "labels":25, 
            "significant_button":20,
            "insignificant button":10
                }

                

color_palette={
    "frame fg":"#0D0D0D",
    # intro window
    "text color 1":"#EAEAEA",
    "text color 2":"#A0A0A0",
    "border color":"#9B5DE5",
    "fg color 1":"#151515",
    "fg color 2":"#1A1A1A",
    "quiz button select":"green",
    "clear button hover color":"red",
    # quiz window
    "card interests": "#1B2E24",     
    "card personality": "#2B1B3A",    
    "card skills": "#1B2D3A",         
    "btn interests": "#0CB943",       
    "btn personality": "#C148E6",
    "btn skills": "#53DFEC",
    "quiz button select":"green",
    "clear button hover color":"red",
    "card interests": "#1B2E24",     
    "card personality": "#2B1B3A",    
    "card skills": "#1B2D3A",         
    "btn interests": "#0CB943",       
    "btn personality": "#C148E6",
    "btn skills": "#53DFEC",
    #interest quiz
    "heading 1":"dark green",
    "question 1":"green",
    "button hover 1":"green",
    "selected button color 1":"green",
    "button color 1":"light green",
    #skills quiz
    "heading 2":"royal blue",
    "question 2":"blue",
    "button hover 2":"cyan",
    "selected button color 2":"blue",
    "button color 2":"cyan"
    }

border_width=5

def intro_window():
    global user
    # window Initialisation and Formatting

    intro_gui = ctk.CTk()
    intro_gui.title("Career Compass")
    intro_gui.title("Career Compass")
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
            intro_gui.destroy()                                   #destroys the window
            quiz_window()                                              #calls next window

    
    def check_username():
        check_name_input=ctk.CTkInputDialog(title="check Username",text="Enter your registered username") 
        check_name=check_name_input.get_input()

        if check_name==None: # exits function if window closed 
            return
        
        if not check_name:
            CTkMessagebox(title="Error", message="Invalid username", icon="cancel")    
        elif check_name not in usernames_with_previews:
            CTkMessagebox(title="Error", message="Username not found!", icon="warning")
        else:
            pass #choice window

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
                                   fg_color=color_palette["fg color 1"],hover_color=color_palette["clear button hover color"],
                                   text_color=color_palette["text color 1"], border_width=1,
                                   command=lambda:name_entry.delete(0, "end"))
    btn_clear_name.grid(row=1, column=5, pady=(5, 10))

    ctk.CTkLabel(input_frame, text="User Already registered? click here", 
                 font=("Arial",15), corner_radius=15, 
                 text_color=color_palette["text color 1"], fg_color=color_palette["fg color 1"]).grid(row=2, column=4, sticky="w")
    
    check_button = ctk.CTkButton(input_frame, text="Enter", 
                               width=80, height=15,
                               fg_color="#2fa572", hover_color="#106a43",
                               command=check_username)
    check_button.grid(row=2, column=5, sticky="w")

    # Career Preview Section
    ctk.CTkLabel(input_frame, text="Career Preview (Optional)", 
                 font=font_styles["labels"]
                 , text_color=color_palette["text color 1"]).grid(row=3, column=4, sticky="w")
    
    preview_textbox = ctk.CTkTextbox(input_frame, height=100,  font=font_styles["text box"],
                                     text_color=color_palette["text color 2"], fg_color=color_palette["fg color 1"], 
                                     border_color=color_palette["border color"],border_width=3)
    preview_textbox.grid(row=4, column=4, columnspan=2, pady=(5, 10), sticky="nsew")


    btn_clear_preview = ctk.CTkButton(input_frame, text="Clear Preview", width=100,
                                      fg_color=color_palette["fg color 1"], hover_color=color_palette["clear button hover color"],
                                        border_width=1,
                                      command=lambda:preview_textbox.delete("1.0", "end"))
    btn_clear_preview.grid(row=5, column=4, sticky="w")

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

    # Main Background Frame
    quiz_gui_frame = ctk.CTkFrame(quiz_gui, fg_color=color_palette["frame fg"])
    quiz_gui_frame.pack(fill="both", expand=True)

    # Quiz functions placeholder
    def personality_quiz():
        pass
    def skills_quiz():
        quiz_gui.withdraw() # keeps the quiz window hidden

        skills_gui = ctk.CTk()
        skills_gui.title("Career Compass")
        skills_gui.geometry("700x600")
        ctk.set_appearance_mode("dark")

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
                questions[i + 20]: linking_list[i].get()
                for i in range(20)
            }
        ###store answers in db

            skills_gui.destroy()
            

        #  Instructions (row 0) 
        instructions = ctk.CTkLabel(
            skills_gui_frame,
            text="answer each question by rating from 1 (Strongly Disagree) to 5 (Strongly Agree).",
            font=font_styles["labels"],
            text_color=color_palette["heading 2"]
        )
        instructions.grid(row=0, column=0, columnspan=7, padx=10, pady=(10, 0), sticky="w")

        # Column headers for 1-5 (row 1)
        for val in range(1, 6):
            header = ctk.CTkLabel(skills_gui_frame, text=str(val), font=font_styles["labels"], text_color=color_palette["heading 2"])
            header.grid(row=1, column=val, padx=(5,110), pady=(6, 0), sticky="n")

        # Questions + radio buttons (rows 2-21) 
        for q in range(20):
            question_label = ctk.CTkLabel(
                skills_gui_frame,
                text= "Q"+str(q+1)+")  "+questions[q], #accesses questions from index 0
                font=font_styles["labels"],
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
                    hover_color=color_palette["button hover 2"],
                    fg_color=color_palette["selected button color 2"],
                    border_color=color_palette["button color 2"]
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
            text="answer each question by rating from 1 (Strongly Disagree) to 5 (Strongly Agree).",
            font=font_styles["labels"],
            text_color=color_palette["heading 1"]
        )
        instructions.grid(row=0, column=0, columnspan=7, padx=10, pady=(10, 0), sticky="w")

        # Column headers for 1-5 (row 1)
        for val in range(1, 6):
            header = ctk.CTkLabel(interests_gui_frame, text=str(val), font=font_styles["labels"], text_color=color_palette["heading 1"])
            header.grid(row=1, column=val, padx=(5,110), pady=(6, 0), sticky="n")

        # Questions + radio buttons (rows 2-21) 
        for q in range(20):
            question_label = ctk.CTkLabel(
                interests_gui_frame,
                text= "Q"+str(q+1)+")  "+questions[q+20], #accesses questions from index 21
                font=font_styles["labels"],
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
                    hover_color=color_palette["button hover 1"],
                    fg_color=color_palette["selected button color 1"],
                    border_color=color_palette["button color 1"]
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
        font=("Helvetica", 40, "bold"), 
        text_color="#FFFFFF"
    )
    heading_label.pack(pady=(40, 20))

    # Container for the 3 Quiz Cards 
    cards_container = ctk.CTkFrame(quiz_gui_frame, fg_color="transparent")
    cards_container.pack(fill="both", expand=True, padx=30, pady=(10, 40))

    # INTERESTS QUIZ CARD
    interests_quiz_frame = ctk.CTkFrame(cards_container, fg_color=color_palette["card interests"], corner_radius=15)
    interests_quiz_frame.pack(side="left", fill="both", expand=True, padx=15)

    interests_quiz_header = ctk.CTkLabel(interests_quiz_frame, text="Interests Quiz", text_color=color_palette["btn interests"], font=font_styles["quiz header"])
    interests_quiz_header.pack(pady=(25, 10))

    try:
        interests_quiz_image = ctk.CTkImage(dark_image=Image.open('icons for quiz/interests quiz icon.png'), size=(100, 100))
        interests_quiz_image_label = ctk.CTkLabel(interests_quiz_frame, text="", image=interests_quiz_image)
    except:
        interests_quiz_image_label = ctk.CTkLabel(interests_quiz_frame, text="[🎨]", font=("Helvetica", 24))
    interests_quiz_image_label.pack(pady=10)

    interests_quiz_instructions = ctk.CTkLabel(
        interests_quiz_frame, 
        text_color="#A0A0A0", 
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
        fg_color=color_palette["btn interests"], text_color="#121212", 
        font=font_styles["button 1"], hover_color="#0A9636", height=35, corner_radius=8,
        command=interests_quiz
    )
    interests_quiz_button.pack(side="bottom", pady=25, padx=20, fill="x")


    #  PERSONALITY QUIZ CARD 
    personality_quiz_frame = ctk.CTkFrame(cards_container, fg_color=color_palette["card personality"], corner_radius=15)
    personality_quiz_frame.pack(side="left", fill="both", expand=True, padx=15)

    personality_quiz_header = ctk.CTkLabel(personality_quiz_frame, text="Personality Quiz", text_color=color_palette["btn personality"], font=font_styles["quiz header"])
    personality_quiz_header.pack(pady=(25, 10))

    extra_note=ctk.CTkLabel(personality_quiz_frame,text="(RECOMMENDED)", text_color="#F50D0D", font=("Arial",15))
    extra_note.pack()

    try:
        personality_quiz_image = ctk.CTkImage(dark_image=Image.open('icons for quiz/personality icon.png'), size=(100, 100))
        personality_quiz_image_label = ctk.CTkLabel(personality_quiz_frame, text="", image=personality_quiz_image)
    except Exception as e:
        print(e)
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
        fg_color=color_palette["btn personality"], text_color="#121212", 
        font=font_styles["button 1"], hover_color="#A037C0", height=35, corner_radius=8,
        command=personality_quiz
    )
    personality_quiz_button.pack(side="bottom", pady=25, padx=20, fill="x")


    #  SKILLS QUIZ CARD 
    skills_quiz_frame = ctk.CTkFrame(cards_container, fg_color=color_palette["card skills"], corner_radius=15)
    skills_quiz_frame.pack(side="left", fill="both", expand=True, padx=15)

    skills_quiz_header = ctk.CTkLabel(skills_quiz_frame, text="Skills Quiz", text_color=color_palette["btn skills"], font=font_styles["quiz header"])
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
        fg_color=color_palette["btn skills"], text_color="#121212", 
        font=font_styles["button 1"], hover_color="#3CBCC8", height=35, corner_radius=8,
        command=skills_quiz
    )
    skills_quiz_button.pack(side="bottom", pady=25, padx=20, fill="x")

    quiz_gui.mainloop()

quiz_window()
