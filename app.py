from flask import Flask, render_template, request
from Bio.Seq import Seq

app = Flask(__name__)


@app.route('/')
def index() -> str:
    return render_template('index.html')


# @app.route('/convert.html')
# def convert_page() -> str:
#     return render_template('convert.html')


@app.route("/convert", methods=['POST', 'GET'])
def convert() -> str:
    dna = request.form.get('seq')

    if dna:
        try:
            sequence = Seq(str(dna))
            return render_template('convert.html',
                                   protein=sequence.translate())
        except:
            return render_template('convert.html',
                                   protein='Error')
    else:
        return render_template('convert.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
