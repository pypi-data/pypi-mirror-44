import pandas as pd
from miner_toolbox import miner_toolbox
from datetime import datetime
import time


if __name__ == '__main__':
    # load dataframe, first in memory
    data = [
        {"oscis": "100", "assignment": "wurst", "since": "2018-01-01", "till": '2018-02-28'},
        {"oscis": "100", "assignment": "energy", "since": "2018-03-01"},
        {"oscis": "101", "assignment": "energy"}
    ]

    oscis_df = pd.DataFrame(data=data)

    print('assignment of 100: ',
          miner_toolbox.decide(
              data_to_use=oscis_df,
              cutoff='2018-02-01',
              category_field='oscis',
              category='100',
              default_assignment=''
          )
          )

    # cutoff_date = datetime.strptime('2018-02-01', '%Y-%m-%d')
    cutoff_date = time.time()

    print('assignment of 101: ',
          miner_toolbox.decide(
              data_to_use=oscis_df,
              cutoff=cutoff_date,
              category_field='oscis',
              category='101',
              default_assignment=''
          )
          )