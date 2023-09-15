import os
from inquire.db import AejgDb
from inquire.gpt import AejgGpt


from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def ask(question) -> str:
    aejg_gpt = AejgGpt()
    aejg_db = AejgDb()

    # Step 1: OPENAI: NLP -> SQL
    # From user question, generate a SQL query
    sql_query = aejg_gpt.get_sql_query(question)
    print("Step 2: querying: " + sql_query)

    # Step 2: run SQL
    # Query AEJG SQL DB
    query_result = aejg_db.execute_query(sql_query)
    print("Step 3:query result: " + query_result)

    # Step 3: OPENAI: SQL -> NLP
    # have openai assess the sql result
    openai_answer = aejg_gpt.assess_result(query_result)
    return openai_answer


@app.route('/answer', methods=['POST'])
def answer():
    question = request.form.get('question')
    if not question:
        return redirect(url_for('index'))
    print('Step 1: Request for answer page received with question: %s' % question)

    openai_answer = ask(question)

    if openai_answer:
        return render_template('answer.html', openai_answer=openai_answer)
    else:
        print('Request for answer page received with no question or blank question -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
