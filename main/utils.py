import razorpay
client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))

data = {"amount": 500, "currency": "INR", "receipt": "order_rcptid_11"}
payment = client.order.create(data=data)
