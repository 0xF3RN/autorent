from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory
from db_connection import get_db_connection, get_db_connection_manager
from report_gen import create_rent_doc, create_service_doc, create_claim_doc


app = Flask(__name__)
app.secret_key = 'admin'

'''
никода, никогда не используйте этот проект для реферанса
ОН ПРОСТО УЖАСЕН
ПРОШУ НЕ ДЕЛАЙТЕ ЭТИХ ОШИБОК
Я ЕГО ДЕЛАЛ НА ОТВАЛИ
ХААХХААХАХАХ
Я НЕ ШУЧУ
ВОТ КАК ТО ТАК И ЖИВЕМ
'''
@app.route("/")
def root():
    if session.get('role') == 'admin':
        return render_template("admin.html")
    if session.get('role') == 'manager':
        return render_template("manager.html")
    return redirect(url_for("login"))


@app.route("/home")
def home():
    if session.get('role') == 'admin':
        return render_template("admin.html")
    if session.get('role') == 'manager':
        return render_template("manager.html")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND passwd = %s", (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        session["username"] = user[1]  
        session["role"] = user[3]  
        if user[3] == "admin":
            return redirect(url_for("admin"))
        elif user[3] == "manager":
            return redirect(url_for("manager"))
    else:
        error = "Неверный логин или пароль."
        return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin")
def admin():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin.html")


@app.route("/admin/automobile")
def admin_automobile():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/automobile.html")


@app.route("/admin/automobile/insert", methods=["GET","POST"])
def admin_automobile_insert():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    if request.method != "POST":
        return render_template("admin_cards/auto_actions/insert.html")
    id_automobile = request.form["id"]
    manufacturer = request.form["manufacturer"]
    registration_number = request.form["registration_number"]
    year_of_car_manufacturer = request.form["year_of_car_manufacture"]
    mileage = request.form["mileage"]
    air_conditioner = request.form["air_conditioner"]
    engine_capacity = request.form["engine_capacity"]
    luggage_capacity = request.form["luggage_capacity"]
    maintenance_date = request.form["maintenance_date"]
    cost_per_day = request.form["cost_per_day"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO automobile (id_automobile, manufacturer, registration_number, year_of_car_manufacture, mileage, air_conditioner, engine_capacity, luggage_capacity, maintenance_date, cost_per_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
        id_automobile, manufacturer, registration_number, year_of_car_manufacturer, mileage, air_conditioner, engine_capacity, luggage_capacity, maintenance_date, cost_per_day
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_automobile_view"))  


@app.route("/admin/automobile/view")
def admin_automobile_view():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""SET lc_monetary TO "ru_RU.UTF-8";SELECT * FROM automobile""")
    data = cur.fetchall()
    conn.close()
    columns = [desc[0] for desc in cur.description]
    return render_template("admin_cards/auto_actions/view.html", data=data, columns=columns)


@app.route("/admin/automobile/delete")
def admin_automobile_delete():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""SET lc_monetary TO "ru_RU.UTF-8";SELECT * FROM automobile""")
    data = cur.fetchall()
    conn.close()
    columns = [desc[0] for desc in cur.description]
    return render_template("admin_cards/auto_actions/delete.html", data=data, columns=columns)


@app.route("/admin/automobile/delete/<int:row_id>", methods=["DELETE"])
def delete_row(row_id):
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM automobile WHERE id_automobile = %s", (row_id,))
    conn.commit()
    conn.close()
    return "Успешно удалено", 200


@app.route("/admin/sql", methods=["GET", "POST"])
def admin_sql():
    if request.method != "POST":
        return render_template("admin_cards/sql.html", data=None, error=None)
    query = request.form["query"]
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return render_template("admin_cards/sql.html", data=data, error=None)
    except Exception as e:
        conn.close()
        return render_template("admin_cards/sql.html", data=None, error=e)


@app.route("/admin/type_of_work")
def admin_type_of_work():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/partner")
def admin_partner():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/service")
def admin_service():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/client")
def admin_client():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/employee")
def admin_employee():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/invoice")
def admin_invoice():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/claim")
def admin_claim():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/rent")
def admin_rent():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/admin/users")
def admin_users():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")


@app.route("/manager")
def manager():
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("manager.html")


@app.route("/manager/sql", methods=["GET", "POST"])
def manager_sql():
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    if request.method != "POST":
        return render_template("manager_cards/sql.html", data=None, error=None)
    query = request.form["query"]
    conn = get_db_connection_manager()
    cur = conn.cursor()
    try:
        cur.execute(query)
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return render_template("manager_cards/sql.html", data=data, error=None)
    except Exception as e :
        conn.close()
        return render_template("manager_cards/sql.html", data=None, error=e)


@app.route("/manager/report/invoice")
def manager_report_invoice():
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SET lc_monetary TO "ru_RU.UTF-8";
    SELECT id_rent, manufacturer, CONCAT(client_surname , ' ',client_name  , ' ', client_fathersname) AS fullname,
    start_of_rent, end_of_rent, rent_cost FROM client join rent on id_client = client_id join invoice on
    invoice_id = id_invoice join automobile on id_automobile = automobile_id """)
    data = cur.fetchall()
    conn.close()
    columns = [desc[0] for desc in cur.description]
    return render_template("manager_cards/report/invoice.html", data=data, columns=columns)


@app.route('/manage/report/invoice/generate_report/<int:row_id>')
def generate_report_invoice(row_id):
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SET lc_monetary TO "ru_RU.UTF-8";
    SELECT id_rent, manufacturer, CONCAT(client_surname , ' ',client_name  , ' ', client_fathersname) AS fullname,
    start_of_rent, end_of_rent, rent_cost FROM client join rent on id_client = client_id join invoice on
    invoice_id = id_invoice join automobile on id_automobile = automobile_id WHERE id_rent = %s""", (row_id,))
    data = cur.fetchone()
    create_rent_doc([data])
    cur.close()
    conn.close()
    directory = 'reports'
    filename = 'invoice.docx'
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/manager/report/TO")
def manager_report_TO():
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SET lc_monetary TO "ru_RU.UTF-8";
    SELECT  id_automobile, manufacturer, organization_name, legal_address, type_of_work, day_of_work
    FROM automobile
    JOIN service ON id_automobile = automobile_id
    JOIN type_of_work ON type_of_work_id = id_type_of_work
    join partner on parter_id = id_partner
    WHERE now()::date - day_of_work::date > 365""")
    data = cur.fetchall()
    conn.close()
    columns = [desc[0] for desc in cur.description]
    return render_template("manager_cards/report/TO.html", data=data, columns=columns)


@app.route('/manage/report/TO/generate_report/<int:row_id>')
def generate_report_TO(row_id):
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SET lc_monetary TO "ru_RU.UTF-8";
    SELECT  id_automobile, manufacturer, organization_name, legal_address, type_of_work, day_of_work
    FROM automobile
    JOIN service ON id_automobile = automobile_id
    JOIN type_of_work ON type_of_work_id = id_type_of_work
    join partner on parter_id = id_partner
    WHERE now()::date - day_of_work::date > 365 and id_automobile = %s""", (row_id,))
    data = cur.fetchone()
    create_service_doc([data])
    cur.close()
    conn.close()
    directory = 'reports'
    filename = 'TO.docx'
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/manager/report/claim")
def manager_report_claim():
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SET lc_monetary TO "ru_RU.UTF-8";
    SELECT id_claim, manufacturer, CONCAT(client_surname , ' ',client_name  , ' ', client_fathersname)
    AS fullname, date_of_creation, description  FROM client join rent on id_client = client_id join
    automobile on id_automobile = automobile_id join claim on claim_id = id_claim;""")
    data = cur.fetchall()
    conn.close()
    columns = [desc[0] for desc in cur.description]
    return render_template("manager_cards/report/claim.html", data=data, columns=columns)


@app.route('/manage/report/claim/generate_report/<int:row_id>')
def generate_report_claim(row_id):
    if session.get('role') not in ('admin','manager'):
        return render_template("unauthorized.html", role=session.get('role'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SET lc_monetary TO "ru_RU.UTF-8";
    SELECT id_claim, manufacturer, CONCAT(client_surname , ' ',client_name  , ' ', client_fathersname)
    AS fullname, date_of_creation, description  FROM client join rent on id_client = client_id join
    automobile on id_automobile = automobile_id join claim on claim_id = id_claim WHERE id_claim = %s""", (row_id,))
    data = cur.fetchone()
    create_claim_doc([data])
    cur.close()
    conn.close()
    directory = 'reports'
    filename = 'claim.docx'
    return send_from_directory(directory, filename, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)
