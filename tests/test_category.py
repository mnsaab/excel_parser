from modules.category import Category
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
]
df = DataFrame(data=data)


def test_catgeory_creation_and_adding_of_fields_and_subsets():
    burgers = Category(
        "Burgers", datetime(2020, 7, 28, 5, 36, 00), datetime(2021, 7, 28, 5, 36, 00)
    )

    burgers.add_field("tomato", 1)
    burgers.add_field("meat", 2)
    burgers.add_field("cheese", 3)
    burgers.add_field("patty", 4)
    burgers.add_field("onion", 5)
    burgers.add_subset("ingredients", 0)

    assert len(burgers.fields_and_indices) == 5
    assert len(burgers.subsets_and_indices) == 1
    assert burgers.subsets_and_indices["ingredients"] == 0
    assert burgers.fields_and_indices["cheese"] == 3


def test_catgeory_creation_and_returning_of_data():
    burgers = Category(
        "Burgers", datetime(2020, 7, 28, 5, 36, 00), datetime(2021, 7, 28, 5, 36, 00)
    )

    burgers.add_field("tomato", 1)
    burgers.add_field("meat", 2)
    burgers.add_subset("ingredients", 0)

    assert_object = {
        "name": "Burgers",
        "fields": ["tomato", "meat"],
        "subsets": ["ingredients"],
        "start_date": "2020-07-28T05:36:00+00:00",
        "end_date": "2021-07-28T05:36:00+00:00",
    }

    assert assert_object == burgers.get_category_info()


def test_build_datasets_for_dates_basic_test():
    burgers = Category(
        "Burgers", datetime(2020, 7, 28, 5, 36, 00), datetime(2021, 10, 28, 5, 36, 00)
    )

    burgers.add_field("tomato", 1)
    burgers.add_field("meat", 2)
    burgers.add_field("cheese", 3)
    burgers.add_field("onion", 4)
    burgers.add_subset("ingredients", 2)

    burgers.build_datasets_for_dates(df)
    assert len(burgers.data) == 4
    assert burgers.data[0]["values"][0]["name"] == "tomato"
    assert burgers.data[0]["values"][0]["subset"] == "ingredients"
    assert burgers.data[0]["values"][0]["value"] == 1
