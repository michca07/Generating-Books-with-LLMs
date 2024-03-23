from langchain.chains import LLMChain

from langchain.chat_models import ChatOpenAI
from langchain_community.llms import ollama
from langchain_community.chat_models import ChatOllama
from langchain_anthropic import ChatAnthropic


class BaseStructureChain:

    PROMPT = ""

    def __init__(self) -> None:

        # self.llm = ChatAnthropic(model_name="claude-3-opus-20240229")
        # self.llm = ChatOpenAI(model="gpt-4-0125-preview")
        # self.llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
        self.llm = ChatOllama(model="gemma:7b")
        # self.llm = ChatOllama(model="mistral-openorca:latest")

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True


class BaseEventChain:

    PROMPT = ""

    def __init__(self) -> None:

        # self.llm = ChatAnthropic(model_name="claude-3-opus-20240229")
        # self.llm = ChatOpenAI(model="gpt-4-0125-preview")
        # self.llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
        self.llm = ChatOllama(model="gemma:7b")
        # self.llm = ChatOllama(model="mistral-openorca:latest")

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True
