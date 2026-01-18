import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    evidence2 = list()
    labels = list()
    labels2 = list()
    file = open(filename, "r")
    for line in file:
        evidence.append(line.split(",")[:17])
        l = line.split(",")[17]
        labels.append(l)
    for element in labels:
        if element == "TRUE\n":
            labels2.append(1)
        elif element == "FALSE\n":
            labels2.append(0)
    evidence.remove(evidence[0])
    for element in evidence:
        list1 = list()
        list1.append(int(element[0]))
        list1.append(float(element[1]))
        list1.append(int(element[2]))
        list1.append(float(element[3]))
        list1.append(int(element[4]))
        list1.append(float(element[5]))
        list1.append(float(element[6]))
        list1.append(float(element[7]))
        list1.append(float(element[8]))
        list1.append(float(element[9]))
        if element[10] == "Jan":
            list1.append(0)
        if element[10] == "Feb":
            list1.append(1)
        if element[10] == "Mar":
            list1.append(2)
        if element[10] == "Apr":
            list1.append(3)
        if element[10] == "May":
            list1.append(4)
        if element[10] == "Jun":
            list1.append(5)
        if element[10] == "Jul":
            list1.append(6)
        if element[10] == "Aug":
            list1.append(7)
        if element[10] == "Sep":
            list1.append(8)
        if element[10] == "Oct":
            list1.append(9)
        if element[10] == "Nov":
            list1.append(10)
        if element[10] == "Dec":
            list1.append(11)
        list1.append(int(element[11]))
        list1.append(int(element[12]))
        list1.append(int(element[13]))
        list1.append(int(element[14]))
        if element[15] == "Returning_Visitor":
            list1.append(1)
        else:
            list1.append(0)
        if element[16] == "TRUE":
            list1.append(1)
        else:
            list1.append(0)
        evidence2.append(list1)
    return (evidence2, labels2)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(1)

    holdout = int(TEST_SIZE * len(labels))
    testing_evidence = evidence[:holdout]
    testing_labels = labels[:holdout]
    training_evidence = evidence[holdout:]
    training_labels = labels[holdout:]

    model.fit(training_evidence, training_labels)
    model.predict(testing_evidence)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive = 0
    false_positive = 0

    true_negative = 0
    false_negative = 0

    for i, label in enumerate(labels):
        if label == 1:
            if label == predictions[i]:
                true_positive += 1
            else:
                false_positive += 1
        if label == 0:
            if label == predictions[i]:
                true_negative += 1
            else:
                false_negative += 1
    sensitivity = true_positive / (true_positive + false_positive)
    specificity = true_negative / (true_negative + false_negative)
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()