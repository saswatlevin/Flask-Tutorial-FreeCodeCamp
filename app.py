from flask import Flask
# The flask app
app = Flask(__name__)

# URL for index()
# Returns web resource (such as a web page)
@app.route('/')
def index():
    return "Hello, World!"

# Main function to run the app
if __name__ == "__main__":
    # Call to run the app
    # Debugging turned on shows any errors with pages
    app.run(debug = True)