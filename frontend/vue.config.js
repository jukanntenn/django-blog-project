const path = require('path');
const WebpackAssetsManifest = require('webpack-assets-manifest');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
// const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    outputDir: path.resolve(__dirname, './build'),
    publicPath: process.env.NODE_ENV == 'production' ? '/static/' : 'http://localhost:8080/',

    configureWebpack: (config) => {
        if (process.env.NODE_ENV == 'production') {
            config.entry = './src/plugin/index.ts';
            config.externals = {
                vue: 'Vue',
                axios: 'axios',
            };
            // config.publicPath = '/static/';
        } else {
            config.entry = './src/main.ts';
            // config.publicPath = 'http://localhost:8080/';
        }
        // // 根据不同的执行环境配置不同的入口
        // // entry: process.env.NODE_ENV == 'development' ? './src/main.ts' : './src/plugin/index.ts',
        // (config.output = {
        //     filename: 'js/[name].js',
        //     library: 'comment', // 指定的就是你使用require时的模块名
        //     // CMD只能在 Node 环境执行，AMD 只能在浏览器端执行，UMD 同时支持两种执行环境
        //     libraryTarget: 'umd', // 指定输出格式
        //     umdNamedDefine: true, // 会对 UMD 的构建过程中的 AMD 模块进行命名。否则就使用匿名的 define
        // }),
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
