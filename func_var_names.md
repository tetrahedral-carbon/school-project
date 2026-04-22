# functions and variables data
store all functions & variables and their uses

# functions & methods
give_ai_data() --> gives the ai model the data dictionary to generate response

pass_result() --> shares the response of the ai model for further processing

get_q() --> retrieves questions from db

store_ans() --> stores user info and asnwers in db


# variables
info_dict --> stores all the questions and answers given by user in the form of a dictionary

response --> temporary response holder

ai_result --> stores the result given by the ai model

db --> database variable

mycursor --> cursor object for db

q_list --> list of questions

data_list --> list of data to be stored in db

placeholders --> stores placeholders for query

columns --> stores column names for query

sql_query --> contains sql query to store data in db