from google import genai
import mysql.connector as mcon

class GUI:
    pass


class DB:
    def __init__(self):
        # info about host, user, database
        db = mcon.connect(
            host = "localhost",
            user = "root",
            passwd = "ilikemysql",
            database = "pythonproject"
        )

        self.mycursor = db.cursor()     # mycursor is used execute read and write queries
    
    # retrieves questions from database
    def get_q(self):
        self.mycursor.execute("SELECT question FROM questions")    # each question comes in the form of a single-element tuple
        
        # creating list to contain all questions
        q_list = []
        for qt in self.mycursor:
            q_list.append(qt[0])
        
        # returning list of questions for further processing
        return q_list
    
    # stores user info and answers (in the form of string) in database
    def store_ans(self, data_list):
        self.data_list = data_list      # data_list should contain 21 elements, 1 name and 20 answers
        
        # placeholders and columns generator
        placeholders = ", ".join(["%s"] * 21)
        columns = "user_name, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20"

        sql_query = f"INSERT INTO answers ({columns}) VALUES ({placeholders})"
        self.mycursor.execute(sql_query, data_list)


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
#                 "i am very honest": 5, 
#                 "i like cars": 2, 
#                 "i am very social": 3})

# my_object.pass_ai_data()
# answer = my_object.pass_result()
# print(answer)