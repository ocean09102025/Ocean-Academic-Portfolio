// Sequential QuickSort Implementation
#include <stdio.h>
#include <stdlib.h>

// Function to swap two elements
void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

// Partition function for QuickSort
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// QuickSort function
void quicksort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

int main() {
    int n = 10;  // You can change this value for testing
    int arr[n];
    
    // Initialize array with random values
    printf("Array before sorting: ");
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100;
        printf("%d ", arr[i]);
    }
    printf("\n");

    // Sort the array using QuickSort
    quicksort(arr, 0, n - 1);

    // Print the sorted array
    printf("Array after sorting: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}

// Parallel QuickSort Implementation using MPI
#include <mpi.h>

// Function to swap two elements
void swap_mpi(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

// Partition function for QuickSort
int partition_mpi(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap_mpi(&arr[i], &arr[j]);
        }
    }
    swap_mpi(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// QuickSort function
void quicksort_mpi(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition_mpi(arr, low, high);
        quicksort_mpi(arr, low, pi - 1);
        quicksort_mpi(arr, pi + 1, high);
    }
}

int main_mpi(int argc, char* argv[]) {
    int rank, size, n = 10;  // Change n to test with larger arrays
    int arr[n];
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        // Master process: initialize array with random values
        printf("Array before sorting: ");
        for (int i = 0; i < n; i++) {
            arr[i] = rand() % 100;
            printf("%d ", arr[i]);
        }
        printf("\n");
    }

    // Broadcast array to all processes
    MPI_Bcast(arr, n, MPI_INT, 0, MPI_COMM_WORLD);

    // Divide array for each process
    int local_n = n / size;
    int local_arr[local_n];

    MPI_Scatter(arr, local_n, MPI_INT, local_arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    // Each process sorts its local array
    quicksort_mpi(local_arr, 0, local_n - 1);

    // Gather the sorted subarrays
    MPI_Gather(local_arr, local_n, MPI_INT, arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        // Master process: display the sorted array
        printf("Array after sorting: ");
        for (int i = 0; i < n; i++) {
            printf("%d ", arr[i]);
        }
        printf("\n");
    }

    MPI_Finalize();
    return 0;
}
