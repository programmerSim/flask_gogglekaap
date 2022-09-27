from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

# 팩토리 패턴
def create_app(config=None):
    print('run_create_app()')
    app = Flask(__name__)
    
    """Flask Configs"""
    from .configs import DevelopmentConfig, ProductionConfig
    
    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()
            
    app.config.from_object(config)
    
    '''CSRF INIT'''
    csrf.init_app(app)
    
    '''DB INIT'''
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    
    '''Routes INIT'''
    from gogglekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)
    
    '''Restx INIT'''
    from gogglekaap.apis import blueprint as api
    app.register_blueprint(api)
    
    '''REQUEST HOOK'''
    from flask import g, current_app
    @app.before_request
    def before_request():
        g.db = db.session
        
    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()
            
    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html'), 404
    
    
    # ''' Routing Practice'''
    # from flask import jsonify, redirect, url_for
    # from markupsafe import escape
    
    # @app.route('/test/name/<name>')
    # def name(name):
    #     return f'Name is {name}, {escape(type(name))}'
    
    # @app.route('/test/id/<int:id>')
    # def id(id):
    #     return 'Id: %d' % id
    
    # @app.route('/test/path/<path:subpath>')
    # def path(subpath):
    #     return subpath
    
    # @app.route('/test/json')
    # def json():
    #     return jsonify({'hello': 'world'})
    
    # @app.route('/test/redirect/<path:subpath>')
    # def redirect_url(subpath):
    #     return redirect(subpath)
    
    # @app.route('/test/urlfor/<path:subpath>')
    # def urlfor(subpath):
    #     return redirect(url_for('path', subpath=subpath))
    
    # ''' Request Hook '''
    # from flask import g, current_app
    # @app.before_first_request
    # def before_first_request():
    #     app.logger.info('BEFORE_FIRST_REQUEST')
    
    # @app.before_request
    # def before_request():
    #     g.test = True
    #     app.logger.info('BEFORE_REQUEST')
        
    # @app.after_request
    # def after_request(response):
    #     app.logger.info(f'g.test:{g.test}\n')
    #     #app.logger.info(f'current_app.config:{current_app.config}')
    #     app.logger.info('AFTER_REQUEST')
    #     return response
    
    # @app.teardown_request
    # def teardown_request(exception):
    #     app.logger.info('TEARDOWN_REQUEST')
    
    # @app.teardown_appcontext
    # def teardown_appcontext(exception):
    #     app.logger.info('TEARDOWN_CONTEXT')
        
    
    # '''Method'''
    # from flask import request
    
    # @app.route('/test/method/<id>')
    # def method_test(id):
        
    #     request.on_json_loading_failed = on_json_loading_failed_return_dict
        
    #     return jsonify({
    #         "request.args": request.args,
    #         "request.from": request.form,
    #         "request.json": request.json,
    #         "request.method": request.method
    #     })
    
    # def on_json_loading_failed_return_dict(e):
    #     return {}
    
    return app