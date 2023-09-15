from promptflow import tool
import openai
import os
import requests
import re
import os

fo = open('./res/system_content.txt', 'r')
SYSTEM_CONTENT = str(fo.read())
fo = open('./res/website_scrap.txt', 'r')
ADDITIONAL_CONTENT = ' '.join(fo.readlines())
max_response_tokens = 250
token_limit = 4096
fo = open('./res/db_prompt.txt', 'r')
SQL_PROMPT = ' '.join(fo.readlines())
fo = open('./res/result_prompt.txt', "r")
RESULT_PROMPT = fo.readline()
fo = open('./res/result_prompt2.txt', "r")
RESULT_PROMPT2 = fo.readline()

fo.close()

class AejgGpt:
    def __init__(self):
        openai.api_version = os.getenv("OPENAI_API_VERSION")
        openai.api_key = os.getenv("AZURE_OPENAI_KEY")
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai.api_type = os.getenv("OPENAI_API_TYPE")
        self.deployment_id = 'gpt-35-turbo-16k'
        self.message = [
            {"role": "system", "content": SYSTEM_CONTENT+"\""+ADDITIONAL_CONTENT+"\""}
        ]

    # convert human language into ms sql query
    @tool
    def get_sql_query(self, user_prompt):
        self.message.append(
            {"role": "user", "content": SQL_PROMPT + user_prompt})
        response = openai.ChatCompletion.create(
            deployment_id=self.deployment_id,
            messages=self.message,
            temperature=0,
        )
        content_str = response["choices"][0]["message"].content
        # SQL data parsing, not fun but necessay
        # may still break from time to time when openai change reply format
        # uncomment next line to debug
        # print(content_str)
        s, e = 0, 0
        if "```" not in content_str:
            s = content_str.index(":")
        else:
            s = content_str.index("```")+2

        if ";" not in content_str:
            e = content_str.index("\n", s+5)
        else:
            e = content_str.index(";")

        sql_query = content_str[s+1: e].rstrip()

        return sql_query

    # translate sql result into human language
    @tool
    def assess_result(self, sql_result):
        self.message.append(
            {"role": "user", "content": RESULT_PROMPT + sql_result + RESULT_PROMPT2})
        response = openai.ChatCompletion.create(
            deployment_id=self.deployment_id,
            messages=self.message,
            temperature=0,
        )
        response_content = response["choices"][0]["message"].content
        return response_content
