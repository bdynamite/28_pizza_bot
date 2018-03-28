from app import app, admin, db, basic_auth
from models import Pizza
from flask_admin.contrib.sqla import ModelView
from flask import render_template


@app.route('/admin')
@basic_auth.required
def admin_view():
    print(1, app.config['SQLALCHEMY_DATABASE_URI'])
    return render_template('admin/index.html')

admin.add_view(ModelView(Pizza, db.session))
app.run()
