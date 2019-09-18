// const merge = require('webpack-merge')
// const baseWebpackConfig = require('./webpack.base.config')
const TerserJSPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
//
// const webpackConfig = merge(baseWebpackConfig, {
//     mode: 'production',
//     output: {
//         filename: "[name]-[hash].js",
//     },
//     optimization: {
//         minimizer: [new TerserJSPlugin({}), new OptimizeCSSAssetsPlugin({})],
//     },
//     plugins: [
//         new MiniCssExtractPlugin({
//             filename: '[name].[hash].css',
//         }),
//         // new UglifyJsPlugin({
//         //     uglifyOptions: {
//         //         compress: {
//         //             warnings: false
//         //         }
//         //     },
//         //     sourceMap: config.build.productionSourceMap,
//         //     parallel: true
//         // }),
//         // new OptimizeCSSPlugin({
//         //     cssProcessorOptions: config.build.productionSourceMap
//         //         ? {safe: true, map: {inline: false}}
//         //         : {safe: true}
//         // }),
//     ]
// })
// module.export = webpackConfig

'use strict'

const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require('webpack');
const {VueLoaderPlugin} = require('vue-loader')

module.exports = {
    externals: {
        vue: 'Vue',
        axios: 'axios',
        jquery: 'jQuery',
    },
    entry: './src/index.js',
    output: {
        filename: "[name]-[hash].js",
        path: path.resolve(__dirname, 'dist'),
    },
    optimization: {
        minimizer: [new TerserJSPlugin({}), new OptimizeCSSAssetsPlugin({})],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
        }),
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
        new CleanWebpackPlugin(),
        new VueLoaderPlugin(),
        new MiniCssExtractPlugin({
            filename: '[name].[hash].css',
        }),
    ],

    module: {
        rules: [
            {
                test: /\.css$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'style-loader'
                    },
                    {
                        loader: MiniCssExtractPlugin.loader
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        }
                    },
                    {
                        loader: 'postcss-loader'
                    }
                ]
            },
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            ["@babel/preset-env", {
                                "useBuiltIns": "usage", // 在每个文件中使用polyfill时，为polyfill添加特定导入。利用捆绑器只加载一次相同的polyfill。
                                "modules": false // 启用将ES6模块语法转换为其他模块类型，设置为false不会转换模块。
                            }],
                        ],
                        plugins: [
                            ["@babel/plugin-transform-runtime", {
                                "helpers": false
                            }]
                        ]
                    }
                }
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: "style-loader" // creates style nodes from JS strings
                    },
                    {
                        loader: MiniCssExtractPlugin.loader
                    },
                    {
                        loader: "css-loader" // translates CSS into CommonJS
                    },
                    {
                        loader: "sass-loader" // compiles Sass to CSS
                    }
                ]
            },
            {
                test: /\.vue$/,
                use: 'vue-loader'
            },
            {
                test: /\.(wav|mp3|eot|ttf)$/,
                loader: 'file-loader',
            },
            {
                test: /\.(woff2?|eot|ttf|otf|svg)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    // name: utils.assetsPath('fonts/[name].[hash:7].[ext]')
                }
            },
        ]
    },
};