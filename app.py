from flask import Flask, jsonify, render_template, session
import requests
import json
import qrcode
import time
import chromadb
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection = client.create_collection("test")
# Add data to ChromaDB collection
collection.add(
        embeddings=[
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
            [1.1, 2.3, 3.2],
            [4.5, 6.9, 4.4],
        ],
        metadatas=[
            {"uri": "img1.png", "style": "style1"},
            {"uri": "img2.png", "style": "style2"},
            {"uri": "img3.png", "style": "style1"},
            {"uri": "img4.png", "style": "style1"},
            {"uri": "img5.png", "style": "style1"},
            {"uri": "img6.png", "style": "style1"},
            {"uri": "img7.png", "style": "style1"},
            {"uri": "img8.png", "style": "style1"},
        ],
        documents=["doc1", "doc2", "doc3", "doc4", "doc5", "doc6", "doc7", "doc8"],
        ids=["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8"],
    )

@app.route('/fetch_data')
def generate_payment_image():
    # Make the HTTP GET request to fetch payment data
    url = 'https://getalby.com/lnurlp/garyok/callback?amount=100000'
    response = requests.get(url)
    data = json.loads(response.text)
    pr_field = data['pr']
    verify_field = data['verify']

    # Generate the QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(pr_field)
    qr.make(fit=True)

    # Save the QR code image
    images_folder = os.path.join(app.root_path, 'images')  # Get the absolute path to the images folder
    os.makedirs(images_folder, exist_ok=True)  # Create the images folder if it doesn't exist
    qr_img_filename = 'qr_code.png'  # Specify the filename for the image file
    qr_img_path = os.path.join('images', qr_img_filename)  # Relative URL path to the image file
    qr.make_image(fill_color="black", back_color="white").save(os.path.join(app.static_folder, qr_img_path))


    # Store verify_field in session
    session['verify_field'] = verify_field
    
    # Return the rendered template with the QR code image
    return render_template('payment.html', qr_img_path=qr_img_path)

@app.route('/payment_status')
def check_payment_status():
    # Retrieve verify_field from session
    verify_field = session.get('verify_field')

    if verify_field:
        # Check the payment status using verify_field
        verify_response = requests.get(verify_field)
        verify_data = json.loads(verify_response.text)
        settled = verify_data.get('settled', False)

        if settled:
            # Payment settled, perform query in ChromaDB collection
            query_result = collection.query(
                query_embeddings=[[1.1, 2.3, 3.2]],
                n_results=2
            )
            # Return the query_result as JSON response
            return jsonify(query_result)
        else:
            # Payment not settled yet
            return 'Payment not processed yet'

    else:
        # verify_field not found in session, handle the case accordingly
        return 'Invalid payment verification'

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("FLASK_RUN_PORT", 8080)))
