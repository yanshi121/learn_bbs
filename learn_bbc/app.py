from flask import Flask, session, g
import config
from extends import db, mail
from bluprints import qa_bp
from bluprints import user_bp
from flask_migrate import Migrate
from modes import UserModel
import logging

app = Flask(__name__)
app.config.from_object(config)
logging.basicConfig(filename="run_log.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
# app.logger.debug()
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            g.user = user
            # setattr(g, "user", user)
        except:
            g.user = None


@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run(debug=True)
