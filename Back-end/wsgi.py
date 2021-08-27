from vessel_app import create_app

app = create_app()

if __name__ == '__main__':
    
    ## Profilier with werkzeug 
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5], profile_dir='Vessel-app\Back-end\profile')
    app.run(ssl_context='adhoc',debug=True)
