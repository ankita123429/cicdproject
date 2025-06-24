import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from  sklearn.neighbors import KNeighborsRegressor
from  xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model
@dataclass
class ModelTraineerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainner_config=ModelTraineerConfig()

    def initiate_model_trainning(self,train_array,test_array):
        try:
            logging.info("trainning and testing data splitting")
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]


            )
            models={
                "RandomForestRegressor":RandomForestRegressor(),
                "GradientBoostingRegressor":GradientBoostingRegressor(),
                "LinearRegression":LinearRegression(),
                "KneighbourRegression":KNeighborsRegressor(),
                "XGBoostRegression":XGBRegressor(),
                "catboostRegrssion":CatBoostRegressor(verbose=False),
                "AdaboostRegression":AdaBoostRegressor()
            }
            model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)
            best_model_score= max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("no best model found")
            logging.info("best model found for both trainning and testing")
            save_object(
                file_path=self.model_trainner_config.trained_model_file_path,
                obj=best_model
            )
            predicted=best_model.predict(x_test)
            r2_score_value=r2_score(y_test,predicted)
            return r2_score_value

        except Exception as e:
            raise CustomException(e,sys)    

