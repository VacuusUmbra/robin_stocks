from csv import writer
from datetime import date, timedelta, datetime
import sys
from pathlib import Path
import robin_stocks.helper as helper
import robin_stocks.orders as orders
import robin_stocks.stocks as stocks


def fix_file_extension(file_name):
    """ Takes a file extension and makes it end with .csv

    :param file_name: Name of the file.
    :type file_name: str
    :returns: Adds or replaces the file suffix with .csv and returns it as a string.

    """
    path = Path(file_name)
    path = path.with_suffix('.csv')
    return path.resolve()

def create_absolute_csv(dir_path, file_name, order_type):
    """ Creates a filepath given a directory and file name.

    :param dir_path: Absolute or relative path to the directory the file will be written.
    :type dir_path: str
    :param file_name: An optional argument for the name of the file. If not defined, filename will be stock_orders_{current date}
    :type file_name: str
    :param file_name: Will be 'stock', 'option', or 'crypto'
    :type file_name: str
    :returns: An absolute file path as a string.

    """
    path = Path(dir_path)
    directory = path.resolve()
    if not file_name:
        file_name = "{}_orders_{}.csv".format(order_type, date.today().strftime('%b-%d-%Y'))
    else:
        file_name = fix_file_extension(file_name)
    return(Path.joinpath(directory, file_name))


@helper.login_required
def export_completed_stock_orders(dir_path, file_name=None):
    """Write all completed orders to a csv file

    :param dir_path: Absolute or relative path to the directory the file will be written.
    :type dir_path: str
    :param file_name: An optional argument for the name of the file. If not defined, filename will be stock_orders_{current date}
    :type file_name: Optional[str]

    """
    file_path = create_absolute_csv(dir_path, file_name, 'stock')
    all_orders = orders.get_all_stock_orders()
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'symbol',
            'date',
            'order_type',
            'side',
            'fees',
            'quantity',
            'average_price'
        ])
        for order in all_orders:
            if order['state'] == 'filled' and order['cancel'] is None:
                csv_writer.writerow([
                    stocks.get_symbol_by_url(order['instrument']),
                    order['last_transaction_at'],
                    order['type'],
                    order['side'],
                    order['fees'],
                    order['quantity'],
                    order['average_price']
                ])
        f.close()

@helper.login_required
def export_all_stock_orders(dir_path, file_name=None):
    """Write all completed orders to a csv file

    :param dir_path: Absolute or relative path to the directory the file will be written.
    :type dir_path: str
    :param file_name: An optional argument for the name of the file. If not defined, filename will be stock_orders_{current date}
    :type file_name: Optional[str]

    """
    file_path = create_absolute_csv(dir_path, file_name, 'stock')
    all_orders = orders.get_all_stock_orders()
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'symbol',
            'date',
            'order_type',
            'side',
            'fees',
            'quantity',
            'average_price'
        ])
        for order in all_orders:
            csv_writer.writerow([
                stocks.get_symbol_by_url(order['instrument']),
                order['last_transaction_at'],
                order['type'],
                order['side'],
                order['fees'],
                order['quantity'],
                order['average_price']
            ])
        f.close()

@helper.login_required
def export_completed_option_orders(dir_path, file_name=None, page_limit=sys.maxsize):
    """Write all completed option orders to a csv

        :param dir_path: Absolute or relative path to the directory the file will be written.
        :type dir_path: str
        :param file_name: An optional argument for the name of the file. If not defined, filename will be option_orders_{current date}
        :type file_name: Optional[str]

    """
    file_path = create_absolute_csv(dir_path, file_name, 'option')
    all_orders = orders.get_all_option_orders(page_limit)
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'chain_symbol',
            'expiration_date',
            'strike_price',
            'option_type',
            'side',
            'order_created_at',
            'direction',
            'order_quantity',
            'order_type',
            'opening_strategy',
            'closing_strategy',
            'price',
            'processed_quantity'
        ])
        for order in all_orders:
            if order['state'] == 'filled':
                for leg in order['legs']:
                    instrument_data = helper.request_get(leg['option'])
                    csv_writer.writerow([
                        order['chain_symbol'],
                        instrument_data['expiration_date'],
                        instrument_data['strike_price'],
                        instrument_data['type'],
                        leg['side'],
                        order['created_at'],
                        order['direction'],
                        order['quantity'],
                        order['type'],
                        order['opening_strategy'],
                        order['closing_strategy'],
                        order['price'],
                        order['processed_quantity']
                    ])
        f.close()

@helper.login_required
def export_all_option_orders(dir_path, file_name=None, page_limit=sys.maxsize):
    """Write all option orders to a csv

        :param dir_path: Absolute or relative path to the directory the file will be written.
        :type dir_path: str
        :param file_name: An optional argument for the name of the file. If not defined, filename will be option_orders_{current date}
        :type file_name: Optional[str]

    """
    file_path = create_absolute_csv(dir_path, file_name, 'option')
    all_orders = orders.get_all_option_orders(page_limit)
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'chain_symbol',
            'expiration_date',
            'strike_price',
            'option_type',
            'side',
            'order_created_at',
            'direction',
            'order_quantity',
            'order_type',
            'opening_strategy',
            'closing_strategy',
            'price',
            'processed_quantity'
        ])
        for order in all_orders:
                for leg in order['legs']:
                    instrument_data = helper.request_get(leg['option'])
                    csv_writer.writerow([
                        order['chain_symbol'],
                        instrument_data['expiration_date'],
                        instrument_data['strike_price'],
                        instrument_data['type'],
                        leg['side'],
                        order['created_at'],
                        order['direction'],
                        order['quantity'],
                        order['type'],
                        order['opening_strategy'],
                        order['closing_strategy'],
                        order['price'],
                        order['processed_quantity']
                    ])
        f.close()

@helper.login_required
def export_option_orders_date_range(dir_path, start_date, end_date, file_name=None, page_limit=sys.maxsize):
    """Write all of the option orders within a date range to a csv

        :param dir_path: Absolute or relative path to the directory the file will be written.
        :type dir_path: str
        :param file_name: An optional argument for the name of the file. If not defined, filename will be option_orders_{current date}
        :type file_name: Optional[str]
        :param start_date: The start of the date range in format 2020-12-21
        :type start_date: str
        :param end_date: The end of the date range in format 2020-12-21
        :type end_date: str

    """
    file_path = create_absolute_csv(dir_path, file_name, 'option')
    all_orders = orders.get_all_option_orders(page_limit)
    with open(file_path, 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerow([
            'chain_symbol',
            'expiration_date',
            'strike_price',
            'option_type',
            'side',
            'order_created_at',
            'direction',
            'order_quantity',
            'order_type',
            'opening_strategy',
            'closing_strategy',
            'price',
            'processed_quantity'
        ])
        for order in all_orders:
            orderDate = datetime.strptime(order['created_at'][:10], "%Y-%m-%d")
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start <= orderDate <= end:
                for leg in order['legs']:
                    instrument_data = helper.request_get(leg['option'])
                    csv_writer.writerow([
                        order['chain_symbol'],
                        instrument_data['expiration_date'],
                        instrument_data['strike_price'],
                        instrument_data['type'],
                        leg['side'],
                        order['created_at'],
                        order['direction'],
                        order['quantity'],
                        order['type'],
                        order['opening_strategy'],
                        order['closing_strategy'],
                        order['price'],
                        order['processed_quantity']
                    ])
        f.close()

@helper.login_required
def export_todays_option_orders(dir_path, file_name=None):
    today = date.today().strftime("%Y-%m-%d")
    yesterday = (today - timedelta(days = 1)).strftime("%Y-%m-%d")
    self.export_option_orders_date_range(dir_path, today, yesterday, file_name,100)