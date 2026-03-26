from django.shortcuts import render
from django.http import JsonResponse
import joblib



def recommend_crop(request):
    if request.method == "POST":
        try:
            data = request.POST
            nitrogen = float(data["nitrogen"])
            phosphorus = float(data["phosphorus"])
            potassium = float(data["potassium"])
            ph = float(data["ph"])
            rainfall = float(data["rainfall"])
            temperature = float(data["temperature"])
            humidity = float(data["humidity"])

                # Local path (replace with your actual local path)
            model_path = r"path to your local model/Crop_Recommend.pkl"

            # Load the ML model
            model = joblib.load(model_path)
            prediction = model.predict(
                [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]
            )

            return JsonResponse({"recommended_crop": prediction[0]})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, "crop_recommend/crop_recommend.html")
