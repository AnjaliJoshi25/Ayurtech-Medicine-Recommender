import streamlit as st
import pickle
import pandas as pd
# from googletrans import Translator

# def translate_to_hindi(text):
#     # Function to translate text to Hindi
#     # translator = Translator()
#     translated_text = translator.translate(text, dest='hi').text
#     return translated_text

# Set Streamlit page configuration
st.set_page_config(page_title="Ayurtech", page_icon="🌿")
header_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Header</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        
        header {
            background-color: #32cd32; /* Dark green */
            color: #ffffff; /* White text */
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .heading-link {
            color: #ffffff; /* White text */
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .heading-link:hover {
            color: #ff5733; /* Orange text on hover */
        }
    </style>
</head>
<body>
    <header>
    </header>
</body>
</html>
"""

footer_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Footer</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"> <!-- Font Awesome Icons -->
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        
        .footer {
            background-color: #f7f2db; /* Background color provided by you */
            padding: 20px;
            text-align: center;
            color: #333333; /* Text color */
            font-size: 14px; /* Font size */
        }
        
        .footer-links {
            margin-top: 10px; /* Add some top margin for spacing */
        }
        
        .footer-links a {
            margin: 0 10px; /* Add horizontal margin for spacing */
            color: #333333;
            text-decoration: none;
        }
        
        .footer-links a:hover {
            color: #ff5733; /* Orange text on hover */
        }
    </style>
</head>
<body>
    <footer class="footer">
        <p>Follow us on:</p>
        <div class="footer-links">
            <a href="https://whatsapp.com/channel/0029VaXpQVX2Jl84qc38EV00 "><i class="fab fa-whatsapp"></i></a> <!-- WhatsApp Icon -->
            <a href="https://www.instagram.com/ayurtech.official?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="><i class="fab fa-instagram"></i></a> <!-- Instagram Icon -->
            <a href="#"><i class="fas fa-globe"></i></a> <!-- Website Icon -->
            <a href="#"><i class="fab fa-facebook"></i></a> <!-- Facebook Icon -->
        </div>
        <p>&copy; 2024 AyurTech. All rights reserved.</p>
    </footer>
</body>
</html>

"""

st.markdown(header_html, unsafe_allow_html=True)

# Load medicine data and similarity vectors
medicines_dict = pickle.load(open('new.df.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(medicine):
    medicine_index = medicines[medicines['Main_Indications'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommended_medicines = []
    for i in medicines_list[:5]:  # Selecting top 2 recommendations
        recommended_medicine = medicines.iloc[i[0]]
        recommended_medicines.append({
            'Name_of_Medicine': recommended_medicine['Name_of_Medicine'],
            'Composition': recommended_medicine['Composition '],
            'Medical_Preparation': recommended_medicine['Medical_Preparation'],
            'Dosage': recommended_medicine['Dose_and_Mode_of_Administration'],
            'Contraindication': recommended_medicine['Precaution/Contraindication'],
            'Reference_Text': recommended_medicine['Reference_Text']
        })
    return recommended_medicines

# Streamlit app frontend
st.title('Ayurtech Medicine Recommender')

# Dropdown to select symptoms
selected_medicine_name = st.selectbox(
    'Select your symptoms',
    medicines['Main_Indications'].values
)

# Checkboxes for Vata, Kapha, and Pitta
with st.expander("Patient Details"):
    patient_name = st.text_input('Patient Name')
    has_vata = st.checkbox('Vata')
    has_kapha = st.checkbox('Kapha')
    has_pitta = st.checkbox('Pitta')
    systolic_bp = st.text_input('Systolic Blood Pressure')
    diastolic_bp = st.text_input('Diastolic Blood Pressure')

    # Save button to save patient details
    if st.button('Save'):
        patient_details = {
            'Patient Name': patient_name,
            'Vata': has_vata,
            'Kapha': has_kapha,
            'Pitta': has_pitta,
            'Systolic Blood Pressure': systolic_bp,
            'Diastolic Blood Pressure': diastolic_bp
        }
        # Save patient details to a CSV file
        saved_data = pd.DataFrame([patient_details])
        saved_data.to_csv('saved_patient_details.csv', index=False)

# Button to recommend medicine
if st.button('Recommend Medicine'):
    recommendations = recommend(selected_medicine_name)
    
    recommendation_df = pd.DataFrame(recommendations)
    recommendation_df['Ayurvedic Official Name'] = recommendation_df['Name_of_Medicine'].apply(translate_to_hindi)
    
    custom_css = """
        <style>
            .stApp {
                max-width: 80%; /* Set maximum width of block container */
            }
            .table-container {
                margin: 0 auto; /* Center horizontally */
            }
            table {
                width: 100%; /* Occupy full width of container */
            }
            th, td {
                padding: 12px; /* Increase padding for better readability */
            }
            th {
                background-color: #f2f2f2; /* Light gray background for header */
            }
            td {
                background-color: #ffffff; /* White background for cells */
            }
        </style>
    """
    st.write('<div class="table-container">', unsafe_allow_html=True)
    st.write(recommendation_df.to_html(escape=False), unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)
    st.write(custom_css, unsafe_allow_html=True)

st.markdown(footer_html, unsafe_allow_html=True)
