from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from pydantic import BaseModel
import logging
import shutil
import os
from tensorflow.keras.models import load_model
from prediction import predict

# Настройка логирования
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Инициализация FastAPI-приложения
app = FastAPI()

# Загрузка модели при старте сервера
MODEL_PATH = "Model/Neural_model.keras"
model = load_model(MODEL_PATH)

# Эндпоинт /predict — принимает изображение и возвращает текстовый результат анализа
@app.post("/predict")
def predict_acne(file: UploadFile = File(...), request: Request = None):
    try:
        # Сохраняем файл временно
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"[{request.client.host if request else 'unknown'}] Получено изображение: {file.filename}")

        # Выполняем предсказание
        result = predict(temp_path, model)

        logging.info(f"Результат анализа изображения: {result[:60]}...")

        # Удаляем временный файл
        os.remove(temp_path)

        return {"result": result}

    except Exception as e:
        logging.error(f"Ошибка в /predict: {e}")
        raise HTTPException(status_code=500, detail="Ошибка обработки изображения")
