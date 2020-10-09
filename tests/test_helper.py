from modules.helper import extract_categories
from datetime import datetime
from pandas import DataFrame
from math import nan

data = [
    [nan, nan, nan, nan, nan, nan],
    [nan, nan, "ingredients", nan, nan, nan],
    [
        nan,
        "ingredients",
        "Burgers",
        datetime(2020, 7, 28, 5, 36, 00),
        datetime(2020, 8, 28, 5, 36, 00),
        datetime(2020, 9, 28, 5, 36, 00),
        datetime(2020, 10, 28, 5, 36, 00),
    ],
    [nan, nan, "tomato", 1, 1, 2, 1],
    [nan, nan, "meat", 2, 0.5, 1, 2],
    [nan, nan, "cheese", 3, nan, 2, 1.5],
    [nan, nan, "onion", 1, 0.25, 0, 3],
    [],
]
df = DataFrame(data=data)


def test_extract_categories_with_only_one_category():
    categories = extract_categories(df)

    assert_object = {
        "name": "Burgers",
        "fields": ["tomato", "meat", "cheese", "onion"],
        "subsets": ["ingredients"],
        "start_date": "2020-07-28T05:36:00+00:00",
        "end_date": "2020-10-28T05:36:00+00:00",
        "data": [],
    }

    assert len(categories) == 1
    assert categories[0].get_category_info(True) == assert_object


def test_extract_categories_with_duplicate_categories_and_two_subsets():
    data.extend(
        [
            [nan, nan, "sandwiches"],
            [
                nan,
                "sandwiches",
                "Burgers",
                datetime(2020, 7, 28, 5, 36, 00),
                datetime(2020, 8, 28, 5, 36, 00),
                datetime(2020, 9, 28, 5, 36, 00),
                datetime(2020, 10, 28, 5, 36, 00),
            ],
            [nan, nan, "tomato", 6, 4, 2, 0.5],
            [nan, nan, "meat", 2, 1, 0.3, 4],
            [nan, nan, "cheese", 3, 8, 2, nan],
            [nan, nan, "onion", 2, 1, nan, 3],
            [],
        ]
    )

    new_df = DataFrame(data=data)

    categories = extract_categories(new_df)

    assert len(categories) == 1
    assert len(categories[0].subsets_and_indices.keys()) == 2
    assert list(categories[0].subsets_and_indices.keys())[1] == "sandwiches"


def test_extract_categories_with_two_categories_and_one_subset():
    data.extend(
        [
            [
                nan,
                nan,
                "grilled cheese",
                datetime(2020, 7, 28, 5, 36, 00),
                datetime(2020, 8, 28, 5, 36, 00),
                datetime(2020, 9, 28, 5, 36, 00),
                datetime(2020, 10, 28, 5, 36, 00),
            ],
            [nan, nan, "cheese", 5, 6, 7, 3],
            [],
        ]
    )

    new_df = DataFrame(data=data)

    categories = extract_categories(new_df)

    assert len(categories) == 2
    assert list(categories[0].subsets_and_indices.keys())[0] == "ingredients"
    assert list(categories[1].subsets_and_indices.keys())[0] == "all"
