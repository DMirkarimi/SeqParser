import re
from flask import Flask, render_template, request
from Bio.Seq import Seq
from Bio.Blast import NCBIWWW, NCBIXML

app = Flask(__name__)


def seq_info(sequence: Seq) -> str:
    if sequence.seq_type == 'DNA':
        rna = sequence.transcribe()
        protein = sequence.translate()

        text = f'Sequence has been classified as DNA\n' \
               f'Transribed: {rna}\n' \
               f'Translated: {protein}'
        return text
    elif sequence.seq_type == 'RNA':
        return 'Sequence contains RNA'
    else:
        result = NCBIWWW.qblast(program="blastp", database="nr",
                                sequence=str(sequence), ncbi_gi=True,
                                hitlist_size=1, format_type='XML',
                                matrix_name='BLOSUM62', gapcosts='11 1',
                                word_size=6)
        try:
            alignment = NCBIXML.read(result).alignments[0]
            accession_code = alignment.accession
        except (IndexError, AttributeError):
            accession_code = 'Not found'

        text = f'Protein detected\n' \
               f'Most likely parent gene: {accession_code}'
        return text


@app.route('/')
def index() -> str:
    return render_template('index.html')


# @app.route('/convert.html')
# def convert_page() -> str:
#     return render_template('convert.html')


@app.route("/convert", methods=['POST', 'GET'])
def convert() -> str:
    seq = request.form.get('seq')

    if seq:
        try:
            seq_type = None
            sequence = str(seq)
            if not re.search(r'[^ATGC]', sequence):
                seq_type = 'DNA'
            elif not re.search(r'[^AUGC]', sequence):
                seq_type = 'RNA'
            elif not re.search(r'[^AC-IK-NP-Y]', seq):
                seq_type = 'protein'


            seq_obj = Seq(sequence)
            seq_obj.seq_type = seq_type
            return render_template('convert.html',
                                   output=seq_info(seq_obj))
        except:
            return render_template('convert.html',
                                   output='Error')
    else:
        return render_template('convert.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
