import tensorflow as tf
from scipy.spatial import distance
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# A modell betöltése az ImageNet súlyaival. 
# Az 'include_top=True' azt jelenti, hogy az osztályozó réteget is betöltjük (az 1000 kategóriát).
# Ez a betöltés az alkalmazás indításakor egyszer fut le.
print("AI Modell betöltése (MobileNetV2)...")
model = MobileNetV2(weights='imagenet')

# Ehhez egy olyan modell kell, aminek nincs 'teteje' (csak a jellemzőket adja vissza)
feature_extractor = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

def analyze_pet_image(img_path):
    """
    Elemzi a megadott képet és visszaadja a legvalószínűbb fajtát.
    """
    try:
        if not os.path.exists(img_path):
            return None

        # 1. Kép betöltése és átméretezése 224x224-re (MobileNetV2 elvárása)
        img = image.load_img(img_path, target_size=(224, 224))
        
        # 2. Átalakítás tömbbé
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        
        # 3. Előfeldolgozás (normalizálás -1 és 1 közé)
        x = preprocess_input(x)

        # 4. Predikció (Jóslás)
        preds = model.predict(x)
        
        # 5. Eredmények dekódolása (a top 3 találat)
        # A decode_predictions visszaadja az osztály nevét (angolul) és a valószínűséget
        decoded = decode_predictions(preds, top=1)[0][0]
        
        # decoded formátuma: (id, label, probability)
        label = decoded[1].replace('_', ' ').capitalize()
        confidence = round(float(decoded[2]) * 100, 2)

        # Mivel a MobileNetV2 alapvetően fajtákat ismer fel, 
        # az életkort és a nemet itt most heurisztikusan szimuláljuk, 
        # vagy a dokumentációban megindokoljuk, hogy ezek manuális finomhangolást igényelnek.
        return {
            'breed': label,
            'age_group': 'Meghatározás alatt...', # Később bővíthető
            'gender': 'Vizsgálat szükséges',      # Később bővíthető
            'confidence': confidence
        }
    except Exception as e:
        print(f"Hiba az AI elemzés során: {e}")
        return None
    
def get_image_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return feature_extractor.predict(x).flatten()

def calculate_similarity(img_path1, img_path2):
    feat1 = get_image_features(img_path1)
    feat2 = get_image_features(img_path2)
    # Koszinusz hasonlóság (1.0 a tökéletes egyezés)
    return 1 - distance.cosine(feat1, feat2)