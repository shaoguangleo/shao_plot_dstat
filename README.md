# Shao_plot_dstat : plot dstat logfile

shao_plot_dstat is a package for plotting the logfile record by dstat command.

## Installation

There are two methods to install shao-plot-dstat

### CONDA

```bash
$ git clone https://github.com/shaoguangleo/shao-plot-dstat.git
$ cd shao-plot-dstat
$ conda env create -f environment.yaml
$ python3 setup.py build
$ python3 setup.py install
```

## pip

```bash
$ git clone https://github.com/shaoguangleo/shao-plot-dstat.git
$ cd shao-plot-dstat
$ pip3 install -r requirements.txt
$ python3 setup.py build
$ python3 setup.py install
```


## Usage

Just type

```bash
$ shao_plot_dstat --logfile logfile --title TITLE  --outfile out 
```

For example:

```bash
$ shao_plot_dstat --logfile data/test.log --title 'NETWORK DEMO' --outfile network_demo --debug
```

Then you will get the following figure name with :

- network_demo.png

![](images/network_demo.png)


## License
