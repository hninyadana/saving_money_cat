from flask import Flask, render_template_string, request
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

# --- Simple HTML Template ---
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Purrse Saver 🐱</title>
</head>
<body style="font-family:Arial; background:#fdf6f0; text-align:center;">
    <h1>Purrse Saver 🐱💰</h1>
    <form method="POST">
        <label>Monthly Income:</label><br>
        <input type="number" name="income" required><br><br>
        
        <label>Target Saving:</label><br>
        <input type="number" name="target" required><br><br>
        
        <label>Today's Expense:</label><br>
        <input type="number" name="expense" required><br><br>
        
        <button type="submit">Log Expense</button>
    </form>
    <h2>{{ message }}</h2>
    {% if chart %}
        <img src="data:image/png;base64,{{ chart }}" />
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    chart = None

    if request.method == "POST":
        income = float(request.form["income"])
        target = float(request.form["target"])
        expense = float(request.form["expense"])

        daily_budget = (income - target) / 30
        if expense <= daily_budget:
            saved = daily_budget - expense
            message = f"Cat is happy 😺 | Saved ${saved:.2f}"
        else:
            message = "Cat is neutral 😐 | Overspent today"

        # --- Simple chart example ---
        fig, ax = plt.subplots()
        ax.bar(["Budget", "Expense"], [daily_budget, expense], color=["green","red"])
        ax.set_title("Daily Spending vs Budget")
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        chart = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close(fig)

    return render_template_string(template, message=message, chart=chart)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
