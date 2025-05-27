# app.py
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True  # για αυτόματη φόρτωση template


def analyze_matrix(R, C, values):
    matrix = np.array(values).reshape(R, C)
    lines = [f"Μήτρα ({R}x{C}):\n{matrix}", f"\nTranspose:\n{matrix.T}"]

    if R == C:
        det = np.linalg.det(matrix)
        tr = np.trace(matrix)
        lines.append(f"\nDeterminant: {det:.2f}")
        lines.append(f"Trace: {tr:.2f}")
        if not np.isclose(det, 0):
            inv = np.linalg.inv(matrix)
            lines.extend([
                f"\nInverse:\n{inv}",
                f"\nVerification (A·A⁻¹):\n{matrix @ inv}",
                f"\nInvertible: {np.allclose(matrix @ inv, np.identity(R))}"
            ])
        else:
            lines.append("\nΗ μήτρα δεν είναι αντιστρέψιμη (det = 0).")
    else:
        lines.append("\nΗ μήτρα δεν είναι τετράγωνη – ορισμένοι υπολογισμοί δεν εφαρμόζονται.")

    lines.append(f"\nRank: {np.linalg.matrix_rank(matrix)}")
    return "\n".join(lines)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            R = int(request.form['rows'])
            C = int(request.form['cols'])
            values_str = request.form['values'].split()
            if len(values_str) != R * C:
                raise ValueError(f"Αναμένονταν {R*C} τιμές, δόθηκαν {len(values_str)}.")
            values = list(map(float, values_str))
            result = analyze_matrix(R, C, values)
        except Exception as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
