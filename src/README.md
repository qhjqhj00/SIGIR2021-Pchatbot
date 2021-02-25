## Data Usage 

- #### Pipeline

  **Firstly**, we filter the raw data. **Secondly**,  we split the data according to users. **Tridly**, we merge all the user data and convert it to a format that can be used in the model.

  We can easily run the **pipeline.py** to directly generate the data with correct format.

  ```python
  python pipeline.py --data_fp ../data/sample.txt --user_data_dir ../data/sample_byuser_filter --model_data_dir ../data/sample_datasets
  ```

- #### data preprocess

  The cleaning script used in first step. The details are in the **Dialog-Preprocessor**.

- #### raw data to user data

  The convert script used in second step. The details are in the **split_user.py**.

- #### user data to model data

  The convert script used in third step. The details are in the **data_byusers_generator.py**.

  ​	

  

