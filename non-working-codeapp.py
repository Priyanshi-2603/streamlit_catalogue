import streamlit as st
import urllib.parse
import json

st.title("Shri Girraj Mukut Shringar Kendra")

# ---------------- LOAD PRODUCTS FROM JSON ----------------
with open("products.json", "r") as f:
    products = json.load(f)

# ---------------- CART SYSTEM ----------------
if "cart" not in st.session_state:
    st.session_state.cart = []

def add_to_cart(product_name, size, price, dozens, image):
    st.session_state.cart.append({
        "product": product_name,
        "size": size,
        "price_per_piece": price,
        "dozens": dozens,
        "quantity": dozens * 12,
        "total_price": price * 12 * dozens,
        "image": image
    })

# ---------------- DISPLAY PRODUCTS ----------------
for product in products:

    st.image(product["image"], use_column_width=True)
    st.subheader(product["name"])

    size = st.selectbox(
        f"Select Size for {product['name']}",
        list(product["prices"].keys()),
        key=f"size_{product['name']}"
    )

    price = product["prices"][size]

    st.write(f"Price per piece: ₹{price}")

    dozens = st.number_input(
        f"Select Quantity (in dozens) - {product['name']}",
        min_value=1,
        step=1,
        value=1,
        key=f"dozen_{product['name']}"
    )

    st.write(f"Total Pieces: {dozens * 12}")
    st.write(f"Total Price: ₹{price * 12 * dozens}")

    if st.button(f"Add to Cart - {product['name']}", key=f"btn_{product['name']}"):
        add_to_cart(product["name"], size, price, dozens, product["image"])
        st.success(f"{dozens} dozen(s) of {product['name']} added to cart!")

    st.markdown("---")

# ---------------- CART DISPLAY ----------------
st.header("🛒 Cart Summary")

total = 0
order_message = "🛍 *New Order - Shri Girraj Mukut Shringar Kendra*\n\n"

for item in st.session_state.cart:
    line = (
        f"📦 *{item['product']}*\n"
        f"{item['image']}\n"
        f"Size: {item['size']}\n"
        f"Quantity: {item['dozens']} dozen ({item['quantity']} pcs)\n"
        f"Amount: ₹{item['total_price']}\n\n"
    )
    order_message += line
    total += item['total_price']

if total > 0:
    order_message += f"💰 *Final Amount:* ₹{total}\n"
    order_message += "🚚 Delivery Charges: Not Included\n"

    st.markdown("---")
    st.subheader(f"💰 Final Amount: ₹{total}")
    st.write("🚚 Delivery Charges Not Included")

    encoded_message = urllib.parse.quote(order_message)

    whatsapp_number = "917417866405"
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

    st.markdown(
        f'<a href="{whatsapp_url}" target="_blank">'
        f'<button style="background-color:green;color:white;padding:10px 20px;'
        f'border:none;border-radius:5px;font-size:16px;">'
        f'Place Order on WhatsApp</button></a>',
        unsafe_allow_html=True
    )
else:
    st.info("Your cart is empty.")