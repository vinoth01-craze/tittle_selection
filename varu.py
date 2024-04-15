import streamlit as st
import sqlite3


# Function to connect to the SQLite database
def connect_to_database():
    conn = sqlite3.connect('registration.db')
    return conn


# Function to create the registration table in the SQLite database
def create_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registration (
            id INTEGER PRIMARY KEY,
            reg_no TEXT,
            topic TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Function to insert registration data into the SQLite database
def insert_data(reg_no, topic):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registration (reg_no, topic) VALUES (?, ?)
    ''', (reg_no, topic))
    conn.commit()
    conn.close()


# Function to fetch all registration data from the SQLite database
def fetch_data():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registration')
    data = cursor.fetchall()
    conn.close()
    return data


# Function to delete registration data from the SQLite database
def delete_data(reg_no):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM registration WHERE reg_no=?
    ''', (reg_no,))
    conn.commit()
    conn.close()


# Main function
def main():
    st.set_page_config(page_title="Registration Form", page_icon=":clipboard:")
    st.markdown(
        """
        <style>

        h1 {
            width: 400px;
            padding: 0%;
            top: 5%;
            left: 40%;
            font-size: 60px;
            color: light=white;
            font-family: Garamond, serif;
            white-space: nowrap; /* Ensures text stays on a single line */
            -webkit-animation: glow 1s ease-in-out infinite alternate;
            -moz-animation: glow 1s ease-in-out infinite alternate;
            animation: glow 1s ease-in-out infinite alternate;
            margin-bottom: 100px;
            background-clip: padding-box;
            box-shadow: 0 0 50px white;
        }
        h2{
            color:lightblue;
            font-family: Copperplate, Papyrus, fantasy;
        }
        h3{
            color:yellow;
          font-family: Copperplate, Papyrus, fantasy;
        }
        P {
            color: black;
            font-family: Copperplate, Papyrus, fantasy;
        }
        .stButton>button {
            background-color: white; /* Background color of the button */
        }
        .stButton>button:hover {
            cursor: pointer;
        }
        .stApp {
            background-image: url("https://static.vecteezy.com/system/resources/thumbnails/039/650/006/small_2x/modern-abstract-technology-background-design-illustration-vector.jpg");
            background-size: cover;
            object-fit:center;
        }

        /* Custom CSS for table text color */
        table.dataframe td {
            color: #666;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    # Create the registration table if it doesn't exist
    create_table()

    # Initialize session state
    if 'to_delete' not in st.session_state:
        st.session_state.to_delete = []

    # Display text input boxes for registration number and topic
    reg_no = st.text_input("Enter Register Number:")
    topic = st.text_input("Enter Topic Name:")

    # Handle form submission without refreshing the page
    submit_button = st.button("Submit", key="submit_button")
    if submit_button:
        if reg_no and topic:
            insert_data(reg_no, topic)
            st.success("Registration successful!")
            # Clear input fields after successful submission
            reg_no = ""
            topic = ""
        else:
            st.error("Please fill in all fields.")

    # Display previous submissions in a table format
    st.header("Previous Submissions")
    data = fetch_data()
    if data:
        # Convert data to a list of dictionaries for table display
        data_dict = [{"Register Number": row[1], "Topic": row[2]} for row in data]
        st.table(data_dict)

        # Add a delete button for each entry
        for index, row in enumerate(data):
            delete_key = f"delete_{index}"
            if st.button(f"Delete {row[1]}", key=delete_key):
                st.session_state.to_delete.append(row[1])

    # Handle deletion of rows without refreshing the page
    if st.session_state.to_delete:
        password = st.text_input("Enter password:", type="password")
        delete_button = st.button("Delete", key="delete_button")
        if delete_button and password == "varuna":  # Replace "varuna" with your actual password
            for reg_no in st.session_state.to_delete:
                delete_data(reg_no)
            st.success("Data deleted successfully!")
            # Clear the list of IDs to delete
            st.session_state.to_delete = []
            # Refresh the page after successful deletion
            st.experimental_rerun()
        elif delete_button and password != "":
            st.error("Incorrect password! Data deletion failed.")


if __name__ == "__main__":
    main()
