from datetime import datetime
# import manager.formatters
from manager.constants import INCOME, EXPENSE


def find_operation_by_id(data, id_operation):
    for operation in data:
        if id_operation == operation['id']:
            return operation
    return None


def add_operation(operations, operation_type, amount, category, description='нет'):
    now_date = datetime.now().strftime('%Y-%m-%d')
    operation = {
        'id': get_next_id(operations),
        'operation_type': operation_type,
        'amount': amount,
        'category': category,
        'description': description,
        'date': now_date
    }
    operations.append(operation)
    return operation


def get_next_id(data):
    if not data:
        return 1
    else:
        max_id = max(operation['id'] for operation in data)
        return max_id + 1


def filter_by_category(data, category):
    result = []
    for operation in data:
        if category in operation['category']:
            result.append(operation)
    return result


def filter_by_amount_range(data, start_amount, end_amount):
    result = []
    for operation in data:
        if start_amount <= operation['amount'] <= end_amount:
            result.append(operation)
    return result


def filter_by_type(data, operation_type):
    result = []
    for operation in data:
        if operation_type == operation['operation_type']:
            result.append(operation)
    return result


def total_amount(data):
    res = 0
    for operation in data:
        if operation['operation_type'] == INCOME:
            res += operation['amount']
        elif operation['operation_type'] == EXPENSE:
            res -= operation['amount']
    return res


def delete_operation(data, operation):
    data.remove(operation)
    return operation


def delete_all_operation(data):
    data.clear()
    return


# def edit_operation(operation, key_operation, value_operation):
#     operation[key_operation] = value_operation
#     return operation


# def has_operations(data):
#     return bool(data)


# def print_operations(data):
#     for operation in data:
#         print(manager.formatters.format_operation(operation))


# def show_empty_operations_message():
#     print("\nОпераций не найдено!")
