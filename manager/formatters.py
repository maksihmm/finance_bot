def format_add_operation(data):
    return f"\nОперация '{data['operation_type']}' на сумму {data['amount']} руб. добавлена. {data['date']}"


def format_del_operation(data):
    return f"\nОперация ID: {data['id']}, '{data['operation_type']}' на сумму {data['amount']} руб. удалена."


def format_del_all_operations():
    return f"\n Все операции удалены!"


def format_edit_operation(data):
    return f"\nОперация ID: {data['id']}, '{data['operation_type']}' на сумму {data['amount']} руб. отредактирована."


def format_operation(data):
    return (f"\nID: {data['id']}, Операция: {data['operation_type']}, Cумма: {data['amount']}, "
            f"Категория: {data['category']}, Комментарии: {data['description']}, Дата: {data['date']}")
