from app import app, admin, db, basic_auth
from models import Pizza, Choice
from flask_admin.contrib.sqla import ModelView
from flask import render_template


@app.route('/admin')
@basic_auth.required
def admin_view():
    return render_template('admin/index.html')

admin.add_view(ModelView(Pizza, db.session))
admin.add_view(ModelView(Choice, db.session))
app.run()
