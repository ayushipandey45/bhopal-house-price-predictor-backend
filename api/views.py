import numpy as np
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .ml_utils import model, encoder, dataset, features
from .preprocessing import clean_property_tokens, engineer_domain_features


@api_view(["GET"])
def hello(request):
    return Response({"message": "Backend Connected Successfully!"})


@api_view(["POST"])
def predict(request):
    data = request.data
    locality = data.get("locality")

    if not locality:
        return Response(
            {"error": "Locality is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1. Match Locality in Raw Dataset (case-insensitive)
    matched_rows = dataset[
        dataset["Locality / Area"].astype(str).str.lower() == locality.lower()
    ]

    if matched_rows.empty:
        return Response(
            {"error": f"Locality '{locality}' not found in dataset"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2. Extract matched row as DataFrame
    matched_row = matched_rows.iloc[[0]].copy()

    try:
        # 3. Step 1: Clean tokens
        row = clean_property_tokens(matched_row)

        # 4. Step 2: Feature engineering
        row = engineer_domain_features(row)

        # 5. Step 3: Encode property types using MultiLabelBinarizer
        if "Primary Property Types" in row.columns:
            encoded = encoder.transform(row["Primary Property Types"])
            encoded_df = pd.DataFrame(
                encoded,
                columns=encoder.classes_,
                index=row.index
            )
            row = pd.concat([row, encoded_df], axis=1)
            row = row.drop(columns=["Primary Property Types"])

        # Clean distance strings to float numbers (e.g., "5.2 km" -> 5.2)
        distance_cols = [
            "Nearest Hospital Distance",
            "Nearest School Distance",
            "Lake Distance (Approx.)",
            "Dist. to MP Nagar/DB Mall",
            "Dist. to AIIMS",
            "Dist. to Airport",
            "Dist. to Bhopal Jn. Rly Station"
        ]

        for col in distance_cols:
            if col in row.columns:
                row[col] = (
                    row[col]
                    .astype(str)
                    .str.extract(r'(\d+\.?\d*)')[0]
                    .astype(float)
                )

        # 6. Step 4: Align columns with model's expected 23 features
        processed_features = row.reindex(columns=features, fill_value=0)

        # Clean strings/booleans column by column safely
        for col in processed_features.columns:
            series = processed_features[col].astype(str).str.strip().str.upper()
            processed_features[col] = np.where(
                series.isin(["TRUE", "1"]), 1.0, 
                np.where(
                    series.isin(["FALSE", "0"]), 0.0, 
                    pd.to_numeric(processed_features[col], errors='coerce')
                )
            )

        # Fill any missing values with 0
        processed_features = processed_features.fillna(0.0)

        # 7. Step 5: Make Prediction
        prediction = model.predict(processed_features)[0]

        return Response({
            "status": "success",
            "locality": locality,
            "predicted_price": float(prediction)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {"error": f"Preprocessing/Prediction failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_localities(request):
    """Returns a list of all unique localities from the dataset."""
    if "Locality / Area" in dataset.columns:
        localities = dataset["Locality / Area"].dropna().astype(str).unique().tolist()
        localities.sort()  # Sort alphabetically
        return Response({"localities": localities}, status=status.HTTP_200_OK)
    
    return Response({"error": "Locality column not found"}, status=status.HTTP_400_BAD_REQUEST)