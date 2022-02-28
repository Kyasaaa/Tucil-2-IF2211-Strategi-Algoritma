# NAMA      : Muhammad Akyas David Al Aleey
# NIM       : 13520011
# DESKRIPSI : Algoritma penyelesaian persoalan convex hull dengan strategi divide and conquer

import math
import numpy as np

# Fungsi partition mengambil elemen terakhir sebagai pivot
# kemudian menempatkan semua elemen yang lebih kecil dari  
# pivot di sebelah kiri dan semua elemen yang lebih besar  
# di sebelah kanan pivot. Fungsi ini akan mengembalikan
# indeks pivot 

def partition(arr_of_points, low, high):
    
    i = (low-1)
    pivot = arr_of_points[high]
 
    for j in range(low, high):
 
        # Mengecek apakah elemen sekarang lebih kecil atau 
        # sama dengan pivot berdasarkan nilai absis terlebih 
        # dahulu kemudian nilai ordinat
        if (arr_of_points[j][0] < pivot[0]) or (arr_of_points[j][0] <= pivot[0] and arr_of_points[j][1] <= pivot[1]):
            
            # Menukar elemen dengan pivot
            i = i+1
            temp = arr_of_points[i]
            arr_of_points[i] = arr_of_points[j] 
            arr_of_points[j] = temp
 
    temp = arr_of_points[i+1]
    arr_of_points[i+1] = arr_of_points[high] 
    arr_of_points[high] = temp
    
    return i+1

# Prosedur pengurutan array of points dengan algoritma quicksort
def quickSort(arr_of_points, low, high):
    
    if len(arr_of_points) == 1:
        return arr_of_points

    if low < high:
 
        pi = partition(arr_of_points, low, high)
 
        # Memproses pengurutan array sebelah 
        # kiri dan kanan indeks partisi
        quickSort(arr_of_points, low, pi-1)
        quickSort(arr_of_points, pi+1, high)

# Menghitung determinan dari titik c terhadap titik a dan b
def determinant(a, b, c):
    
    return (a[0] * b[1]) + (c[0] * a[1]) + (b[0] * c[1]) - (c[0] * b[1]) - (b[0] * a[1]) - (a[0] * c[1])

# Menghitung jarak dari titik p3 ke garis yang dihubungkan oleh titik p1 dan p2
def point_to_line_distance(p1, p2, p3):
    
    p1=np.array(p1)
    p2=np.array(p2)
    p3=np.array(p3)
    
    return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)

# Menghitung besar sudut yang dibentuk oleh titik p3 terhadap titik p1 dan p2
def getAngle(p1, p2, p3):
    
    angle = math.degrees(math.atan2(p3[1]-p2[1], p3[0]-p2[0]) - math.atan2(p1[1]-p2[1], p1[0]-p2[0]))
    
    if angle < 0:
        return angle + 360
    
    else:
        return angle

# Mencari titik-titik ekstrim penyusun convex hull dengan algoritma divide and conquer.
def find_hull(sorted_points, hull_set, leftmost_idx, rightmost_idx, convex_set):
    
    if len(hull_set):
        
        extreme_dis = -1
        extreme_angle = 0
        candidate_points1 = []
        candidate_points2 = []

        # Mencari titik ekstrim (Pmax) yang memiliki jarah terjauh dari garis P1Pn
        # Jika terdapat beberapa titik dengan jarak yang sama, akan dipilih
        # titik dengan sudut terhadap P1Pn yang terbesar.
        for i in hull_set:
            curr_dis = point_to_line_distance(sorted_points[leftmost_idx], sorted_points[rightmost_idx], sorted_points[i])
            
            if (curr_dis > extreme_dis):
                extreme_dis = curr_dis
                extreme_idx = i
                extreme_angle = getAngle(sorted_points[leftmost_idx], sorted_points[rightmost_idx], sorted_points[i])

            elif (curr_dis == extreme_dis):
                angle_point = getAngle(sorted_points[leftmost_idx], sorted_points[rightmost_idx], sorted_points[i])
                
                if (angle_point > extreme_angle):
                    extreme_idx = i
                    extreme_angle = angle_point

        # Mengklasifikasikan kumpulan titik di sebelah kiri garis P1Pmax
        # dan di sebelah kanan garis PmaxPn
        for i in hull_set:
            
            if (extreme_idx != i):
                
                det1 = determinant(sorted_points[leftmost_idx], sorted_points[extreme_idx], sorted_points[i])
                det2 = determinant(sorted_points[extreme_idx], sorted_points[rightmost_idx], sorted_points[i])

                if det1 > 0 and det2 < 0:
                    candidate_points1.append(i)

                elif det2 > 0 and det1 < 0:
                    candidate_points2.append(i)

        find_hull(sorted_points, candidate_points1, leftmost_idx, extreme_idx, convex_set)
        find_hull(sorted_points, candidate_points2, extreme_idx, rightmost_idx, convex_set)

    # Jika tidak ada titik lain selain P1 dan Pn, maka titik tersebut menjadi 
    # pasangan titik pembentuk convex hull
    else:
        convex_set.append([leftmost_idx, rightmost_idx]) 

# Algoritma utama pencarian convex hull dari array of points yang sudah terurut.
# Fungsi ini akan mengembalikan array berisi pasangan indeks dari koordinat yang  
# mewakili titik-titik penyusun convex hull. Pasangan indeks ini nantinya akan 
# dihubungkan oleh suatu garis lurus.
def convex_hull(sorted_points):
    
    arr_len = len(sorted_points)
    upper_hull = []
    lower_hull = []
    convex_set = []

    # Mengklasifikasi titik-titik yang membentuk convex hull bagian atas 
    # atau bawah dari garis yang menghubungkan titik pada indeks pertama (P1)
    # dengan titik pada indeks terakhir (Pn)
    for i in range(1, arr_len - 1):
        det = determinant(sorted_points[0], sorted_points[arr_len - 1], sorted_points[i])

        if det > 0:
            upper_hull.append(i)
        
        elif det < 0:
            lower_hull.append(i)

    find_hull(sorted_points, upper_hull, 0, arr_len - 1, convex_set)
    find_hull(sorted_points, lower_hull, arr_len - 1, 0, convex_set)

    return convex_set