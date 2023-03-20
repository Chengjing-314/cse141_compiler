## CSE141L Winter2023

### Overview 
The code this repo implemented a 9-bit ISA system for cse 141L to perform three programs. The three .py program ending with poc are python implementation of intended program for proof of concept. The three programs ending with .ikun are the actual assembly code.

### Compiler Usage

```bash
python3 -f path_to_assembly_code -l path_to_label_file 
```
To compile the program. A dictionary of labels and their associated lines are printed out if the you do not have the path_to_label_file ready. 
