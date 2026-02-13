from flask import Flask, render_template, request, jsonify
import os
import re
from utils import process_mashup_request, create_zip, send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mashup', methods=['POST'])
def mashup():
    try:
        data = request.json
        singer = data.get('singer')
        n = int(data.get('count'))
        y = int(data.get('duration'))
        email = data.get('email')

        if n <= 10 or y <= 20:
            return jsonify({'success': False, 'error': 'N must be > 10 and Y must be > 20.'}), 400

        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_pattern, email):
            return jsonify({'success': False, 'error': 'Invalid email format.'}), 400

        output_mp3 = f"{singer.replace(' ', '_')}_mashup.mp3"
        output_zip = f"{singer.replace(' ', '_')}_mashup.zip"

        generated_mp3 = process_mashup_request(singer, n, y, email, output_mp3)
        generated_zip = create_zip(generated_mp3, output_zip)

        send_email(email, generated_zip)

        if os.path.exists(generated_mp3):
            os.remove(generated_mp3)
        if os.path.exists(generated_zip):
            os.remove(generated_zip)

        return jsonify({'success': True, 'message': 'Mashup sent to your email!'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


