from flask import Blueprint, redirect, request, render_template, jsonify, url_for
from app.services import get_all_accounts, create_new_account, get_account, delete_account,get_account_transactions

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

from flask import redirect, url_for

@app_routes.route('/accounts/delete/<account_number>', methods=['GET'])
def remove_account(account_number):
    """
    Route to delete an account and reload the accounts page.
    """
    try:
        # Call the DAL function to delete the account
        delete_account(account_number)

        # Redirect to the list accounts page after deletion
        return redirect(url_for('app_routes.list_accounts'))
    
    except ValueError as e:
        # Redirect to the list accounts page with an error (optional)
        return redirect(url_for('app_routes.list_accounts', error="Account not found"))
    
    except Exception as e:
        # Redirect in case of an unexpected error
        return redirect(url_for('app_routes.list_accounts', error="An error occurred"))
@app_routes.route("/accounts/view/<account_number>", methods = ['GET'])
def view_account(account_number):
    
    try:
        account = get_account(account_number)
        
        return render_template("account_details.html", account = account)
    except ValueError:
        return render_template("account_details.html",error= "Account not found")
    except Exception as e:
        return render_template("account_details.html", error = "An error occurred")
@app_routes.route("/accounts/deposit/<account_number>", methods = ['POST'])
def deposit_account(account_number):
    
    
    try:
        amount=float(request.form.get("amount"))
        
        from app.services import deposit
        deposit(account_number, amount)
        
        return redirect(url_for("app_routes.view_account", account_number=account_number))
    except ValueError as e:
        return render_template("accounts_details.html", error=str(e), account = search_account(account_number))
    except Exception as e:
        return render_template("account_details.html", error="unexpected error", account = search_account(account_number) )
@app_routes.route("/accounts/withdraw/<account_number>", methods = ['POST'])
def withdraw_account(account_number):
    try:
        amount = float(request.form.get("amount"))
        from app.services import withdraw
        withdraw(account_number, amount)
        return redirect(url_for("app_routes.view_account", account_number=account_number))
    except ValueError as e:
        return render_template("account_details.html", error=str(e), account = search_account(account_number))
    except Exception as e:
        return render_template("account_details.html", error="Unexpected error", account = search_account(account_number))
@app_routes.route("/accounts/transfer", methods = ['POST'])
def transfer_money():
    try:
        sender_account_number = request.form.get("sender_account_number")
        receiver_account_number = request.form.get("receiver_account_number")
        amount = float(request.form.get("amount"))
        from app.services import transfer
        transfer(sender_account_number, receiver_account_number, amount)
        
        return redirect(url_for("app_routes.list_accounts"))
    except ValueError as e:
        return render_template("account_details.html", error=str(e), account = search_account(sender_account_number))
    except Exception as e:
        return render_template("account_details.html", error="Unexpected error.")
@app_routes.route("/accounts/receipt/<account_number>", methods = ['GET'])
def account_receipt(account_number):
    
    try:
        transactions = get_account_transactions(account_number)
        
        account = get_account(account_number)
        
        return render_template("receipt.html", account=account, transactions=transactions)
    except Exception as e:
        return render_template("receipt.html", error = "error unexpected")
    
