const path = require("path");
const BrowserSyncPlugin = require('browser-sync-webpack-plugin')

module.exports = {
  entry: "./src/index.ts",
  mode: "development",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/
      }
    ]
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"]
  },
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "dist/js")
  },
  plugins: [
    new BrowserSyncPlugin({
      host: 'localhost',
      port: 4000,
      server: { baseDir: ['dist'] }
    })
  ]
};