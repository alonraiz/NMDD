"use strict";
const webpack = require("webpack");
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const DashboardPlugin = require("webpack-dashboard/plugin");
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const ExtractCSS = new ExtractTextPlugin("styles/[hash].css");

const loaders = [
  {
    test: /\.jsx?$/,
    exclude: /(node_modules|bower_components|build\/)/,
    loader: "babel-loader",
    query: {
      presets: ["react"]
    }
  },
  {
    test: /\.css$/,
    loaders: ["style-loader", "css-loader?importLoaders=1"],
    exclude: ["node_modules"]
  },
  {
    test: /\.scss$/,
    loaders: ["style-loader", "css-loader?importLoaders=1", "sass-loader"],
    exclude: ["node_modules"]
  },
  {
    test: /\.less$/,
    loader: ExtractCSS.extract("css-loader?module&importLoaders=1!less-loader"),
    exclude: ["node_modules"]
  },
  {
    test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
    loader: "file-loader"
  },
  {
    test: /\.(woff|woff2)$/,
    loader: "url-loader?prefix=font/&limit=5000"
  },
  {
    test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
    loader: "url-loader?limit=10000&mimetype=application/octet-stream"
  },
  {
    test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
    loader: "url-loader?limit=10000&mimetype=image/svg+xml"
  },
  {
    test: /\.gif/,
    loader: "url-loader?limit=10000&mimetype=image/gif"
  },
  {
    test: /\.jpg/,
    loader: "url-loader?limit=10000&mimetype=image/jpg"
  },
  {
    test: /\.jpeg/,
    loader: "url-loader?limit=10000&mimetype=image/jpeg"
  },
  {
    test: /\.png/,
    loader: "url-loader?limit=10000&mimetype=image/png"
  }
];


module.exports = {
  entry: [
    "./src/main.jsx",
  ],
  devtool: process.env.WEBPACK_DEVTOOL || "eval-source-map",
  output: {
    publicPath: "/static",
    path: path.join(__dirname, "build"),
    filename: "bundle.js"
  },
  resolve: {
    extensions: [".js", ".jsx"]
  },
  module: {
    loaders
  },
  plugins: [
    ExtractCSS,
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.NamedModulesPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new ExtractTextPlugin({
      filename: "style.css",
      allChunks: true
    }),
    new DashboardPlugin(),
    new HtmlWebpackPlugin({
      template: "./src/index.html",
      files: {
        css: ["style.css"],
        js: [ "bundle.js"],
      }
    }),
  ]
};