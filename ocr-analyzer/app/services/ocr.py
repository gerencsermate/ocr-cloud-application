import os
from typing import List

import cv2

from app.utils.easy_reader import get_ocr_reader


class OCRService:
    def process_and_overwrite_image(self, file_name: str) -> List[str]:
        file_path = os.path.join("UPLOADED_FILES", file_name)
        if not os.path.exists(file_path):
            raise ValueError("Image does not exist!")

        image_bgr = cv2.imread(file_path)

        if image_bgr is None:
            raise ValueError("Could not open the image")

        annotated_image = image_bgr.copy()

        reader = get_ocr_reader()

        results = reader.readtext(file_path)

        texts = []
        for bbox, text, prob in results:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))

            cv2.rectangle(annotated_image, top_left, bottom_right, (0, 255, 0), 2)

            if prob > 0.4:
                texts.append(text)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.6
                text_color = (255, 0, 0)
                thickness = 2

                text_position = (top_left[0], max(10, top_left[1] - 10))

                cv2.putText(
                    annotated_image,
                    text,
                    text_position,
                    font,
                    font_scale,
                    text_color,
                    thickness,
                )

        success = cv2.imwrite(file_path, annotated_image)

        if not success:
            raise ValueError(f"Falied to process image: {file_path}")

        return texts
