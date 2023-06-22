import csv


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


def writeResults(csv_path: str, results_obj):
    """
    Records results of a speed test to the csv file at the path specified. May raise any errors from open() statement.
    :param csv_path: path to the csv file
    :param results_obj: the results to store, as a Results object
    """

    with open(csv_path, "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([results_obj.download, results_obj.upload, results_obj.timestamp, results_obj.bug_type])


def readResults(csv_path: str):
    """
    Reads the results stored in the file at csv_path. May raise any errors from open() statement.
    :param csv_path: path to csv file to read from
    :return: a list of results objects
    """

    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)