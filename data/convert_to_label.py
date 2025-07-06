import os

# Base directory paths
base_dir = '/Users/grantbiellak/PycharmProjects/CRK-AutoRoller/data'
gt_dir = os.path.join(base_dir, 'groundtruth')
splits = ['images', 'test', 'eval']  # data folders

for split in splits:
    folder = os.path.join(base_dir, split)
    label_path = os.path.join(folder, 'label.txt')
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    with open(label_path, 'w') as label_out:
        for img in image_files:
            img_id, _ = os.path.splitext(img)  # '123.jpg' → '123'
            gt_file = os.path.join(gt_dir, f"{img_id}.gt.txt")

            if os.path.exists(gt_file):
                with open(gt_file, 'r') as gt_in:
                    label = gt_in.read().strip()
                    label_out.write(f"{split}/{img}\t{label}\n")
            else:
                print(f"⚠️ No ground truth found for: {img_id}.gt.txt")

print("✅ label.txt created for images/, test/, and eval/ using .gt.txt format")
