# routes/view_routes.py
from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index(): return render_template('index.html')

@views_bp.route('/dashboard')
def dashboard(): return render_template('dashboard.html')

@views_bp.route('/login')
def login(): return render_template('login.html')

@views_bp.route('/diario')
def diario(): return render_template('diario.html')

@views_bp.route('/signup')
def signup(): return render_template('signup.html')

@views_bp.route('/mayor')
def mayor(): return render_template('mayor.html')

@views_bp.route('/balance-saldos-view')
def balance_saldos(): return render_template('balance_saldos.html')

@views_bp.route('/estado-resultados-view')
def estado_resultados(): return render_template('estado_resultados.html')

@views_bp.route('/balance-situacion-view')
def balance_situacion(): return render_template('balance_situacion.html')