import momoko

db = momoko.Pool(
    dsn='dbname=your_db user=your_user password=very_secret_password '
        'host=localhost port=5432',
    size=1
)