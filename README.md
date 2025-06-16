# flask-riddles
 An example flask site. Display the riddle and answer sourced from riddles-api.vercel.app

### Created by Colin Kujala


# How to set up a flask site

Flask is a simple python web framework - it abstracts away the backend web server 
communications, allowing the programmer to easily recieve and send information 
through the Flask site.

This simple example I created is a 1-page, GET-only, Flask site. Additional page 
views would be simple to add if wanted.

Read further for details on how to implement a Flask site and add some 
custom formatting through CSS and background images.

## Page Contents:

1. Install Flask
2. Set Up Main Python File to Run Flask Site
3. Set Up HTML Templates
4. Set Up Static Files
5. CSS Details
6. Conclusion

## 1. Install Flask

Before starting, create a virtual environment to install the necessary python 
packages. I work on a Windows machine. After navigating to the folder where I 
will build the project, the command I use to set up a virtual environment 
looks like this:

`py -m venv venv`

- "py -m venv" tells the command line to run the venv module of my python implementation
- "venv" at the end is the argument passed to name the virtual environment I am creating

Once the virtual environment is created, then activated with `venv/Scripts/activate`, you 
are ready to start installing packages in the virtual environment. Using a virtual 
environment is recommended to control version dependencies, avoid package conflicts, 
and not affect other projects.

For this Flask riddles site, install flask and requests:

```
pip install flask
pip install requests
```

## 2. Set Up Main Python File to Run Flask Site

### Imports:

```
import os

import requests
from flask import Flask, render_template
```

### Initialize the flask app:

`app = Flask(__name__)`

Feed the module name "__name__" to the Flask constructor to generate the app.

### Define Function to Get Riddle

```
def get_riddle():
    """Retrieve a random riddle from page on internet"""
    return requests.get("https://riddles-api.vercel.app/random").json()
```

The get_riddle function uses the requests library to make a GET request 
of the riddles API, and returns the json object that the api sends back.

### Define a View Function for Flask Site

```
@app.route("/")
def home():
    riddle = get_riddle()

    return render_template(
        "home.jinja2",
        riddle=riddle
    )
```

The @app.route("/") decorator tells the flask app to run this function to 
generate a view for the root address "/".

The home() function uses the get_riddle function, then injects the riddle 
into the html template that it returns.

### Run the Flask App

```
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
```

The port is defined by either the "PORT" environment variable if it exists, or defaults 
to 6787. The Flask site then runs the on the localhost using the defined port. It 
listents on this host/port for any http requests, and then uses the defined app 
routes to determine what views/data to return to the requests.

## 3. Set Up HTML Templates

Flask uses jinja2 as it's templating library. This example site has a base template to 
hold a lot of the boiler plate html file content, which can then be referenced 
when writing the site's other page-specific html files.

### base.jinja2

```
<html>
<head>
<title>Random Riddle</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
	<div class="page-container">
		<div class="main-content">
			<h1>Random Riddle</h1>
			<h2>{% block subtitle %} {% endblock subtitle %}</h2>
			{% block content %} {% endblock content %}
		</div>
		<footer>
			Riddles sourced from riddles-api.vercel.app
		</footer>
	</div>
</body>
</html>
```

The base.jinja2 file creates the html skeleton for our site. The stylesheet for our 
site is set in the head, linking to the css file to be used. There are a couple 
areas where blocks are set up for content to be added from other jinja2 files. A 
footer was placed at the end of the body page.

### home.jinja2

```
{% extends 'base.jinja2' %}

{% block subtitle %}Can you solve the riddle?{% endblock subtitle %}

{% block content %}
    <h3>{{ riddle["riddle"] }}</h3>
    
    <div id="shown_answer">
        <p><b>Answer:</b> {{ riddle["answer"] }}</p>
        <button onclick="toggleanswer()">
            Hide Answer
        </button>
    </div>
    <div id="hidden_answer">
        <button onclick="toggleanswer()">
            Show Answer
        </button>
    </div>
    <script>
        window.onload = function() {
            document.getElementById("shown_answer").style.display = "none";
            document.getElementById("hidden_answer").style.display = "block";
        };
    </script>
    <script>
        function toggleanswer() {
            const shown_answer_div = document.getElementById("shown_answer");
            const hidden_answer_div = document.getElementById("hidden_answer");
            if (shown_answer_div.style.display.toString() === "none") {
                shown_answer_div.style.display = "block";
                hidden_answer_div.style.display = "none";
            } else {
                shown_answer_div.style.display = "none";
                hidden_answer_div.style.display = "block";
            }
        }
    </script>
{% endblock content %}
```

The home.jinja2 file is the template for any calls to the home function 
(which is accessed through the root address for the site). At the top 
of the home template, it specifies that it is extending the base.jinja2 
template. Two blocks of content are filled out, the subtitle block and 
the content block.

In the content block, we display the riddle and place the answer in a div that 
is hidden by a script when the page loads. A button allows the user to 
unhide the answer, or rehide the answer, using a javascript function that 
flips the display setting for the answer div between "block" or "none".

## 4. Set Up Static Files

The static css files and images are placed in folders under the "static" 
folder, which is the best practice for folder structure. The css file is 
referenced in the head of the base.jinja2 html template.

`<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">`

The href url_for function looks in the static folder and finds the css 
file at the filepath "css/main.css".

The background image for the site is referenced through the css file, in the 
style settings for the body of the html.

`background-image: url('/static/img/question_background.jpg');`

## 5. CSS Details

The css file manages the style settings for all components of the html files.

```
body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    background-image: url('/static/img/question_background.jpg');
    background-size: cover;
}

.page-container {
    position: relative;
    min-height: 95vh;
}

.main-content {
    margin: 20px;
    padding: 10px;
    padding-bottom: 2.5rem;  /* Footer height */
}

footer {
    position: absolute;
    text-align: center;
    width: 100%;
    bottom: 0;
    height: 2.5rem;  /* Footer height */
}
```

### body

The body settings apply to the entire body of the html page. The background 
image size is set to cover the body.

### .page-container

The .page-container settings apply to the div with the class "page-container". 
For this site, the page-container is being used to hold all the contents of the 
site. The position is set to relative so it can be dynamic. Of note, the 
min-height is set to 95vh (95% of viewport height) so that we can position 
the footer for the page to sit at the bottom of the viewport, referencing the 
lower-end of the page-container when postitioning the footer.

### .main-content

The .main-content settings apply to the div with the class "main-content". 
The padding-bottom setting of 2.5rem means 2.5x root element size; default root 
element size is 16px. This padding-bottom setting is meant to ensure space is 
padding the footer.

### footer

The footer style settings apply to the footer of the page. Of note, the settings 
of "position: absolute" and "bottom: 0" make the footer stick to the bottom 
of the page-container.

## Conclusion

Flask is a web framework used to simplify serving views and data to the web. 
Use jinja2 templating, along with css files, to determine what your views 
will look like, and use the flask framework to set how the app will recieve 
requests and send responses.
