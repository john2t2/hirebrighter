from os import listdir
from os.path import isfile, join

from data import *

import pandas as pd

import streamlit as st

import ast
import copy

from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.agents import Tool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.schema import AIMessage, HumanMessage, SystemMessage

def get_database_from_resume(resumes, method='retrieval', summarize=True):

    # get template ------------------------------
    prompt_template = ChatPromptTemplate.from_template(TEMPLATE_STRING)

    # define llm --------------------------------
    llm = ChatOpenAI(temperature=0)

    # resume database
    resume_database = {}
    raw_resumes = {}
    retrieval_chains = {}

    # clean up resume text
    prompt_template = """Remove all the 1) useless characters and terms and 2) remove specific work experience/project description from the resume. Return a cleaned version:
    "{text}"
    CLEANED RESUME:"""
    prompt = PromptTemplate.from_template(prompt_template)
    llm = ChatOpenAI(temperature=0)
    summarize_chain = LLMChain(llm=llm, prompt=prompt)

    resume_sample_local = RESUME_SAMPLE
    if summarize:
        resume_sample_local = summarize_chain.run(RESUME_SAMPLE)

    # progress bar
    status_bar = st.progress(0, text='Parsing resume...')

    for i, resume in enumerate(resumes):

        # split text --------------------------------
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        splits = text_splitter.split_text(resume)
        splits = [Document(page_content=t) for t in splits[:]]

        # create vectorstore for retrieval --------------------------------
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(splits, embeddings, collection_name=f'candiate{i}')

        retrieval_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
        )

        # create vectorstore for retrieval --------------------------------
        question = 'Provide the full name of the person in the document in this format:{Full Name}'
        candidate = retrieval_chain.run(question)

        if method == 'retrieval':
            # get template ------------------------------
            prompt_template = ChatPromptTemplate.from_template(TEMPLATE_STRING_ZERO_SHOT)
            resume_data = parse_resume_from_retrieval(retrieval_chain, QUESTION_SCHEMA , ANSWER_DATA, prompt_template)

        else:
            # get template ------------------------------
            prompt_template = ChatPromptTemplate.from_template(TEMPLATE_STRING)
            if summarize:
                resume = summarize_chain.run(resume)

            resume_data = parse_resume(llm, resume, resume_sample_local, QUESTION_SCHEMA, ANSWER_DATA, prompt_template)

        # save data ----------------------------------------------------------------
        resume_database[candidate] = resume_data
        raw_resumes[candidate] = resume
        retrieval_chains[(f'candiate{i}', candidate)] = retrieval_chain

        # progress bar ----------------------------------------------------------------
        status_bar.progress(int((i+1)/len(resumes)*100), text='Parsing resume...')

    return resume_database, raw_resumes, retrieval_chains

def get_complete_database(resume_database, raw_resumes):

    # get template ------------------------------
    prompt_template = ChatPromptTemplate.from_template(TEMPLATE_STRING)

    complete_resume_database = copy.deepcopy(resume_database)
    section_queries = {
                    'Work Experience': {
                        'schema': WORK_EXPERIENCE_SCHEMA,
                        'answer': WORK_EXPERIENCE_ANSWER,
                    }, 
                    'Projects': {
                        'schema': PROJECT_SCHEMA,
                        'answer': PROJECT_ANSWER,
                    },
                }

    for app_name in resume_database:
        resume = raw_resumes[app_name]
        data_obj= resume_database[app_name]

        for target_key in section_queries:
            schema = section_queries[target_key]['schema']
            answer = section_queries[target_key]['answer']
            
            section_data = get_item_info(target_key, data_obj, resume, RESUME_SAMPLE, schema, answer, prompt_template)

            complete_resume_database[app_name][target_key] = section_data

    return complete_resume_database

def parse_resume(llm, resume, resume_sample, question_schema, answer_data, prompt_template, keys_to_skip=[]):
    ''' one-shot query '''
    parsed_resume = {}

    for key in question_schema:
        if key in keys_to_skip:
            continue

        question = question_schema[key]
        answer_sample = answer_data[key]
        
        query = prompt_template.format_messages(
                    resume_sample=resume_sample,
                    question=question,
                    answer_sample=answer_sample,
                    resume=resume)
        
        data = llm(query).content
        parsed_resume[key] = data

    return parsed_resume

def direct_parse_resume(llm, resume, system_message, fields=[]):
    # output parser --------------------------------
    response_schemas = [ResponseSchema(name=field, description=field) for field in fields]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    
    # llm parser --------------------------------
    messages = [
        SystemMessage(
            content=system_message + str(fields)
        ),
        HumanMessage(
            content=resume
        ),
    ]

    output = llm(messages).content

    return output_parser.parse(output)

def parse_resume_from_retrieval(retrieval_chain, question_schema, answer_data, prompt_template):
    parsed_resume = {}
    for key in question_schema:
        question = question_schema[key]
        answer = answer_data[key]
        
        query = prompt_template.format_messages(
                    question=question,
                    answer=answer,
                )[0].content
        
        data = retrieval_chain.run(query)
        parsed_resume[key] = data

    return parsed_resume

def get_item_info(target_key, data_obj, resume, resume_sample, question_schema, answer_data, prompt_template):

    # define llm --------------------------------
    llm = ChatOpenAI(temperature=0)
    
    items = data_obj[target_key]
    parsed_items = [i.strip() for i in ast.literal_eval(items)]
    
    parsed_section = {}

    for item in parsed_items:
        parsed_item = {}

        for key in question_schema:
            question_template = ChatPromptTemplate.from_template(question_schema[key])
            answer_sample = answer_data[key]

            question = question_template.format_messages(
                        entity=item)[0].content
            
            query = prompt_template.format_messages(
                        resume_sample=resume_sample,
                        question=question,
                        answer_sample=answer_sample,
                        resume=resume)
            
            data = llm(query).content
            parsed_item[key] = data
        
        parsed_section[item] = parsed_item

    return parsed_section


def get_text_from_json(database):

    text = ''

    text += 'List of candidates:'
    for person in database:
        text += f'{person},'
    text += '\n\n'

    for person in database:
        for key, info in database[person].items():
            if type(info) == str:
                text += f"{person}'s {key}: {info}"
                text += '\n'
            else:
                for entity, entity_info in info.items():
                    for term, detail in entity_info.items():
                        text += f"{person}'s {key} at {entity}: {term}: {detail}"
                        text += '\n'
        text += '\n'

    return text


def get_df_from_json(database):
    database_dict = {
        'Name': [],
        'Location': [],
        'University': [],
        'Major': [],
        'Expertise': [],
        'Graduation Date': [],
        'Email': [],
    }

    fields = ['Location', 'University', 'Major', 'Expertise', 'Graduation Date', 'Email']

    for name in database:
        database_dict['Name'].append(name)
        person_info = database[name]

        for field in fields:
            database_dict[field].append(person_info[field])

    return pd.DataFrame(database_dict)

def get_combined_text(resumes, add_name=False):
    # define llm --------------------------------
    llm = ChatOpenAI(temperature=0)

    # personal info --------------------------------
    info_dict = {
        'Name':[],
        'Email':[],
        'Phone Number': [], 
    }

    # clean up resume text --------------------
    prompt_template = """Remove all the 1) useless characters and terms and 2) remove specific work experience/project description from the resume. Return a cleaned version:
    "{text}"
    CLEANED RESUME:"""
    prompt = PromptTemplate.from_template(prompt_template)
    llm = ChatOpenAI(temperature=0)
    summarize_chain = LLMChain(llm=llm, prompt=prompt)
    resume_sample_local = summarize_chain.run(RESUME_SAMPLE)

    # set up ----------------------------------------------------------------
    all_resume_text = ''
    status_bar = st.progress(0, text='Parsing resume...')

    for i, resume in enumerate(resumes):
        print(f'Parsing {i}')

        # info extraction ----------------------------------------------------------------
        # split text --------------------------------
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        splits = text_splitter.split_text(resume)
        splits = [Document(page_content=t) for t in splits[:]]

        # create vectorstore for retrieval --------------------------------
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(splits, embeddings, collection_name=f'candiate{i}')

        retrieval_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
        )

        # create vectorstore for retrieval --------------------------------
        question = 'Provide the full name of the person in the document in this format:{Full Name}'
        candidate = retrieval_chain.run(question)

        # info retreiver --------------------------------
        info_dict['Name'].append(candidate)
        info_fields = ['Phone Number', 'Email']
        for f in info_fields:
            query = QUESTION_SCHEMA[f]
            info_dict[f].append(retrieval_chain.run(query))
        

        if not add_name:
            template = ChatPromptTemplate.from_messages([
                ("system", DIRECT_PARSE_SYSTEM_MESSAGE),
                ("human", DIRECT_PARSE_TEMPLATE),
            ])

            messages = template.format_messages(
                resume_sample=resume_sample_local,
                resume_sample_output=DIRECT_PARSE_ANSWER,
                resume=resume,
            )
            all_resume_text += llm(messages).content

        else:
            resume = summarize_chain.run(resume)
            resume_text = ('\n').join([f'{candidate} {l}' for l in resume.split("\n")])
            all_resume_text += resume_text

        all_resume_text += '\n\n'

        status_bar.progress(int((i+1)/len(resumes)*100), text='Parsing resume...')

    return all_resume_text, info_dict