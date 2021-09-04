<template>
  <a-upload
    name="file"
    action="/api/file"
    v-bind="$attrs"
    v-on="$listeners"
    @change="handleChange"
  >
    <slot/>
  </a-upload>
</template>
<script>
export default {
  model: {
    prop: 'value',
    event: 'upload',
  },
  prop: {
    value: String,
  },
  methods: {
    handleChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        this.$message.success(`${info.file.name} file uploaded successfully`);
        this.$emit('upload', info.file.response?.url);
      } else if (info.file.status === 'error') {
        this.$message.error(`${info.file.name} file upload failed.`);
      }
    },
  },
};
</script>
