from app import app
from app.models import db, Player

@app.shell_context_processor
def shell_context():
    return {'db': db, 'Player': Player}