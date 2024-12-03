<template>
  <div class="upload-container">
    <h3>Upload Image</h3>
    <p class="blurb">Use our powerful AI to recognize your grocery items from an image.</p>
    <input type="file" @change="handleFileUpload" />
    <button @click="recognizeItem" class="btn btn-primary">Recognize Item</button>
    <div v-if="recognizedItem" class="result">
      <p>Recognized Item: {{ recognizedItem }}</p>
    </div>
    <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const recognizedItem = ref('');
const file = ref(null);

const handleFileUpload = (event) => {
  file.value = event.target.files[0];
};

const recognizeItem = async () => {
  if (!file.value) {
    alert('Please upload an image first.');
    return;
  }

  try {
    const formData = new FormData();
    formData.append('image', file.value); // Ensure the key matches the backend expectation

    const response = await fetch('/api/recognize', { 
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to recognize item');
    }

    const data = await response.json();
    recognizedItem.value = data.recognized_items.join(', ');
  } catch (error) {
    console.error('Error recognizing item:', error);
    alert('There was an error recognizing the item. Please try again.');
  }
};
</script>

<style scoped>
.upload-container {
  background-color: var(--darkerMountainShadow);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h3 {
  text-align: center;
  margin-bottom: 10px;
  color: var(--freshVeg);
}

.blurb {
  text-align: center;
  margin-bottom: 20px;
  color: var(--glacierWater);
  font: bold;
}

input[type="file"] {
  display: block;
  margin-bottom: 20px;
}

.btn {
  display: block;
  margin: 10px auto;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  width: 100%; 
  max-width: 200px;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-secondary {
  background-color: #f44336;
  color: white;
}

.btn-secondary:hover {
  background-color: #e53935;
}

.result {
  margin-top: 20px;
  text-align: center;
  color: var(--freshVeg);
}
</style>
