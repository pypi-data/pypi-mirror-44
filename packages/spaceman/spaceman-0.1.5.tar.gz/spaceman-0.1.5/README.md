# Spaceman
Spaceman is the checkpoint library for funguana's internal systems. We use it to save models and internal states for later use. We also intend to have a form of look back to see how states change between two points in time using this library. It's currently in working status.

# Installation and Setup:
After reviewing some of your code, I've inferred that you use Windows and possibly pycharm. To ensure you have the best experience possible, we're going to have you install Ubuntu on Windows. Prior to following the rest of the document, please read and follow:

> https://tutorials.ubuntu.com/tutorial/tutorial-ubuntu-on-windows#0

After you follow that tutorial, please follow this tutorial to install all of python/python3:
> http://timmyreilly.azurewebsites.net/python-with-ubuntu-on-windows/

## Installing Pip3 and pipenv
I use `pipenv` to ensure all of this code works properly. Before continuing. Open `Ubuntu on Windows` and begin with installing the following commands:

**This upgrades your system**
```bash
sudo apt-get update
sudo apt-get -y upgrade
```

**This installs everything necessary**

```
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```

**Try testing to see if that worked by running a simple numpy operation**

```
pip3 install numpy
python3
```

You should enter into a shell and be able to run python code.


Now install pipenv:

>`pip install --user --upgrade pipenv`

### Installing MongoDB Ubuntu
We use mongodb to manage timeseries data. Make sure to install. 
Run these from the site given:
> https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```

```
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
```

```
sudo apt-get update
sudo apt-get install -y mongodb-org
```

#### Run it:
```
sudo service mongod start
```

```
sudo service mongod stop # To stop
sudo service mongod restart # To restart
```


## Accessing Your Files In Ubuntu On Windows 10

Please follow the tutorial for accessing your files:

> https://www.howtogeek.com/261383/how-to-access-your-ubuntu-bash-files-in-windows-and-your-windows-system-drive-in-bash/


## Finishing Setup
Now enter into the folder containing `setup.py`. Downloaded from the funsuite repo.

To install all of the dependencies: **Run:** 

```
pipenv install -e .
```

This installs all of the main dependencies for the project. Follow that with: `pipenv shell` in the main directory to enter into the project's virtual environment.


### How to Run
To run the necessary test, you'll need to first get IAM keys for s3 (to test s3 functionality). The keys need to have s3 access and be stored in `~/.aws/credentials`

### Test Methods

To test, after you activate `pipenv shell`, run `python setup.py test` at the root of the command line. After it's run you should have the full capacity see which tests work or don't.

### Testing for local checkpoints

```python
from spaceman import Spaceman

# Declare a class to use contextually
spacem = Spaceman(storage_type="local", bucket="checkpoint-location", store_folder="/tmp/checkpoint")

with spacem as space:
    info = space.store([{}, 1, 2]) # Returns all information pertaining 
    unserialized_information = space.load(info.query) # TODO: Put
    print(unserialized_information)
```

### Using Lookback functionality

```python
from spaceman import Spaceman
import time
# Declare a class to use contextually
spacem = Spaceman(storage_type="local", bucket="checkpoint-location", store_folder="/tmp/checkpoint")

with spacem as space:
    info = space.store([{}, 1, 2], query={'type': "general", "timestamp": time.time()-30} current_time=False) # Returns all information pertaining 
    current_query = info.query
    current_query['timestamp'] = time.time()
    unserialized_information = space.load(query=current_query, is_timefore=True, seconds=30)
    print(unserialized)
```




## TODO:

* [] Refactor load functionaility to include s3 and better understand lookback functionality.
* [] Add space storage to load class to standardize interface (too many if statements)
* [] Full test functionality for S3 spaceman functionality