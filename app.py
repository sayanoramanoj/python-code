from flask import Flask, request, jsonify, redirect, render_template
import string, random

app = Flask(__name__)

url_map = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    if not long_url:
        return jsonify({'error': 'No URL provided'}), 400

    short_code = generate_short_code()
    while short_code in url_map:
        short_code = generate_short_code()

    url_map[short_code] = long_url
    short_url = request.host_url + short_code
    return jsonify({'short_url': short_url})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    long_url = url_map.get(short_code)
    if long_url:
        return redirect(long_url)
    return jsonify({'error': 'Short URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
