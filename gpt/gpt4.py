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
                       "The recipient has the name {recipient_name}. "
                       "Do not alter the meaning of the text in any way, only its formatting."),
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

        emotional_suggestions_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Please give a suggestions to a lawyer what to do, based on the emotional state of the client "
                       "and the last message from the client. The suggestions should focus on handling the client's "
                       "emotions well. The suggestion should only be one sentence long."),
            ("user", "The client's emotional state:\n{emotional_state}.\n\nThe client's last message:\n{last_message}.")
        ])

        answer_suggestion_prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Please give a suggestions to a lawyer what to do, based on the last message from the client."),
            ("user", "The client's last message:\n{last_message}.")
        ])

        llm = ChatOpenAI(model_name="gpt-3.5-turbo")

        self.mail_chain = mail_prompt_template | llm | StrOutputParser()
        self.mail_subject_chain = mail_subject_prompt_template | llm | StrOutputParser()
        self.legal_explanation_chain = legal_explanation_prompt_template | llm | StrOutputParser()
        self.emotional_suggestions_chain = emotional_suggestions_prompt_template | llm | StrOutputParser()
        self.answer_suggestion_chain = answer_suggestion_prompt_template | llm | StrOutputParser()

    def chat_to_mail(self, text, lawyer_name: str, recipient_name: str):
        return self.mail_chain.invoke({"input": text, "lawyer_name": lawyer_name, "recipient_name": recipient_name})

    def chat_to_mail_subject(self, text):
        return self.mail_subject_chain.invoke({"input": text})

    def legal_explain(self, legal_term, context):
        return self.legal_explanation_chain.invoke({"legal_term": legal_term, "context": context})

    def emotional_suggestions(self, emotional_state, last_message):
        return self.emotional_suggestions_chain.invoke({"emotional_state": emotional_state, "last_message": last_message})

    def answer_suggestion(self, last_message):
        return self.answer_suggestion_chain.invoke({"last_message": last_message})
