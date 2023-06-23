import csv

from broadbandbug.library.classes import Result


# Checks whether the file specified exists, making it if it does not.
def makeFile(path: str):
    try:
        path = open(str(path), "r")
        path.close()
        return True
    except FileNotFoundError:
        path = open(str(path), "w")
        path.close()
        return False


def writeResults(csv_path: str, result_obj):
    """
    Records results of a speed test to the csv file at the path specified. May raise any errors from open() statement.
    :param csv_path: path to the csv file
    :param result_obj: the results to store, as a Result object
    """

    with open(csv_path, "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([result_obj.download, result_obj.upload, result_obj.timestamp, result_obj.method])


def readResults(csv_path: str):
    """
    Reads the results stored in the file at csv_path. May raise any errors from open() statement.
    :param csv_path: path to csv file to read from
    :return: a dictionary of results objects, separating different types of bugs
    """

    results_dict = {}

    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)

        # Unpack each row into Result object
        for row in reader:
            result = Result(*row)

            # If the result type has not yet been encountered, make a new category
            if result.method not in results_dict.keys():
                # Add the result to the new list when instantiating the new list
                results_dict[result.method] = [result]

            # Otherwise, add the result to the relevant type
            else:
                results_dict[result.method].append(result)

    return results_dict
