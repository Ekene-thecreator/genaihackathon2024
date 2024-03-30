import io
import os
from google.cloud import vision

def detect_text():
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    file = os.path.abspath("resources/image_test.jpg")

    with io.open(file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return(texts[0].description)

if __name__ == "__main__":
    detect_text()