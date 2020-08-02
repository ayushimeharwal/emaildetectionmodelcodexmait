import streamlit as st
import pandas as pd
import pickle
import numpy as np
from PIL import Image
import string
df1=pd.read_csv('stopwords')
b=[]
def func(df1):
    for i in df1['words']:
        b.append(i)
func(df1)
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
import hashlib
def text_process(mess):
    nopunc = [char for char in mess if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in b]
model=pickle.load(open('model.pkl','rb'))
model1=pickle.load(open('model1.pkl','rb'))
#model1=pickle.load(open('model1.pkl','rb'))
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def create_spamtable():
    c.execute('CREATE TABLE IF NOT EXISTS spamtable(username TEXT,spam INTEGER)')
def create_hamtable():
    c.execute('CREATE TABLE IF NOT EXISTS hamtable(username TEXT,message TEXT,ham INTEGER)')
def add_spamdata(username,spam):
	c.execute('INSERT INTO spamtable(username,spam) VALUES (?,?)',(username,spam))
	conn.commit()
def add_hamdata(username,message,ham):
	c.execute('INSERT INTO hamtable(username,message,ham) VALUES (?,?,?)',(username,message,ham))
	conn.commit()
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def view_all_spam():
	c.execute('SELECT * FROM spamtable')
	data = c.fetchall()
	return data
def view_all_ham():
	c.execute('SELECT * FROM hamtable')
	data = c.fetchall()
	return data
def main():
    st.title("Built By CodeX MAIT")
    status = st.sidebar.radio("Know About Our Model's", ("Model 1", "Model 2"))
    if status == 'Model 2':
        st.sidebar.success('Model 2 Is Made By using Support Vector Machines And Has Testing Accuracy of 0.932')
    if status == 'Model 1':
        st.sidebar.info('Model 1 Is Made By using Naive Bayes classifier And Has Testing Accuracy of 0.978')
    html_temp = """
               <div style="background-color:#025246 ;padding:10px">
               <h1 style="color:white;text-align:center;">EMAIL DETECTION MODEL</h1>
               </div>
               """
    st.markdown(html_temp, unsafe_allow_html=True)
    img = Image.open("bg2.png")
    st.image(img, width=697)
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.info("This Is a Email Detection Model Used to Detect Whether A Mail Recieved By The User Is Spam Or Ham.")
        st.success("You Need To Sign Up to Access The Model")
    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task", ["Detect Your Mail","Analytics of Ham Mails", "Analytics of Spam Mails", "Profiles"])
                if task=="Detect Your Mail":
                    st.subheader("detect")
                    st.markdown("Fill Your Information Here")
                    message = st.text_input("Add Your Mail Here to check")
                    f = open('demofile3.txt', "w")
                    f.write(message)
                    f.close()
                    create_spamtable()
                    create_hamtable()
                    st.warning('Click Here To Check Your Results')

                    safe_html = """  
                                 <div style="background-color:#F4D03F;padding:10px >
                                  <h2 style="color:white;text-align:center;"> Hey,this is a ham Email Don't Delete It</h2>
                                  </div>
                               """
                    danger_html = """  
                                 <div style="background-color:#F08080;padding:10px >
                                  <h2 style="color:red ;text-align:center;"> Hey ,this is a spam Email Delete It</h2>
                                  </div>
                               """

                    if st.button("Model 1"):
                        output = model.predict(open('demofile3.txt', "r"))[0]
                        # output=predict_cancer_svm(message)
                        st.success('')
                        spam=6
                        ham=0
                        add_spamdata(username, spam)


                        if output == 1:
                            st.markdown(danger_html, unsafe_allow_html=True)
                            spam = spam + 1
                            add_spamdata(username, spam)
                        else:
                            st.markdown(safe_html, unsafe_allow_html=True)
                            ham=ham+1
                            add_hamdata(username,message,ham)
                            st.balloons()
                    if st.button("Model 2"):
                        output = model1.predict(open('demofile3.txt', "r"))[0]
                        # output=predict_cancer_svm(message)
                        st.success('')
                        if output == 1:
                            st.markdown(danger_html, unsafe_allow_html=True)

                        else:
                            st.markdown(safe_html, unsafe_allow_html=True)
                            st.balloons()
                elif task=="Analytics of Ham Mails":
                    st.subheader("Analytics")
                    spam = view_all_ham()
                    clean = pd.DataFrame(spam, columns=["Username", "message","ham"])
                    st.dataframe(clean)
                elif task == "Analytics of Spam Mails":
                    st.subheader("Analytics")
                    spam=view_all_spam()
                    clean= pd.DataFrame(spam, columns=["Username", "Spam"])
                    st.dataframe(clean)


                elif task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        st.selectbox("Your Gender", ["Male", "Female", "Others"])
        Age=st.text_input("Age")


        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to Login Your Account")
if __name__ == '__main__':
	main()

