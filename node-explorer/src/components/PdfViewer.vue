<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <iframe ref="pdfIframe" class="pdf-viewer" :src="viewerPath" @load="handleIframeLoad"></iframe>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const route = useRoute();
    const fileName = route.params.fileName;
    const loading = ref(true);
    const viewerPath = ref('/pdfjs-dist/web/viewer.html');
    const pdfIframe = ref(null);
    const pdfUrl = ref('');

    onMounted(async () => {
      await fetchFileContent();
    });

    async function fetchFileContent() {
      try {
        const response = await axios.get(`http://localhost:8000/files/${fileName}/content`, { responseType: 'blob' });
        if (response.headers['content-type'] === 'application/pdf') {
          pdfUrl.value = window.URL.createObjectURL(response.data);
        } else {
          console.error("Error: the file is not a PDF.");
        }
        loading.value = false;
      } catch (error) {
        console.error("Error fetching file content:", error);
        loading.value = false;
      }
    }

    function handleIframeLoad() {
      if (pdfUrl.value && pdfIframe.value && pdfIframe.value.contentWindow) {
        console.log("Loading PDF in viewer");
        pdfIframe.value.contentWindow.PDFViewerApplication.open({url: pdfUrl.value});
      }
    }

    return {
      fileName,
      loading,
      viewerPath,
      pdfIframe,
      handleIframeLoad
    };
  }
};
</script>

<style>
.pdf-viewer {
  width: 100%;
  height: 90vh; /* Adjust the height based on your layout */
}
</style>
