from typing import Literal

from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel


class GraphComponent(BaseModel):
    type: Literal["node", "relationship"]
    name: str


parser = PydanticOutputParser(pydantic_object=GraphComponent)

find_graph_component_prompt = PromptTemplate(
    template="""
    select nodes and relationships that are most relevant to the question.
    [user question]
    {user_question}
    [node information]
    {node_information}
    [relationship information]
    {relationship_information}
    [format instructions]
    {format_instructions}
    type should be either node or relationship.
    """,
    input_variables=[
        "user_question",
        "node_information",
        "relationship_information",
    ],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
