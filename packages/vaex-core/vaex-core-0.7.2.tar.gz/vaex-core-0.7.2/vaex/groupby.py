class GroupBy(object):
    def __init__(self, df, by):
        self.df = df
        self.by = by
        self._waslist, [self.by, ] = vaex.utils.listify(by)

    def size(self):
        import pandas as pd
        result = self.df.count(binby=self.by, shape=[10000] * len(self.by)).astype(np.int64)
        #values = vaex.utils.unlistify(self._waslist, result)
        values = result
        series = pd.Series(values, index=self.df.category_labels(self.by[0]))
        return series

    def agg