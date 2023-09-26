import psycopg2
from psycopg2.extras import RealDictCursor
import random
from config import Config


def kon_connection():
    c = psycopg2.connect(user=Config.POSTGRES_CREDS["user"],
                         password=Config.POSTGRES_CREDS["password"],
                         host=Config.POSTGRES_CREDS["host"],
                         port=Config.POSTGRES_CREDS["port"],
                         database=Config.POSTGRES_CREDS["database"])
    return c


conn = kon_connection()
cur = conn.cursor(cursor_factory=RealDictCursor)


def close_connection():
    try:
        global conn
        global cur
        if conn:
            if cur:
                cur.close()
            conn.close()
        print("connection closed")
    except Exception as e:
        print("Some error occured while closing connection: ", e)


def reconnect():
    global conn
    global cur
    conn = kon_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    print("Reconnected database NOKI!")


# cols: a list of column names
# args: a dict of (column: value) pairs
def select_by_query(table_name, cols, args=None, unique=True, is_or=False, is_view=False):
    select_cols = "*"
    if len(cols) > 0:
        select_cols = ", ".join(cols)
    columns = []
    values = []
    if args:
        for k, v in args.items():
            columns.append(str(k) + "=%s")
            value = "'" + str(v) + "'"
            values.append(value)
    where_clause = ""
    if len(columns) > 0:
        where_clause = " WHERE " + " AND ".join(columns)
    if is_or:
        where_clause = " WHERE " + " OR ".join(columns)
    if is_view:
        query = "SELECT " + select_cols + " FROM " + table_name + where_clause % tuple(values)
    else:
        query = "SELECT " + select_cols + " FROM \"" + table_name + "\"" + where_clause % tuple(values)
    cur.execute(query)
    if unique:
        res = cur.fetchone()
    else:
        res = cur.fetchall()
    conn.commit()
    return res


def get_by_ids_in(table, id_column, ids):
    query = f'select * from {table} where {id_column} in (' + "'" + "','".join(ids) + "')"
    cur.execute(query)
    return cur.fetchall()


def insert_row_query(table_name, args):
    col_str = "(" + ", ".join(args.keys()) + ")"
    values = []
    for v in args.values():
        if type(v) == str:
            v1 = v.replace("'", "''")
        else:
            v1 = v
        values.append("'" + str(v1) + "'")
    val_str = "(" + ", ".join(values) + ")"
    query = "INSERT INTO " + "\"" + table_name + "\" " + col_str + " VALUES " + val_str
    cur.execute(query)
    conn.commit()


# update x set a = 'aa', b = 're' where c = 'd';
def update_row_query(table_name, cols, conditions):
    values = []
    where_conds = []
    for k, v in cols.items():
        v1 = v.replace("'", "''")
        values.append(str(k) + "=" + "'" + str(v1) + "'")
    for k, v in conditions.items():
        where_conds.append(str(k) + "=" + "'" + str(v) + "'")
    val_str = ", ".join(values)
    where_str = " AND ".join(where_conds)
    query = "UPDATE " + "\"" + table_name + "\" SET " + val_str + " WHERE " + where_str
    cur.execute(query)
    conn.commit()


# Inserts a new user to the database, WITH random_id, enter all entries
def insertUser(userid, username, deployment_id, referral_code):
    random_id = random.randint(0, 1)
    referred_by = referral_code
    referral_code = username[-5:]
    print("insertUser(userid, username, deployment_id, random_id, referred_by, referral_code) ",
          [userid, username, deployment_id, random_id, referred_by, referral_code])
    insert_row_query("userinfo", {"userid": userid, "username": username, "deployment_id": deployment_id, "random_id": random_id, "referred_by": referred_by, "referral_code": referral_code})




def getRandomId(userid):
    print("getRandomId(userid) ", userid)
    res = select_by_query("userinfo", ["random_id"], {"userid": userid})
    return res["random_id"]


def get_deployment_by_name(deployment_name):
    res = select_by_query("deployment", [], {"deployment_name": deployment_name})
    return res


def get_deployment_by_user_start_message(user_start_message):
    res = select_by_query("deployment", [], {"user_start_message": user_start_message})
    return res


def get_user_by_id(userid):
    res = select_by_query("userinfo", [], {"userid": userid})
    return res


def update_username(userid, new_username):
    query = "UPDATE userinfo SET username=\'" + new_username + "\' WHERE userid=\'" + userid + "\'"
    cur.execute(query)
    conn.commit()


# *** noki v2 *** #
def get_response_by_user_step_deployment(user_id, step_name, deployment_name):
    res = select_by_query("response_v2", [], {"user_id": user_id, "step_name": step_name,
                                              "deployment_name": deployment_name}, unique=False)
    return res


def insert_response(user_id, step_name, answer, deployment_name, question, question_type, hashed_user_id):
    insert_row_query("response_v2", {"user_id": user_id, "step_name": step_name,
                                     "answer": answer, "deployment_name": deployment_name,
                                     "question": question, "question_type": question_type,
                                     "hashed_user_id": hashed_user_id})


def insert_followup(user_id, status, followup_on, from_deployment, to_deployment, repeat_every, end_date):
    columns = {"user_id": user_id, "status": status,
               "followup_on": followup_on, "from_deployment": from_deployment,
               "to_deployment": to_deployment, "repeat_every": repeat_every}
    if end_date is not None and end_date != '':
        columns['end_date'] = end_date
    insert_row_query("followup", columns)


def get_active_followup(user_id, from_deployment, to_deployment):
    res = select_by_query("followup", [], {"user_id": user_id, "status": "active", "from_deployment": from_deployment,
                                           "to_deployment": to_deployment}, unique=False)
    return res


def set_followup_status_ignore(user_id, status, from_deployment, to_deployment):
    query = f"UPDATE followup SET status='ignore' WHERE user_id='{user_id}' AND status='{status}' AND " \
            f"from_deployment='{from_deployment}' AND to_deployment='{to_deployment}' "
    cur.execute(query)
    conn.commit()


def followup_opt_out(user_id):
    query = f"UPDATE followup SET status='opt_out' WHERE user_id='{user_id}' AND status='active' "
    cur.execute(query)
    conn.commit()


def get_valid_followups(status):
    query = f"select * from followup f where followup_on <= current_date and status = '{status}' and " \
            f"(end_date is null or end_date >= current_date) and " \
            f"(last_successful_followup is null or last_successful_followup < followup_on)"
    cur.execute(query)
    return cur.fetchall()


def update_followup(status, id, followup_on, last_successful_followup):
    if last_successful_followup:
        query = f"UPDATE followup SET status='{status}', followup_on='{followup_on}', " \
                f"last_successful_followup='{last_successful_followup}' WHERE id='{id}' "
    else:
        query = f"UPDATE followup SET status='{status}', followup_on='{followup_on}' WHERE id='{id}' "
    cur.execute(query)
    conn.commit()


def get_all_deployments():
    results = select_by_query(table_name='deployment',
                           cols=['deployment_name', 'instance_name', 'user_start_message', 'comments'],
                           unique=False)
    return results


def insert_deployment(deployment_name, instance_name, script, user_start_message, comments):
    insert_row_query("deployment", {"deployment_name": deployment_name, "instance_name": instance_name,
                                    "script": script, "user_start_message": user_start_message,
                                    "comments": comments})


def insert_deployment_snapshot(deployment_name, instance_name, script, user_start_message, comments):
    insert_row_query("deployment_snapshot", {"deployment_name": deployment_name, "instance_name": instance_name,
                                             "script": script, "user_start_message": user_start_message,
                                             "comments": comments})


def update_deployment(deployment_name, instance_name, script, user_start_message, comments):
    update_row_query("deployment", {"instance_name": instance_name,
                                    "script": script, "user_start_message": user_start_message,
                                    "comments": comments}, {"deployment_name": deployment_name})


def get_forecast(month_val, year):
    query = f"select * from noki_forecast where issue_season_end = {month_val} and issue_year = {year}"
    cur.execute(query)
    res = cur.fetchone()
    conn.commit()
    return res


def get_deployment_stats(deployment_name):
    query = f"select rv.step_name , rv.question , count(*) as cnt from public.response_v2 rv " \
            f"where rv.deployment_name = '{deployment_name}' group by rv.step_name , rv.question;"
    cur.execute(query)
    res = cur.fetchall()
    conn.commit()
    return res


def get_unique_deployment_stats(deployment_name):
    query = f"select step_name , question , count(*) as cnt from (select rv.step_name , rv.question , " \
            f"rv.hashed_user_id , count(*) as cnt from public.response_v2 rv where rv.deployment_name = '{deployment_name}' " \
            f"group by rv.step_name , rv.question, rv.hashed_user_id) rvg  group by rvg.step_name, rvg.question"
    cur.execute(query)
    res = cur.fetchall()
    conn.commit()
    return res


def rollback_on_error():
    try:
        conn.rollback()
    except psycopg2.Error as e:
        print(f"Error on rollback! Error: {e} \nTrying to reconnect...")
        close_connection()
        reconnect()

