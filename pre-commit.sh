#!
# This formatter uses autopep 8 (https://pypi.org/project/autopep8/)

echo -e "Formatting"
autopep8 --in-place -a -a *.py

echo -e "Testing"
python3 -u engine_test.py

echo -e "Done"
