from flask import Flask, render_template_string, request
import numpy as np

app = Flask(__name__)

# HTML template with Bootstrap for a prettier GUI
FORM_HTML = '''
<!doctype html>
<html lang="el">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <title>Matrix Analyzer</title>
</head>
<body class="bg-light">
  <div class="container py-5">
    <div class="card shadow-sm">
      <div class="card-header bg-primary text-white">
        <h1 class="h3 mb-0">Matrix Analyzer</h1>
      </div>
      <div class="card-body">
        <form method="post">
          <div class="row g-3">
            <div class="col-md-6">
              <label for="rows" class="form-label">Αριθμός γραμμών</label>
              <input type="number" class="form-control" id="rows" name="rows" required min="1">
            </div>
            <div class="col-md-6">
              <label for="cols" class="form-label">Αριθμός στηλών</label>
              <input type="number" class="form-control" id="cols" name="cols" required min="1">
            </div>
          </div>
          <div class="mt-3">
            <label for="values" class="form-label">Τιμές μήτρας (χωρισμένες με κενά)</label>
            <textarea class="form-control" id="values" name="values" rows="4" required></textarea>
          </div>
          <button type="submit" class="btn btn-success mt-4">Ανάλυση</button>
        </form>
        {% if error %}
          <div class="alert alert-danger mt-4">{{ error }}</div>
        {% endif %}
        {% if result %}
          <hr>
          <h2 class="h5 mt-4">Αποτελέσματα</h2>
          <pre class="bg-light p-3 rounded shadow-sm">{{ result }}</pre>
        {% endif %}
      </div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

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
            lines.extend([f"\nInverse:\n{inv}", f"\nVerification (A·A⁻¹):\n{matrix @ inv}", f"\nInvertible: {np.allclose(matrix @ inv, np.identity(R))}"])
        else:
            lines.append("\nΗ μήτρα δεν είναι αντιστρέψιμη (det = 0).")
    else:
        lines.append("\nΗ μήτρα δεν είναι τετράγωνη – ορισμένοι υπολογισμοί δεν εφαρμόζονται.")

    lines.append(f"\nRank: {np.linalg.matrix_rank(matrix)}")
    return "\n".join(lines)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            R = int(request.form['rows'])
            C = int(request.form['cols'])
            values_str = request.form['values'].split()
            if len(values_str) != R * C:
                raise ValueError(f"Αναμένονταν {R*C} τιμές, δόθηκαν {len(values_str)}.")
            values = list(map(float, values_str))
            result = analyze_matrix(R, C, values)
            return render_template_string(FORM_HTML, result=result)
        except Exception as e:
            return render_template_string(FORM_HTML, error=str(e))
    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
