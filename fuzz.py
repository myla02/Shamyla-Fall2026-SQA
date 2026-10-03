
import contextlib
import io
import os
import random
import string
import tempfile

import parser


TESTS_PER_METHOD = 100
RANDOM_SEED = 42

failures = []


def random_string(max_length=100):
    """Generate a random string for fuzz testing."""
    length = random.randint(0, max_length)

    characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
        + " \n\t"
    )

    return "".join(
        random.choice(characters)
        for _ in range(length)
    )


def random_value():
    """Generate different values for fuzz testing."""
    values = [
        None,
        "",
        random_string(),
        random.randint(-10000, 10000),
        random.random(),
        True,
        False,
        [],
        {},
        [random_string()],
        {random_string(): random_string()},
    ]

    return random.choice(values)


def record_failure(method_name, test_number, test_input, error):
    """Store a fuzz failure for later review."""
    failures.append(
        {
            "method": method_name,
            "test": test_number,
            "input_type": type(test_input).__name__,
            "input": repr(test_input),
            "error_type": type(error).__name__,
            "error": str(error),
        }
    )


# Method 1
def fuzz_checkIfWeirdYAML():
    print("1. Fuzzing parser.checkIfWeirdYAML...")

    for i in range(TESTS_PER_METHOD):
        test_input = random_value()

        try:
            parser.checkIfWeirdYAML(test_input)
        except Exception as error:
            record_failure(
                "checkIfWeirdYAML",
                i + 1,
                test_input,
                error,
            )


# Method 2
def fuzz_checkIfValidHelm():
    print("2. Fuzzing parser.checkIfValidHelm...")

    for i in range(TESTS_PER_METHOD):
        test_input = random_value()

        try:
            parser.checkIfValidHelm(test_input)
        except Exception as error:
            record_failure(
                "checkIfValidHelm",
                i + 1,
                test_input,
                error,
            )


# Method 3
def fuzz_keyMiner():
    print("3. Fuzzing parser.keyMiner...")

    for i in range(TESTS_PER_METHOD):
        dictionary_input = random_value()
        value_input = random_value()

        try:
            parser.keyMiner(
                dictionary_input,
                value_input,
            )
        except Exception as error:
            record_failure(
                "keyMiner",
                i + 1,
                (dictionary_input, value_input),
                error,
            )


# Method 4
def fuzz_getKeyRecursively():
    print("4. Fuzzing parser.getKeyRecursively...")

    for i in range(TESTS_PER_METHOD):
        test_input = random_value()

        try:
            parser.getKeyRecursively(
                test_input,
                [],
            )
        except Exception as error:
            record_failure(
                "getKeyRecursively",
                i + 1,
                test_input,
                error,
            )


# Method 5
def fuzz_getValuesRecursively():
    print("5. Fuzzing parser.getValuesRecursively...")

    for i in range(TESTS_PER_METHOD):
        test_input = random_value()

        try:
            parser.getValuesRecursively(
                test_input
            )
        except Exception as error:
            record_failure(
                "getValuesRecursively",
                i + 1,
                test_input,
                error,
            )


# Method 6
def fuzz_getValsFromKey():
    print("6. Fuzzing parser.getValsFromKey...")

    for i in range(TESTS_PER_METHOD):
        dictionary_input = random_value()
        target_input = random_value()

        try:
            parser.getValsFromKey(
                dictionary_input,
                target_input,
                [],
            )
        except Exception as error:
            record_failure(
                "getValsFromKey",
                i + 1,
                (dictionary_input, target_input),
                error,
            )


# Method 7
def fuzz_update_json_paths():
    print("7. Fuzzing parser.update_json_paths...")

    for i in range(TESTS_PER_METHOD):
        test_input = random_value()

        try:
            parser.update_json_paths(
                test_input
            )
        except Exception as error:
            record_failure(
                "update_json_paths",
                i + 1,
                test_input,
                error,
            )


# Method 8
def fuzz_getSingleDict4MultiDocs():
    print("8. Fuzzing parser.getSingleDict4MultiDocs...")

    for i in range(TESTS_PER_METHOD):
        test_input = random_value()

        try:
            parser.getSingleDict4MultiDocs(
                test_input
            )
        except Exception as error:
            record_failure(
                "getSingleDict4MultiDocs",
                i + 1,
                test_input,
                error,
            )


def create_fuzz_file():
    """Create a temporary YAML file containing random data."""
    content = random_string(500)

    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".yaml",
        delete=False,
    )

    temp_file.write(content)
    temp_file.close()

    return temp_file.name, content


# Method 9
def fuzz_readYAMLAsStr():
    print("9. Fuzzing parser.readYAMLAsStr...")

    for i in range(TESTS_PER_METHOD):
        file_path, content = create_fuzz_file()

        try:
            parser.readYAMLAsStr(file_path)
        except Exception as error:
            record_failure(
                "readYAMLAsStr",
                i + 1,
                content,
                error,
            )
        finally:
            os.remove(file_path)


# Method 10
def fuzz_loadMultiYAML():
    print("10. Fuzzing parser.loadMultiYAML...")

    for i in range(TESTS_PER_METHOD):
        file_path, content = create_fuzz_file()

        try:
            # Prevent parser messages such as "skipping"
            # from filling the fuzz-test output.
            with contextlib.redirect_stdout(io.StringIO()):
                parser.loadMultiYAML(file_path)

        except Exception as error:
            record_failure(
                "loadMultiYAML",
                i + 1,
                content,
                error,
            )

        finally:
            os.remove(file_path)


def write_log():
    """Write fuzz-test results to fuzz_results.log."""

    with open("fuzz_results.log", "w") as log:
        log.write("Slikube Fuzz Testing Results\n")
        log.write("============================\n\n")

        log.write(f"Random seed: {RANDOM_SEED}\n")
        log.write(f"Methods fuzzed: 10\n")
        log.write(
            f"Tests per method: {TESTS_PER_METHOD}\n"
        )
        log.write(
            f"Total fuzz cases: {10 * TESTS_PER_METHOD}\n"
        )
        log.write(
            f"Failures detected: {len(failures)}\n\n"
        )

        if not failures:
            log.write("No exceptions were detected.\n")
            return

        log.write(
            "Failures are fuzzing observations and "
            "must be manually reviewed before being "
            "classified as software bugs.\n\n"
        )

        for failure in failures:
            log.write(
                f"Method: {failure['method']}\n"
            )
            log.write(
                f"Test: {failure['test']}\n"
            )
            log.write(
                f"Input type: {failure['input_type']}\n"
            )
            log.write(
                f"Input: {failure['input']}\n"
            )
            log.write(
                f"Error: "
                f"{failure['error_type']}: "
                f"{failure['error']}\n"
            )
            log.write("-" * 50 + "\n")


def print_failure_summary():
    """Display a short summary of unique failure types."""

    unique_failures = {}

    for failure in failures:
        key = (
            failure["method"],
            failure["error_type"],
            failure["error"],
        )

        unique_failures[key] = (
            unique_failures.get(key, 0) + 1
        )

    print("\nFailure summary:")

    if not unique_failures:
        print("No exceptions detected.")
        return

    for key, count in unique_failures.items():
        method, error_type, error = key

        print(
            f"- {method}: "
            f"{error_type}: {error} "
            f"({count} occurrence(s))"
        )


if __name__ == "__main__":
    random.seed(RANDOM_SEED)

    print("Starting Slikube fuzz testing...")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Tests per method: {TESTS_PER_METHOD}")
    print()

    fuzz_checkIfWeirdYAML()
    fuzz_checkIfValidHelm()
    fuzz_keyMiner()
    fuzz_getKeyRecursively()
    fuzz_getValuesRecursively()
    fuzz_getValsFromKey()
    fuzz_update_json_paths()
    fuzz_getSingleDict4MultiDocs()
    fuzz_readYAMLAsStr()
    fuzz_loadMultiYAML()

    write_log()
    print_failure_summary()

    print("\n--------------------------------")
    print("Fuzz testing complete.")
    print("Methods fuzzed: 10")
    print(
        f"Total fuzz cases: "
        f"{10 * TESTS_PER_METHOD}"
    )
    print(
        f"Failures detected: {len(failures)}"
    )
    print(
        "Detailed results: fuzz_results.log"
    )
    print("--------------------------------")