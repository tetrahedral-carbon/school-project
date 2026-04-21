#modules imported
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox  #customtkinter doesnt have a messagebox

#intialising of variables used multiple times
h,w=60,50



#intro window function
def intro_window():
    global submit
    #intro window initialising
    intro_gui=ctk.CTk()
    #name variable for entry
    name=ctk.StringVar(master=intro_gui)

    #list of usernames for reference later
    list_of_usernames=[]

    #default submit value
    submit=False
    
    #intro button functions 
    
    def quit_window():
        #needed for calling functions
        global submit
        submit=False
        intro_gui.destroy()
    
    def submit_details():
        global submit
        submit=True
        if name.get() not in list_of_usernames:
                user_name=name.get()
                list_of_usernames.append(user_name)
        else:
            CTkMessagebox(title="username not available",
                           message="Username already in use,Enter a new one")
            name_entry.delete(0,"END")#deletes the invalid name
        intro_gui.destroy()


    #intro window formatting
    intro_gui.title("Career Suggestion quiz program")
    intro_gui.geometry("500x500")
    intro_gui._set_appearance_mode("dark")

    #intro window widgets
    name_label=ctk.CTkLabel(master=intro_gui,
                            text="Enter your name"
                            ) 
    name_entry=ctk.CTkEntry(master=intro_gui,
                            font=("Arial",20,"bold"),
                            textvariable=name
                            )
    submit_button=ctk.CTkButton(master=intro_gui,
                                text="Submit",
                                command=submit_details
                            )
    quit_button=ctk.CTkButton(master=intro_gui,
                                text="quit",
                                command=quit
                                )

    #widgets display
    
    name_label.pack()
    name_entry.pack()
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
    #first call of quiz window
    quiz_window()

class DB:
    pass

class AI:
    def __init__(self, info_dict):
        self.info_dict = info_dict      # stores the dictionary of user's answers
        self.ai_result = None           # stores the output of the ai model
    
    # gives ai model the user's answers and gets the output
    def give_ai_data(self):
        from google import genai
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
#                 "i am very honest": 5, 
#                 "i like cars": 2, 
#                 "i am very social": 3})

# my_object.pass_ai_data()
# answer = my_object.pass_result()
# print(answer)
