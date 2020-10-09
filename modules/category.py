from datetime import datetime, timezone
from pandas import isnull

VALUES = "values"


class Category:
    def __init__(self, cat_name, start_date, end_date):
        self.category = cat_name
        self.start_date = start_date.replace(tzinfo=timezone.utc)
        self.end_date = end_date.replace(tzinfo=timezone.utc)
        self.data = []

        # This dictionary keeps track of two things:
        ## 1. What the fields are for this category
        ## 2. Where the field is in relation to the category on the dataframe
        self.fields_and_indices = {}

        # This dictionary keeps track of two things:
        ## 1. What the subsets are for this category
        ## 2. Where the subset is for this category on the dataframe
        self.subsets_and_indices = {}

    def get_category_info(self, add_data=False):
        return_object = {
            "name": self.category,
            "fields": [field for field in self.fields_and_indices.keys()],
            "subsets": [subset for subset in self.subsets_and_indices.keys()],
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }

        if not add_data:
            return return_object

        return_object["data"] = self.data
        return return_object

    def build_datasets_for_dates(self, dataframe):
        start_col = 3
        end_range = len(dataframe.columns)

        for date_col in range(start_col, end_range):
            subset_index_1 = list(self.subsets_and_indices.keys())[0]
            date = dataframe[date_col][
                self.subsets_and_indices[subset_index_1]
            ].replace(tzinfo=timezone.utc)
            dataset = {"date": date.isoformat(), VALUES: []}

            for subset, sindex in self.subsets_and_indices.items():
                for field, findex in self.fields_and_indices.items():
                    if isnull(dataframe[date_col][findex + sindex]):
                        continue
                    dataset[VALUES].append(
                        {
                            "name": field,
                            "subset": subset,
                            "value": dataframe[date_col][findex + sindex],
                        }
                    )
            if dataset[VALUES]:
                self.data.append(dataset)

    def add_field(self, field, index):
        self.fields_and_indices[field] = index

    def add_subset(self, subset, index):
        self.subsets_and_indices[subset] = index
