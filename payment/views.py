from django.shortcuts import render

# Create your views here.


APP_KEY = 'a59b6fddb26240cb05da2dfe2d3008288a479dd5'
ACCESS_KEY = 'a2e383e6-abff-44f2-b7f7-03d1874d3044'
SECRET_KEY = '45308b46-e370-43be-849c-fa47711d5cc8'

from django.shortcuts import render
from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator
from datetime import datetime

def collect_money(request):
    operation = PaymentOperation(APP_KEY, ACCESS_KEY, SECRET_KEY)
    response = operation.make_collect({
        'amount': 100,
        'service': 'MTN',
        'payer': '670000000',
        'date': datetime.now(),
        'nonce': RandomGenerator.nonce(),
        'trxID': '1'
    })
    print(response.is_operation_success())
    print(response.is_transaction_success())

    response_dict = {
        'is_operation_success': response.is_operation_success(),
        'is_transaction_success': response.is_transaction_success(),
        # Add other response attributes as needed
    }

    return render(request, 'payment/collect.html', response_dict)


def deposit(request):
    operation = PaymentOperation(APP_KEY, ACCESS_KEY, SECRET_KEY)
    response = operation.make_deposit({
        'amount': 100,
        'service': 'MTN',
        'receiver': '670000000',
        'date': datetime.now(),
        'nonce': RandomGenerator.nonce(),
        'trxID': '1'
    })
    print(response.is_operation_success())
    print(response.is_transaction_success())

    response_dict = {
        'is_operation_success': response.is_operation_success(),
        'is_transaction_success': response.is_transaction_success(),
        # Add other response attributes as needed
    }

    return render(request, 'payment/deposit.html', response_dict)

def status(request):
    operation = PaymentOperation(APP_KEY, ACCESS_KEY, SECRET_KEY)
    response = operation.get_status()
    context = {
        'response': response
    }
    print(response.name)

    return render(request, 'payment/status.html', context)

def transaction_id(request):
    operation = PaymentOperation(APP_KEY, ACCESS_KEY, SECRET_KEY)
    response = operation.get_transactions(['ID1', 'ID2'])
    print(response)
    context = {
        'response': response
    }

    return render(request, 'payment/transaction.html', context)