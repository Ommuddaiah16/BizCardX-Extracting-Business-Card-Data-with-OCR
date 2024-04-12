# BizCardX-Extracting-Business-Card-Data-with-OCR
BizCardX automates business card data extraction via OCR. Upload cards, extract info, and manage data effortlessly. Save to MySQL. Streamlined GUI for intuitive use.

BizCardX is a Streamlit application designed to extract relevant information from business cards using Optical Character Recognition (OCR) technology. The application allows users to upload images of business cards, from which it extracts details such as company name, cardholder name, designation, contact information, email address, website URL, address, and pin code. The extracted information is then displayed in a clean and organized manner in the application's graphical user interface (GUI). Users can also save the extracted data along with the uploaded business card image into a database for future reference.

## Technologies Used

- Python: Programming language used for application development.
- Streamlit: Web application framework for building interactive and customizable GUIs.
- easyOCR: Python library for performing OCR tasks on images.
- PIL (Python Imaging Library): Library for opening, manipulating, and saving many different image file formats.
- Pandas: Library for data manipulation and analysis.
- NumPy: Library for numerical computing.
- Regular Expressions (regex): Used for text pattern matching and extraction.
- MySQL: Relational database management system for storing extracted business card data.

## Problem Statement

The goal of BizCardX is to simplify the process of extracting and managing information from business cards. Traditional methods of manually entering data from business cards into digital formats can be time-consuming and error-prone. BizCardX addresses this challenge by automating the extraction process using OCR technology, thereby saving time and improving accuracy.

## Application Features

- **Image Upload**: Users can upload images of business cards through the application interface.
- **OCR Extraction**: The application uses easyOCR to extract text from the uploaded images.
- **Data Display**: Extracted information is displayed in a structured format within the application's GUI.
- **Database Integration**: Users can save extracted data along with the uploaded images into a MySQL database.
- **Data Management**: The application allows users to read, update, and delete data entries from the database through the Streamlit UI.
- **User-Friendly Interface**: The GUI is designed to be intuitive and easy to navigate, guiding users through the extraction and management process.

## Application Workflow

1. User uploads an image of a business card through the application interface.
2. OCR technology extracts text from the uploaded image.
3. Extracted information is displayed in the application's GUI.
4. User has the option to save the extracted data into a MySQL database along with the uploaded image.
5. Users can also perform CRUD (Create, Read, Update, Delete) operations on data entries from the database through the Streamlit UI.

## Getting Started

To run the BizCardX application locally, follow these steps:

1. Clone this GitHub repository to your local machine:

   ```bash
   git clone https://github.com/your-username/bizcardx.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up a MySQL database and update the connection details in the `app.py` file.

4. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

5. Access the application in your web browser at `http://localhost:8501`.

## Contributing

Contributions to BizCardX are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

