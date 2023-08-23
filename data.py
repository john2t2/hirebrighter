# data file
QUESTION_SCHEMA = {

    'Location': '''
        Interpret and suggest the current city and country the candidate resides in. 
        Output the full name of the city and country.
        If this is not found, output N/A.
    ''',

    'University': '''
        Provide the most recent academic institution the candidate studied at. 
        Output the full name of the institution.
        If this is not found, output N/A.
    ''',

    'Degree': '''
        Provide the most recent university degree the candidate pursued.
        Output merely the full name of the degree.
        If this is not found, output N/A.
    ''',

    'Major': '''
        Provide the most recent university major/program the candidate was in.
        Output merely the full name of the major.
        If this is not found, output N/A.
    ''',

    'Expertise': '''
        Interpret and list the top three expertise of the candidate.
        Output the expertise as a comma-separated Python list.
        If this is not found, output an empty Python list.
    ''',

    'Graduation Date': '''
        Provide the most recent graducation month and year for the candidate.
        Output the month and year in the following format: MM/YYYY.
        If this is not found, output N/A.
    ''',

    'Email': '''
        Provide the complete email address of the candidate in this format: {Email Address}
        If this is not found, output N/A.
    ''',

    'Phone Number': '''
        Provide the phone number of the candidate in this format: {Phone number}
        The output should only contain numbers. Remove any symbols and spaces.
        Example answer: 4379706389
        If this is not found, output N/A.
    ''',

    'GPA': '''
        Provide the GPA of the candidate if avaliable.
        The output should only contain numbers. Remove any symbols, spaces and characters.
        If this is not found, output N/A.
    ''',

    'Work Experience': '''
        List all the companies the candidate worked for.
        Output the names as a comma-separated Python list.
        If this is not found, output an empty Python list.
    ''',

    'Projects': '''
        List all the projects the candidate completed.
        Output the project names as a comma-separated Python list.
        If this is not found, output an empty Python list.
    ''',

    'Skills': '''
        List all the skills the candidate possesses, including all skills mentioned under the work experience and projects sections.
        Output the skills as a comma-separated Python list.
        If this is not found, output an empty Python list.
    ''',
}
# ----------------------------------------------------------------
# Data from Liam Ma

ANSWER_DATA = {
    'Location': 'Toronto, Canada',

    'University': 'University of Toronto',

    'Degree': 'Bachelor of Applied Science',

    'Major': 'Civil Engineering',

    'Expertise': 'Pipeline Engineering, Structural Engineering, Modelling and Analysis',

    'Graduation Date': '06/2021',

    'Email': 'MaL2K16@outlook.com',

    'Phone Number': '4039684717',

    'GPA': '3.5',

    'Work Experience': '''
        ['Pembina Pipeline Corporation, Technical Services Unit']
    ''',

    'Projects': '''
        ['University of Toronto Seismic Design Team', 'Capstone Project - Football Stadium Concept Design', 'Steel Building Frame Design Project']
    ''',

    'Skills': '''
         ['S-Steel', 'S-Concrete', 'AutoCAD', 'NBCC 2015', 'CSA S16-14', 'CSA A23.3', 'Pipeline Bending Strain Analysis', 'MATLAB', 'S-Frame', 'SAP2000', 'Microsoft Excel', 'Visual Basic (VBA)', 'LaTex', 'Python', 'Technical report writing', 'English and Mandarion speaker']
    ''',
}
# ----------------------------------------------------------------

TEMPLATE_STRING = '''
    You are a hiring professional reviewing resumes from potential candidates. Answer the following question based on the resume delimited by triple backticks.

    Resume:

    ```{resume_sample}```

    Question: {question}

    {answer_sample}

    You are a hiring professional reviewing resumes from potential candidates. Answer the following question based on the resume delimited by triple backticks.

    Resume:

    ```{resume}```

    Question: {question}
'''

TEMPLATE_STRING_ZERO_SHOT = '''
    You are a hiring professional reviewing resumes from potential candidates. Answer the following question accurately based on the resume database.

    Question: {question}

    An example of a possible answer and format is delimited by triple backticks. The answer must not be a paragraph or sentence.

    ```{answer}```
'''
# ----------------------------------------------------------------
# Create an sample QnA for work and project related information
WORK_EXPERIENCE_SCHEMA = {
    'Title': '''
        Output the job title of the candidate at {entity}.
        Output only the complete job title of the candidate.
    ''',

    'Job Details': '''
        Provide a list of accomplishments and responsibilities of the candidate at {entity}.
        List all the details in point form.
    ''',

    'Start Date': '''
        Provide the start month and year of candidate's job at {entity}.
        Output the month and year in the following format: MM/YYYY.
        If this is not found, output N/A.
    ''',

    'End Date': '''
        Provide the end month and year for the candidate's job at {entity}.
        Output the month and year in the following format: MM/YYYY.
        If this is not found, output N/A.
    ''',
}

WORK_EXPERIENCE_ANSWER = {
    'Title': 'Pipeline Integrity Intern',
    'Job Details': 
    '''
        1. Conducted qualitative pipeline bending strain analyses for landslide areas
        2. Categorized geological hazards and potential ground movement during site visits
        3. Calculated soil stress and strains for third-party pipeline crossings
        4. Wrote in-line inspection (ILI) engineering reports and dig plans
        5. Prepared monthly team KPI summaries for manager to review
    ''',
    'Start Date': '05/2019',
    'End Date': '08/2020',
}

PROJECT_SCHEMA = {
    'Project Description': '''
        Provide the description of the {entity} the candidate did.
        List all the details in point form.
    ''',

    'Start Date': '''
        Provide the start month and year of the {entity} the candidate did.
        Output the month and year in the following format: MM/YYYY.
        If this is not found, output N/A.
    ''',

    'End Date': '''
        Provide the end month and year of the {entity} the candidate did.
        Output the month and year in the following format: MM/YYYY.
        If this is not found, output N/A.
    ''',
}

PROJECT_ANSWER = {
    'Project Description': '''
        1. Developed seismically resistant balsa wood towers using S-Frame and SAP2000
        2. Used MATLAB and Python to evaluate designs and brainstorm other structural concept ideas
        3. Led a topology optimization project to improve tower displacement and acceleration responses
        4. Hosted least squares linear regression and free vibration tutorials for undergraduate students
        5. Team ranked 6th out of 46 international teams in the 2020 seismic design competition
    ''',
    'Start Date': '05/2019',
    'End Date': '08/2020',
}

#--------------------------------------------------

DIRECT_PARSE_SYSTEM_MESSAGE = '''
    You will be provided with unstructured data.
    Your task is to parse it into a structured text format in the following format:
    <Person's Name> <Field Name>: <Content>
'''
DIRECT_PARSE_ANSWER = '''
Hongyu (Liam) Ma Location: Toronto, Canada
Hongyu (Liam) Ma University': University of Toronto
Hongyu (Liam) Ma Degree': 'Bachelor of Applied Science',
Hongyu (Liam) Ma Major': 'Civil Engineering',
Hongyu (Liam) Ma Expertise': 'Pipeline Engineering, Structural Engineering, Modelling and Analysis',
Hongyu (Liam) Ma Graduation Date': '06/2021',
Hongyu (Liam) Ma Email': 'MaL2K16@outlook.com',
Hongyu (Liam) Ma Phone Number': '4039684717',
Hongyu (Liam) Ma GPA': '3.5',
Hongyu (Liam) Ma Work Experience':
    - Hongyu (Liam) Ma at 'Pembina Pipeline Corporation, Technical Services Unit' 
        - Applied Skills:['Pipeline bending strain analysis']
Hongyu (Liam) Ma Projects':
    - Hongyu (Liam) Ma on 'University of Toronto Seismic Design Team'
        - Applied Skills: ['S-Frame', 'SAP2000', 'MATLAB', 'Python']
    - Hongyu (Liam) Ma on 'Capstone Project - Football Stadium Concept Design'
        - Applied Skills: ['AutoCAD', 'S-Frame', 'S-Steel', 'S-Concrete', 'NBCC 2015', 'CSA S16-14', 'CSA A23.3']
    - Hongyu (Liam) Ma on 'Steel Building Frame Design Project' 
        - Applied Skills: ['S-Frame', 'NBCC 2015', 'CSA S16-14', 'NBCC 2015']
Hongyu (Liam) Ma Skills': ['S-Steel', 'S-Concrete', 'AutoCAD', 'NBCC 2015', 'CSA S16-14', 'CSA A23.3', 'Pipeline Bending Strain Analysis', 'MATLAB', 'S-Frame', 'SAP2000', 'Microsoft Excel', 'Visual Basic (VBA)', 'LaTex', 'Python', 'Technical report writing', 'English and Mandarion speaker']
'''

DIRECT_PARSE_TEMPLATE = '''
Unstructured Data Input:
{resume_sample}

Structured Data Output:
{resume_sample_output}

Unstructured Data Input:
{resume}

Structured Data Output:
'''

# --------------------------------------------------------------------------------

RESUME_SAMPLE = '''
    Hongyu (Liam) Ma
    126 Cranarch Hts. SE – Calgary – Canada
    /mobile_phone(403) 968 4717 /envelopeMaL2K16@outlook.com /globelinkedin.com/in/hongyuma
    Education
    University of Toronto Sep 2017 – June 2021
    High Honours in Bachelor of Applied Science
    Major in Civil Engineering, GPA of 3.6
    /circle_blankStructural Analysis
    /circle_blankSteel Structural Design
    /circle_blankStructural Dynamics/circle_blankSolid Mechanics I and II
    /circle_blankEngineering Mathematics
    /circle_blankStatistics and Probability Theory/circle_blankReinforced Concrete Design
    /circle_blankGeotechnical Engineering
    /circle_blankTransportation Planning
    University of Toronto Sep 2016 – Apr 2017
    Bachelor of Applied Science
    Engineering Science
    /circle_blankCalculus I and II
    /circle_blankNumerical Methods/circle_blankLinear Algebra
    /circle_blankClassical Mechanics/circle_blankMaterials Science
    /circle_blankPython Programming
    Projects
    University of Toronto Seismic Design Team Oct 2017 – Apr 2021
    /circle_blankDeveloped seismically resistant balsa wood towers using S-Frame andSAP2000
    /circle_blankUsedMATLAB andPythonto evaluate designs and brainstorm other structural concept ideas
    /circle_blankLed a topology optimization project to improve tower displacement and acceleration responses
    /circle_blankHosted least squares linear regression and free vibration tutorials for undergraduate students
    /circle_blankTeam ranked 6thout of 46 international teams in the 2020 seismic design competition
    Capstone Project – Football Stadium Concept Design Jan 2021 – Apr 2021
    /circle_blankDeveloped using AutoCAD andS-Frame
    /circle_blankDesigned a steel roof, reinforced concrete seating tiers, and foundations
    /circle_blankAnalyzed governing NBCC 2015 load cases and load combinations
    /circle_blankUsedS-Steelto run CSA S16-14 code design checks for the roof and exterior
    /circle_blankUsedS-Concrete to run CSA A23.3 code design checks for seating tiers and walls
    /circle_blankPresented design concept options and team progress in a comprehensive ﬁnal report
    Steel Building Frame Design Project Sep 2018 – Dec 2018
    /circle_blankModelled using S-Frame
    /circle_blankDimensioned lateral bracing, moment resistance frames, and beam-columns
    /circle_blankAnalyzed governing NBCC 2015 load cases and load combinations
    /circle_blankEnsured compliance with CSA S16-14 and NBCC 2015
    /circle_blankPresented a preliminary project proposal for the instructor to review
    Work Experience
    Pipeline Integrity Intern May 2019 – Aug 2020
    Pembina Pipeline Corporation, Technical Services Unit
    Reference: Pavle Canji, Senior Manager, Asset Integrity
    /circle_blankConducted qualitative pipeline bending strain analyses for landslide areas
    /circle_blankCategorized geological hazards and potential ground movement during site visits
    /circle_blankCalculated soil stress and strains for third-party pipeline crossings
    /circle_blankWrote in-line inspection (ILI) engineering reports and dig plans
    /circle_blankPrepared monthly team KPI summaries for manager to review
    Awards
    Faculty of Applied Science and Engineering Dean’s Honour List Jan 2018 – Jan 2021
    /circle_blankAwarded to undergraduate students with a sessional GPA of 3.5 or above on a rolling basis
    Jack Young Memorial Award Nov 2019
    /circle_blankAwarded to the student with the highest grade in the CME358 survey camp practical course
    University of Toronto President’s Entrance Scholar Sep 2016
    /circle_blankAwarded to incoming undergraduate students with a secondary school average of 95% or above
    Skills
    /circle_blankMATLAB
    /circle_blankS-Frame
    /circle_blankSAP2000/circle_blankMicrosoft Excel
    /circle_blankVisual Basic (VBA)
    /circle_blankLaTeX/circle_blankPython
    /circle_blankTechnical report writing
    /circle_blankEnglish and Mandarin speaker
'''