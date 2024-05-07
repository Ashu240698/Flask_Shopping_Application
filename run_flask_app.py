import os
import subprocess
from flask_package.models import ItemModel

def runApp():
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['FLASK_RUN_HOST'] = 'localhost'
    os.environ['FLASK_RUN_PORT'] = '5555'
    os.environ['FLASK_APP'] = 'flask_package'
    subprocess.run(['flask', 'run'])
    # app.run(debug=True)

if __name__ =='__main__':
    ItemModel.Item.load_database()
    runApp()