<template>
    <div>
      <input type="file" @change="handleFileUpload">
      <button @click="submitFile">Upload</button>
    </div>
  </template>
  
  <script>
  import { useFileStore } from '../stores/useFileStore';
  
  export default {
    setup() {
      const fileStore = useFileStore();
      let file = null;
  
      const handleFileUpload = (event) => {
        file = event.target.files[0];
      };
  
      const submitFile = async () => {
        if (!file) {
          alert("Please select a file.");
          return;
        }
        await fileStore.uploadFile(file);
      };
  
      return { handleFileUpload, submitFile };
    }
  }
  </script>
  