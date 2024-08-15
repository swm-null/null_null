from fastapi import HTTPException
import openai
import os
from dotenv import load_dotenv
import re
import logging

load_dotenv()

def get_regex(q: str, country: str="korea") -> str:
    res=openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                You're an expert at listening to customer requests and building regexes.
                If they give you an example, you make the most of it.
                When you find the right answer, just print the expression.

                I've included a few examples for your reference, as per request.
                The customer is asking a question from {country}. Please give an answer that suits customer's country.

                Don't add ^ or $ to a pattern unless you're asking to create a regex that begins or ends with that pattern.
             
                # -- Example --
                # 주민등록번호: \\d{6}-\\d{7}
                # 전화번호: \\d{2,3}-\\d{3,4}-\\d{4}
            """},
            {"role": "user", "content": q}
        ],
        temperature=0,
    )
    ret=str(res.choices[0].message.content)
    logging.info("[RG] regex result: %s", ret)
    
    try:
        re.compile(ret) # check the returned regex
    except:
        logging.error("[RG] Failed regex validation: %s", ret)
        raise HTTPException(status_code=500, headers={"RG": "Failed to get regex."})
    
    return ret