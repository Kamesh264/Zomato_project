from flask import Flask, jsonify, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

DATABASE_NAME = "postgres"
USERNAME = "postgres"
PASSWORD = "2003"
HOST = "localhost"
PORT = "5432"

connection = psycopg2.connect(dbname = DATABASE_NAME, user = USERNAME, password = PASSWORD, host = HOST, port = PORT)
cursor = connection.cursor()


# Query to fetch column names from a specific table
table_name = 'restaurant_info'
cursor.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = %s
""", (table_name,))

# Fetch all rows from the result set
columns = cursor.fetchall()

# Print the column names
for column in columns:
    print(column[0])

cursor = connection.cursor()

    # Construct query with pagination
query = f"""
    SELECT *
    FROM restaurant_info;
    """

cursor.execute(query)
restaurants_details = cursor.fetchall()

all_restaurants = []

for k in restaurants_details:
    l = list(k)
    all_restaurants.append(l)

restaurants = []
for row in restaurants_details:
    row_dict = dict(zip(columns, row))
    restaurants.append(row_dict)

# Convert the DataFrame to a dictionary for easy access


PER_PAGE = 10

# Home route
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_restaurants = restaurants[start:end]
    
    prev_url = None
    next_url = None
    if start > 0:
        prev_url = f"?page={page - 1}"
    if end < len(restaurants):
        next_url = f"?page={page + 1}"
    
    return render_template('home.html', restaurants=paginated_restaurants, prev_url=prev_url, next_url=next_url)

# Endpoint to retrieve restaurant details by ID and render template
@app.route('/restaurant/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    for restaurant in restaurants:
        if restaurant['Restaurant ID'] == restaurant_id:
            return render_template('restaurant.html', restaurant=restaurant)
    return jsonify({'error': 'Restaurant not found'}), 404

# Route to handle the search form submission
@app.route('/search', methods=['GET'])
def search():
    restaurant_id = request.args.get('restaurant_id')
    return redirect(url_for('get_restaurant', restaurant_id=restaurant_id))

if __name__ == '__main__':
    app.run(debug=True)
