import streamlit as st
from config import SqlEngine, SetStyle, ValidEmail
#style
SetStyle(st)

#contact form
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

#about the members

st.header("Contributers")

def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

# Make the grid
mygrid = make_grid(4,(2,4,4))

# Row 0

mygrid[0][0].image('Divi-img..jpeg', width=150)
mygrid[0][1].markdown("""
#### Divyangana Kothari
""")
mygrid[0][1].write("""
Hello there! I'm pursuing my M.Sc. in Computer Engineering(Specialization Interactive Systems and Visualization) at the moment. Feel free to reach out to me on Github at DivyanganKothari or drop me an email at divyanganakothari@stud.uni-due.de.
""")


#row1
mygrid[1][0].image('farnaz-img.jpeg', width=150)
mygrid[1][1].markdown("""
#### Farnaz Arghavan
""")

mygrid[1][1].write("""
Greetings! I am currently enrolled in a Master of Science program in Angewandte Informatik (with a focus on Information Engineering). If you'd like to connect with me, my Github handle is Farnaz-AR and my email address is farnaz.arghavan@stud.uni-due.de.
""")
#row2

mygrid[2][0].image('manoj-img.jpg', width=150)

mygrid[2][1].markdown("""
#### Manoj Kumar Dara
""")

mygrid[2][1].write("""
Hey, just a heads up - I'm currently pursuing my M.Sc. in Computational Mechanics. If you'd like to chat or ask me any questions, you can find me on Github as Manojkdara or drop me an email at manoj.dara@stud.uni-due.de
""")
#row3
mygrid[3][0].image('julian-img.jpg', width=150)

mygrid[3][1].markdown("""
#### Julian Stülp
""")

mygrid[3][1].write("""
Hiya! Right now, I'm knee-deep in my M.Sc. program for Applied Computer Science(Specialization- Interactive Cooperative Systems). If you want to get in touch,  you can shoot me an email at julian.stuelp@stud.uni-due.de
""")


