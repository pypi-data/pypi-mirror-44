import pandas as pd
import io
from miner_toolbox import miner_toolbox
from datetime import datetime
import time


if __name__ == '__main__':
    # load dataframe, at first into memory
    costs_df = pd.read_excel(
        io='C://Users/rovna/AnacondaProjects/180619_MonthlyClosure/work/costs.xls',
        index_col=0
    )

    bbs_enum = pd.read_excel(
        io='C://Users/rovna/AnacondaProjects/180619_MonthlyClosure/enums/budget_bones_details.xlsx',
        sheet_name='enum',
        index_col=0,
        usecols=(0, 4),
        na_values='NaN',
        keep_default_na=False
    )

    # print('bbs_enum', bbs_enum)
    # print('bbs_enum.index', bbs_enum.index)
    # print('bbs_enum', bbs_enum['bdg_bone_id'])

    miner_toolbox.fix_assignment_using_bbs(
        bbs_enum_df=bbs_enum,
        target_df=costs_df,
        source_column_name='person',
        target_column_name='repaired_2',
        bbs_column_name='budgetBoneId',
        overwrite=True,
        fill_unused_with_source_column_value=True
    )

    # output back to excel
    writer = pd.ExcelWriter(
        path='C://Users/rovna/AnacondaProjects/180619_MonthlyClosure/work/costs_team_assignment_test_0.0.2.xlsx',
        engine='xlsxwriter'
    )

    # export specific data frame
    costs_df.to_excel(writer, sheet_name = "costs_manual_corr", freeze_panes=(1,1))

    writer.save()