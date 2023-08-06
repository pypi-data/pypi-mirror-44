from typing import Iterable

from fireant import Metric
from .pandas import Pandas


class CSV(Pandas):
    def __init__(self, metric: Metric, *metrics: Iterable[Metric], group_pagination=False, **kwargs):
        super().__init__(metric, *metrics, **kwargs)
        self.group_pagination = group_pagination

    def transform(self, data_frame, slicer, dimensions, references):
        result_df = super(CSV, self).transform(data_frame, slicer, dimensions, references)
        result_df.columns.names = [None]
        return result_df.to_csv()
