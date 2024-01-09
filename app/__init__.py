from urllib.parse import quote

from flask import Flask, redirect
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, expose, AdminIndexView

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost:3306/khachsan_db?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class DashboardView(AdminIndexView):
    def is_visible(self):
        # This view won't appear in the menu structure
        return False
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            return self.render('admin/index.html')
        return redirect('/admin/login')

admin = Admin(app=app, name='QUẢN TRỊ KHÁCH SẠN',template_mode='bootstrap4', index_view=DashboardView())
login = LoginManager(app=app)