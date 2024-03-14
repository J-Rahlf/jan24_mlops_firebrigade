import pytest
import sys
import io
import os



# Store the original stdout
original_stdout = sys.stdout

# Create an in-memory buffer to capture stdout
sys.stdout = io.StringIO()

pytest.main(["lh_model_evaluation_test.py"])

# Capture the output
output = sys.stdout.getvalue()

# Close the stream and reset stdout to the original value (console)
sys.stdout.close()
sys.stdout = original_stdout

if os.environ.get('LOG') == '1':
        with open('./tests/model_test_log.txt', 'a') as file:
            file.write(output)
