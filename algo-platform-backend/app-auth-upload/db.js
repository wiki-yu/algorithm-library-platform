"use strict";
const sqlite3 = require('sqlite3').verbose();

class Db {
    constructor(file) {
        this.db = new sqlite3.Database(file);
        this.createTableUser()
        this.createTableVideo()
        this.createTableAnnotation()
        this.createTableModel()
    }

    createTableUser() {
        const sql = `
            CREATE TABLE IF NOT EXISTS "user" (
                userID integer PRIMARY KEY,
                userName text,
                email text UNIQUE,
                userPwd text,
                isAdmin integer);`
        return this.db.run(sql);
    }

    createTableVideo() {
        const sql = `
            CREATE TABLE IF NOT EXISTS "video" (
                "videoID"	INTEGER,
                "recordTime"	TEXT,
                "stopTime"	TEXT,
                "fps"   INTEGER,
                "videoName"	TEXT,
                PRIMARY KEY("videoID")); `
        return this.db.run(sql);
    }

    createTableAnnotation() {
        const sql = `
            CREATE TABLE IF NOT EXISTS "annotation" (
                "annoID"	INTEGER,
                "videoID"	INTEGER,
                "annoBatch"  INTEGER,
                "startTime"	TEXT,
                "endTime"	TEXT,
                "videoName"   TEXT,
                "task"	TEXT,
                "project" TEXT, 
                PRIMARY KEY("annoID")); `
        return this.db.run(sql); 
    }

    createTableModel() {
        const sql = `
            CREATE TABLE IF NOT EXISTS "model" (
                "modelID"	INTEGER,
                "videoName"   TEXT,
                "modelName" TEXT, 
                PRIMARY KEY("modelID")); `
        return this.db.run(sql);
    }
        
        
    selectByEmail(email, callback) {
        console.log("db.js auth by email!")
        return this.db.get(
            `SELECT * FROM user WHERE email = ?`,
            [email],function(err,row){
                callback(err,row)
            })
    }

    // insertAdmin(user, callback) {
    //     return this.db.run(
    //         'INSERT INTO user (userName, email, userPwd, isAdmin) VALUES (?,?,?,?)',
    //         user, (err) => {
    //             callback(err)
    //         })
    // }

    // selectAll(callback) {
    //     return this.db.all(`SELECT * FROM user`, function(err,rows){
    //         callback(err,rows)
    //     })
    // }

    insertUser(user, callback) {
        console.log("db.js inserting user info!")
        return this.db.run(
            'INSERT INTO user (userName, email, userPwd) VALUES (?,?,?)',
            user, (err) => {
                callback(err)
            })
    }
    
    insertVideoInfo(videoInfo, callback) {
        console.log("db.js inserting video info!")
        console.log(videoInfo)
        return this.db.run(
            'INSERT INTO video (recordTime, stopTime, videoName) VALUES (?,?,?)',
             videoInfo, (err) => {
                callback(err)
            })
    }

    insertAnnoInfo(annoInfo, callback) {
        console.log("db.js inserting annotation info!")
        console.log(annoInfo)
        return this.db.run(
            'INSERT INTO annotation (recordTime, stopTime, videoName) VALUES (?,?,?)',
            annoInfo, (err) => {
                callback(err)
            })
    }

    selectVideoInfo(callback) {
        console.log("db.js selecting all video info!")
        return this.db.all( `SELECT * FROM video`, function(err,row){
                callback(err,row)
            })
    }

    deleteVideoInfo(videoName, callback) {
        console.log("db.js deleting video info!")
        console.log(videoName)
        return this.db.run(
            'DELETE FROM video WHERE videoName=?',
            videoName, (err) => {
                callback(err)
            })
    }
}

module.exports = Db