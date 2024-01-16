import langchain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

langchain.verbose = True


class GPT:
    def __init__(self):
        mail_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Please rewrite the following text into email format. "
                       "The sender has the name {lawyer_name}. "
                       "The recipient has the name {recipient_name}."),
            ("user", "{input}")
        ])

        mail_subject_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Please write a subject for the email."),
            ("user", "{input}")
        ])

        legal_explanation_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a world class lawyer. Please Explain the following legal term to a non-lawyer."
                       " Use simple language."),
            ("user", "The legal term you must explain: {legal_term}."
                     "\nIt was used in the following context: {context}"),
        ])

        llm = ChatOpenAI()

        self.mail_chain = mail_prompt_template | llm | StrOutputParser()
        self.mail_subject_chain = mail_subject_prompt_template | llm | StrOutputParser()
        self.legal_explanation_chain = legal_explanation_prompt_template | llm | StrOutputParser()

    def chat_to_mail(self, text, lawyer_name: str, recipient_name: str):
        return self.mail_chain.invoke({"input": text, "lawyer_name": lawyer_name, "recipient_name": recipient_name})

    def chat_to_mail_subject(self, text):
        return self.mail_subject_chain.invoke({"input": text})

    def legal_explain(self, legal_term, context):
        return self.legal_explanation_chain.invoke({"legal_term": legal_term, "context": context})
