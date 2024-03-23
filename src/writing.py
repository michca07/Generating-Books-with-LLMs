from utils import BaseEventChain


class WriterChain(BaseEventChain):

    PROMPT = """
    You are a philosophical book writer. The book is described by a list of ideas. 
    You have already written the book up to the last idea. 
    Your job is to generate the paragraphs of the book about the new idea.
    You are provided with a the title, the framework of the book, the profile of the book, 
    and a framework of the current chapter.
    Make sure the paragraphs are consistent with the framework of the chapter.
    Additionally you are provided with the list of ideas you have already written about.
    The paragraphs should be consistent with the genre of the book.
    The paragraphs should be consistent with the style of the book.

    Genre: {genre}
    Style: {style}
    Profile of the book: {profile}
    Title: {title}
    Framework of the book: {framework}

    Previous ideas: {previous_ideas}
    Current Chapter summary: {summary}
    Previous paragraphs: {previous_paragraphs}
    
    New idea you need to write about now: {current_idea}
    
    You are the author and write the paragraphs as if they were part of the book.
    The idea should be well supported by valid arguments, illustrated with clear examples, and endorsed by 
    historical facts o events. 
    Do Not start any paragraph with "In conclusion" or "In summary"!
    Make sure each sentence in each paragraph is complete! Do NOT leave any paragraph incomplete!
    Make sure each paragraph is more than 6 lines!  
    DON'T refer to the author nor the chapters in the paragraphs!
    Only write the paragraphs related to that idea with the necessary arguements, examples, and related historical facts.
    Paragraphs of the book describing that idea:"""

    def run(
        self,
        genre,
        style,
        profile,
        title,
        framework,
        previous_ideas,
        summary,
        previous_paragraphs,
        current_idea,
    ):

        previous_ideas = "\n".join(previous_ideas)

        return self.chain.predict(
            genre=genre,
            style=style,
            title=title,
            profile=profile,
            framework=framework,
            previous_ideas=previous_ideas,
            summary=summary,
            previous_paragraphs=previous_paragraphs,
            current_idea=current_idea,
        )


def write_book(genre, style, profile, title, framework, summaries_dict, idea_dict):

    writer_chain = WriterChain()
    previous_ideas = []
    book = {}
    paragraphs = ""

    for chapter, idea_list in idea_dict.items():

        book[chapter] = []

        for idea in idea_list:

            paragraphs = writer_chain.run(
                genre=genre,
                style=style,
                profile=profile,
                title=title,
                framework=framework,
                previous_ideas=previous_ideas,
                summary=summaries_dict[chapter],
                previous_paragraphs=paragraphs,
                current_idea=idea,
            )

            previous_ideas.append(idea)
            book[chapter].append(paragraphs)

    return book
