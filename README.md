#  MY FINAL PROJECT — Jasmeé Flower Shop

Jasmeé Flower Shop is a complete online flower shop where users can browse bouquets, like their favorites, place orders, update orders, and cancel orders within a 1-hour limit.

##  What does it do?
This is a full web application that allows users to:
- Browse flowers  
- View details of each bouquet  
- Like/favorite flowers using JavaScript + localStorage  
- Place orders  
- Update/cancel an order (within 1 hour only)  
- Store and retrieve orders from a file  
- Send messages in the Contact page  

##  New Feature
A full **Order Management System**:
- Users can **cancel** or **update** an order within 1 hour  
- Order status changes to *Active/Cancelled* inside the file  
- Dynamic Thank You page that changes based on status  
- Working **Favorites System** using JavaScript + LocalStorage  

---

##  Prerequisites
Install Flask:
pip install flask

No additional Python modules are required.

---

# PROJECT CHECKLIST

###  It is available on GitHub.
- [x] Yes

---

###  It uses the Flask web framework.
- File: `app.py`

---

###  It uses a module from the Python Standard Library (other than random)
You used:

- `datetime`  
- `timedelta`

Both from the Python Standard Library.

---

###  It contains at least one class written by you  
#### Class:
- File name: `app.py`
- Line numbers: **7**

#### Two properties:
- `self.name`
- `self.price`

#### Two methods:
- `price_with_discount()`
- `short_description()`

#### Where the methods are used:
- Flowers are instantiated at  
  **Line 16 → Line 21** in `app.py`

---

###  It makes use of JavaScript + localStorage
- File: `static/js/script.js`
- Favorites system uses localStorage.

---

###  It uses modern JavaScript (let, const)
- Verified in `script.js`

---

###  It uses reading and writing to the same file  
You use **orders.txt** for read & write:

  - Write: `submit_order()`  
  - File: `app.py`  
  - Line: **90**

  - Read: in several places  
  - For loop reading file inside `thankyou()`  
  - Line: **103**

---

###  It contains conditional statements  
Example:

```python
if not order_data:
    File: app.py
    Line number: 109

It contains loops
Example loop:
for line in f:
File: app.py
Line: 103
Another loop:  for line in lines
Line: 166

It lets the user enter a value in a text box
Order form: order.html
Contact form: contact.html
Data processed by backend in submit_order() and contact().

It handles wrong input safely
Example:
if not name or not email or not message:
    return render_template("contact.html", error="Please fill in all fields")

It is styled using your own CSS
File: static/css/style.css

Code follows conventions, documented, and without unused debug prints
Your code does not use print() or console.log() for user messages.

All exercises have been completed
 Yes, all files are included and pushed.
