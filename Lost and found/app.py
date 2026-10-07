from flask import Flask, render_template, request

# Create Flask application
app = Flask(__name__)


# -------------------------------------------------
# Create text files if they do not already exist
# -------------------------------------------------

file = open("lost_items.txt", "a")
file.close()

file = open("found_items.txt", "a")
file.close()


# -------------------------------------------------
# Function to save a lost item
# -------------------------------------------------

def save_lost(item, location, date, contact):

    # Dictionary to store item details
    lost = {
        "item": item,
        "location": location,
        "date": date,
        "contact": contact
    }

    # Open lost_items.txt in append mode
    file = open("lost_items.txt", "a")

    # Write details into the file
    file.write(lost["item"] + "\n")
    file.write(lost["location"] + "\n")
    file.write(lost["date"] + "\n")
    file.write(lost["contact"] + "\n")
    file.write("--------------------\n")

    file.close()


# -------------------------------------------------
# Function to save a found item
# -------------------------------------------------

def save_found(item, location, date, contact):

    # Dictionary to store item details
    found = {
        "item": item,
        "location": location,
        "date": date,
        "contact": contact
    }

    # Open found_items.txt
    file = open("found_items.txt", "a")

    # Write details into the file
    file.write(found["item"] + "\n")
    file.write(found["location"] + "\n")
    file.write(found["date"] + "\n")
    file.write(found["contact"] + "\n")
    file.write("--------------------\n")

    file.close()


# -------------------------------------------------
# Function to read lost items
# -------------------------------------------------

def get_lost_items():

    items = []

    file = open("lost_items.txt", "r")

    while True:

        item = file.readline()

        # If file has ended
        if item == "":
            break

        location = file.readline()
        date = file.readline()
        contact = file.readline()

        # Read separator line
        file.readline()

        # Dictionary for one item
        data = {
            "item": item,
            "location": location,
            "date": date,
            "contact": contact
        }

        # Add dictionary to list
        items.append(data)

    file.close()

    return items


# -------------------------------------------------
# Function to read found items
# -------------------------------------------------

def get_found_items():

    items = []

    file = open("found_items.txt", "r")

    while True:

        item = file.readline()

        if item == "":
            break

        location = file.readline()
        date = file.readline()
        contact = file.readline()

        file.readline()

        data = {
            "item": item,
            "location": location,
            "date": date,
            "contact": contact
        }

        items.append(data)

    file.close()

    return items


# -------------------------------------------------
# Home page
# -------------------------------------------------

@app.route("/")
def home():

    lost = get_lost_items()
    found = get_found_items()

    return render_template(
        "index.html",
        lost_count=len(lost),
        found_count=len(found)
    )


# -------------------------------------------------
# Report Lost Item
# -------------------------------------------------

@app.route("/lost", methods=["GET", "POST"])
def lost_page():

    message = ""

    # Check whether form was submitted
    if request.method == "POST":

        # Get data from HTML form
        item = request.form["item"]
        location = request.form["location"]
        date = request.form["date"]
        contact = request.form["contact"]

        # Call save function
        save_lost(item, location, date, contact)

        message = "Lost item reported successfully!"

    return render_template(
        "lost.html",
        message=message
    )


# -------------------------------------------------
# Report Found Item
# -------------------------------------------------

@app.route("/found", methods=["GET", "POST"])
def found_page():

    message = ""

    if request.method == "POST":

        item = request.form["item"]
        location = request.form["location"]
        date = request.form["date"]
        contact = request.form["contact"]

        save_found(item, location, date, contact)

        message = "Found item reported successfully!"

    return render_template(
        "found.html",
        message=message
    )


# -------------------------------------------------
# Search Item
# -------------------------------------------------

@app.route("/search", methods=["GET", "POST"])
def search_page():

    results = []

    if request.method == "POST":

        search = request.form["search"]

        # Get both types of items
        lost = get_lost_items()
        found = get_found_items()

        # Search in lost items
        for data in lost:

            if search.lower() in data["item"].lower():

                data["type"] = "Lost"
                results.append(data)

        # Search in found items
        for data in found:

            if search.lower() in data["item"].lower():

                data["type"] = "Found"
                results.append(data)

    return render_template(
        "search.html",
        results=results
    )


# -------------------------------------------------
# Display all items
# -------------------------------------------------

@app.route("/items")
def all_items():

    lost = get_lost_items()
    found = get_found_items()

    return render_template(
        "items.html",
        lost=lost,
        found=found
    )


# -------------------------------------------------
# Start the Flask application
# -------------------------------------------------

app.run()