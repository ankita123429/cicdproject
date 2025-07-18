import sys
import os
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_Transformation_Config=DataTransformationConfig()    

    def get_data_transformer_obj(self):  
        try:
            numerical_columns=['reading_score', 'writing_score']
            categorical_columns=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            num_pipeline =Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler" ,StandardScaler(with_mean=False))
            ])
          
            cat_pipeline= Pipeline(steps=[("imputer",SimpleImputer(strategy='most_frequent')),
                                          ("one_hot_encoder",OneHotEncoder())
                                          ] )
            
            logging.info(f"categorical_columns{categorical_columns}")

            logging.info(f"numerical columns{numerical_columns}")

            preprocessor= ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
            ]
            )
            return preprocessor

        except Exception as e:
          raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_data_path,test_data_path):

        try:
            train_df=pd.read_csv(train_data_path)
            test_df=pd.read_csv(test_data_path)
            logging.info("reading trainning  and testing data")
            logging.info("obtaining the data set")

            preprocessing_obj=self.get_data_transformer_obj()
            target_column_name="math_score"
            numerical_columns=['reading_score', 'writing_score']
            input_feature_train_df= train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(f"applying preprocessing object on trainning and testing data sets")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)


            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info("saved preprocessing object")

            save_object(
                file_path=self.data_Transformation_Config.preprocessor_obj_file_path,
                obj=preprocessing_obj
                )
                
          
            return(
                 train_arr,
                 test_arr,
                 self.data_Transformation_Config.preprocessor_obj_file_path)
       
            
        except Exception as e:
           raise CustomException(e,sys)

           
