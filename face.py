import cv2
from skimage.metrics import structural_similarity as ssim

def check_student_photo(student_id, student_photo_path, db_photo_path):
    """
    Compare a student's photo with the photo stored in the database.

    Args:
    student_id (int): The student's ID.
    student_photo_path (str): The file path to the student's photo.
    db_photo_path (str): The file path to the photo stored in the database.

    Returns:
    int or bool: The student ID if the photos match, otherwise False.
    """
    
    # Load the student's photo
    student_photo = cv2.imread(student_photo_path, cv2.IMREAD_GRAYSCALE)
    
    # Load the database photo
    db_photo = cv2.imread(db_photo_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if photos are loaded successfully
    if student_photo is None:
        print(f"Failed to load student photo from {student_photo_path}")
        return False
    
    if db_photo is None:
        print(f"Failed to load database photo from {db_photo_path}")
        return False

    # Resize the photos to the same size if necessary
    if student_photo.shape != db_photo.shape:
        db_photo = cv2.resize(db_photo, (student_photo.shape[1], student_photo.shape[0]))

    # Compute the SSIM between the two photos
    score, _ = ssim(student_photo, db_photo, full=True)

    # Define a threshold for the SSIM to consider the photos as matching
    threshold = 0.85
    
    if score > threshold:
        return student_id
    else:
        return False

# Example usage
student_id = 1234
student_photo_path = "download-amir.jpeg"
db_photo_path = "download-live.jpeg"
print("started!")

result = check_student_photo(student_id, student_photo_path, db_photo_path)
print(result)