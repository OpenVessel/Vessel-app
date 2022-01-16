from plaid_container import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
