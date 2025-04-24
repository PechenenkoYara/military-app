from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# from website import create_app

# app = create_app()

# if __name__ == '__main__':
#     # Create an application context before accessing the database
#     with app.app_context():
#         from website import db
#         # Only run this if you're okay with losing all data
#         db.drop_all()
#         db.create_all()
    
#     app.run(debug=True)