import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import pymysql

# Install the required packages if not already installed
# !pip install streamlit easyocr pymysql pillow sqlalchemy

def img_to_text(path):
    input_image = Image.open(path)
    image_array = np.array(input_image)
    reader = easyocr.Reader(['en'])
    text = reader.readtext(image_array, detail=0)
    return text, input_image

def extract_info(text):
    extract_dict = {
        'Name': [], 'Designation': [],
        'Company_name': [], 'Contact': [],
        'Email': [], 'Website': [],
        'Address': [], 'Pincode': []
    }

    extract_dict['Name'].append(text[0])
    extract_dict['Designation'].append(text[1])

    for i in range(2, len(text)):

        if text[i].startswith('+') or (text[i].replace("-", '').isdigit() and '-' in text[i]):
            extract_dict['Contact'].append(text[i])

        elif "@" in text[i] and '.com' in text[i]:
            extract_dict['Email'].append(text[i])

        elif 'WWW' in text[i] or "www" in text[i] or 'Www' in text[i] or 'wWw' in text[i] or 'wwW' in text[i]:
            small = text[i].lower()
            extract_dict['Website'].append(small)

        elif "Taml Nadu" in text[i] or 'TamilNadu' in text[i] or text[i].isdigit():
            extract_dict['Pincode'].append(text[i])

        elif re.match(r'^[A-Za-z]', text[i]):
            extract_dict['Company_name'].append(text[i])

        else:
            remove_colon = re.sub(r'[,;]', '', text[i])
            extract_dict['Address'].append(text[i])

    for key, value in extract_dict.items():
        if len(value) > 0:
            Concadenate = " ".join(value)
            extract_dict[key] = [Concadenate]
        else:
            value = "NA"
            extract_dict[key] = [value]

    return extract_dict

# Database connection details
db_username = 'root'
db_password = 'password'
db_name = 'Biz_card_data'
db_host = 'localhost'  # Assuming MySQL is running locally
db_port = 3306  # Default port for MySQL

# Create database and table if not exists
try:
    connection = pymysql.connect(host=db_host,
                                 user=db_username,
                                 password=db_password,
                                 database=db_name,
                                 port=db_port,
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_cards (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255),
                Designation VARCHAR(255),
                Company_name VARCHAR(255),
                Contact VARCHAR(255),
                Email VARCHAR(255),
                Website VARCHAR(255),
                Address VARCHAR(255),
                Pincode VARCHAR(255),
                Image LONGBLOB
            )
        """)
    connection.commit()
finally:
    connection.close()

st.set_page_config(layout="wide")

select = st.sidebar.radio("Main Menu", ['Home', 'Upload & Modify', 'Delete'])

if select == 'Home':
    st.write("""
    # BizCardX: Extracting Business Card Data with OCR

    ## Introduction:
    BizCardX is a Streamlit application designed to extract relevant information from business cards using Optical Character Recognition (OCR) technology. The application allows users to upload images of business cards, from which it extracts details such as company name, cardholder name, designation, contact information, email address, website URL, address, and pin code. The extracted information is then displayed in a clean and organized manner in the application's graphical user interface (GUI). Users can also save the extracted data along with the uploaded business card image into a database for future reference.

    ## Technologies Used:
    - Python: Programming language used for application development.
    - Streamlit: Web application framework for building interactive and customizable GUIs.
    - easyOCR: Python library for performing OCR tasks on images.
    - PIL (Python Imaging Library): Library for opening, manipulating, and saving many different image file formats.
    - Pandas: Library for data manipulation and analysis.
    - NumPy: Library for numerical computing.
    - Regular Expressions (regex): Used for text pattern matching and extraction.
    - MySQL: Relational database management system for storing extracted business card data.

    ## Problem Statement:
    The goal of BizCardX is to simplify the process of extracting and managing information from business cards. Traditional methods of manually entering data from business cards into digital formats can be time-consuming and error-prone. BizCardX addresses this challenge by automating the extraction process using OCR technology, thereby saving time and improving accuracy.

    ## Application Features:
    - Image Upload: Users can upload images of business cards through the application interface.
    - OCR Extraction: The application uses easyOCR to extract text from the uploaded images.
    - Data Display: Extracted information is displayed in a structured format within the application's GUI.
    - Database Integration: Users can save extracted data along with the uploaded images into a MySQL database.
    - Data Management: The application allows users to read, update, and delete data entries from the database through the Streamlit UI.
    - User-Friendly Interface: The GUI is designed to be intuitive and easy to navigate, guiding users through the extraction and management process.

    ## Application Workflow:
    - User uploads an image of a business card through the application interface.
    - OCR technology extracts text from the uploaded image.
    - Extracted information is displayed in the application's GUI.
    - User has the option to save the extracted data into a MySQL database along with the uploaded image.
    - Users can also perform CRUD (Create, Read, Update, Delete) operations on the database entries through the Streamlit UI.

    ## Conclusion:
    BizCardX simplifies the process of managing business card information by leveraging OCR technology and database integration. It streamlines data extraction, improves accuracy, and provides users with a convenient way to store and manage business card details digitally. With its user-friendly interface and robust features, BizCardX is a valuable tool for businesses and individuals alike.
    """)


elif select == 'Upload & Modify':
    img = st.file_uploader("Upload the Image", type=["png", "jpeg", "jpg"])
    if img is not None:
        st.image(img, width=300)

        text, input_image = img_to_text(img)

        text_dict = extract_info(text)
        if text_dict:
            st.success("Text extracted Successfully")

        df = pd.DataFrame(text_dict)

        # Converting image to bytes
        image_bytes = io.BytesIO()
        input_image.save(image_bytes, format='PNG')
        image_data = image_bytes.getvalue()

         # Creating dictionary
        data = {"IMAGE": [image_data]}
        df_1 = pd.DataFrame(data)

        Concat_df = pd.concat([df, df_1], axis=1)

        st.dataframe(Concat_df)

        # Save to MySQL
        if st.button('Save to MySQL',use_container_width= True):
            try:
                connection = pymysql.connect(host=db_host,
                                            user=db_username,
                                            password=db_password,
                                            database=db_name,
                                            port=db_port,
                                            cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    for _, row in df.iterrows():
                        # Check if data with the same values already exists
                        cursor.execute("""
                            SELECT * FROM business_cards 
                            WHERE Name = %s 
                            AND Designation = %s 
                            AND Company_name = %s 
                            AND Contact = %s 
                            AND Email = %s 
                            AND Website = %s 
                            AND Address = %s 
                            AND Pincode = %s
                        """, (row['Name'], row['Designation'], row['Company_name'], row['Contact'], row['Email'], row['Website'], row['Address'], row['Pincode']))
                        existing_data = cursor.fetchone()

                        if existing_data:
                            # Data with the same values already exists
                            st.warning(f"Data with the same values already exists.")
                        else:
                            # Insert the new data
                            cursor.execute("""
                                INSERT INTO business_cards (Name, Designation, Company_name, Contact, Email, Website, Address, Pincode, Image) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (row['Name'], row['Designation'], row['Company_name'], row['Contact'], row['Email'], row['Website'], row['Address'], row['Pincode'], image_data))
                    connection.commit()
                    st.success("Data successfully saved to MySQL database!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                connection.close()


    method = st.radio("select the methos", ["None","Preview", "Modify"])
    if method == "None":
        st.write(" ")

    if method == "Preview":
        try:
            connection = pymysql.connect(host=db_host,
                                         user=db_username,
                                         password=db_password,
                                         database=db_name,
                                         port=db_port,
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                select_query = "select * from business_cards"
                cursor.execute(select_query)
                table = cursor.fetchall()
                table_df = pd.DataFrame(table)
                st.dataframe(table_df)
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            connection.close()
    
    elif method == "Modify":
        try:
            connection = pymysql.connect(host=db_host,
                                        user=db_username,
                                        password=db_password,
                                        database=db_name,
                                        port=db_port,
                                        cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                select_query = "SELECT * FROM business_cards"
                cursor.execute(select_query)
                table = cursor.fetchall()
                table_df = pd.DataFrame(table)
                
                # Display dropdown to select name
                selected_name = st.selectbox("Select Name to Modify", table_df['Name'].unique())
                
                # Filter the DataFrame based on selected name
                selected_row = table_df[table_df['Name'] == selected_name]
                
                if not selected_row.empty:
                    # Display the selected row
                    st.write("Selected Row:")
                    st.write(selected_row)
                    
                    # Allow user to select columns to modify
                    columns_to_modify = st.multiselect("Select Columns to Modify", table_df.columns)
                    
                    # Allow user to input new values for selected columns
                    new_values = {}
                    for column in columns_to_modify:
                        new_value = st.text_input(f"Enter new value for {column}", selected_row.iloc[0][column])
                        new_values[column] = new_value
                    
                    # Update the row in the database with modified values
                    if st.button("Update Row"):
                        with connection.cursor() as cursor:
                            update_query = "UPDATE business_cards SET "
                            for column, value in new_values.items():
                                update_query += f"{column} = '{value}', "
                            update_query = update_query[:-2]  # Remove the trailing comma and space
                            update_query += f" WHERE Name = '{selected_name}'"
                            
                            cursor.execute(update_query)
                            connection.commit()
                            st.success("Row updated successfully!")
                            
                            # Fetch the updated row from the database
                            cursor.execute(f"SELECT * FROM business_cards WHERE Name = '{selected_name}'")
                            updated_row = cursor.fetchone()
                            if updated_row:
                                updated_row_df = pd.DataFrame([updated_row])
                                st.write("Updated Row:")
                                st.dataframe(updated_row_df)
                            else:
                                st.warning("No data found for the selected name.")
                else:
                    st.warning("No data found for the selected name.")
                        
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            connection.close()


elif select == 'Delete':
    try:
        connection = pymysql.connect(host=db_host,
                                     user=db_username,
                                     password=db_password,
                                     database=db_name,
                                     port=db_port,
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Fetch all data from the database table
            select_query = "SELECT * FROM business_cards"
            cursor.execute(select_query)
            table = cursor.fetchall()
            table_df = pd.DataFrame(table)
            
            # Display the MySQL table in DataFrame format
            st.write("MySQL Table:")
            st.dataframe(table_df)
            
            # Provide options to select data based on name and company name
            selected_name = st.selectbox("Select Name to Delete", table_df['Name'].unique())
            selected_company = st.selectbox("Select Company Name to Delete", table_df['Company_name'].unique())
            
            # Provide a button to delete the selected data
            if st.button("Delete Selected Data"):
                # Execute DELETE query to remove selected rows from the database table
                delete_query = f"DELETE FROM business_cards WHERE Name = '{selected_name}' AND Company_name = '{selected_company}'"
                cursor.execute(delete_query)
                connection.commit()
                st.success("Selected data deleted successfully!")
                
                # Fetch the remaining data after deletion
                cursor.execute(select_query)
                remaining_data = cursor.fetchall()
                remaining_df = pd.DataFrame(remaining_data)
                
                # Display the updated data
                st.write("Updated MySQL Table:")
                st.dataframe(remaining_df)
                
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        connection.close()
