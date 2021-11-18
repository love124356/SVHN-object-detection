from sklearn.model_selection import train_test_split
import shutil
import os


if __name__ == "__main__":
    data = [n for n in range(1, 33403)]

    train_set, val_set = train_test_split(
                data, random_state=310553027, train_size=0.8)

    # print(train_set)
    # print(val_set)
    print("Make folder val/train")
    os.makedirs('data/svhn/val/', exist_ok=True)
    os.makedirs('data/svhn/train/', exist_ok=True)
    train_val_path = 'data/svhn/trainval/'
    train_path = 'data/svhn/train/'
    val_path = 'data/svhn/val/'

    for num in data:
        if num in train_set:
            # print("train")
            shutil.move(train_val_path + str(num) + '.png', train_path)
            shutil.move(train_val_path + str(num) + '.txt', train_path)
        elif num in val_set:
            # print("val")
            shutil.move(train_val_path + str(num) + '.png', val_path)
            shutil.move(train_val_path + str(num) + '.txt', val_path)
    print("DONE.")
