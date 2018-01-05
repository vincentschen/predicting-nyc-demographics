# Understanding NYC Demographics from FourSquare Check-in Data
by [Vincent Chen](http://vincentsc.com) and [Dan Yu](http://danyu.me/)

This repository includes all the data and code for predicting demographics from FourSquare check-in data.

## Directory Structure 
```
├── notebooks
│   ├── data-visualization.ipynb
│   ├── feature-analysis.ipynb
│   ├── feature-extraction.ipynb
│   ├── model-evaluation.ipynb
├── scripts
│   ├── compute_block_codes.py
├── data
│   ├── processed
│   │   ├── cat_251.csv
│   │   ├── ...
│   │   ├── cat_week_time_timepercat_timeperweekpercat_9028.csv
│   ├── raw
│   │   ├── foursquare-nyc-check-ins
│   │   │   ├── dataset_TSMC2014_NYC.csv
│   │   │   ├── dataset_TSMC2014_NYC.npy # same as .csv, converted to .npy
│   │   ├── new-york-city-census-data
│   │   │   ├── nyc_census_tracts.csv
```
## Setup
### Dependencies 
* Ensure the following are installed using your favorite package manager (`pip`?): `numpy`, `pandas`, `scikit-learn`, `jupyter`, `gmaps`, `gmplot`

### Notebooks 
* Run `jupyter nbextension enable --py gmaps` 
  * to view `data-visualization.ipynb`
* `jupyter notebook`
* Get a Google Maps API key: https://developers.google.com/maps/documentation/javascript/get-api-key
### Preprocessing 
* Convert all lat/long coordinates from the check-in data to census tracts
* To run: `cd scripts && python coord_to_census_tracts.py`
  * Reads: `/data/raw/foursquare-nyc-and-tokyo-check-ins/dataset_TSMC2014_NYC.npy`
  * Writes: `/data/processed/census_tracts_per_checkin.csv`
  * Keeps track of failed requests and retries entries until complete
  * ~22 hour runtime 

### Feature Engineering 
Use `notebooks/feature-extraction.ipynb` to extract features from check-in data and generates different datasets based on subsets of features (as seen in `data/processed/`)
 
### Model Evaluation 
Use `model-evaluation.ipynb` to train and compare different models and perform hyperparameter tuning. 

### Data Visualization (Feature Heatmaps)
Use `data-visualization.ipynb`: to generate heat maps for feature visualization.

### Feature Analysis
Use `feature-analysis.ipynb` to identify most predictive features by sorting the weights of a logistic regression model. 

# Attribution
* FourSqare data (`data/raw/foursquare-nyc-checkins/`)retrieved from https://www.kaggle.com/chetanism/foursquare-nyc-and-tokyo-checkin-dataset/
* Census Data data (`data/raw/new-yrok-city-census-data/`)retrieved from https://www.kaggle.com/muonneutrino/new-york-city-census-data

# Contact 
Please reach out (`vincentsc@cs.stanford.edu`, `dxyu@stanford.edu`) if you have any issues! 