# webcui

A Python package for creating Webcui apps. A Webcui app is to the web what a Command Line Interface app is for the command line.
The goal of Webcui is to make it as easy as possible for Python developers to share their Python app with the world.

Webcui idea:
* A web page with a HTML form is generated from a basic Python function.
* Function parameters become input fields.
* The function is executed when the user submit the form.
* The result is displayed on the web page.

## Installation
Install Python 3.6 or later and then webcui using pip.
```
$ pip install webcui
```

## Usage

Here's an example of a simple Webcui app:
```python
import webcui

def cmd(number_of_spam: int, side: str = "eggs"):
   """Calculate the price of a breakfast order."""
   spams = number_of_spam * ["spam"]
   dish = f"{', '.join(spams)} and {side}"
   price = number_of_spam * 1.5 + 2
   return f"The price of an order of {dish} is €{price:.2f}"

if __name__ == '__main__':
   webcui.run(cmd)
```

To run the Webcui app on your own computer run:
```
$ python app.py --run
```
