import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from mcq import generate_mcqs_with_description

app = Flask(__name__)
app.secret_key = "skillscore_secret"

# ========== SQLITE CONFIG ==========
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skillscore.db')


def get_db():
    """Get a database connection for the current request."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of each request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ========== AUTO-CREATE DB & TABLES ==========
def init_db():
    """Create the database and required tables if they don't exist."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student'
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[OK] Database ready at {DATABASE}")
    except Exception as e:
        print(f"[ERROR] Could not initialise database: {e}")


# ========== AUTH HELPERS ==========
def login_required(f):
    """Decorator: redirect to login if not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """Decorator: restrict access to specific roles."""
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in first.", "danger")
                return redirect(url_for("login"))
            if session.get("role") not in roles:
                flash("Access denied.", "danger")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated
    return wrapper


def current_user():
    """Return a dict with the current session user info."""
    return {
        "id": session.get("user_id"),
        "name": session.get("user_name", ""),
        "email": session.get("user_email", ""),
        "role": session.get("role", ""),
    }


@app.context_processor
def inject_user():
    """Make user info available in every template automatically."""
    return dict(user=current_user())


# ========== BASIC PAGES (public) ==========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


# ========== LOGIN ==========
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        try:
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        except Exception as e:
            flash(f"Database error: {e}", "danger")
            return render_template("login.html")

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user["role"] == "teacher":
                return redirect(url_for("teacher_dashboard"))
            else:
                return redirect(url_for("student_dashboard"))

        flash("Invalid email or password.", "danger")
        return render_template("login.html")

    return render_template("login.html")


# ========== REGISTER ==========
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password_raw = request.form.get("password", "")
        role = request.form.get("role", "student")

        if not name or not email or not password_raw:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        password = generate_password_hash(password_raw)

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, password, role)
            )
            db.commit()
        except Exception as e:
            flash(f"Registration failed: {e}", "danger")
            return render_template("register.html")

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ========== LOGOUT ==========
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


# ========== FORGOT PASSWORD ==========
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not email or not new_password:
            flash("All fields are required.", "danger")
            return render_template("forgot_pass.html")

        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("forgot_pass.html")

        try:
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if not user:
                flash("Email not found.", "danger")
                return render_template("forgot_pass.html")
            db.execute(
                "UPDATE users SET password=? WHERE email=?",
                (generate_password_hash(new_password), email)
            )
            db.commit()
            flash("Password updated! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("forgot_pass.html")


# ====================================================================
#                        ADMIN ROUTES
# ====================================================================
@app.route("/admin/dashboard")
@role_required("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html", active_page='dashboard')

@app.route("/admin/manage-users")
@role_required("admin")
def manage_users():
    db = get_db()
    users = db.execute("SELECT id, name, email, role FROM users ORDER BY id DESC").fetchall()
    return render_template("manage_users.html", active_page='users', users=users)

@app.route("/admin/add-user", methods=["POST"])
@role_required("admin")
def admin_add_user():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    role = request.form.get("role", "student")
    if name and email:
        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, generate_password_hash("default123"), role)
            )
            db.commit()
            flash(f"User '{name}' added with default password.", "success")
        except Exception as e:
            flash(f"Failed: {e}", "danger")
    return redirect(url_for("manage_users"))

@app.route("/admin/delete-user/<int:uid>")
@role_required("admin")
def admin_delete_user(uid):
    try:
        db = get_db()
        db.execute("DELETE FROM users WHERE id=?", (uid,))
        db.commit()
        flash("User deleted.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("manage_users"))

@app.route("/admin/all-exams")
@role_required("admin")
def all_exams():
    return render_template("all_exams.html", active_page='exams')

@app.route("/admin/reports")
@role_required("admin")
def reports():
    return render_template("reports.html", active_page='reports')

@app.route("/admin/settings")
@role_required("admin")
def settings():
    return render_template("settings.html", active_page='settings')

@app.route("/admin/audit-logs")
@role_required("admin")
def audit_logs():
    return render_template("audit_logs.html", active_page='audit_logs')


# ====================================================================
#                       TEACHER ROUTES
# ====================================================================
@app.route("/teacher/dashboard")
@role_required("teacher")
def teacher_dashboard():
    return render_template("teacher_dashboard.html", active_page='dashboard')

@app.route("/teacher/upload-notes")
@role_required("teacher")
def upload_notes():
    return render_template("upload_notes.html", active_page='upload_notes')

@app.route("/teacher/create-exam")
@role_required("teacher")
def create_exam():
    return render_template("create exam.html", active_page='create_exam')

@app.route("/teacher/view-results")
@role_required("teacher")
def view_results():
    return render_template("view_results.html", active_page='view_results')

@app.route("/teacher/exam-schedule")
@role_required("teacher")
def exam_schedule():
    return render_template("exam_schedule.html", active_page='exam_schedule')

@app.route("/teacher/attendance")
@role_required("teacher")
def attendance():
    return render_template("attendance.html", active_page='attendance')

@app.route("/teacher/subject-notes")
@role_required("teacher")
def teacher_subject_notes():
    return render_template("subject_notes.html", active_page='subject_notes')

@app.route("/teacher/placement-notes")
@role_required("teacher")
def teacher_placement_notes():
    return render_template("placement_notes.html", active_page='placement_notes')


# ====================================================================
#                       STUDENT ROUTES
# ====================================================================
@app.route("/student/dashboard")
@role_required("student")
def student_dashboard():
    return render_template("student_dashboard.html", active_page='dashboard')

@app.route("/student/profile")
@role_required("student")
def profile():
    return render_template("profile.html", active_page='profile')

@app.route("/student/subject-notes")
@role_required("student")
def subject_notes():
    return render_template("subject_notes.html", active_page='subject_notes')

@app.route("/student/placement-notes")
@role_required("student")
def placement_notes():
    return render_template("placement_notes.html", active_page='placement_notes')

@app.route("/student/take-exam")
@role_required("student")
def take_exam():
    return render_template("take_exam.html", active_page='take_exam')

@app.route("/student/aptitude")
@role_required("student")
def aptitude():
    return render_template("aptitude.html", active_page='aptitude')

@app.route("/student/exam-result")
@role_required("student")
def exam_result():
    return render_template("exam_result.html", active_page='exam_result')

@app.route("/student/upload", methods=["GET", "POST"])
@role_required("student")
def upload():
    mcqs = []
    if request.method == "POST":
        file = request.files.get("notes")
        if file and file.filename:
            text = file.read().decode("utf-8", errors="ignore")
            if text.strip():
                mcqs = generate_mcqs_with_description(text, num_questions=5)
            else:
                flash("Uploaded file is empty.", "danger")
        else:
            flash("Please upload a text file.", "danger")
    return render_template("upload.html", mcqs=mcqs, active_page='mcq_gen')


# ========== RUN ==========
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
