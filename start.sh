export SECRET_KEY='ghostblogopinions'
export MAIL_USERNAME='vvmmddgg@gmail.com'
export MAIL_PASSWORD='vicrades'
export SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://sarah:sarah@localhost/opinions'

python3.10 manage.py server
# python3.10 manage.py shell
# python3.10 manage.py db init
# python3.10 manage.py db migrate -m'Initial Migration'
# python3.10 manage.py db upgrade