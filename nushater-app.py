import streamlit as st
from src.inference import get_prediction

#Initialise session state variable
if 'input_features' not in st.session_state:
    st.session_state['input_features'] = {}

def app_sidebar():
    st.sidebar.header('University Details')
    university_options = ['NUS-ISS', 'NUS', 'SMU', 'NTU']
    universities = st.sidebar.selectbox("University", university_options)
    degree_options = ['Accountancy', 'Accountancy and Business', 'Aerospace Engineering', 'Art, Design and Media', 'Artificial Intelligence Systems', 'Arts', 'Arts (Architecture)', 'Arts (Industrial Design)', 'Arts and Education', 'Bioengineering', 'Biological and Biomedical Sciences', 'Biomedical Sciences and Chinese Medicine', 'Business', 'Business Administration', 'Business Administration (Accountancy)', 'Business Management', 'Business and Computer Engineering/Computing', 'Chemical and Biomolecular Engineering', 'Chemistry and Biological Chemistry', 'Chinese', 'Civil Engineering', 'Communication Studies', 'Computer Engineering', 'Computer Science', 'Computing (Computer Science)', 'Computing (Information Security)', 'Computing (Information Systems)', 'Data Science and Artificial Intelligence', 'Dental Surgery', 'Digital Leadership', 'Economics', 'Electrical and Electronic Engineering', 'Engineering (Biomedical Engineering)', 'Engineering (Chemical Engineering)', 'Engineering (Civil Engineering)', 'Engineering (Computer Engineering)', 'Engineering (Electrical Engineering)', 'Engineering (Engineering Science)', 'Engineering (Environmental Engineering)', 'Engineering (Industrial and Systems Engineering)', 'Engineering (Materials Science and Engineering)', 'Engineering (Mechanical Engineering)', 'Engineering and Economics', 'English', 'Enterprise Business Analytics', 'Environmental Earth Systems Science', 'Environmental Engineering', 'Environmental Studies', 'History', 'Information Engineering and Media', 'Information Systems', 'Interdisciplinary Double Major', 'Landscape Architecture', 'Law', 'Linguistics and Multilingual Studies', 'Maritime Studies', 'Materials Engineering', 'Mathematics and Mathematical Sciences', 'Mechanical Engineering', 'Medicine', 'Medicine and Surgery', 'Music', 'Philosophy', 'Physics and Applied Physics', 'Psychology', 'Public Policy and Global Affairs', 'Science', 'Science (Business Analytics)', 'Science (Computational Biology)', 'Science (Data Science and Analytics)', 'Science (Nursing)', 'Science (Pharmaceutical Science)', 'Science (Pharmacy)', 'Science (Project and Facilities Management)', 'Science (Real Estate)', 'Science and Education', 'Social Sciences', 'Sociology', 'Software Engineering', 'Sports Science and Management']
    degrees = st.sidebar.selectbox("Degree", degree_options)

    def get_input_features():
        input_features = {'universities': universities,
                          'degrees': degrees
                         }
        return input_features
    
    sdb_col1, sdb_col2 = st.sidebar.columns(2)
    with sdb_col1:
        predict_button = st.sidebar.button("Predict", key="predict")
    with sdb_col2:
        reset_button = st.sidebar.button("Reset", key="clear")
    if predict_button:
        st.session_state['input_features'] = get_input_features()
    if reset_button:
        st.session_state['input_features'] = {}
    return None
def app_body():

    title = '<p style="font-family:arial, sans-serif; color:Black;background-color:White; font-size: 30px;padding:5px;text-align:center;border-radius:10px"><b>N</b>ovel <b>U</b>nderstanding <b>S</b>ystem of <br><b>H</b>onest <b>A</b>ppraisal <b>T</b>ool for <b>E</b>ducational <b>R</b>eputation</p><br><p>Select a university and degree to predict how good it is.</p>'
    st.markdown(title, unsafe_allow_html=True)
    default_msg = '**System assessment says:** {}'
    if st.session_state['input_features']:
        assessment = get_prediction(University=st.session_state['input_features']['universities'],
                                    Degree=st.session_state['input_features']['degrees']
                                )           
                    
        if assessment >= 3:
            st.success(default_msg.format(f"This university's rating is {assessment}."))
        elif assessment >= 1:
            st.error(default_msg.format(f'''This university's rating is {assessment}. It is **TRASH**, run.'''))
        else:
            st.error(default_msg.format(f'''This university's rating is {assessment}. It is **ABSOLUTE TRASH**, quit and run!!'''))
    
    footer = '''<br><br><br><br><br><br><br><br><br><br><br><br><br><p styles="font-size:9px"><em>Note: This system is not trained on actual data, the ratings used to train it is generated from random data.</em></p>'''
    st.markdown(footer, unsafe_allow_html=True)
    return None



def main():
    app_sidebar()
    app_body()
    return None

if __name__ == "__main__":
    main()