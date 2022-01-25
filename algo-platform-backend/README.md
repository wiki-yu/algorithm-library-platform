<h1>
OPTIMO Express Backend AI model Test
    <h3>The back end server is implemented withe Express framework</h3>
</h1>

# stream page reconstruction
# Features

- File Upload
- File Processing 
- Communication with Front end


# Getting started
## Clone the project
```bash
git clone https://github.com/team-zazu/OPTIMO-Express-backend.git
```
## Install dependencies
```bash
npm install
```
## Run the auth service
```bash
node auth.js
```
## Run visualization service
```bash
$env:FLASK_APP = "visualization.py"
```
or
```bash
set FLASK_APP=visualization.py
```
and
```bash
python -m flask run -h localhost -p 4500
```
## Run the upload service
```bash
node upload-files.js
```
## Run yolo detection service
```bash
node yolo-model.js
```


