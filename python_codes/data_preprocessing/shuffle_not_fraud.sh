#!/bin/bash

file_path="../data/processed"

echo "$file_path/not_fraud_cases.csv"
head -n 1 "$file_path/not_fraud_cases.csv" > "$file_path/header.csv"
tail -n +2 "$file_path/not_fraud_cases.csv" | shuf > "$file_path/shuffled_rows.csv"
cat "$file_path/header.csv" "$file_path/shuffled_rows.csv" > "$file_path/shuffled_not_fraud_cases.csv"
rm "$file_path/header.csv" "$file_path/shuffled_rows.csv"
