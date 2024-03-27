# Install required packages

```bash
pip install -r requirements.txt
```

# How to run

```bash
python3 main.py
``` 

# How to use

> The program is very intuitive, first you will be greeted with a message where you will need to type between ```1``` or ```0```. If you type ```1``` you will be prompted to type the number of packages and next the size of the map where those packages are going to be distributed. If you type ```0``` you won't need to prompt anything as the program will run with a fixed number of packages and map size that we used to test the algorithms performance and other aspects. Either way the program will run and will show for each algorithm a pandas dataframe with the order of the packages and their components (position, type, etc.), the cost of that algorithm and a visual interface that shows the path between all the packages for each algorithm.