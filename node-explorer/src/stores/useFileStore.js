import { defineStore } from 'pinia';
import axios from 'axios';

export const useFileStore = defineStore('fileStore', {
  state: () => ({
    files: []
  }),
  actions: {
    async fetchFiles() {
      try {
        const response = await axios.get('http://localhost:8000/files/');
        this.files = response.data.files;
        console.log(this.files)
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    },
    async uploadFile(file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        await axios.post('http://localhost:8000/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        await this.fetchFiles();  // ファイル一覧を更新
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  }
});
