<template>
    <div>
      <h1>File Content: {{ fileName }}</h1>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <div v-if="isPdf">
          <pdf-viewer :pdfUrl="fileContentUrl"></pdf-viewer>
        </div>
        <div v-else>
          <pre>{{ fileContent }}</pre>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  import PdfViewer from '../components/PdfViewer.vue';
  
  export default {
    components: {
      PdfViewer
    },
    setup() {
      const route = useRoute();
      const fileName = route.params.fileName;
      const fileContent = ref('');
      const fileContentUrl = ref('');
      const isPdf = ref(false);
      const loading = ref(true);
  
      onMounted(async () => {
        await fetchFileContent();
      });
  
      async function fetchFileContent() {
        try {
          const response = await axios.get(`http://localhost:8000/files/${fileName}/content`, { responseType: 'blob' });
          if (response.headers['content-type'] === 'application/pdf') {
            fileContentUrl.value = URL.createObjectURL(response.data);
            isPdf.value = true;
          } else {
            fileContent.value = await response.data.text();
            isPdf.value = false;
          }
          loading.value = false;
        } catch (error) {
          console.error("Error fetching file content:", error);
          loading.value = false;
        }
      }
  
      return {
        fileName,
        fileContent,
        fileContentUrl,
        isPdf,
        loading
      };
    }
  }
  </script>
  