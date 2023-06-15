from flask import Flask, render_template, url_for, request, redirect  # imports
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # create app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # set the config
db = SQLAlchemy(app)  # initialize database


class Todo(db.Model):  # create model : Todo
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # dunder print
        return "<Task %r>" % self.id


# routes
# create
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        # try push to database or catch exception
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task :("
    else:
        # get database content
        tasks = Todo.query.order_by(Todo.date_created).all()

        # pass task to template
        return render_template("index.html", tasks=tasks)


# delete
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    # try deleting task or catch errors
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task!"


# update
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]

        # commit or catch error
        try:
            db.session.commit()
            return redirect("/")

        except:
            return "There was a problem in updating the Task :("
    else:
        return render_template("update.html", task=task)


# run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
