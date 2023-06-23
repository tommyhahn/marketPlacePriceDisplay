## Setup and Instructions

Make sure you have python 3.6+ installed.

```bash
pip3 install -r requirements.txt
```

### Running the Python Flask Server

```bash
cd marketPlacePriceDisplay
python backend/app.py
```

### Then Running the React Server

```bash
cd marketplace-price-display-frontend
npm install && npm start
```
Now it will automatically go to e.g. http://localhost:3001/ via a default web browser
We can now click on Fetch data button to fetch the collated data or click on Download button to 
download the transformed data in our choice of the following formats: JSON, CSV, or .xlsx. 