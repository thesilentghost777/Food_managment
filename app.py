from app import create_app
# Créer l'application Flask
app = create_app()
# Pour Gunicorn - il cherche 'application'
application = app


    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
