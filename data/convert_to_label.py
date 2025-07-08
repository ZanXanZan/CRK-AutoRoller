import os

split_dir = "/Users/grantbiellak/PycharmProjects/CRK-AutoRoller/data/split"
label_path = os.path.join(split_dir, "label.txt")

with open(label_path, "w", encoding="utf-8") as label_file:
    for fname in sorted(os.listdir(split_dir)):
        if fname.endswith(".gt.txt"):
            base = fname[:-7]  # remove .gt.txt
            img_path = f"{base}.png"
            gt_path = os.path.join(split_dir, fname)
            with open(gt_path, "r", encoding="utf-8") as f:
                label = f.read().strip()
            label_file.write(f"{img_path}\t{label}\n")

print("✅ label.txt generated.")
