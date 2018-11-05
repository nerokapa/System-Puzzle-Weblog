import datetime
import os
import psycopg2

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def index():
    # Connect to database
    conn = psycopg2.connect(host='db',
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'])
    cur = conn.cursor()

    # Get number of all GET requests
    sql_all_grouped = """SELECT source, COUNT(*) FROM weblogs GROUP BY source;"""
    cur.execute(sql_all_grouped)
    all_counted = dict(cur.fetchall())

    # Get number of all succesful requests
    sql_success_grouped = """SELECT source, COUNT(*) FROM weblogs WHERE status LIKE \'2__\' GROUP BY source;"""
    cur.execute(sql_success_grouped)
    success_counted = dict(cur.fetchall())
    total_suucess_count = success_counted["local"] + success_counted["remote"]
    total_count = all_counted["local"] + all_counted["remote"]
    remote_rate = "No remote entries yet" if all_counted["remote"] == 0 \
            else success_counted["remote"] / all_counted["remote"]
    local_rate = "No local entries yet" if all_counted["local"] == 0 \
            else success_counted["local"] / all_counted["local"]
    total_rate = "No entries yet" if total_count == 0 \
            else total_suucess_count / total_count
    return render_template(
            'index.html',
            remote_rate = remote_rate,
            local_rate = local_rate,
            total_rate = total_rate)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
