#imports

from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#my app

app= Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)


class MyTask(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    Content = db.Column(db.String(150), nullable=False )
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Task{self.id}"
    
with app.app_context():
        db.create_all()


#Home page
@app.route("/", methods=["POST", "GET", ])
def index():
    #Add a task
    if request.method=="POST":
        current_task = request.form['content']
        new_task = MyTask(Content=current_task)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            
            return redirect("/")
        except Exception as e:
            print("ERROR:{e}")
            return f"ERROR:{e}"
        
    else:
        tasks= MyTask.query.order_by(MyTask.created).all()
    

                
        return render_template("index.html", tasks=tasks)
    
#deleting task

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task= MyTask.query.get_or_404(id)
    
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        
        return f"ERROR:{e}"
        

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task= MyTask.query.get_or_404(id)
    if request.method=="POST":
        task.Content = request.form['content']
        
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html' ,task=task)
    











# Runner and debugger

if __name__ == "__main__":
   
    app.run(debug=True)
    
    


