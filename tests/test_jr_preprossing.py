import os
import subprocess

# Get the absolute path to the tests directory
tests_dir = os.path.dirname(os.path.abspath(__file__))
# Set the path to the log.txt file in the tests directory
log_file_path = os.path.join(tests_dir, "log.txt")

# Check if log.txt exists in the tests directory, if not, create it
if not os.path.exists(log_file_path):
    open(log_file_path, "w").close()

# Test whether the script executes successfully
def test_script_execution():
    # Define the command to execute the script
    command = "python src/features/jr_preprossing.py"
    # Execute the command and check if it runs successfully
    process = subprocess.run(command, shell=True)
    # Write the test result to log.txt in the tests directory
    with open(log_file_path, "a") as log_file:
        log_file.write("====================================\n")
        log_file.write("pytest: \"jr_preprossing.py\"\n")
        log_file.write("====================================\n")
        log_file.write("test_script_execution(): ")
        if process.returncode == 0:
            log_file.write("Success\n")
        else:
            log_file.write("Failure\n")
            log_file.write("Reason: The script execution failed\n")

# Test whether the output file is created
def test_output_file_creation():
    # Check if the output file exists
    output_file_path = os.path.join("data", "processed", "df_mi5.csv")
    if os.path.exists(output_file_path):
        result = "Success"
    else:
        result = "Failure"
    # Write the test result to log.txt in the tests directory
    with open(log_file_path, "a") as log_file:
        log_file.write("====================================\n")
        log_file.write("pytest: \"jr_preprossing.py\"\n")
        log_file.write("====================================\n")
        log_file.write("test_output_file_creation(): ")
        log_file.write(result + "\n")





