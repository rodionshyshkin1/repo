import os
import json
import argparse
import random
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold

class CrossValidationDataFactory:
    # CLASSES = ["Atlas_Pinnacle", "CertainTeed_Landmark", "IKO_Dynasty", "Malarkey_Vista"]

    def __init__(
            self, 
            data_dir: str = "raw/", 
            output_dir: str = "folds/", 
            num_folds: int = 10, 
            seed: int = 42, 
            stratified_flag: bool = True
            ):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.num_folds = num_folds
        self.seed = seed
        self.stratified_flag = stratified_flag

        self.dataset = []
        self.class_labels = []
        self.class_mapping = {}

        self.folds = []

    def __call__(self):
        pipeline = [
            self.load_dataset,
            self.create_folds,
            self.save_folds
        ]
        for step in pipeline:
            step()

    def load_dataset(self):
        class_folders = sorted(os.listdir(self.data_dir))
        for class_idx, class_name in enumerate(class_folders):
            class_path = os.path.join(self.data_dir, class_name)
            if not os.path.isdir(class_path):
                continue

            self.class_mapping[class_name] = class_idx

            for filename in sorted(os.listdir(class_path)): 
                if filename.endswith(".jpg"):
                    self.dataset.append(os.path.join(class_name, filename))
                    self.class_labels.append(class_idx)
    
    def create_folds(self):
        random.seed(self.seed)
        np.random.seed(self.seed)

        if self.stratified_flag:
            labels = [random.randint(0, 9) for _ in self.dataset]
            kf = StratifiedKFold(n_splits=self.num_folds, shuffle=True, random_state=self.seed)
            splits = list(kf.split(self.dataset, labels))
        else:
            kf = KFold(n_splits=self.num_folds, shuffle=True, random_state=self.seed)
            splits = list(kf.split(self.dataset))

        for fold_idx, (train_idx, val_idx) in enumerate(splits):
            train_files = [self.dataset[i] for i in train_idx]
            val_files = [self.dataset[i] for i in val_idx]
            self.folds.append({"fold": fold_idx, "train": train_files, "val": val_files})

    def save_folds(self):
        os.makedirs(self.output_dir, exist_ok=True)
        for fold in self.folds:
            fold_path = os.path.join(self.output_dir, f"fold_{fold['fold']}.json")
            with open(fold_path, "w") as f:
                json.dump(fold, f, indent=4)

def main():
    factory = CrossValidationDataFactory()
    factory()


if __name__ == "__main__":
    main()

