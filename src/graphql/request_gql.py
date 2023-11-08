from typing import Any, Dict, List, Optional

import requests
from requests.models import ProtocolError

HASURA_ENDPOINT_URL: str = "https://data.smclab.io/v1/graphql"

# **************************
# HELPER
# **************************
def _flatten_dict(response: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Flatten the elements in response."""
    tmp_response: List[Dict[str, Any]] = []
    for el in response:
        tmp_el: Dict[str, Any] = {}
        for key, val in el.items():
            if isinstance(val, dict):
                for sub_key, sub_val in val.items():
                    tmp_el[sub_key] = sub_val
            else:
                tmp_el[key] = val
        tmp_response.append(tmp_el)
    return tmp_response

def run_query(
    query: str, endpoint_url: str, headers: Optional[Dict[str, str]] = None, variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """A simple function to use requests.post to make the API call. Note the json= section."""
    request_data: Dict[str, Any] = {"query": query}
    if variables is not None:
        request_data["variables"] = variables

    try:
        if headers is None:
            response = requests.post(endpoint_url, json=request_data, verify=False)
        else:
            response = requests.post(endpoint_url, json=request_data, headers=headers, verify=False)
    except ConnectionResetError:
        print("==> ConnectionResetError")
        return {}
    except ProtocolError:
        print("==> ProtocolError")
        return {}
    except Exception as e:
        print(f"==> {e}")
        return {}

    return response.json()


# **************************
# GET / QUERIES
# **************************
def get_general_query(
    table_name: str,
    schema_name: str,
    return_nodes: str,
    where_clause: Optional[str] = None,
    args_clause: Optional[str] = None,
    distinct_on: Optional[str] = None,
    flatten_response: bool = True,
) -> List[Dict[str, Any]]:
    """
    Get all story_no of stories that are neither "Press Briefings" nor "Data Reports" by requesting GraphQL endpoint of smc database.
    Parameter:
    - where_clause: pass the complete clause within the where block, i.e.:
      'type: {{_nin: ["Press Briefing", "Data Report"]}}'
    - return_nodes: pass string of nodes to return, i.e.:
      "story_no"
    - args_clause: 
        - pass the complete args part, i.e.:
            "order_by: {publication_date: desc}"
        - default is None.
        - use with tracked FUNCTIONS, only!

    Example:
        get_general_query(
            table_name="story_meta",
            schema_name="smc",
            return_nodes="story_no"
            where_clause='type: {{_nin: ["Press Briefing", "Data Report"]}}',
            args_clause="order_by: {publication_date: desc}"
        )

    Returns List flattened on table level:
        {data: {table_name}: [{result: 1}, {result: 2}]} -> [{result: 1}, {result: 2}]
    """
    query_on: str = f"{schema_name}_{table_name}"

    if distinct_on:
        distinct_on = f"distinct_on: {distinct_on}"
    if where_clause and len(where_clause) > 0:
        where_clause = f"where: {{{where_clause}}}"

    # write empty str/empty arg if parameter is None
    query: str = f"""query getGeneralQuery {{
        {query_on}(
            {args_clause or ''}
            {where_clause or f"where: {{}}"}
            {distinct_on or ''}
        ) {{
            {return_nodes}
        }}
    }}"""

    # print(query)
    
    response: Dict[str, Any] = run_query(query=query, endpoint_url=HASURA_ENDPOINT_URL)
    # print(response)

    if flatten_response:
        flattened_response: List[Dict[str, Any]] = _flatten_dict(response["data"][query_on])

    return flattened_response