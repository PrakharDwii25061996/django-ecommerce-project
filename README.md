
### Steps to install and run Django

1. Create virtualenvironment
```
virtualenv venv
source venv/bin/activate
```

2. Load and Dump data of category and sub-category
```
python3 manage.py dumpdata product.SubCategory --output=fixtures/sub_category.json --indent=4
python3 manage.py dumpdata product.Category --output=fixtures/category.json --indent=4
```

3. Load data of Category and SubCategory
```
python3 manage.py loaddata fixtures/category.json --app product.SubCategory
python3 manage.py loaddata fixtures/sub_category.json --app product.Category
```
