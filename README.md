WP07 Desertification Indicators - LULC
======================

Land Use/Land Cover (LULC)

Local land use and land cover changes are fundamental agents of global climate change and are significant forces that impact biodiversity, water and radiation budgets, trace gas emissions, and ultimately, climate at all scales.
The Land Use/Land Cover service implementation generates both LULC and LULC changes maps which will answer the requirements specified in the latest AGTE recommendations, namely for generating the “Trends in Land Structure” indicator. The processing chain is implemented in GRASS GIS orchestrated by Python/Shell scripting.
To run the process please follow the following steps:

1) Clone this repository to your Unix system:

`       git clone https://github.com/ec-melodies/wp07-lulc`

2) Make sure all required dependencies are installed (see ~/requirements.txt);

3) Define your parameters in ~/bin/variables.txt;

4) Initiate the process with: 

`       sh $HOME/wp07-lulc/ini.sh`

