from flask import Flask, render_template, url_for, request, redirect
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   #refereence the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 3 slahes = relative path; 4 slashes is absolute path.
#relative path for hinding the exact location.

# Initialized database with settings for app.
db =  SQLAlchemy(app)

# Create a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Set string to 200 and allow null or empty entry
    content =  db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    # Date set to time it was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # Retrun the task and ID of that task
        return '<Task %r>' % self.id

#Index page where where we made the form.
@app.route('/', methods=['POST','GET'])
def index():

        if request.method == 'POST':
            # Logic for adding a task
            #pass the name of form
            task_content = request.form['content']
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')

            except:
                return 'There was an issue adding your task.'

        else:
            #Tasks look at db content by date_created
            # .first() if you  want recent by date.
            tasks = Todo.query.order_by(Todo.date_created).all()
            task_len = len(tasks)
            #pass the task db query to our template.
            return render_template('index.html', tasks=tasks, lent=task_len)

#Delete
@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')

    except:
        return "There was a problem deleting that task." 


#update
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    update_task_now = Todo.query.get_or_404(id)

    if request.method == 'POST':
        
        update_task_now.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue updating your task.'

    else:
        return render_template('update.html',update_task_now=update_task_now)

if __name__ == "__main__":
    app.run(debug=True)