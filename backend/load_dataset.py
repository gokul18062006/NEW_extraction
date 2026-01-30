from datasets import load_dataset

dataset = load_dataset("Nevidu/tamil_synthetic_ocr")
print(dataset)

# Print some sample data
print("\n" + "="*50)
print("SAMPLE DATA:")
print("="*50 + "\n")

# Get the first 5 examples
for i in range(5):
    example = dataset['data'][i]
    print(f"Example {i+1}:")
    print(f"Text: {example['text']}")
    print(f"Image: {example['image']}")
    print("-" * 50)
