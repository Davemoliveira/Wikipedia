import paramiko
import wikipedia as wikipedia

from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True


@app.route('/results')
def search():
    search_term = request.args.get('search_term')
    search_results = wiki_search(search_term)

    x = search_results[0].find("URL:")
    title = search_results[0][7:x]

    y = search_results[0].find("Content:")
    url = search_results[0][x+5:y]
    content = (search_results[0][y+9]) + "".join(search_results[1:])
    return render_template('results.html', title=title, url=url, content=content, search_results=search_results)




def wiki_search(search):
    host = '127.0.0.1'
    port = 2233
    username = 'user'
    password = 'x'

    # connect to server
    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.connect(hostname=host, port=port, username=username, password=password)
    stdin, stdout, stderr = con.exec_command('python3 /home/user/Downloads/originalwiki.py "' + search + '"')
    outerr = stderr.readlines()
    print("ERRORS: ", outerr)
    output = stdout.readlines()
    print("output:", output)
    for items in output:
        print(items)
        return output


@app.route('/')
def hello_world():
    return render_template('search.html')


if __name__ == '__main__':
    app.run()

