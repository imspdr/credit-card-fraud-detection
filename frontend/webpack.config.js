const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const path = require("path");

module.exports = (env) => {
  return {
    mode: env.development ? "development" : "production",
    entry: path.join(__dirname, "src/index.tsx"),
    devtool: env.development ? "eval-source-map" : false,
    output: {
      path: path.join(__dirname, "build"),
      filename: "main.js",
      publicPath: "/",
    },
    resolve: {
      extensions: [".js", ".jsx", ".ts", ".tsx"],
      alias: {
        "@src": path.resolve(__dirname, "src/"),
      },
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: path.resolve(__dirname, "src/index.ejs"),
        favicon: "imspdr.png",
        filename: "index.html",
      }),
      new CleanWebpackPlugin(),
    ],
    module: {
      rules: [
        {
          test: /\.(tsx|ts|jsx|js)?$/,
          exclude: /node_modules/,
          use: ["babel-loader", "ts-loader"],
        },
        {
          test: /\.(css)?$/,
          use: ["style-loader", "css-loader"],
        },
        {
          test: /\.s[ac]ss$/i,
          use: ["style-loader", "css-loader", "sass-loader"],
        },
        {
          test: /\.svg$/i,
          issuer: /\.[jt]sx?$/,
          use: [
            {
              loader: "@svgr/webpack",
            },
            {
              loader: "file-loader",
            },
            {
              loader: "url-loader",
            },
          ],
        },
        {
          test: /\.(gif|png|jpe?g|ttf|mp3|ogg|wav|otf|woff|jpg|ico)$/,
          type: "asset/resource",
        },
      ],
    },
    devServer: {
      historyApiFallback: true,
      host: "localhost",
      port: 4545,
      proxy: {
        "/api": {
          target: "http://localhost:8000",
          pathRewrite: { "/api": "" },
        },
      },
    },
  };
};
