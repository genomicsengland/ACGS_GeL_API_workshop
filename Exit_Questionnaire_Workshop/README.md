Getting started
=======

*NOTE: Please use Python 2.7*

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
4. To use GelReportModels
```
cd ..
git clone git@github.com:genomicsengland/GelReportModels.git
cd GelReportModels
pip install .
```

5. You should now be able to run the notebook:
```
cd ../ACGS_GeL_API_workshop
jupyter-notebook Exit_Questionnaire_Workshop/CIP_API_examples.ipynb
```

GelReportModels Doc
https://genomicsengland.github.io/GelReportModels/
