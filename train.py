from pathlib import Path
import joblib
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

ARTIFACT_DIR = Path("artifacts")
ARTIFACT_DIR.mkdir(exist_ok = True)

def main():

    X, y = make_classification(
        n_samples= 2000,
        n_features= 8,
        n_classes=2,
        n_informative=5,
        n_redundant=1,
        weights = [0.98, 0.02],
        flip_y=0.01,
        random_state=42
    )

    feature_names = [f"f{i}" for i in range(X.shape[1])]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)
    print(f"Saved baseline model. Test ROC-AUC: {auc:.4f} (don’t tune yet)")

    joblib.dump(
        {"model": model, "feature_names": feature_names},
        ARTIFACT_DIR / "fraud_model.joblib"
    )

if __name__ == "__main__":
    main()
