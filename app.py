
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime,date
import os
import time
import sys
from streamlit_modal import Modal
import time
from streamlit_extras.colored_header import colored_header
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import yfinance as yf


def example():
    colored_header(
        label="Portfolio App",
        description="Shows personal portfolio as Stock, Gold and Foreign Exchange",
        color_name="violet-70",
    )

example()

appdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
conn = sqlite3.connect(os.path.join(appdir, 'stocks1.db'))
cursor = conn.cursor()
opt=st.sidebar.radio("Enter Asset Group",options=["Stock","USD","EUR","CUM","TAM","YAR","CEY","BIL","GRAM"])
sql=cursor.fetchall()

#user_auth
#'C:/Users/BQ2PDDO/PycharmProjects/notesdb/configx.yaml'

with open('configx.yaml') as file:
    config=yaml.load(file,Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'])

authenticator.login()



if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(st.session_state["name"])
    #st.title('Input Areas')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

#--end of the user_auth


if st.session_state["authentication_status"] is True:
    with st.form("Stock Recorder", clear_on_submit=True):
        if opt == "Stock":

            v1a = st.text_input("Stock", max_chars=40)
            v1 = v1a + ".IS"
            v2 = st.number_input("Cost Per Share ")
            v3 = st.number_input("pieces", min_value=1, max_value=9999, step=1, format='%d')
            v4 = datetime.now()

            s_state = st.form_submit_button("Record")
            if s_state:
                if v1 == "" or v2 == "" or v3 == "" or v2 == 0:
                    if s_state:
                        st.warning("Please Fill")
                else:
                    cursor.execute("INSERT INTO stocks (GROUP_NAME,STOCK_NAME,PIECES,COST,CREATED_AT) VALUES (?,?,?,?,?)",
                                   (opt, v1, v3, v2, v4))
                    conn.commit()
                    conn.close()
                    if s_state:
                        st.success("Completed !")
                        time.sleep(3)
        elif opt == "USD" or opt == "EUR":
            opt = opt
            if opt == "USD":
                v1 = "USDTRY=X"
            else:
                v1 = "EURTRY=X"
            v3 = st.number_input("Cost Per Unit")
            v2 = st.number_input("pieces", min_value=1, max_value=50000, step=1, format='%d')
            v4 = datetime.now()
            f_state = st.form_submit_button("Record")

            if f_state:

                if v1 == "" or v2 == "" or v3 == "" or v3 == 0:
                    if f_state:
                        st.warning("Please Fill")
                else:
                    cursor.execute("INSERT INTO stocks (GROUP_NAME,STOCK_NAME,PIECES,COST,CREATED_AT) VALUES (?,?,?,?,?)",
                                   (opt, v1, v2, v3, v4))
                    conn.commit()
                    conn.close()

                    if f_state:
                        st.success("Completed !")
                        time.sleep(3)

        else:
            opt = opt
            v1 = "GC=F"
            v2x = st.number_input("Cost Per Unit", min_value=1, max_value=150000, step=1, format='%d')
            v3x = st.number_input("pieces", min_value=1, max_value=9999, step=1, format='%d')
            x_state = st.form_submit_button("Record")
            if opt == "CUM":
                v3 = v2x / 0.212666471635951
                v2 = v3x * 0.212666471635951
            elif opt == "TAM":
                v3 = v2x / 0.206772168098369
                v2 = v3x * 0.206772168098369

            elif opt == "YAR":
                v3 = v2x / 0.103386084049185
                v2 = v3x * 0.103386084049185
            elif opt == "CEY":
                v3 = v2x / 0.0516930420245924
                v2 = v3x * 0.0516930420245924
            elif opt == "BIL":
                v3 = v2x / 0.029471518

                v2 = v3x * 0.029471518
            else:
                v3 = v2x / 0.032150746568628
                v2 = v3x * 0.032150746568628

            v4 = datetime.now()
            if x_state:
                if v1 == "" or v2 == "" or v3 == "" or v2 == 0:
                    if f_state:
                        st.write("Please Fill")
                else:
                    cursor.execute("INSERT INTO stocks (GROUP_NAME,STOCK_NAME,PIECES,COST,CREATED_AT) VALUES (?,?,?,?,?)",
                                   (opt, v1, v2, v3, v4))
                    conn.commit()
                    conn.close()

                    if x_state:
                        st.success("Completed !")
                        time.sleep(3)

    delete = st.sidebar.button('Delete last entry')
    modal = Modal(key="confirmation_modal", title="Are you sure?")
    if delete:
        modal.open()
    if modal.is_open():
        with modal.container():
            st.write("Are you sure you want to proceed?")
            if st.button("Yes"):
                cursor.execute("DELETE FROM stocks WHERE rowid = (SELECT MAX(rowid) FROM stocks);")
                conn.commit()
                conn.close()
                # Perform the transaction or action here
                st.success("Transaction completed!")
                time.sleep(3)
                modal.close()  # Close the modal
            if st.button("No"):
                st.warning("Transaction canceled.")
                time.sleep(3)
                modal.close()  # Close the modal

    totalcost = st.sidebar.button('Total Cost')
    if totalcost:
        cursor.execute("SELECT * FROM stocks")
        x = cursor.fetchall()
        conn.commit()

        cols = [column[0:5] for column in x]
        df = pd.DataFrame(cols)
        TotalCost = sum(df[2] * df[3])
        st.sidebar.success(f'Total Cost is {TotalCost} TRY')


















