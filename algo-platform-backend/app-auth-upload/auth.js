const express = require('express');
const DB = require('./db');
const config = require('./config');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
const axios = require('axios');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const fs = require('fs');
const {spawn} = require('child_process');

const db = new DB("../sqlitedb")
const app = express();
const router = express.Router();
router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json());
router.use(express.static('public'))
router.use(cors())
router.use(fileUpload());

// CORS middleware
const allowCrossDomain = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', '*');
    res.header('Access-Control-Allow-Headers', '*');
    next();
}
app.use(allowCrossDomain)

// Register
router.post('/register', function(req, res) {
    console.log("[INFO]Start the register process!")
    console.log(req.body.name, req.body.email, req.body.password)
    db.insertUser([
        req.body.name,
        req.body.email,
        bcrypt.hashSync(req.body.password, 8)
    ],
    function (err) {
        if (err) {
            console.log("[ERR]There is a problem registering the user!")
            return res.status(500).send("There is a problem registering the user")
        }
        
        db.selectByEmail(req.body.email, (err,user) => {
            if (err) return res.status(500).send("There was a problem getting user")
            let token = jwt.sign({ id: user.id }, config.secret, {expiresIn: 86400 // expires in 24 hours
            });
            res.status(200).send({ auth: true, token: token, user: user });
        });
    });
});

// Login
router.post('/userLogin', (req, res) => {
    console.log("[INFO]Start the login process!")
    console.log(req.body.userName, req.body.password)
    db.selectByEmail(req.body.userName, (err, user) => {
        if (err) 
        {
            console.log("[ERR]There is login problem!")
            return res.status(500).send('There is login problem with the server');
        }
        if (!user) return res.status(404).send('No user found.');
        let passwordIsValid = bcrypt.compareSync(req.body.password, user.userPwd);
        if (!passwordIsValid) return res.status(401).send({ auth: false, token: null });
        let token = jwt.sign({ id: user.id }, config.secret, { expiresIn: 86400 // expires in 24 hours
        });
        res.status(200).send({ auth: true, token: token, user: user });
    });
})

// Save stream page video info
router.post('/saveVideoInfo', function(req, res) {
    console.log("[INFO]Start saving video info!")
    for (var i = 0; i<req.body.length; i++ ) {
        db.insertVideoInfo([
            req.body[i].start,
            req.body[i].end,
            req.body[i].videoName,
        ],
        function (err) {
            if (err) {
                console.log("there is error inserting the video info!!!")
                return res.status(500).send("There was a problem saving the video info.")  
            }
        });
    }
    res.status(200).send("sucess saving video!!!");
});

// Save annotation info
router.post('/saveAnnoInfo', function(req, res) {
    console.log("[INFO]Start saving annotation info!")
    // for (var i = 0; i<req.body.length; i++ ) {
    //     db.insertAnnoInfo([
    //         req.body[i].start,
    //         req.body[i].end,
    //         req.body[i].videoName,
    //     ],
    //     function (err) {
    //         if (err) {
    //             console.log("there is error inserting the video info!!!")
    //             return res.status(500).send("There was a problem saving the video info.")  
    //         }
    //     });
    // }
    res.status(200).send("sucess saving annotation info!!!");
});

// Get video info for display
router.get('/getVideoInfo', (req, res) => {
    console.log("[INFO]Get database video info!")
    db.selectVideoInfo((err, videoList) => {
        if (err) return res.status(
            500).send('Error on the server.');
        if (!videoList) return res.status(404).send('No video list found.');
        res.status(200).send(JSON.stringify(videoList));
    });
})



// display video and video info on original data page
router.get('/showVideo', (req, res) => {
    console.log("[INFO]Show Video!!!!!!!!",req.query.filename)
    var filename = "../Data/" + req.query.filename;
    console.log(filename)
    // // This line opens the file as a readable stream
    var readStream = fs.createReadStream(filename);
    // This will wait until we know the readable stream is actually valid before piping
    readStream.on('open', function () {
      // This just pipes the read stream to the response object (which goes to the client)
      readStream.pipe(res);
    });
    // This catches any errors that happen while creating the readable stream (usually invalid names)
    readStream.on('error', function(err) {
      res.end(err);
    });
})

// Delete video 
router.post('/delVideo', function(req, res) {
    console.log(req.body.videoName)
    curPath = `../Data/${req.body.videoName}`
    console.log(curPath)
    fs.unlinkSync(curPath); 
    db.deleteVideoInfo(
        req.body.videoName,
        function (err) {
            if (err) {
                console.log("[ERR]There is error deleting the videos!!!")
                return res.status(500).send("There is error delting the video!!!")  
            }
        }
    )
    res.status(200).send("sucess saving video!!!");
});

router.post('/trainProcess', (req, res) => {
    console.log(res.body)
    console.log("this is training!!!!!!!!!!!!!!!!!!!!!!!!!")
    res.status(200).send("Training request received!!!");
})


// Upload video
router.post('/uploadVideo', (req, res) => {
    console.log("[INFO]Saving videos!")
    if (!req.files) {
        return res.status(500).send({ msg: "file is not found" })
    }
    const myFile = req.files.file;
    console.log("[INFO]File name:", myFile.name)
    // Use the mv() method to place the file somewhere on your server
    myFile.mv(`${__dirname}/Data/${myFile.name}`, function (err) {
        console.log('[INFO]mv callback')
        if (err) {
            console.log(err)
            return res.status(500).send({ msg: "[ERR]there is error" });
        }
    });
})

router.post('/uploadFile', (req, res) => {
    console.log("[INFO]Get ready to recieve files!")
    console.log(req.body)
    if (!req.files) {
        return res.status(500).send({ msg: "file is not found" })
    }
    const myFile = req.files.file;
    console.log("[INFO]Receiving files!")
    console.log("[INFO]File name:", myFile.name)
    myFile.mv(`${__dirname}/Data/${myFile.name}`, function (err) {
        console.log('[INFO]mv callback');
        var filePath = `${__dirname}/Data/${myFile.name}`;
        console.log(filePath);
        if (err) {
            console.log(err)
            return res.status(500).send({ msg: "[ERR]there is error" });
        }
        res.send({ file: myFile.name, path: `/${myFile.name}`, ty: myFile.type });
    });
})

app.use(router)
let port = process.env.PORT || 3000;
let server = app.listen(port, function() {
    console.log('Express server listening on port ' + port)
});
