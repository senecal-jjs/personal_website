import hmac
from flask import request, Blueprint, jsonify, current_app 
from subprocess import Popen, PIPE
from app.git_hook import bp
from flask import current_app

@bp.route('/bitbucket', methods=['POST']) 
def handle_bitbucket_hook(): 
    """ Entry point for github webhook """
    try:
        (stdout, stderr) = Popen(['/home/snj/update.sh',], stdout=PIPE).communicate()
        return 'success'
    except:
        return 'failure'