#modules imported
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox  #customtkinter doesnt have a messagebox
from google import genai
import mysql.connector as mcon


#intialising of variables used multiple times
h,w=60,50
button_design=("Arial",20,"bold")
entry_design=("Arial",25,"italic")

#user reference material default values
preview_text=""     
usernames_with_previews={"hi":"games"}              
submit=False                            


#intro window function
def intro_window(): 
    intro_gui=ctk.CTk()                     
    
    name=ctk.StringVar(master=intro_gui)     #name variable for entry
    
    
    #intro button functions
    def submit_details():
        global submit

        #test to check if name is non empty
        
        if bool(name.get()) == False:                      
             CTkMessagebox(title="username not entered",message="Enter a Valid username")

        #test to check if username is already available
        elif name.get() in usernames_with_previews:     
            CTkMessagebox(title="username not available",message="Username already in use,Enter a new one")
            name_entry.delete(0,"end")                   
        
        #executes if all tests work
        else:
            submit=True
            user_name=name.get()
            preview_text=preveiw_textbox.get("0.0","end")
            usernames_with_previews[user_name]=preview_text 
            intro_gui.destroy()
    
    #button functions is delete text easily
    def delete_name():
         name_entry.delete("0","end")
         
     
    def delete_preview():
         preveiw_textbox.delete("0.0","end")      

    def quit_window():
        intro_gui.destroy()




    #intro window formatting
    intro_gui.title("Career Suggestion quiz program")
    intro_gui.geometry("500x500")
    intro_gui._set_appearance_mode("dark")


    #intstruction widgets
    instructions_textbox=ctk.CTkTextbox(master=intro_gui,font=("Arial",30,"bold"),height=350,width=1090)
    
    info_list=["Hi welcome to our career guidance quiz\n\n",
               "LETS GO OVER HOW THIS WORKS:\n",
               "1)you get an option to choose one of our three quizzes\n",
               "which we have designed to predict an career appropriate for you\n\n",
               
               "2)you can also add a preveiw on what career you think you would do in\n", 
               "the textbox below\n\n",
               
               "3)answer truthfully it will allow us to predict an appropriate\n",
                "career without inaccuracies,remember there are no wrong answers\n\n",
               
                "4)dont worry you come back to see the other quizzes later\n"]
    
    text_inserter=ctk.StringVar(master=intro_gui)   #placeholder to insert text into text box
    for text in info_list[::-1]:                    #list in reverse so text starts being added from top
        text_inserter.set(text)               
        instructions_textbox.insert("0.0",text_inserter.get())      #adds text to textbox
    else:
         instructions_textbox.configure(state="disabled")   #disables textbox so it cant be altered


    #name related widgets
    name_label=ctk.CTkLabel(master=intro_gui,
                            text="Enter your name to get started",
                            font=button_design
                            ) 
    name_entry=ctk.CTkEntry(master=intro_gui,
                            font=entry_design,
                            textvariable=name,
                            )
    name_delete=ctk.CTkButton(master=intro_gui,font=button_design,text="delete name",command=delete_name)

    #preveiw related widgets
    preveiw_instructions=ctk.CTkLabel(master=intro_gui,font=entry_design,text="enter a preview of the career you think you would take (optional) \n you can comapare it with the quiz result")
    preveiw_textbox=ctk.CTkTextbox(master=intro_gui)
    preview_delete=ctk.CTkButton(master=intro_gui,font=button_design,text="delete Preveiw",command=delete_preview)

    #submit and quit window buttons
    submit_button=ctk.CTkButton(master=intro_gui,
                                text="Submit",
                                command=submit_details,
                                font=button_design
                            )
    quit_button=ctk.CTkButton(master=intro_gui,
                                text="quit",
                                command=quit_window,
                                font=button_design
                                )
    
    
    
    
                                   
                                   
         
    
    #widgets display
    instructions_textbox.pack()
    
    name_label.pack()
    name_entry.pack()
    name_delete.pack()
    
    preveiw_instructions.pack()
    preveiw_textbox.pack()    
    preview_delete.pack()
    
    submit_button.pack()
    quit_button.pack()

    #intro window display
    intro_gui.mainloop()





#main window function
def quiz_window():
    
    #intialising the main window
    quiz_gui=ctk.CTk()

    #quiz button functions
    def personality_quiz():
        pass
    def interests_quiz():
            pass
    def skills_quiz():
        pass

        
    #quiz window formatting 
    quiz_gui.title("Career Suggestive Quizzes")
    quiz_gui.geometry("500x500")
    quiz_gui._set_appearance_mode("dark")


    #frame widget to place buttons
    quiz_gui.frame=ctk.CTkFrame(master=quiz_gui)





    #starting quiz buttons
    quiz_gui.personality_button=ctk.CTkButton(master=quiz_gui.frame,
                                                text="Personality quiz (with AI)",
                                                height=h,
                                                width=w,
                                                command=personality_quiz
                                                )
    quiz_gui.interests_button=ctk.CTkButton(master=quiz_gui.frame,
                                                
                                                text="interests quiz",
                                                height=h,
                                                width=w,
                                                command=interests_quiz
                                                )
    quiz_gui.skills_button=ctk.CTkButton(master=quiz_gui.frame,
                                                
                                                text="skills quiz ",
                                                height=h,
                                                width=w,
                                                command=skills_quiz
                                                )


    #widgets display
    quiz_gui.personality_button.pack()
    quiz_gui.interests_button.pack()
    quiz_gui.skills_button.pack()
    quiz_gui.frame.pack()

    #quiz window display
    quiz_gui.mainloop()

# call of intro window
intro_window()

if submit==True:
    quiz_window()




class DB:
    def __init__(self):
        # info about host, user, database
        self.db = mcon.connect(
            host = "database-1.c09cucuk2ssf.us-east-1.rds.amazonaws.com",
            user = "admin",
            passwd = "aws123services!456",
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
        
        for qt in self.mycursor:
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
    

# sample usage of AI class
# my_object = AI({"initial": "this dictionary contains a set of questions and answers on a scale of 1 to 5 (1-strongly disagree, 5-strongly agree). recommend me 3 suitable career options", 
#                  "i am very honest": 5, 
#                  "i like cars": 2, 
#                  "i am very social": 3})

# my_object.pass_ai_data()
# answer = my_object.pass_result()
# print(answer)
