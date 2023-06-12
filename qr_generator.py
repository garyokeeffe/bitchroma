
import requests
import json
import qrcode
import time

import matplotlib
matplotlib.use('TkAgg')


import matplotlib.pyplot as plt
import matplotlib.image as mpimg




import chromadb

client = chromadb.Client()

collection = client.create_collection("test")

# Make the HTTP GET request
url = 'https://getalby.com/lnurlp/garyok/callback?amount=100000'
response = requests.get(url)

# Extract the "pr" field from the JSON response
data = json.loads(response.text)
pr_field = data['pr']
verify_field = data['verify']
# Generate the QR code
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
print(pr_field)
print(verify_field)
qr.add_data(pr_field)
qr.make(fit=True)

# Save the QR code image
qr_img = qr.make_image(fill_color="black", back_color="white")
qr_img.save("qr_code.png")


print("QR code generated and saved as qr_code.png")
# Load the image file
img = mpimg.imread('qr_code.png')

# Display the image
plt.imshow(img)
plt.show(block=False)
# Check the verify URL every second until settled is true
settled = False
while not settled:
    verify_response = requests.get(verify_field)
    verify_data = json.loads(verify_response.text)
    settled = verify_data.get('settled', False)

    if not settled:
        time.sleep(.5)  # Wait for .5 second before checking again
print("found it")
plt.close()
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

query_result = collection.query(
        query_embeddings=[[1.1, 2.3, 3.2], [5.1, 4.3, 2.2]],
        n_results=2,
    )

print(query_result)
