import sys 
import csv
import logging

from classifier.classifier import classify_statements

logging.getLogger().setLevel(logging.DEBUG)
logging_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging_formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

def add_categories_to_statements(statements, categories):
    """
    """
    logger.debug(f"combining {statements=} and {categories=}")
    return [[*x, y] for x, y in zip(statements, categories)]

def main():
    with open("testdata/user_instructions.txt", "r") as user_info_file:
        user_info = user_info_file.read()
    with open("testdata/mutations_small.csv", "r") as statements_file:
        reader = csv.reader(statements_file)
        statements = [row for row in reader]
    
    categories = classify_statements(statements, user_info)
    logger.info(f"found {categories=}")
    output = add_categories_to_statements(statements, categories)
    logger.debug(f"{output=}")
    with open("target/classified.csv", "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(output)

if __name__ == "__main__":
    main()