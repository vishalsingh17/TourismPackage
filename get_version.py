import jupyter,\
pymongo,\
pandas,\
evidently,\
category_encoders,\
from_root,\
matplotlib,\
seaborn,\
imblearn,\
xgboost,\
catboost,\
boto3

list_of_libs = [
jupyter,
pymongo,
pandas,
evidently,
category_encoders,
from_root,
matplotlib,
seaborn,
imblearn,
xgboost,
catboost,
boto3
]

for lib in list_of_libs:
    try:
        name = lib.__name__.replace("_", "-")
        print(f"{name}=={lib.__version__}")
    except:
        print(f"{name}")

