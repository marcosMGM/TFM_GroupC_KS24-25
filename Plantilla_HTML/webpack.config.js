const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');
const autoprefixer = require('autoprefixer'); // Import autoprefixer

module.exports = {
  entry: {
    style: './assets/scss/style.scss', // Entry point for style.scss
    responsive: './assets/scss/responsive.scss' // Entry point for responsive.scss, add more as needed
  },
  output: {
    path: path.resolve(__dirname, 'assets/css'), // Output directory for CSS
  },
  module: {
    rules: [
      {
        test: /\.scss$/, // Match SCSS files
        use: [
          MiniCssExtractPlugin.loader, // Extracts CSS into separate files
          'css-loader', // Translates CSS into CommonJS
          {
            loader: 'postcss-loader', // PostCSS loader for autoprefixing
            options: {
              postcssOptions: {
                plugins: [
                  autoprefixer(), // Auto-prefix CSS
                ],
              },
            },
          },
          'sass-loader' // Compiles Sass to CSS
        ],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css', // Output CSS filename based on entry point name
    }),
    new BrowserSyncPlugin({
      host: 'localhost',
      port: 3000,
      server: { baseDir: ['./'] },
      startPath: 'template/index.html', // Specify your starting HTML file
      files: ['./assets/css/*.css', './template/*.html'], // Watch for CSS changes and HTML changes
    }),
  ],
};
