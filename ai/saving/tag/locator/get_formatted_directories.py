import json
import os
import requests


backend_url: str=str(os.getenv("BACKEND_API_URL"))

# TODO: parallelize this
def get_formatted_directories(current: str="", depth: int=0) -> str:
    current_directories: list[dict[str, str]]=_get_current_directories(current)
    
    result: str=""
    for next in current_directories:
        next_line: str="-"*depth+' '
        next_line+=f'{next["name"]} (id: {next["id"]})'
        next_result=get_formatted_directories(next["id"], depth+1)
        if next_result != "":
            next_line+='\n'+next_result+'\n'
            
        result+=next_line
        
    return result
        
def _get_current_directories(current: str) -> list[dict[str, str]]:
    endpoint=backend_url+"/tags"+("/root" if current=="" else f'/{current}/childTags')
    result=requests.get(endpoint).json()
    
    return result
