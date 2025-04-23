from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

periodic_table = {
    1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne",
    11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
    21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn"
}

home_template = """
<!DOCTYPE html>
<html>
<head><title>퀴즈 시작</title></head>
<body>
    <h1>원소 기호 퀴즈</h1>
    <form action="{{ url_for('problem') }}" method="get">
        <button type="submit">퀴즈 시작</button>
    </form>
</body>
</html>
"""

quiz_template = """
<!DOCTYPE html>
<html>
<head><title>원소 퀴즈</title></head>
<body>
    <h1>##### 문제: {{ number }}의 원소는? #####</h1>
    <form method="post">
        <input name="user_input" placeholder="원소 기호 입력" autofocus>
        <input type="submit" value="제출">
    </form>
    {% if result %}
        <h2>{{ result }}</h2>
        <a href="{{ url_for('problem') }}">다시 하기</a>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(home_template)

@app.route("/problem", methods=["GET", "POST"])
def problem():
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        correct_answer = session.get("answer")
        if user_input == correct_answer:
            result = "정답"
        else:
            result = f"틀림 (정답: {correct_answer})"
        return render_template_string(quiz_template, number=session.get("question"), result=result)

    # GET 요청이면 새로운 문제 출제
    randint = random.randint(1, 30)
    session["question"] = randint
    session["answer"] = periodic_table[randint]
    return render_template_string(quiz_template, number=randint, result=None)

if __name__ == "__main__":
    app.run(debug=True)
