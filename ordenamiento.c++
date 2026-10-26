#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <cmath>
#include <algorithm>
#include <sys/resource.h>
#include <fstream>

// Medición de Memoria Residente
long getMemoryUsageKB() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    return usage.ru_maxrss;
}

// 1. Bubble Sort
void bubbleSort(std::vector<double>& arr) {
    size_t n = arr.size();
    for (size_t i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (size_t j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

// 2. Merge Sort
void merge(std::vector<double>& arr, std::vector<double>& temp, size_t left, size_t mid, size_t right) {
    size_t i = left, j = mid + 1, k = left;
    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) temp[k++] = arr[i++];
        else temp[k++] = arr[j++];
    }
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    for (i = left; i <= right; ++i) arr[i] = temp[i];
}

void mergeSortRec(std::vector<double>& arr, std::vector<double>& temp, size_t left, size_t right) {
    if (left >= right) return;
    size_t mid = left + (right - left) / 2;
    mergeSortRec(arr, temp, left, mid);
    mergeSortRec(arr, temp, mid + 1, right);
    merge(arr, temp, left, mid, right);
}

void mergeSort(std::vector<double>& arr) {
    if (arr.size() <= 1) return;
    std::vector<double> temp(arr.size());
    mergeSortRec(arr, temp, 0, arr.size() - 1);
}

// 3. Tree Sort
struct TreeNode {
    double val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(double v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* insertBST(TreeNode* root, double val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insertBST(root->left, val);
    else root->right = insertBST(root->right, val);
    return root;
}

void inOrderTraversal(TreeNode* root, std::vector<double>& arr, size_t& index) {
    if (!root) return;
    inOrderTraversal(root->left, arr, index);
    arr[index++] = root->val;
    inOrderTraversal(root->right, arr, index);
}

void freeBST(TreeNode* root) {
    if (!root) return;
    freeBST(root->left);
    freeBST(root->right);
    delete root;
}

void treeSort(std::vector<double>& arr) {
    if (arr.empty()) return;
    TreeNode* root = nullptr;
    for (double v : arr) root = insertBST(root, v);
    size_t index = 0;
    inOrderTraversal(root, arr, index);
    freeBST(root);
}

// 4. Heap Sort
void heapify(std::vector<double>& arr, size_t n, size_t i) {
    size_t largest = i;
    size_t left = 2 * i + 1;
    size_t right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;

    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(std::vector<double>& arr) {
    size_t n = arr.size();
    for (long long i = (n / 2) - 1; i >= 0; --i) {
        heapify(arr, n, i);
    }
    for (size_t i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

// 5. Counting Sort Adaptado para Reales
void countingSortReals(std::vector<double>& arr, size_t buckets = 100000) {
    if (arr.empty()) return;
    double minVal = *std::min_element(arr.begin(), arr.end());
    double maxVal = *std::max_element(arr.begin(), arr.end());
    double range = maxVal - minVal;
    if (range == 0) return;

    std::vector<std::vector<double>> b(buckets);
    for (double v : arr) {
        size_t idx = static_cast<size_t>((v - minVal) / range * (buckets - 1));
        b[idx].push_back(v);
    }

    size_t k = 0;
    for (size_t i = 0; i < buckets; ++i) {
        std::sort(b[i].begin(), b[i].end());
        for (double v : b[i]) arr[k++] = v;
    }
}

int main() {
    std::vector<size_t> sizes = {100000, 1000000, 10000000, 100000000}; 
    
    std::ofstream file("resultados_cpp.csv");
    file << "Algoritmo,Tamaño,Tiempo_s,Memoria_KB\n";
    
    std::mt19937 gen(42);
    std::uniform_real_distribution<double> dist(0.0, 1000000.0);

    for (size_t n : sizes) {
        std::cout << "\nGenerando arreglo de tamaño " << n << "...\n";
        std::vector<double> original(n);
        for (size_t i = 0; i < n; ++i) original[i] = dist(gen);

        // Merge Sort
        std::vector<double> copy1 = original;
        auto start = std::chrono::high_resolution_clock::now();
        long mem_start = getMemoryUsageKB();
        mergeSort(copy1);
        long mem_end = getMemoryUsageKB();
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = end - start;
        file << "MergeSort," << n << "," << diff.count() << "," << (mem_end - mem_start) << "\n";
        std::cout << "MergeSort listo para " << n << "\n";

        // Heap Sort
        std::vector<double> copy2 = original;
        start = std::chrono::high_resolution_clock::now();
        mem_start = getMemoryUsageKB();
        heapSort(copy2);
        mem_end = getMemoryUsageKB();
        end = std::chrono::high_resolution_clock::now();
        diff = end - start;
        file << "HeapSort," << n << "," << diff.count() << "," << (mem_end - mem_start) << "\n";
        std::cout << "HeapSort listo para " << n << "\n";
        
        // Tree Sort (restringido a 1,000,000 para no agotar la memoria)
        if (n <= 1000000) {
            std::vector<double> copy3 = original;
            start = std::chrono::high_resolution_clock::now();
            mem_start = getMemoryUsageKB();
            treeSort(copy3);
            mem_end = getMemoryUsageKB();
            end = std::chrono::high_resolution_clock::now();
            diff = end - start;
            file << "TreeSort," << n << "," << diff.count() << "," << (mem_end - mem_start) << "\n";
            std::cout << "TreeSort listo para " << n << "\n";
        }

        // Counting Sort
        std::vector<double> copy4 = original;
        start = std::chrono::high_resolution_clock::now();
        mem_start = getMemoryUsageKB();
        countingSortReals(copy4);
        mem_end = getMemoryUsageKB();
        end = std::chrono::high_resolution_clock::now();
        diff = end - start;
        file << "CountingSort," << n << "," << diff.count() << "," << (mem_end - mem_start) << "\n";
        std::cout << "CountingSort listo para " << n << "\n";
    }
    
    file.close();
    std::cout << "\nResultados de C++ guardados en resultados_cpp.csv\n";
    return 0;
}