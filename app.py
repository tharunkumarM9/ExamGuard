import os
from flask import Flask, redirect, request, render_template, session, redirect 
from database import init_db, get_db
from werkzeug.security import check_password_hash, generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from database import init_db, get_db
from camera import capture_photo

app = Flask(__name__)
app.secret_key = "examguard_secret_key"
upload_folder = "static/uploads"

@app.route("/capture-photo", methods =["POST"])
def captureCandidatephoto():
    photo = request.files.get("photo")
    if not photo:
        return {
            "success" : "False",
            "message" : "Photo not Received"
        },400
    image_data = photo.read()
    photo_path = capture_photo(image_data)
    if not photo_path:
        return {
            "success": "False",
            "message": "could not process photo"
        },400
    return {
        "success" : "True",
        "message" : "Photo captured Successfully",
        "photo_path": photo_path
    },200

print(app.url_map)
init_db()


@app.route("/")
def home():
    return "Welcome to Exam Guard"


# @app.route("/register", methods=["GET", "POST"])
# def register():

#     if request.method == "POST":

#         name = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]
#         hashed_password = generate_password_hash(password)
#         print(f"Name: {name}, Email: {email}, Password: {hashed_password}")
#         photo= request.files.get("photo")

#         if not photo or photo.filename == "":
#             return "please select a photo"


    #     os.makedirs(upload_folder, exist_ok=True)
    #     filename=secure_filename(photo.filename)
    #     photo_path=os.path.join(upload_folder, filename)
    #     photo.save(photo_path)

    #     connection = get_db()

    #     connection.execute(
    #         """
    #         INSERT INTO candidates
    #         (name, email, password, photo)
    #         VALUES (?, ?, ?, ?)
    #         """,
    #         (name, email, hashed_password, photo_path)
    #     )

    #     connection.commit()
    #     connection.close()

    #    # return "Registration successful" 
    #     return redirect("/login") 

    # return render_template("register.html")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
       # photo = request.files.get('candidate_photo')

        if not username or not email or not password:
            return render_template('register.html', error="Please fill in all required fields.")
        photo_path = session.get("capture_photo")
        if not photo_path:
            return render_template('register.html', error="Please capture a photo before registering.")
    try:    
        connection = get_db()
        print("candidate email:", email)

        
    
        
        # Check if email is already registered
        # connection.execute("SELECT id FROM candidates WHERE email = ?", (email,))
        # if connection.fetchone():
        #     connection.close()
        #     return render_template('register.html', error="An account with this email already exists.")

        connection.execute(
            """
            INSERT INTO candidates(name, email, password, photo)
            VALUES(?, ?, ?, ?)
            """,
            (username, email, generate_password_hash(password), photo_path)
        )
        connection.commit()
        # connection.close()
        session.pop("capture_photo", None)
        print("Registration successful for:", username)

        # return render_template('register.html', success=True, username=username)
        print("Registration successful for:", username)
        print("Redirecting to login page...")
        return redirect("/login")
        print("Registration successful for:")
    except Exception as e:
        connection.rollback()
    
        print("Error during registration:", e)
        return render_template('register.html', error="An error occurred during registration. Please try again.")
    finally:
        connection.close()

    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db()

        candidate = connection.execute(
            """
            SELECT *
            FROM candidates
            WHERE email = ?  
            """,
            (email,)
        ).fetchone()

        connection.close()

        if candidate and check_password_hash(candidate["password"], password):
            session["candidate_id"] = candidate["id"]
            return redirect("/dashboard")

        return "Invalid email or password"

    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db()

        candidate = connection.execute(
            """
            SELECT *
            FROM candidates
            WHERE email = ?  
            """,
            (email,)
        ).fetchone()

        connection.close()

        if candidate and check_password_hash(candidate["password"], password):
            session["candidate_id"] = candidate["id"]
            return redirect("/dashboard")

        return "Invalid email or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "candidate_id" not in session:
        return "Please login first"

    return render_template("dashboard.html")


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")




if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)