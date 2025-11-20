from flask import Flask, render_template , request, redirect, url_for
from datetime import datetime, timedelta


app = Flask(__name__)

class Flower:
    def __init__(self, id, name, price, img, description):
        self.id = id
        self.name = name
        self.price = price
        self.img = img
        self.description = description

          # Method لحساب السعر بعد خصم 5%
    def price_with_discount(self, discount=5):
        discounted_price = self.price * (1 - discount/100)
        return round(discounted_price, 2)

    # Method لإظهار وصف مختصر
    def short_description(self, length=30):
        if len(self.description) > length:
            return self.description[:length] + "..."
        return self.description

# بيانات البوكيهات
flowers = [
    Flower(1, "Blushing Lilies", 19.99,
           "https://www.freshblooms.ca/cdn/shop/files/pink-rose-lily.jpg?v=1691372939",
           "Soft pink lilies that whisper grace and beauty 💕"),

    Flower(2, "Red Roses", 19.99,
           "https://st4.depositphotos.com/16122460/20570/i/1600/depositphotos_205709086-stock-photo-bouquet-beautiful-red-roses-white.jpg",
           "A timeless symbol of love and passion ❤️"),

    Flower(3, "Snowy Elegance", 19.99,
           "https://media.cloudidd.com/media/pro-mediaprint/641564.jpg",
           "Pure white blossoms that bring serenity and charm 🤍"),

    Flower(4, "Tulip Bouquet", 19.99, "https://dicentra.ua/assets/images/products/1915/ddd122ea6f0bb354192effb7aa030e14744e81e8.jpg",
           "Soft pink tulips full of elegance 🌷"),

    Flower(5, "Sunflower Bouquet", 19.99, "https://content2.flowwow-images.com/data/flowers/1000x1000/22/1748353842_39183022.jpg", 
           "Bright golden sunflowers full of joy 🌻"),   

    Flower(6, "Spring Mix", 19.99, "https://barbarasfloral.com/cdn/shop/products/image6_7_1024x.jpg?v=1651302127",
           "A colorful spring mix for any occasion 💐"),    

    Flower(7, "Lavender Dream", 19.99, "https://asset.bloomnation.com/c_pad,d_vendor:global:catalog:product:image.png,f_auto,fl_preserve_transparency,q_auto/v1605443997/vendor/7226/catalog/product/2/0/20200106064613_file_5e13807555ca5_5e138129c422e.jpg",
            "Calming purple lavender with natural scent 💜"),

    Flower(8, "Peony Bouquet", 19.99, "https://www.fnp.com/images/pr/uae/l/v20250701125125/everlasting-love-peonies-bouquet_1.jpg",
            "Romantic soft pink peonies with fluffy petals 🌸")
]

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html', flowers=flowers)


@app.route("/favorites")
def favorites():
    return render_template("favorites.html")


# صفحة الأوردر
@app.route('/order/<int:id>')
def order(id):
    flower = next((f for f in flowers if f.id == id), None)
    return render_template('order.html', flower=flower)


@app.route("/submit_order/<int:id>", methods=["POST"])
def submit_order(id):
    flower = next((f for f in flowers if f.id == id), None)

    full_name = request.form.get("full_name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    card_message = request.form.get("card_message")
    order_time = datetime.now()
    time_str= order_time.isoformat()

    # نعطي كل طلب رقم ID فريد
    order_id = int(datetime.timestamp(order_time))

    # حفظ الطلب في ملف 
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(f"{order_id};;;{full_name};;;{phone};;;{address};;;{card_message};;;{id};;;{time_str};;;Active\n")


    
    return redirect(url_for("thankyou", order_id=order_id))


# صفحة الشكر مع تحقق الساعة
@app.route('/thankyou/<int:order_id>')
def thankyou(order_id):
    order_data = None

    with open("orders.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(";;;")
            if parts[0].isdigit() and int(parts[0]) == order_id:
                order_data = parts
                break

    if not order_data:
        return "Order not found"

    order_id, name, phone, address, card_message, flower_id, time_str, status = order_data
    order_time = datetime.fromisoformat(time_str)
    
    # المدة المسموح بها (ساعة = 3600 ثانية)
    remaining_seconds = 3600 - int((datetime.now() - order_time).total_seconds())

    if remaining_seconds < 0:
        remaining_seconds = 0

    flower = next((f for f in flowers if f.id == int(flower_id)), None)

    return render_template(
        "thankyou.html",
        name=name,
        phone=phone,
        address=address,
        card_message=card_message,
        flower=flower,
        order_id=order_id,
        remaining_seconds=remaining_seconds,
        status=status
    )




@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        message = request.form.get("message", "").strip()

        if not name or not email or not phone or not message:
            return render_template("contact.html", error="Please fill in all fields")
        with open("messages.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Message: {message}\n"
                    f"---\n"
                 )

        return render_template("contact.html", success=True)

    return render_template("contact.html")



    # كتابة الطلب مع ID
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(f"{order_id},{full_name},{phone},{address},{card_message},{flower.name}\n")

    return render_template("thankyou.html", name=full_name, flower=flower, order_id=order_id)


# Cancel Order
@app.route("/cancel_order/<int:order_id>")
def cancel_order(order_id):
    updated_lines = []
    found = False

    with open("orders.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split(";;;")
        if parts[0].isdigit() and int(parts[0]) == order_id:
            parts[7] = "Cancelled"  # تحديث حالة الطلب
            found = True
            line = ";;;".join(parts) + "\n"
        updated_lines.append(line)

    if found:
        with open("orders.txt", "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        # رسالة النجاح
        
        return redirect(url_for("thankyou", order_id=order_id, msg="Your order has been cancelled"))
    else:
        return "Order not found"


# Update Order

@app.route('/update_order/<int:order_id>', methods=['GET', 'POST'])
def update_order(order_id):
    order_data = None

    with open("orders.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(";;;")
            if parts[0].isdigit() and int(parts[0]) == order_id:
                order_data = parts
                break

    if not order_data:
        return "Order not found"

    order_id, name, phone, address, card_message, flower_id, time_str, status = order_data
    order_time = datetime.fromisoformat(time_str)
    allow_update = datetime.now() - order_time < timedelta(hours=1)

    flower = next((f for f in flowers if f.id == int(flower_id)), None)

    if request.method == "POST":
        new_name = request.form.get("full_name")
        new_phone = request.form.get("phone")
        new_address = request.form.get("address")
        new_card_message = request.form.get("card_message")

        # تحديث السطر في الفايل
        for i, line in enumerate(lines):
            parts = line.strip().split(";;;")
            if parts[0].isdigit() and int(parts[0]) == order_id:
                lines[i] = f"{order_id};;;{new_name};;;{new_phone};;;{new_address};;;{new_card_message};;;{flower_id};;;{time_str};;;{status}\n"
                break

        with open("orders.txt", "w", encoding="utf-8") as f:
            f.writelines(lines)

        return redirect(url_for("thankyou", order_id=order_id, msg="Your order has been updated successfully!"))

    return render_template("update_order.html",
                           name=name, phone=phone, address=address,
                           card_message=card_message, flower=flower,
                           order_id=order_id, allow_update=allow_update,
                           status=status)





# تشغيل السيرفر — مرة واحدة بس
if __name__ == '__main__':
    app.run(debug=True)



 
           
            


