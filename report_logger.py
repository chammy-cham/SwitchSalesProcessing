import pandas as pd

from sale import Sale
from sales_calculator import SalesCalculator

class ReportLogger:
    """
        Keeping this name generic as it could be used
        for items that are not sales ...

        These reports will probably share some functionality ...

    """

    def __init__(self, sales):
        self.sales_list = sales
        self.sales_calculator = SalesCalculator(sales)

    def _get_sales_dict(self):
        df = pd.DataFrame.from_records([sale.to_dict() for sale in self.sales_list])
        return df

    def basic_report(self):
        """ return a basic report """
        df = self._get_sales_dict()
        df['total_value'] = df.apply(lambda row: row['amount'] * row['value'], axis=1)
        total_value_df = df.groupby(['product'])['total_value'].sum().reset_index(name='full_value')
        count_df = df.groupby(['product'])['value'].count().reset_index(name='count')
        basic_report_df = pd.merge(count_df, total_value_df, on=['product'])
        return basic_report_df

    def end_report(self):
        """ return the end report """


def main():
    rl = ReportLogger([Sale('Orange', 10), Sale('Apple', 20), Sale('Apple', 20, amount=5)])
    report = rl.basic_report()
    print(report)
    """
    count is counting the number of times apple shows up but it should do 
    for each apple - look at amount, add this amount to previous value.
    
    split apply combine 
     
    """

if __name__ == '__main__':
    main()