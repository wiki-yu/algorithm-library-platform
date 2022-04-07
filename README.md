# action-localization-realtime-demo

It is a real-time action localization demo including FE and BE

## STEPS
1. Check if webcam is connected to the PC
2. Clone the whole project (FE and BE are in two subfilefolders)
2. Run the BE 
3. Run the FE, go to the "motion dection" page, check the live stream after action localization processing.
4. The model is trained with UCSP data, so the detection result would not make sense, just for real-time review purpose


## SET UP
### Clone the project
```
# clone the project
git clone https://github.com/wiki-yu/realtime-action-localization-flask.git
```

## Backend set up

### Build virtual enviroment

```
# enter BE folder
cd algo-platform-backend
```

_For Windows:_

```
py -m venv env # Only run this if env folder does not exist
.\env\Scripts\activate
pip install -r requirements.txt
```

_For MacOS/Linux:_

```
python3 -m venv env # Only run this if env folder does not exist
source env/bin/activate
pip install -r requirements.txt
```

### Download model weights file
Download C3D_tf_vgg_test_ines_3.hdf5 to the folder "app-stream/models"
Data link: [\[Teams drive\]](https://foxconno365.sharepoint.com/:f:/s/FiiUSA-iAIGroup-IAI-AI/EnmBVrZzWYpAmBysSzhHVTUB7b2Vpp1sP-QjhAUnN2o3kA?e=fZ7f8g)

```
### run the action detection script
cd app-stream
python app_rolling.py
```

## Frontend set up
```
### enter FE folder
cd algo-platform-frontend
```
```
### install dependencies
npm install
```
```
### develop
npm run dev
```
## Check real-time live stream
Go to "motion detection" to check the live stream


