<template>
    <div class="file-nodes">
      <div v-if="loading">Loading...</div>
      <div v-else v-for="file in fileStore.files" :key="file" class="node" @click="goToFileContent(file)">
        {{ file }}
      </div>
    </div>
  </template>
  
  <script>
  import { useFileStore } from '@/stores/useFileStore';
  import { onMounted, ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const fileStore = useFileStore();
      const loading = ref(true);
      const router = useRouter(); // Vue Router インスタンスを使用
  
      onMounted(async () => {
        await fileStore.fetchFiles();
        loading.value = false;
      });
  
      const goToFileContent = (fileName) => {
        router.push({ name: 'FileContent', params: { fileName } });
      };
  
      return {
        fileStore,
        loading,
        goToFileContent
      };
    }
  }
  </script>
  
  <style scoped>
  .node {
    width: 100px;
    height: 100px;
    background-color: #42b983;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px;
    cursor: pointer; /* クリック可能であることを示すカーソルスタイル */
  }
  </style>
  