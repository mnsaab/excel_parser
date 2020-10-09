from modules.helper import generate_outfile_for_kpi_dashboard, extract_categories
from pandas import read_excel
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--part1", action="store_true")
    parser.add_argument("--part2", action="store_true")
    args = parser.parse_args()

    dframe = read_excel(
        "Demo_Assessment_Model_08.18.20.xlsx", sheet_name="KPI Dashboard", header=None
    )

    categories = extract_categories(dframe)

    if args.part2:
        for cat in categories:
            cat.build_datasets_for_dates(dframe)
        generate_outfile_for_kpi_dashboard(categories, True)
    else:
        generate_outfile_for_kpi_dashboard(categories, False)


if __name__ == "__main__":
    main()
