from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('movies.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_title TEXT NOT NULL,
                review TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Review System</title>
    </head>
    <body>
        <h1>Movie Review System</h1>
        <form id="reviewForm">
            <input type="text" id="movie_title" placeholder="Movie Title" required>
            <textarea id="review" placeholder="Your Review" required></textarea>
            <button type="submit">Submit Review</button>
        </form>
        <h2>Reviews</h2>
        <ul id="reviewsList"></ul>

        <script>
            document.getElementById('reviewForm').addEventListener('submit', function(event) {
                event.preventDefault();
                const movieTitle = document.getElementById('movie_title').value;
                const review = document.getElementById('review').value;

                fetch('/reviews', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ movie_title: movieTitle, review: review })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    loadReviews();
                });
            });

            function loadReviews() {
                fetch('/reviews')
                    .then(response => response.json())
                    .then(data => {
                        const reviewsList = document.getElementById('reviewsList');
                        reviewsList.innerHTML = '';
                        data.forEach(review => {
                            const li = document.createElement('li');
                            li.textContent = `${review[1]}: ${review[2]}`;
                            reviewsList.appendChild(li);
                        });
                    });
            }

            loadReviews();
        </script>
    </body>
    </html>
    ''')

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        data = request.get_json()
        movie_title = data['movie_title']
        review = data['review']
        with sqlite3.connect('movies.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO reviews (movie_title, review) VALUES (?, ?)', (movie_title, review))
            conn.commit()
        return jsonify({'message': 'Review added!'}), 201

    elif request.method == 'GET':
        with sqlite3.connect('movies.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM reviews')
            reviews = cursor.fetchall()
            return jsonify(reviews)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)