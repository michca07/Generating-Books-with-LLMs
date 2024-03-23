from utils import BaseEventChain, ChatOllama, ChatOpenAI, ChatAnthropic


class ChapterFrameworkChain(BaseEventChain):

    HELPER_PROMPT = """
    Generate a list of attributes that characterizes a thought-provoking philosophical non-fiction book, 
    including a consistent chain of ideas, which support the main framework of the book.
    List of attributes:"""

    PROMPT = """
    You are a writer and your job is to generate the framework for one and only one chapter of a philosophical non-fiction book. 
    You are provided with the subject, genre, style, title, profile, and the main framework of the book. 
    Additionally, you are provided with the framework of the previous chapters and the outline of the book.
    Make sure to generate a framework that describes accurately the ideas and arguments of the chapter. 
    Each chapter should have its own ideas and arguements, but should be consistent with 
    the other chapters and the overall framework of the book.
    The framework of the chapter should be consistent with the genre of the novel.
    The framework of the chapter should be according to the style of the book. 

    Consider the following attributes to write a stimulating and insightful book:
    {features}

    subject: {subject}
    genre: {genre}
    style: {style}
    title: {title}
    profile of the book: {profile}
    framework: {framework}

    Outline:
    {outline}

    Chapter Framework:
    {summaries}

    Return a detailled framework. DON'T refer to the title nor the chapter's name in the framework!
    Return the framework and only the framework of the ideas and supporting arguements in the chapter.
    Framework of {chapter}:"""

    def run(
        self,
        subject,
        genre,
        style,
        profile,
        title,
        framework,
        summaries_dict,
        chapter_dict,
        chapter,
    ):

        # features = ChatAnthropic(model_name="claude-3-opus-20240229").predict(self.HELPER_PROMPT)
        # features = ChatOpenAI(model="gpt-4-0125-preview").predict(self.HELPER_PROMPT)
        # features = ChatOpenAI(model="gpt-3.5-turbo-16k").predict(self.HELPER_PROMPT)
        features = ChatOllama(model="gemma:7b").predict(self.HELPER_PROMPT)
        # features = ChatOllama(model="mistral-openorca:latest").predict(self.HELPER_PROMPT)

        outline = "\n".join(
            [
                "{} - {}".format(chapter, description)
                for chapter, description in chapter_dict.items()
            ]
        )

        summaries = "\n\n".join(
            [
                "Framework of {}: {}".format(chapter, summary)
                for chapter, summary in summaries_dict.items()
            ]
        )

        return self.chain.predict(
            subject=subject,
            genre=genre,
            style=style,
            profile=profile,
            title=title,
            framework=framework,
            features=features,
            outline=outline,
            summaries=summaries,
            chapter=chapter,
        )


class IdeasChain(BaseEventChain):

    PROMPT = """
    You are a philosophical writer and your job is to come up with a detailed list of ideas discussed 
    in the current chapter of the book.
    Be very specific about the supporting arguements and traits of the different ideas.
    Those ideas describe the framework of that chapter and the supporting arguments of the different ideas
     should be in rigorous order. 
    You are provided with the subject, genre, style, title, profile, and the main framework of the book, and 
    also the framework of that chapter.
    Additionally, you are provided with the list of the ideas that were outlined in the previous chapters.
    The idea list should be consistent with the genre of the book.
    The idea list should be consistent with the style of the book.

    The each element of that list should be returned on different lines. Follow this template:

    Idea 1
    Idea 2
    ...
    Final idea

    subject: {subject}
    genre: {genre}
    style: {style}
    title: {title}
    profile of the book: {profile}
    framework: {framework}

    Ideas you outlined for previous chapters: {previous_ideas}

    Framework of the current chapter:
    {summary}

    Don't hesitate to create the necessary idaes to generate a meaningful framework.
    Return the ideas and only the ideas that capture the framework!
    Idea list for that chapter:"""

    def run(self, subject, genre, style, profile, title, framework, summary, idea_dict):

        previous_ideas = ""
        for chapter, ideas in idea_dict.items():
            previous_ideas += "\n" + chapter
            for idea in ideas:
                previous_ideas += "\n" + idea

        response = self.chain.predict(
            subject=subject,
            genre=genre,
            style=style,
            profile=profile,
            title=title,
            framework=framework,
            summary=summary,
            previous_ideas=previous_ideas,
        )

        return self.parse(response)

    def parse(self, response):

        idea_list = response.strip().split("\n")
        idea_list = [idea.strip() for idea in idea_list if idea.strip()]
        return idea_list


def get_ideas(subject, genre, style, profile, title, framework, chapter_dict):

    chapter_framework_chain = ChapterFrameworkChain()
    ideas_chain = IdeasChain()
    summaries_dict = {}
    idea_dict = {}

    for chapter, _ in chapter_dict.items():

        summaries_dict[chapter] = chapter_framework_chain.run(
            subject=subject,
            genre=genre,
            style=style,
            profile=profile,
            title=title,
            framework=framework,
            summaries_dict=summaries_dict,
            chapter_dict=chapter_dict,
            chapter=chapter,
        )

        idea_dict[chapter] = ideas_chain.run(
            subject=subject,
            genre=genre,
            style=style,
            profile=profile,
            title=title,
            framework=framework,
            summary=summaries_dict[chapter],
            idea_dict=idea_dict,
        )

    return summaries_dict, idea_dict
