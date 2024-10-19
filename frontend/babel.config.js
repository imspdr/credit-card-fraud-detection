// babel.config.js
module.exports = {
  presets: [
    ["@babel/preset-env", { targets: { node: "current" } }],
    ["@babel/preset-react", { runtime: "automatic", importSource: "@emotion/react" }],
    "@babel/preset-typescript",
  ],
  plugins: ["@babel/plugin-transform-optional-chaining", "@emotion/babel-plugin"],
};
