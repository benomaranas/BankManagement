from flask import Blueprint, redirect, request, render_template, jsonify, url_for
from app.services import get_all_accounts, create_new_account, get_account, delete_account

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    return render_template('base.html')

@app_routes.route('/accounts', methods=['GET'])
def list_accounts():
    accounts = get_all_accounts()
    return render_template("accounts.html", accounts=accounts)
    
@app_routes.route('/accounts/create', methods=['POST'])
def create_account():
    try:
            
        if request.is_json:
            data = request.get_json()
            account_number = data.get("account_number")
            account_holder = data.get("account_holder")
            balance = float(data.get("balance"))
        else:
            account_number = request.form.get("account_number")
            account_holder = request.form.get("account_holder")
            balance = float(request.form.get("balance")) # type: ignore
            
        create_new_account(account_number, account_holder, balance)
        return redirect (url_for("app_routes.list_accounts"))
    except ValueError as e:
        return jsonify({"message": "Invalid balance"}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred"}), 500
@app_routes.route('/accounts/search/<account_number>', methods=['GET'])
def search_account(account_number):
    # account_number = request.args.get('account_number')
    try:
        account = get_account(account_number)
        return jsonify(account), 200
    except ValueError as e:
        return jsonify({"message": "Account not found"}), 404
    except Exception as e:
        return jsonify({"message": "Error searching account"}), 500

@app_routes.route('/accounts/delete/<account_number>', methods=['DELETE'])

def remove_account(account_number):
    try:
        
        delete_account(account_number)
        return jsonify({"message": "accouunted deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"message": "Error deleting account"}), 500
    except Exception as e:
        return jsonify({"message": "Account not found"}), 404
    
    
