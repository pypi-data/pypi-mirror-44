DIRECTORY STRUCTURE
-------------------

MySimpleLRUCache_KaranMaheshwari/
	
	MySimpleLRUCache_KaranMaheshwari/

		__init__.py
		lru_cache.py
		helper.py

	tests/

		test_helper.py
		test_lru_cache.py

	LICENSE.txt
	README.md
	setup.cfg
	setup.py


TESTING INSTRUCTIONS
---------------------

To test the code, first install the library using pip:

	pip install MySimpleLRUCache-KaranMaheshwari

To test the code, I have written a small test file called my_test.py which has comments on 
how to import the library, which functions to use and how to check outputs.

One can play around with the code using the example.

When the test file is run, logs will automatically get generated in a new file called app.log which will give a clear
picture of how the operations were performed and their results.

To run the unit tests written, use the following command after entering the directory of the folder. Test case names
clearly explain what the code is testing. Running the test cases will also create a log file.

	python -m unittest discover -s tests
