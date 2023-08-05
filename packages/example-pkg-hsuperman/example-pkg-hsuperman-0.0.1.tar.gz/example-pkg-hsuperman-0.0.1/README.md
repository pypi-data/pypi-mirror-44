# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

https://packaging.python.org/tutorials/packaging-projects/#create-an-account


#Upload onto test pypi
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* 


#trying upload to regular
python3 -m twine upload --repository-url https://pypi.org/p/twine/ dist/* 
