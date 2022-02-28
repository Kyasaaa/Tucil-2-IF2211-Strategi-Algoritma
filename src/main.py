import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import myConvexHull
import random
from sklearn import datasets

def getInput():

    print("==============================================================")
    print("| Berikut daftar dataset yang dapat kalian coba:             |")
    print("| 1. Iris                                                    |")
    print("| 2. Digits                                                  |")
    print("| 3. Wine                                                    |")
    print("| 4. Breast cancer                                           |")
    print("==============================================================")
    opsi = int(input("Masukkan nomor dataset yang ingin dicoba: "))
    print("+------------------------------------------------------------+")

    # Memuat dataset sesuai pilihan user
    if (opsi == 1):
        data = datasets.load_iris()
    elif (opsi == 2):
        data = datasets.load_digits()
    elif (opsi == 3):
        data = datasets.load_wine()
    else:
        data = datasets.load_breast_cancer()
    
    doProcess(data)

def doProcess(data):

    # Create a DataFrame
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target'] = pd.DataFrame(data.target)
    print("Dimensi dataset yang dipilih sebesar:", df.shape)
    print("Dengan spesifikasi ukuran yaitu", df.shape[0], "baris dan", df.shape[1], "kolom.")
    print("+------------------------------------------------------------+")
    print("Berikut daftar kolom yang dapat digunakan:")
    
    i = 1
    for col in df.columns:
        if (col != "Target"):
            print(str(i) + ". " + str(col))
            i += 1
    print("+------------------------------------------------------------+")
    column_1 = int(input("Masukkan nomor kolom pertama yang akan digunakan: "))
    column_2 = int(input("Masukkan nomor kolom kedua yang akan digunakan: "))
    print("==============================================================")

    # Visualisasi hasil ConvexHull
    plt.figure(figsize = (10, 6))
    plt.title(str(df.columns[column_1 - 1]) + " vs " + str(df.columns[column_2 - 1]))
    plt.xlabel(data.feature_names[column_1 - 1])
    plt.ylabel(data.feature_names[column_2 - 1])

    for i in range(0, len(data.target_names)):
        bucket = df[df['Target'] == i]
        bucket = bucket.iloc[:, [column_1 - 1, column_2 - 1]].values.tolist()
        myConvexHull.quickSort(bucket, 0, len(bucket) - 1)
        hull = myConvexHull.convex_hull(bucket) #bagian ini diganti dengan hasil implementasi ConvexHull Divide & Conquer
        
        colors2 = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
        
        bucket = np.array(bucket)
        hull = np.array(hull)
        plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i], color = colors2)
        for simplex in hull:
            plt.plot(bucket[simplex, 0], bucket[simplex, 1], color = colors2)
    
    plt.legend()
    plt.show()

if __name__ == "__main__":
    getInput()