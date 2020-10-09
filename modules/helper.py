import json
from pandas import to_datetime, isnull
from datetime import datetime, timezone
from modules.category import Category


def extract_categories(dataframe):
    SUBSET_CELL = 1
    CAT_FIELD_CELL = 2
    DATE_CELL = 3

    categories = {}
    cur_category = None
    cur_index = 0
    accounted_for = False

    for index, item in dataframe.iterrows():
        # On Category
        if isinstance(item[DATE_CELL], datetime):
            cur_category = item[CAT_FIELD_CELL]
            accounted_for = False
            if cur_category not in categories:
                cur_index = index
                categories[cur_category] = Category(
                    cur_category, item[DATE_CELL], item[len(item) - 1]
                )
            else:
                accounted_for = True

            if not isnull(item[SUBSET_CELL]):
                categories[cur_category].add_subset(item[1], index)
            elif isnull(item[SUBSET_CELL]) and accounted_for == False:
                categories[cur_category].add_subset("all", index)

        # This elif checks for 4 things:
        ## 1. Row is not empty
        ## 2. There is a category already added to the whole dict for this field
        ## 3. If the fields have already been added by visiting this category again
        ## 4. The current cell does not equal to the subset cell 1 row below and
        ### one cell to the left
        elif (
            not isnull(item[CAT_FIELD_CELL])
            and cur_category in categories
            and not accounted_for
            and dataframe[SUBSET_CELL][index + 1] != item[CAT_FIELD_CELL]
        ):
            categories[cur_category].add_field(item[CAT_FIELD_CELL], index - cur_index)

    return [cat for cat in categories.values()]


def generate_outfile_for_kpi_dashboard(categories, include_data=False):
    with open("output.json", "w") as outfile:
        json.dump(
            {
                "source": "KPI Dashboard",
                "categories": [
                    cat.get_category_info(include_data) for cat in categories
                ],
            },
            outfile,
        )
