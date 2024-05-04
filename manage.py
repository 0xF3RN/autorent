from flask import Flask, render_template, redirect, url_for, request, session
from db_connection import get_db_connection

app = Flask(__name__)
app.secret_key = 'admin'

# рут -> логин
@app.route("/")
def root():
    if session.get('role') == 'admin':
        return render_template("admin.html")
    if session.get('role') == 'manager':
        return render_template("manager.html")
    return redirect(url_for("login"))

# хоум, для быстрого редиректа на хоумпйдж в зависимости от роли
@app.route("/home")
def home():
    if session.get('role') == 'admin':
        return render_template("admin.html")
    if session.get('role') == 'manager':
        return render_template("manager.html")
    return redirect(url_for("login"))

# логин
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND passwd = %s", (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session["username"] = user[1]  # хранение юзернейма в сессии
            session["role"] = user[3]  # хранение роли в сессии
            if user[3] == "admin":
                return redirect(url_for("admin"))
            elif user[3] == "manager":
                return redirect(url_for("manager"))
        else:
            error = "Неверный логин или пароль."
            return render_template("login.html", error=error)
    return render_template("login.html")

# логаут
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# страница админа
@app.route("/admin")
def admin():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin.html")

#TODO наладить взаимодействие страниц с БД
@app.route("/admin/automobile")
def admin_automobile():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/automobile.html")

#инсерт в таблицу automobile
@app.route("/admin/automobile/insert", methods=["GET","POST"])
def admin_automobile_insert():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    if request.method == "POST":
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
    return render_template("admin_cards/auto_actions/insert.html")

#просмотр записей automobile
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


@app.route("/admin/type_of_work")
def admin_type_of_work():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/type_of_work.html")

#TODO partner
@app.route("/admin/partner")
def admin_partner():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/partner.html")

@app.route("/admin/service")
def admin_service():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/service.html")

@app.route("/admin/client")
def admin_client():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/client.html")

@app.route("/admin/employee")
def admin_employee():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/employee.html")

@app.route("/admin/invoice")
def admin_invoice():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/invoice.html")

@app.route("/admin/claim")
def admin_claim():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/claim.html")

@app.route("/admin/rent")
def admin_rent():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/rent.html")

@app.route("/admin/users")
def admin_users():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin_cards/users.html")

#TODO придумать будет делать менеджер
@app.route("/manager")
def manager():
    return render_template("manager.html")

if __name__ == "__main__":
    app.run(debug=True)