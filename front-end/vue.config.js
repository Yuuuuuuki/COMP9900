module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.142.130:8881',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  pages: {
    index: {
      entry: 'src/diner.js',
    },
    eatery: {
      entry: 'src/eatery.js',
    },
    admin: {
      entry: 'src/admin.js',
    },
  },
};
