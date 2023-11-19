import os

# Define the base directory
base_directory = "Dataset"

# Define classes and categories
classes = ["Dictation", "Copywriting"]
categories = ["Below_Average", "Average", "Above_Average"]

# Create the directory structure
for data_type in ["Train", "Test", "Validation"]:
    data_path = os.path.join(base_directory, data_type)
    
    for class_name in classes:
        class_path = os.path.join(data_path, class_name)
        
        for category in categories:
            category_path = os.path.join(class_path, category)
            
            # Create folders named Class{i} (i = 1 to 21)
            for i in range(1, 22):
                class_i_path = os.path.join(category_path, f"Class{i}")
                os.makedirs(class_i_path, exist_ok=True)
