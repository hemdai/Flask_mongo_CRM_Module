from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "Crm Sample Application with mongodb"
heading = "Keep log of your costumer"

#host uri
client = MongoClient("mongodb://127.0.0.1:27017")
#Select the database
db = client.mycrmdb
#Select the collection name
crmd = db.crm

status = (
            '...','Order', 'Processing','Deliverd'
            )
priority = ('...','Normal','Express','Urgent')

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')
@app.route('/')
@app.route("/list")

def lists ():

    #Display the all Tasks
    crmd_l = crmd.find()
    a1="order"
    return render_template('index.html',status=status ,a1=a1,crmd=crmd_l,t=title,h=heading,priority=priority)

#@app.route("/")
@app.route("/processing")
def tasks ():
    #Display the Uncompleted Tasks
    crmd_l = crmd.find({"status":"Processing"})
    a2="Processing"
    return render_template('index.html',a2=a2,crmd=crmd_l,t=title,h=heading)


@app.route("/delivered")
def completed ():
    #Display the Completed Tasks
    crmd_l = crmd.find({"status":"Deliverd"})
    a3="delivered"
    return render_template('index.html',a3=a3,crmd=crmd_l,t=title,h=heading)

@app.route("/done")
def done ():
    #Done-or-not ICON
    id=request.values.get("_id")
    task=crmd.find({"_id":ObjectId(id)})
    if(task[0]["done"]=="yes"):
        crmd.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
    else:
        crmd.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
    redir=redirect_url('/list')

    return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
    #Adding a Task
    name=request.values.get("name")
    desc=request.values.get("desc")
    date=request.values.get("date")
    pr=request.values.get("pr")
    status=request.values.get("status")
    crmd.insert({ "status":status,"name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
    return redirect("/list")

@app.route("/remove")
def remove ():
    #Deleting a Task with various references
    key=request.values.get("_id")
    crmd.remove({"_id":ObjectId(key)})
    return redirect("/list")

@app.route("/update")
def update ():
    id=request.values.get("_id")
    task=crmd.find({"_id":ObjectId(id)})
    return render_template('update.html',priority=priority,status=status,tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
    #Updating a Task with various references
    name=request.values.get("name")
    desc=request.values.get("desc")
    date=request.values.get("date")
    pr=request.values.get("pr")
    id=request.values.get("_id")
    status=request.values.get("status")
    crmd.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr, "status":status }})
    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    #Searching a Task with various references

    key=request.args.get("key")
    refer=request.args.get("refer")
    crmd_l = crmd.find({refer:key})
    a3 = "Details on "+ key


    return render_template('searchlist.html',a3=a3,crmd=crmd_l,t=title,h=heading)

if __name__ == "__main__":
    app.run()
