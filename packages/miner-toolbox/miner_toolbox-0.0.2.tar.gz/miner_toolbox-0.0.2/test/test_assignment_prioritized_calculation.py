import pandas as pd
import io
from miner_toolbox import miner_toolbox
from datetime import datetime
import time


if __name__ == '__main__':
    # load dataframe, at first into memory
    costs_df = pd.read_excel(
        io='C://Users/rovna/AnacondaProjects/180619_MonthlyClosure/output/closure_gen_Aston_09_2018_v3.52.xlsx',
        sheet_name='costs',
        index_col=0
    )

    miner_toolbox.decide_multiple_assignments(
        target_df=costs_df,
        columns_prioritized=['person_to_team', 'project_to_team', 'team'],
        new_column_name='etwas'
    )

    # output back to excel
    writer = pd.ExcelWriter(
        path='C://Users/rovna/AnacondaProjects/180619_MonthlyClosure/work/costs_assignment_prioritization_0.0.2.b.xlsx',
        engine='xlsxwriter'
    )

    # export specific data frame
    costs_df.to_excel(
        writer,
        sheet_name='costs_wo_priority',
        freeze_panes=(1,1)
    )

    writer.save()