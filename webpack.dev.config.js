const HtmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");
const webpack = require("webpack");

module.exports = {
  mode: "development",
  context: path.resolve(__dirname),
  entry: "./semesterweb/src/index.tsx",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "index.js",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        loader: "babel-loader",
        exclude: /(node_modules)/,
      },
      {
        // https://github.com/webpack/webpack/issues/11467
        // https://github.com/babel/babel/pull/10853
        test: /\.m?js/,
        resolve: {
          fullySpecified: false,
        },
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "fonts/",
            },
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: [".ts", ".tsx", ".js", ".jsx"],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./semesterweb/static/index.html",
    }),
    new webpack.DefinePlugin({
      "process.env": {
        APIROOTPATH: JSON.stringify("/api"),
      },
    }),
  ],
  devServer: {
    contentBase: path.join(__dirname, "dist"),
    publicPath: "/",
    historyApiFallback: true,
    compress: true,
    port: 9001,
    proxy: {
      "/api": {
        target: "http://localhost:9000",
        pathRewrite: { "^/api": "" },
      },
    },
  },
};
