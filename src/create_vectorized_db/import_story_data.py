from graphql.request_gql import get_general_query
import os
import json
from typing import Any, Dict, List

DATA_LOCATION = os.environ.get("DATA_LOCATION")

def import_story_data():
    # check if story data already exists
    if os.path.exists(f"{DATA_LOCATION}/story_metadata.json"):
        print("Story metadata found. Importing new stories only")
        with open(f"{DATA_LOCATION}/story_metadata.json", "r") as f:
            old_story_data = json.load(f)

        old_story_nos = [story["story_no"] for story in old_story_data]

        story_data = get_general_query(
            table_name="story_meta",
            schema_name="smc",
            return_nodes="""
                story_no, 
                title, 
                type, 
                url, 
                ressort, 
                publication_date, 
                expert_statements {
                    expert_affiliation, 
                    expert_name, 
                    statement,
                    question
                },
                smc_content {
                    teaser
                }""",
            where_clause=f'type: {{_nin: ["Press Briefing", "Data Report"]}}, story_no: {{_nin: {old_story_nos}}}',
            args_clause="order_by: {publication_date: desc}"
        )

    else:
        print("No story metadata found. Importing all stories")
        old_story_nos = []
        story_data = get_general_query(
            table_name="story_meta",
            schema_name="smc",
            return_nodes="""
                story_no, 
                title, 
                type, 
                url, 
                ressort, 
                publication_date, 
                expert_statements {
                    expert_affiliation, 
                    expert_name, 
                    statement,
                    question
                },
                smc_content {
                    teaser
                }""",
            where_clause='type: {_nin: ["Press Briefing", "Data Report"]}',
            args_clause="order_by: {publication_date: desc}"
        )

    return story_data, old_story_nos

def process_story_data(story_data: List[Dict[str, Any]], old_story_nos: List[str]):
    
    story_metadata: List[Dict[str, Any]] = []
    for story in story_data:
        print(story["story_no"])
        # keep only stories with expert statements and teaser
        if len(story["expert_statements"]) == 0 or story["smc_content"][0]["teaser"] == "":
            continue
        
        # create txt files for each story teaser and story statement   
        story_teaser = f'{story["title"]}\n\n{story["smc_content"][0]["teaser"]}'
        with open(f"{DATA_LOCATION}/story_teaser/{story['story_no']}.txt", "w") as f:
            f.write(story_teaser)

        statements_metadata: List[Dict[str, Any]] = []
        expert_statements = story["expert_statements"]

        if story["type"] == "Science Response": # statement_block for each answer by expert and question -> group by expert
            statements_grouped_by_expert: Dict[str, Dict[str, str]] = {}
            for statement_block in expert_statements:
                expert_name = statement_block["expert_name"]
                question = statement_block["question"]
                question = question if question != None else ""
                if expert_name not in statements_grouped_by_expert.keys():
                    statements_grouped_by_expert[expert_name] = {
                        "statement": f"{question}\n\n{statement_block['statement']}",
                        "expert_name": expert_name,
                        "expert_affiliation": statement_block["expert_affiliation"],
                    }
                else:
                    new_statement = f"{question}\n\n{statement_block['statement']}"
                    current_statements = statements_grouped_by_expert[expert_name]["statement"]
                    statements_grouped_by_expert[expert_name]["statement"] = f"{current_statements}\n\n{new_statement}"

            expert_statements = list(statements_grouped_by_expert.values())

        for i, statement_block in enumerate(expert_statements):
            expert_statement_parts = statement_block["statement"].split("\n")
            expert_statement_parts = [p.strip('" "„“"”" "') for p in expert_statement_parts if (p != "" and p != " ")]
            
            expert_statement = "\n\n".join(expert_statement_parts)            
            story_statement = f'{story["title"]}\n\n{expert_statement}'

            statements_metadata.append({
                "statement_no": f"{story['story_no']}_{i}",
                "expert_name": statement_block["expert_name"],
                "expert_affiliation": statement_block["expert_affiliation"],
            })
            
            with open(f"{DATA_LOCATION}/story_statement/{story['story_no']}_{i}.txt", "w") as f:
                f.write(story_statement)
        
        # Append story metadata 
        metadata = {
            "story_no": story["story_no"],
            "type": story["type"],
            "url": story["url"],
            "ressort": story["ressort"],
            "publication_date": story["publication_date"],
            "statements_metadata": statements_metadata
        }
        story_metadata.append(metadata)
    
    if len(old_story_nos) > 0:
        with open(f"{DATA_LOCATION}/story_metadata.json", "r") as f:
            old_story_metadata = json.load(f)
        
        story_metadata = old_story_metadata + story_metadata

        with open(f"{DATA_LOCATION}/story_metadata.json", "w") as f:
            json.dump(story_metadata, f, indent=2)
    else:
        with open(f"{DATA_LOCATION}/story_metadata.json", "w") as f:
            json.dump(story_metadata, f, indent=2)

if __name__ == "__main__":
    story_data, old_story_nos = import_story_data()
    process_story_data(story_data, old_story_nos)

