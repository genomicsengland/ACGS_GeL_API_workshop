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

1. Change into the directory:
```
cd ACGS_GeL_API_workshop
```
2. Install `virtualenv` if you don't have it already or upgrade if you do:
```
pip install --upgrade virtualenv
```
3. Then create a virtual environment and install the requirements:

```
virtualenv .env
source ./.env/bin/activate
pip install -r requirements.txt
```
4. Either place your CIP API credentials and the url of the server you want to use in the notebook, or create 
a file (e.g. cip_api_credentials):
```
export CIP_API_USERNAME="username"
export CIP_API_PASSWORD="password"
export CIP_API_SERVER_URL="https://cipapi-server-url/api/{endpoint}"
```
adding your credentials and the server you want to conect to. 

5. Then run:
```
source cip_api_credentials
```
6. -Optional- to use Gel-Models
```
git clone git@github.com:genomicsengland/GelReportModels.git
cd GelReportModels
pip install .
```

7. You should now be able to run the notebook:
```
jupyter-notebook CIP_API_examples.ipynb
```


This will open the notebook in [http://localhost:8888/notebooks/CIP_API_examples.ipynb](http://localhost:8888/notebooks/CIP_API_examples.ipynb)

GelReportModels Doc
https://genomicsengland.github.io/GelReportModels/
