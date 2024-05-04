from flask import Flask, render_template, redirect, url_for, request, session
import psycopg2


app = Flask(__name__)
app.secret_key = 'admin'

# креды postgres
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "12345"

# подключение к бд
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# рут -> логин
@app.route("/")
def root():
    return redirect(url_for("login"))

# логин
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # подключение к бд
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
            error = "Invalid username or password."
            return render_template("login.html", error=error)
    return render_template("login.html")

# страница админа
@app.route("/admin")
def admin():
    if session.get('role') != 'admin':
        return render_template("unauthorized.html", role=session.get('role'))
    return render_template("admin.html")

#TODO наладить взаимодействие страниц с БД
@app.route("/admin/automobile")
def admin_automobile():
    return render_template("admin_cards/automobile.html")

@app.route("/admin/type_of_work")
def admin_type_of_work():
    return render_template("admin_cards/type_of_work.html")

@app.route("/admin/partner")
def admin_partner():
    return render_template("admin_cards/partner.html")

@app.route("/admin/service")
def admin_service():
    return render_template("admin_cards/service.html")

@app.route("/admin/client")
def admin_client():
    return render_template("admin_cards/client.html")

@app.route("/admin/employee")
def admin_employee():
    return render_template("admin_cards/employee.html")

@app.route("/admin/invoice")
def admin_invoice():
    return render_template("admin_cards/invoice.html")

@app.route("/admin/claim")
def admin_claim():
    return render_template("admin_cards/claim.html")

@app.route("/admin/rent")
def admin_rent():
    return render_template("admin_cards/rent.html")

@app.route("/admin/users")
def admin_users():
    return render_template("admin_cards/users.html")

#TODO придумать будет делать менеджер
@app.route("/manager")
def manager():
    return render_template("manager.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)