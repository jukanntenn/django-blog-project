const path = require('path');
const WebpackAssetsManifest = require('webpack-assets-manifest');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
// const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    outputDir: path.resolve(__dirname, './build'),
    publicPath: process.env.NODE_ENV == 'production' ? '/static/' : 'http://localhost:8080/',

    configureWebpack: (config) => {
        if (process.env.NODE_ENV == 'production') {
            config.externals = {
                vue: 'Vue',
                axios: 'axios',
            };
        }

        config.entry = './src/main.ts';
        // 为了暴露自定义的class组件
        config.output.library = { name: 'blogComponents', type: 'umd' };

        config.plugins.push(
            new WebpackAssetsManifest({
                entrypoints: true,
                output: 'manifest.json',
                writeToDisk: true,
                publicPath: true,
            }),
            new BundleAnalyzerPlugin({
                analyzerPort: process.env.VUE_CLI_MODERN_BUILD ? 8888 : 9999, // Prevents build errors when running --modern
            }),
        );
    },
};
