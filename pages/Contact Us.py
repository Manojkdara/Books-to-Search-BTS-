import streamlit as st
from config import SqlEngine, SetStyle, ValidEmail
#style
SetStyle(st)

# Title
st.header(":mailbox: Get in touch with us!")

with st.form("EmailForm", clear_on_submit=True):
    fullname = st.text_input("Full Name", placeholder="Please enter your full name")
    email = st.text_input("Email Address", placeholder="Please enter your email address")
    message = st.text_area("Message", max_chars=2048, placeholder="Please enter your message here")

    if st.form_submit_button("Send"):
        if fullname == "" or email == "" or message == "":
            st.markdown("Please fill out everything")
            st.stop()
            
        if not ValidEmail(email):
            st.markdown("Invalid Email")
            st.stop()
        
        from sqlalchemy import table, column, insert, text
        contact_message = table("contact_message", column("fullname"), column("email"), column("message"))
        stmt = insert(contact_message).values(fullname = fullname, email = email, message = message)
        
        engine = SqlEngine()
        with engine.connect() as connection:
            connection.execute(stmt)
            connection.commit()
        st.markdown("Thanks for your message!")