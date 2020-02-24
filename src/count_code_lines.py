"""Program to count the number of lines added and deleted by an indvividual."""

# from git import Repo
from pydriller import RepositoryMining
from prettytable import PrettyTable

# from pydriller.domain.commit import ModificationType


def print_in_table(dictionary):
    """Create and print the table using prettytable."""
    data_table = PrettyTable()
    headings = [
        "Username",
        "Email",
        "Commits",
        "+",
        "-",
        "Total",
        "Lines/Commit",
        "Changed_Lines",
    ]
    data_table.field_names = headings
    for key in dictionary:
        data_table.add_row(
            [
                key,
                dictionary[key][0],
                dictionary[key][1],
                dictionary[key][2],
                dictionary[key][3],
                dictionary[key][4],
                dictionary[key][5],
                dictionary[key][6],
            ]
        )
    print(data_table)


def delete_duplicates(data, keys_to_delete):
    """Delete keys from dictionary, keys are sent in a list."""
    dictionary = data
    for key in keys_to_delete:
        print(dictionary[key], " will be removed")
        del dictionary[key]
        print(key in dictionary)
    return dictionary


def parse_email(email):
    """Locate @ and + sign in email and returns the string between them."""
    # find the index of @ sign
    plus_index = email.find("+")
    # find the index of + sign
    at_index = email.find("@")
    # slices string accordingly
    revised_email = email[(plus_index + 1) : at_index]
    return revised_email


# NOTE: there are issues with this function, calls have been commented out
def check_emails(data):
    """Remove @github email from users and merges data with duplicates."""
    dictionary = data
    # list intended to gather keys with issues
    name_issues = []
    # gather keys that have issues and duplicates in dictionary
    keys_to_delete = []
    # loop through the data and add keys that have @github email to name_issues
    for key in dictionary:
        # checks if the email is a github email
        if "noreply.github.com" in dictionary[key][0]:
            # adds the key to issues list
            name_issues.append(key)
            # send email to parsing function
            new_name = parse_email(dictionary[key][0])
            if new_name in dictionary:
                print(new_name, " name to be merged with ", key)
                dictionary[new_name][1] += dictionary[key][1]
                dictionary[new_name][2] += dictionary[key][2]
                dictionary[new_name][3] += dictionary[key][3]
                dictionary[new_name][4] += dictionary[key][4]
                keys_to_delete.append(key)
            else:
                print(new_name, " not found in data")

    dictionary = delete_duplicates(dictionary, keys_to_delete)
    return dictionary


def get_commit_average(dictionary):
    """ Add number of commits and rounds up the number."""
    data = dictionary
    for key in data:
        average = (int)((dictionary[key][2] + dictionary[key][3]) / dictionary[key][1])
        dictionary[key].append(average)
    return data


def get_commit_lines(repo_path):
    """Return the number of lines that were added or deleted.

    as a dictionary.
    """
    data_list = {}
    # creates a hashmap where the key is the authors username
    # goes through all the commits in the current branch of the repo
    for commit in RepositoryMining(repo_path).traverse_commits():
        author = commit.author.name
        email = commit.author.email
        if author in data_list:
            data_list[author][1] += 1
        else:
            # creates a new key and add the data
            data_list[author] = [email, 1, 0, 0, 0, 0]
        # goes through the files in the current commit
        for file in commit.modifications:
            added_lines = file.added
            removed_lines = file.removed

            total_lines = added_lines - removed_lines
            data_list[author][2] += added_lines
            data_list[author][3] += removed_lines
            data_list[author][4] += total_lines
            data_list[author][5] += added_lines + removed_lines
    return data_list


def main():
    """Call other functions in this module asking for user input."""
    # takes input for the repository local path OR URL
    path_repo = input("Enter the path to the repo : ")
    data = get_commit_lines(path_repo)
    data = get_commit_average(data)
    # print("data before checking")
    print_in_table(data)
    # print("data after checking")
    # data = check_emails(data)
    # print_in_table(data)


if __name__ == "__main__":
    main()