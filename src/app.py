from dotenv import load_dotenv

load_dotenv()

from structure import get_structure
from ideas import get_ideas
from writing import write_book
from publishing import DocWriter

subject = """
The subject of the book is the intersection of AI and Philosophy. 
This includes exploring philosophical questions arising from AI technology, 
examining ethical implications, discussing the nature of intelligence, consciousness, 
agency, and autonomy in AI systems, and considering the impact of AI on society, 
culture, and human existence.
"""

profile = """
This interdisciplinary book aims to provide a comprehensive exploration of the philosophical 
dimensions of artificial intelligence (AI) for a diverse audience interested in both AI and 
philosophy. It targets academics, researchers, students of philosophy or computer science, 
professionals in AI development, and general readers intrigued by the societal implications of AI. 
By bridging the gap between philosophy and AI, the book delves into key themes such as ethics and morality, 
consciousness and agency, epistemology and knowledge, and socio-cultural impacts. Through an interdisciplinary 
approach drawing from philosophy, cognitive science, computer science, psychology, and sociology, each chapter 
offers historical context, theoretical frameworks, current research findings, and speculative considerations 
for the future, fostering critical thinking and informed discourse on the ethical and societal implications of AI.
"""

style = "Analytical-Speculative-Historical"
genre = "Non-fiction: Philosophy of Technology/Science"

doc_writer = DocWriter()

title, framework, chapter_dict = get_structure(subject, genre, style, profile)
summaries_dict, idea_dict = get_ideas(
    subject, genre, style, profile, title, framework, chapter_dict
)

book = write_book(genre, style, profile, title, framework, summaries_dict, idea_dict)

doc_writer.write_doc(book, chapter_dict, title)
