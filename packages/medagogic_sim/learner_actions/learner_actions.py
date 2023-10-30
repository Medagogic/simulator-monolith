from pydantic import BaseModel
import pandas as pd
import os

class LearnerAction(BaseModel):
    Action: str
    Optional_Mandatory: str

class LearnerActions:
    def __init__(self, file_path="learner_actions.csv"):
        self.file_path = self.get_full_path(file_path)
        self.mandatory_actions = []
        self.optional_actions = []
        self.load_and_filter_csv()

    def get_full_path(self, relative_path):
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def load_and_filter_csv(self):
        df = pd.read_csv(self.file_path)
        mandatory_df = df[df['Optional/Mandatory'] == 'Mandatory']
        optional_df = df[df['Optional/Mandatory'] == 'Optional']
        
        self.mandatory_actions = self.convert_df_to_models(mandatory_df)
        self.optional_actions = self.convert_df_to_models(optional_df)

    def convert_df_to_models(self, df):
        return [LearnerAction(Action=row['Action'], Optional_Mandatory=row['Optional/Mandatory']) for _, row in df.iterrows()]

    def get_mandatory(self):
        return self.mandatory_actions

    def get_optional(self):
        return self.optional_actions

if __name__ == "__main__":
    learner_actions = LearnerActions("learner_actions.csv")
    
    print("Mandatory Actions:")
    for action in learner_actions.get_mandatory():
        print(action)
    
    print("Optional Actions:")
    for action in learner_actions.get_optional():
        print(action)
