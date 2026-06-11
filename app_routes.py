from flask import render_template, request, redirect, session, flash, jsonify
from models.opportunity import Opportunity
from models.user import User
from groq_ai import career_advice
from mochi_engine import calculate_match
from models.application import Application
from extensions import db


def register_routes(app):

 # ---------------- HOME ----------------
    @app.route("/")
    def home():
        return render_template("index.html")


    # ---------------- SIGNUP ----------------
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role", "candidate")

            user = User(username=username, email=email, role=role)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return redirect("/login")

        return render_template("signup.html")


    # ---------------- LOGIN ----------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            print("EMAIL:", email)

            user = User.query.filter_by(email=email).first()

            print("USER:", user)

            if user:
                print("HASH:", user.password_hash)
                print("PASSWORD MATCH:", user.check_password(password))

            if user and user.check_password(password):
                print("LOGIN SUCCESS")

                session["user_id"] = user.id
                session["username"] = user.username
                session["role"] = user.role

                return redirect("/dashboard")

            print("LOGIN FAILED")
            return redirect("/login")

        return render_template("login.html")
    # ---------------- LOGOUT ----------------
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")


    # ---------------- DASHBOARD ----------------
    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            return redirect("/login")

        user = User.query.get(session["user_id"])

        if user.role == "recruiter":
            return render_template("dashboard_recruiter.html", user=user)

        return render_template("dashboard_candidate.html", user=user)
    # ---------------- OPPORTUNITIES ----------------
    @app.route("/opportunities")
    def opportunities():

        jobs = Opportunity.query.order_by(Opportunity.id.desc()).all()

        user_skills = ""
        if "user_id" in session:
            user = User.query.get(session["user_id"])
            user_skills = user.skills or ""

        enriched_jobs = []

        for job in jobs:
            score, reason = calculate_match(user_skills, job.skills)

            enriched_jobs.append({
                "job": job,
                "score": score,
                "reason": reason
            })

        # 🔥 SORT BY MATCH SCORE (KEY UPGRADE)
        enriched_jobs.sort(key=lambda x: x["score"], reverse=True)

        # 🔥 TOP RECOMMENDATIONS
        top_jobs = enriched_jobs[:5]

        return render_template(
            "opportunities.html",
            jobs=enriched_jobs,
            top_jobs=top_jobs
        )
    # ---------------- RECRUITER ----------------
    @app.route("/recruiter", methods=["GET", "POST"])
    def recruiter():
        if request.method == "POST":
            job = Opportunity(
                title=request.form["title"],
                company=request.form["company"],
                description=request.form["description"],
                skills=request.form["skills"]
            )
            db.session.add(job)
            db.session.commit()
            return redirect("/opportunities")

        return render_template("recruiter.html")


    # ---------------- DELETE ----------------
    @app.route("/delete-job/<int:job_id>", methods=["POST"])
    def delete_job(job_id):
        job = Opportunity.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        return redirect("/opportunities")


    # ---------------- EXTRA PAGES ----------------
    @app.route("/discover")
    def discover():
        return render_template("discover.html")


    @app.route("/mochi")
    def mochi():
        return render_template("mochi.html")
    
    @app.route("/apply/<int:job_id>", methods=["POST"])
    def apply(job_id):
        if "user_id" not in session:
            return redirect("/login")

        existing = Application.query.filter_by(
            user_id=session["user_id"],
            job_id=job_id
        ).first()

        if existing:
            return redirect("/opportunities")

        application = Application(
            user_id=session["user_id"],
            job_id=job_id
        )

        db.session.add(application)
        db.session.commit()

        return redirect("/opportunities")
    
    
    @app.route("/job-applicants/<int:job_id>")
    def job_applicants(job_id):
        if "user_id" not in session:
            return redirect("/login")

        if session.get("role") != "recruiter":
            return "Access denied (recruiters only)"

        job = Opportunity.query.get_or_404(job_id)
        applications = Application.query.filter_by(job_id=job_id).all()

        return render_template("job_applicants.html", job=job, applications=applications)
    
# ---------------- gorq ai  ----------------
    @app.route("/mochi-chat", methods=["POST"])
    def mochi_chat():

        print("🔥 ROUTE HIT")  # DEBUG 1

        user_input = request.form.get("message")

        print("USER:", user_input)  # DEBUG 2

        reply = career_advice(user_input)

        print("AI DONE")  # DEBUG 3

        return jsonify({"reply": reply})