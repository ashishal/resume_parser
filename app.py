import nltk
import pandas as pd

from imports import *

st.header('Resume Parser Ekatra')
resumes = st.file_uploader(label='Upload your resume here', type=['pdf', 'docx', 'doc'],accept_multiple_files=True)

skills_list = ['laravel', 'php', 'web application', 'html', 'react', 'cordova', 'mobile app', 'python', 'keras']

def extract_skills(resume, skill_list):
    ratio = []
    resume = nlp(resume)
    for tok in resume:
        for i in skill_list:
            fuzz_ratio = fuzz.ratio(i, str(tok.text))
            if fuzz_ratio > 75:
                ratio.append(tok)
    return ratio

def extract_name(resume):
    doc = nlp(resume)
    names = []
    for token in doc.ents:
        if token.label_ == 'PERSON':
            names.append(token)
            name = names[0]
            return name

def extract_email(resume):
    lst = re.findall('\S+@\S+', resume)
    if lst:
        return lst[0]
    return None

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')

def extract_phone_number(resume):
    phone = re.findall(PHONE_REG, resume)

    if phone:
        number = ''.join(phone[0])

        if resume.find(number) >= 0 and len(number)>=10:
            return number
    return None

df_final    =   pd.DataFrame()
for resume in resumes:
    if resume:
        name = " "
        email = " "
        phone_number = " "
        skills = []

        if resume.name.endswith('.docx'):
            text = docx2txt.process(resume)
            name = extract_name(text)
            phone_number = extract_phone_number(text)
            email = extract_email(text)
            skills  = extract_skills(text, skills_list)


        elif resume.name.endswith('.pdf'):
            text = extract_text(resume)
            name = extract_name(text)
            phone_number = extract_phone_number(text)
            email = extract_email(text)
            skills = extract_skills(text, skills_list)


        elif resume.name.endswith('.doc'):
            text = docx2txt.process(resume)
            name = extract_name(text)
            phone_number = extract_phone_number(text)
            email = extract_email(text)
            skills = extract_skills(text, skills_list)


    name = str(name)
    name_df = pd.DataFrame({'Name': [name]})
    phone_number_df = pd.DataFrame({'Phone Number': [phone_number]})
    email_df = pd.DataFrame({'Email' : [email]})
    skills_df = pd.DataFrame({'Skills' : [skills]})



    final_df = pd.concat([name_df, phone_number_df,email_df,skills_df['Skills']], axis=1)

    # st.dataframe(final_df)

    df_final = df_final.append(final_df)


final_df_2 = df_final.to_csv()
st.download_button('Download Predictions', data=final_df_2)
