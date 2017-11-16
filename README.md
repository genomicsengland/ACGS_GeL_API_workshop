Getting started
=======
0. Clone this repository:
```
git clone git@github.com:genomicsengland/ACGS_GeL_API_workshop.git
```
or
```
git clone https://github.com/genomicsengland/ACGS_GeL_API_workshop.git
```
if using https.

1. Then create a virtual environment and install the requirements:

```
virtualenv .env
source ./.env/bin/activate
pip install -r requirements.txt
```

2. Either place your CIP API credentials and the url of the server you want to use in the notebook, or create 
a file (e.g. cip_api_credentials):
```
export CIP_API_USERNAME="username"
export CIP_API_PASSWORD="password"
export CIP_API_SERVER_URL="https://cipapi-server-url/api/{endpoint}"
```
adding your credentials and the server you want to conect to. 

3. Then run:
```
source cip_api_credentials
```

4. You should now be able to run the notebook:
```
jupyter-notebook CIP_API_examples.ipynb
```

This will open the notebook in [http://localhost:8888/notebooks/CIP_API_examples.ipynb](http://localhost:8888/notebooks/CIP_API_examples.ipynb)

