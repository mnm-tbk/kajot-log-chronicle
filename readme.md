# Log chronicle 

This is a challenge for a SW developer position at Kajot company.  

This script automates archiving and compression of a specified log folder.
The script is expected to be run in production under `cron`. 

I decided to use `Click` for the ease of developing and testing CLI application. The script is tested on python3.7

### remarks:
   - symlinks are followed by default
   
## How to use

The script has a friendly CLI. Try `python log_chronicle --help` to see more details.

to run this script using `cron`:
1. change owner to `root`: `chwon root log_chronicle.py`
1. create virtualenv inside the project: `python3 -m venv venv-log-chronicle`
1. install requirements: `pip install -e requirements.txt`
1. automate the script:
    - run `crontab -e`
    - add ` 0/30 0 0 1/30 * ? * source /destination_of_downloaded_repo/venv-log-chronicle/bin/activate && python log-chronicle.py` to the file
    - save it


## Tests

Pytest is used as the testing framework, config is located in `conftest.py` and `pytest.ini`.
To run the tests, run `pytest`. Test report will be available at htmlcov/test_report.html.


### Test cases
Four basic test cases are tested: 

1. source does NOT exist
1. source is a file
1. source is a symlink (target is copied)
1. tar is saved to relative location